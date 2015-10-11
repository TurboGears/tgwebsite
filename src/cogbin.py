#!/usr/bin/env python
from docutils import nodes
from docutils.statemachine import ViewList
from docutils.parsers.rst import Directive, directives

from sphinx.util.nodes import nested_parse_with_titles

import codecs
import datetime
import xmlrpclib
import unicodecsv
from multiprocessing.pool import ThreadPool

from cStringIO import StringIO
from traceback import print_exc

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


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=unicodecsv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = StringIO()
        self.writer = unicodecsv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([str(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def genKeywordsToc(options, title, keywordlist):
    output = []
    output.append('`%s`_' % title)
    for catname in keywordlist:
        output.append('  `%s`_' % (catname))
        output.append('    Add ``keyword="%s"`` to your setup.py before uploading to `Python Package Index`_' % (categories.get(catname, {'keyword':''})['keyword']))
    return "\n".join(output)


def genPackages(options, title, keywordlist, cogs):
    output = []

    output.append('.. _`%s`:' % (title))
    output.append('')
    output.append(title)
    for catname in keywordlist:
        output.append('  .. _`%s`:' % (catname))
        output.append('')
        output.append('  %s (keyword: %s) (Back To Top of `The Cogbin`_)' % (catname, categories.get(catname, {'keyword':''})['keyword']))

        if catname in cogs and len(cogs[catname].keys()) > 0:
            outio = StringIO()
            out = UnicodeWriter(outio)
            for pname in sorted(cogs[catname].keys()):
                prgent = cogs[catname][pname]
                url = '%s/%s/%s' % (options.url, pname, prgent['version'])
                out.writerow(['`%s <%s>`_' % (pname, url), prgent['summary'], prgent['version'], prgent['uploaded']])
            rows = outio.getvalue().split('\n')
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


def getPackageList(options):
    packages = []
    cogs = {}

    def _fetch_last_update(result):
        proxy = xmlrpclib.ServerProxy(options.url)
        uploaded = datetime.datetime(1970, 1, 1, 0, 0, 0).timetuple()
        try:
            release_urls = proxy.release_urls(result['name'], result['version'])
        except:
            print 'Failed to fetch release urls for %s' % result['name']
            print_exc()
            return

        for url in release_urls:
            utime = url['upload_time']
            if utime:
                uploaded = utime.timetuple()
            uploaded = '%04d-%02d-%02d' % (uploaded.tm_year, uploaded.tm_mon, uploaded.tm_mday)

        try:
            release_data = proxy.release_data(result['name'], result['version'])
        except:
            print 'Failed to fetch release data for %s' % result['name']
            print_exc()
            return

        keywords = release_data.get('keywords', '')
        keywords_list = keywords.split()
        if len(keywords_list) == 1:
            keywords_list = keywords.split(',')

        packages.append({
            'name': result['name'],
            'version': result['version'],
            'summary': result['summary'],
            'keywords': keywords_list,
            'uploaded': uploaded
        })

    def _fetch_all_packages():
        proxy = xmlrpclib.ServerProxy(options.url)
        results = proxy.search({'keywords': BASE_KEYWORD})

        last_update_pool = ThreadPool(processes=10)
        if results:
            last_update_pool.map(_fetch_last_update, results)


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


class CogBinOptions(object):
    url = 'https://pypi.python.org/pypi'


def _get_cogbin_data():
    options = CogBinOptions()
    cogs = getPackageList(options)

    output = []
    output.extend(genPackages(options, "TurboGears 2 Packages", tg2, cogs).split('\n'))
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
    print '\n'.join(_get_cogbin_data())

