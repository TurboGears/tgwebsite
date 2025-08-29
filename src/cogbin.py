#!/usr/bin/env python
from docutils import nodes
from docutils.statemachine import ViewList
from docutils.parsers.rst import Directive, directives

from sphinx.util.nodes import nested_parse_with_titles

import datetime
import re
import socket
import requests
import csv
from multiprocessing.pool import ThreadPool

from io import StringIO
from traceback import print_exc

# Network timeout for HTTP calls during build
socket.setdefaulttimeout(10)

# Force import of strptime in main thread, this is a work-around for strptime
# not being thread safe
datetime.datetime.strptime("1970-01-01 01:01:01.01", "%Y-%m-%d %H:%M:%S.%f")


BASE_KEYWORD = 'turbogears2'
categories = {
    "Applications": {'keyword': "turbogears2.application"},
    "Extensions": {'keyword': "turbogears2.extension"},
    "Widgets": {'keyword': "turbogears2.widgets"},
    "Commands": {'keyword': "turbogears2.command"},
}

tg2 = [
    'Applications',
    'Extensions',
    'Widgets',
    'Commands',
    'Uncategorized'
]


class UnicodeWriter:
    """Minimal CSV writer for Python 3 using csv + StringIO."""

    def __init__(self):
        self.buffer = StringIO()
        self.writer = csv.writer(self.buffer)

    def writerow(self, row):
        self.writer.writerow([str(s) for s in row])

    def getvalue(self):
        return self.buffer.getvalue()


def genPackages(title, keywordlist, cogs):
    output = []

    output.append('.. _`%s`:' % (title))
    output.append('')
    output.append(title)
    output.append('')
    if not cogs:
        output.append('.. note::')
        output.append('   Unable to fetch CogBin data from PyPI at build time (offline or network error).')
        output.append('   Categories are shown below without package entries.')
        output.append('')
    for catname in keywordlist:
        output.append('  .. _`%s`:' % (catname))
        output.append('')
        output.append('  %s (keyword: %s) (Back To Top of `The Cogbin`_)' % (catname, categories.get(catname, {'keyword':''})['keyword']))

        if catname in cogs and len(cogs[catname].keys()) > 0:
            out = UnicodeWriter()
            for pname in sorted(cogs[catname].keys()):
                prgent = cogs[catname][pname]
                # Link to the PyPI project page (not the XML-RPC endpoint)
                url = 'https://pypi.org/project/%s/%s/' % (pname, prgent['version'])
                out.writerow(['`%s <%s>`_' % (pname, url), prgent['summary'], prgent['version'], prgent['uploaded']])
            rows = out.getvalue().split('\n')
            rows = ['       %s' % (row) for row in rows]
            output.append('    .. csv-table::')
            output.append('       :header: "Project Name", "Summary", "Version", "Uploaded"')
            output.append('       :widths: 17, 59, 11, 11')
            output.append('       ')
            output.append('\n'.join(rows))
        else:
            output.append('    No packages uploaded yet. You can be the first!')
            output.append('')

    return "\n".join(output)


def getPackageList():
    packages = []
    cogs = {}

    def _add_package_from_json(name):
        try:
            resp = requests.get(f'https://pypi.org/pypi/{name}/json', timeout=10)
            if resp.status_code != 200:
                return
            data = resp.json()
        except Exception:
            print(f'Failed to fetch JSON for {name}')
            print_exc()
            return

        info = data.get('info', {})
        version = info.get('version') or ''
        summary = info.get('summary') or ''
        keywords = info.get('keywords') or ''
        classifiers = info.get('classifiers') or []
        if isinstance(keywords, list):
            keywords_list = keywords
        else:
            # split on comma or whitespace
            parts = re.split(r'[\s,]+', keywords.strip()) if isinstance(keywords, str) else []
            keywords_list = [p for p in parts if p]

        uploaded = ''
        try:
            files = data.get('releases', {}).get(version, [])
            if files:
                up = files[0].get('upload_time_iso_8601') or files[0].get('upload_time')
                if up:
                    uploaded = up[:10]
        except Exception:
            pass

        packages.append({
            'name': name,
            'version': version,
            'summary': summary,
            'keywords': keywords_list,
            'uploaded': uploaded,
            'classifiers': classifiers,
        })

    def _discover_project_names():
        names = set()
        # 1) Trove classifiers
        classifiers = [
            'Framework :: TurboGears',
            'Framework :: TurboGears :: 2',
        ]
        for c in classifiers:
            for page in range(1, 11):
                try:
                    resp = requests.get('https://pypi.org/search/', params={'q': '', 'c': c, 'page': page}, timeout=10)
                except Exception:
                    print('Failed to fetch PyPI search page for classifier')
                    print_exc()
                    break
                if resp.status_code != 200 or 'No projects found' in resp.text:
                    break
                for m in re.findall(r'/project/([A-Za-z0-9_.\-]+)/', resp.text):
                    names.add(m)

        # 2) Free text queries likely to hit TG packages
        queries = [
            ('tgext', 15), ('tgext.', 15),
            ('tgapp', 15), ('tgapp.', 15),
            ('turbogears', 10), ('turbogears2', 10),
        ]
        for q, max_pages in queries:
            for page in range(1, max_pages + 1):
                try:
                    resp = requests.get('https://pypi.org/search/', params={'q': q, 'page': page}, timeout=10)
                except Exception:
                    print('Failed to fetch PyPI search page for query')
                    print_exc()
                    break
                if resp.status_code != 200 or 'No projects found' in resp.text:
                    break
                for m in re.findall(r'/project/([A-Za-z0-9_.\-]+)/', resp.text):
                    names.add(m)

        # No seeding: rely entirely on discovery mechanisms
        # Debug logging removed after validation
        return names

    def _discover_from_simple_index():
        names = set()
        try:
            resp = requests.get('https://pypi.org/simple/', timeout=20)
            if resp.status_code != 200:
                return names
            # Extract project anchors: <a href='/simple/<name>/'>
            for m in re.findall(r"/simple/([A-Za-z0-9_.\-]+)/", resp.text):
                nm = m.lower()
                if nm.startswith('tgext') or nm.startswith('tgapp') or nm.startswith('turbogears') or nm.startswith('tg'):
                    names.add(m)
        except Exception:
            print('CogBin: failed to fetch/parse simple index')
            print_exc()
        # Debug logging removed after validation
        return names

    def _is_tg_related(name, info):
        # Strict: include only if keywords contain 'turbogears2' or 'turbogears2.*'
        kw_val = info.get('keywords')
        if isinstance(kw_val, list):
            kw_list = [str(k).lower() for k in kw_val]
        else:
            kw_list = [k for k in re.split(r'[\s,]+', (kw_val or '')) if k]
            kw_list = [k.lower() for k in kw_list]
        return any(k == 'turbogears2' or k.startswith('turbogears2.') for k in kw_list)

    def _fetch_all_packages():
        names = _discover_project_names()
        if len(names) < 20:
            names |= _discover_from_simple_index()
        # No name-based prefiltering; rely on keywords in package metadata
        # Fetch JSON for discovered names and keep only TG-related
        pool = ThreadPool(processes=10)
        for n in list(names):
            pool.apply_async(_add_package_from_json, (n,))
        pool.close()
        pool.join()
        # Debug logging removed after validation
        # Filter to TG related
        filtered = []
        for pkg in packages:
            # Reconstruct minimal info dict for filter
            info = {'summary': pkg.get('summary'), 'keywords': pkg.get('keywords'), 'classifiers': pkg.get('classifiers', [])}
            if _is_tg_related(pkg['name'], info):
                filtered.append(pkg)
        packages[:] = filtered
        # Debug logging removed after validation


    def _allot_categories(packages):
        while packages:
            package_data = packages.pop()

            for category_name, category_data in categories.items():
                keyword = category_data['keyword']
                if keyword in package_data['keywords']:
                    cogs.setdefault(category_name, {})[package_data['name']] = package_data
                    break
            else:
                cogs.setdefault('Uncategorized',{})[package_data['name']] = package_data

    _fetch_all_packages()
    _allot_categories(packages)
    return cogs


def _get_cogbin_data():
    cogs = getPackageList()

    output = []
    output.extend(genPackages("TurboGears 2 Packages", tg2, cogs).split('\n'))
    output.append('')
    return output


class CogBinDirective(Directive):
    def run(self):
        result = ViewList()

        for line in _get_cogbin_data():
            result.append(line, '<cogbin>')

        node = nodes.section()
        node.document = self.state.document
        nested_parse_with_titles(self.state, result, node)
        return node.children

def setup(app):
    app.add_directive('cogbin', CogBinDirective)


if __name__ == '__main__':
    """ Mostly for testing pourpose """
    print('\n'.join(_get_cogbin_data()))
