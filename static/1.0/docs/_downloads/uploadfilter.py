'''
UploadFilter - File upload functionality.
    2006, James Kassemi - http://www.kepty.com
    2006, Ian Charnas <icc@case.edu> made the following minor changes:

          Immediately return from FieldStorage.__del__ so as not to 
          delete information about transfers when the transfers are over.  
          Instead we leave the deletion up to the controlling app.

          Fixed bug on line 218 (change 'upload_limit_filter" to "upload_filter")

          Changed 'transfered' to correctly-spelled 'transferred'

If you allow users to upload files to your site you're definitely going to want
to use the uploadfilter.max_concurrent setting, and set it to less than the
number of threads in your server.thread_pool setting. Without it you'll be
opening your site up to a simple dos if there are a number of concurrent
file uploads that utilize all of your threads.

As you'll be doing anyway, make sure that the enctype of your form is
multipart/form-data, as that's what we'll be using to determine whether or not
to track a file upload.

Configuration:
    - uploadfilter.max_concurrent
        Set the number of files that can be concurrently uploaded to the site.
        If the number exceeds the number set here, Upload_MaxConcError will be
        raised.

    - uploadfilter.max_size
        Size, in kb, to limit uploaded files to. This will check both the
        header version, but in case that's spoofed, it will also check during
        the writing of the file to the temporary area. Raises
        Upload_MaxSizeError if the size exceeds this number. This will
        also override cherrypy.max_request_body_size for this area, so you don't
        have to worry about conflicting with that. If this is NOT set then
        you'll be dealing with the max_request_body_size, and we'll do NO
        checks.

    - uploadfilter.timeout
        Time cap. will raise Upload_TimeoutError if the user has been uploading a file
        for longer than the value set here.

    - uploadfilter.explicit
        Tells the system to check whether or not pages allows uploads. Set
        this at a root directory, and then add

            uploadfilter.declared=True

        where a page accepts file uploads. This prevents someone from posting file
        data to other fields, tying up your bandwidth by exploiting the fact cp
        will upload the file before you can check it.

    - uploadfilter.min_upspeed
        To keep someone from maintaining a connection and tying up a thread by
        uploading at a VERY slow rate, you can set this value (make sure it's
        somewhat low). It will raise Upload_UpSpeedError if the user's average
        upload speed drops below this value. the uploadfilter.timeout filter
        can be used as an alternative, but this might be preferable, depending
        on your situation.

Real-time statistics:
    The 'file_transfers' attribute is added to the cherrypy object, and can be
    used to keep track of files being uploaded from a remote host. The format
    is as follows:

    cherrypy.file_transfers[remote_addr][filename] = ProgressFile object

    And the ProgressFile object will maintain these attributes:
        - transferred          byte size of transferred data thus far.
        - speed               bytes/sec
        - remaining           bytes remaining
        - eta                 estimated seconds until arrival

    It's possible to create an AJAX-style interface to show the user the status
    of their file uploads now, so long as you have an available thread to take
    the requests for it...
'''

import cgi
import cherrypy
import tempfile
import time

from cherrypy.filters.basefilter import BaseFilter

class Upload_MaxConcError(Exception):
    pass
class Upload_TimeoutError(Exception):
    pass
class Upload_MaxSizeError(Exception):
    pass
class Upload_UnauthorizedError(Exception):
    pass
class Upload_UpSpeedError(Exception):
    pass

current_uploads = 0
cherrypy.file_transfers = dict()

class ProgressFile(object):
    def __init__(self, buf, *args, **kwargs):
        self.file_object = tempfile.TemporaryFile(
                *args, **kwargs)
        self.transferred = 0
        self.buf = buf
        self.pre_sized = float(cherrypy.request.headers['Content-length'])
        self.speed = 1
        self.remaining = 0
        self.eta = 0
        self._start = time.time()

    def write(self, data):
        now = time.time()
        self.transferred += len(data)
        upload_timeout = getattr(cherrypy.thread_data, 'upload_timeout', False)
        if upload_timeout:
            if (now - self._start) > upload_timeout:
                raise Upload_TimeoutError

        upload_maxsize = getattr(cherrypy.thread_data, 'upload_maxsize', False)
        if upload_maxsize:
            if self.transferred > upload_maxsize:
                raise Upload_MaxSizeError

        self.speed = self.transferred / (now - self._start)

        upload_minspeed = getattr(cherrypy.thread_data, 'upload_minspeed', False)
        if upload_minspeed:
            if self.transferred > (5 * self.buf): # gives us a reasonable wait period.
                if self.speed < upload_minspeed:
                    raise Upload_UpSpeedError

        self.remaining = self.pre_sized - self.transferred

        if self.speed == 0: self.eta = 9999999
        else: self.eta = self.remaining / self.speed

        return self.file_object.write(data)

    def seek(self, pos):
        self.post_sized = self.transferred
        self.transferred = True
        return self.file_object.seek(pos)

    def read(self, size):
        return self.file_object.read(size)

class FieldStorage(cherrypy._cpcgifs.FieldStorage):
    ''' We want control over our timing and download status,
        so we've got to override the original. This will work
        transparently without interfering with the user, but
        might warrant addition to _cpcgifs '''

    def __del__(self, *args, **kwargs):
        return
        try:
            dcopy = cherrypy.file_transfers[cherrypy.request.remote_addr].copy()
            for key, val in dcopy.iteritems():
                if val.transferred == True:
                    del cherrypy.file_transfers[cherrypy.request.remote_addr][key]
            del dcopy
            if len(cherrypy.file_transfers[cherrypy.request.remote_addr]) == 0:
                del cherrypy.file_transfers[cherrypy.request.remote_addr]

        except KeyError:
            pass

    def make_file(self, binary=None):
        fo = ProgressFile(self.bufsize)
        if cherrypy.file_transfers.has_key(cherrypy.request.remote_addr):
            cherrypy.file_transfers[cherrypy.request.remote_addr]\
                    [self.filename] = fo
        else:
            cherrypy.file_transfers[cherrypy.request.remote_addr]\
                    = {self.filename:fo}

        return fo

cherrypy._cpcgifs.FieldStorage = FieldStorage

class UploadFilter(BaseFilter):

    #def on_start_resource(self):
    #    cherrypy.request.rfile = cherrypy.request.rfile.rfile

    def before_request_body(self):
        global current_uploads

        if not cherrypy.config.get('upload_filter.on', False):
            return

        if cherrypy.request.headers.get('Content-Type', '').split(';')[0] ==\
            'multipart/form-data':

            upload_explicit = cherrypy.config.get('upload_filter.explicit', False)
            upload_declared = cherrypy.config.get('upload_filter.declared', False)
            upload_limit = cherrypy.config.get('upload_filter.max_concurrent', False)
            upload_timeout = cherrypy.config.get('upload_filter.timeout', False)
            upload_maxsize = cherrypy.config.get('upload_filter.max_size', False)
            upload_minspeed = cherrypy.config.get('upload_filter.min_upspeed', False)


            cherrypy.thread_data.upload_minspeed = upload_minspeed

            if upload_explicit and not upload_declared:
                raise Upload_UnauthorizedError

            if upload_limit:
                if current_uploads > upload_limit:
                    raise Upload_MaxConcError
                current_uploads += 1

            if upload_timeout:
                cherrypy.thread_data.upload_timeout = upload_timeout

            if upload_maxsize:
                upload_maxsize *= 1024
                cherrypy.thread_data.upload_maxsize = upload_maxsize
                size = float(cherrypy.request.headers['Content-length'])
                if size > upload_maxsize:
                    raise Upload_MaxSizeError
                # the following line is commented out to accomodate a
                # change in CherryPy >= 2.3.0
                #cherrypy.request.rfile = cherrypy.request.rfile.rfile

    def on_end_resource(self):
        global current_uploads

        if not cherrypy.config.get('upload_filter.on', False):
            return

        if cherrypy.request.headers.get('Content-Type', '').split(';')[0] ==\
            'multipart/form-data':

            upload_explicit = cherrypy.config.get('upload_filter.explicit',
                    False)
            upload_declared = cherrypy.config.get('upload_filter.declared',
                    False)
            upload_limit = cherrypy.config.get('upload_filter.max_concurrent',
                    False)
            upload_timeout = cherrypy.config.get('upload_filter.timeout',
                    False)
            upload_maxsize = cherrypy.config.get('upload_filter.max_size',
                    False)

            if upload_explicit and not upload_declared:
                return

            if upload_limit:
                current_uploads -= 1

            if upload_timeout:
                del cherrypy.thread_data.upload_timeout

            if upload_maxsize:
                del cherrypy.thread_data.upload_maxsize
