#!/usr/bin/env python

import codecs
import csv
import datetime
import json
import os.path
import sys
import xmlrpclib

from cStringIO import StringIO
from optparse import OptionParser

categories = {
    "Applications": {'keywords':"turbogears.app"},
    "Widgets": {'keywords':"turbogears.widgets"},
    "Template Engine Plugins": {'keywords':"python.templating.engines"},
    "Quickstart Templates": {'keywords':"turbogears.quickstart.template"},
    "Extension Components": {'keywords':"turbogears.extension"},
    "Identity Providers": {'keywords':"turbogears.identity.provider"},
    "tg-admin Commands": {'keywords':"turbogears.command"},
    "ToscaWidgets": {'keywords':"toscawidgets.widgets"},
    "Toolbox Plugins": {'keywords':"turbogears.toolboxcommand"},
    "TurboGears2": {'keywords': "turbogears2"},
    "TurboGears2 Applications": {'keywords': "turbogears2.application"},
    "TurboGears2 Widgets": {'keywords': "turbogears2.widgets"},
    "TurboGears2 Command": {'keywords': "turbogears2.command"},
    "TurboGears2 Extension": {'keywords': "turbogears2.extension"},
}

nontg = sorted(filter(lambda x: not categories[x]['keywords'].startswith('turbogears'), categories.keys()))
tg1 = sorted(filter(lambda x: categories[x]['keywords'].startswith('turbogears.'), categories.keys()))
tg2 = sorted(filter(lambda x: categories[x]['keywords'].startswith('turbogears2.'), categories.keys()))

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

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
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
        output.append('    Add ``keywords="%s"`` to your setup.py before uploading to `Python Package Index`_' % (categories[catname]['keywords']))
    return "\n".join(output)

def genPackages(options, title, keywordlist, cogs):
    output = []

    output.append('.. _`%s`:' % (title))
    output.append('')
    output.append(title)
    for catname in keywordlist:
        output.append('  .. _`%s`:' % (catname))
        output.append('')
        output.append('  %s (keywords: %s) (Back To Top of `The Cogbin`_)' % (catname, categories[catname]['keywords']))

        if len(cogs[catname].keys()) > 0:
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
    proxy = xmlrpclib.ServerProxy(options.url)

    cogs = {}
    for category in categories:
        if 'keywords' in categories[category]:
            if category not in cogs:
                cogs[category] = {}
            for keyword in categories[category]['keywords'].split(':'):
                results = proxy.search({'keywords': keyword})
                if results:
                    for result in results:
                        uploaded = datetime.datetime(1970, 1, 1, 0, 0, 0).timetuple()
                        for url in proxy.release_urls(result['name'], result['version']):
                            utime = url['upload_time']
                            if utime:
                                uploaded = utime.timetuple()
                        uploaded = '%04d-%02d-%02d' % (uploaded.tm_year, uploaded.tm_mon, uploaded.tm_mday)
                        cogs[category][result['name']] = {
                            'version': result['version'],
                            'summary': result['summary'],
                            'uploaded': uploaded
                            }
    return cogs

def main():
    parser = OptionParser()
    parser.add_option('--file', action='store', dest='file', default='cogbin.rst', help='Specify the .rst file to insert cogbin entries into. default: %default')
    parser.add_option('--url', action='store', dest='url', default='http://pypi.python.org/pypi', help='Change the URL for the PyPi. default: %default')
    (options, args) = parser.parse_args()

    if not os.path.exists(options.file):
        print 'cogbin file (%s) does not exist, cannot update. Aborting' % (options.file)
        sys.exit(1)
    
    cogs = getPackageList(options)
    #c = open('cogs.json', 'w')
    #c.write(json.dumps(cogs))
    #c.close()
    #cogs = json.load(open('cogs.json'))

    output = []
    output.append(genKeywordsToc(options, 'TurboGears 2 Packages', tg2))
    output.append(genKeywordsToc(options, 'TurboGears 1 Packages', tg1))
    output.append(genKeywordsToc(options, 'Non-TurboGears (but important) Packages', nontg))
    output.append('')
    output.append(genPackages(options, "TurboGears 2 Packages", tg2, cogs))
    output.append(genPackages(options, "TurboGears 1 Packages", tg1, cogs))
    output.append(genPackages(options, "Non-TurboGears (but important) Packages", nontg, cogs))
    output.append('')
    
    cogbin = '\n'.join(output)

    data = open(options.file).readlines()
    for i in range(len(data)):
        if data[i].strip()=='COGBINRST':
            data[i] = cogbin

    f = open(options.file, 'w')
    f.write(''.join(data))
    f.close()
    

if __name__ == '__main__':
    main()
    
