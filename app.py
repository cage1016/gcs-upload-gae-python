import webapp2
import httplib2
import json

from functools import wraps
from google.appengine.api import memcache

from apiclient.discovery import build
from oauth2client.contrib.appengine import AppAssertionCredentials

from apiclient.http import MediaIoBaseUpload
from StringIO import StringIO

DEVELOPER_KEY = ''
BUCKET = ''


def ValidateGCSWithCredential(function):
    @wraps(function)
    def _decorated(self, *args, **kwargs):
        credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/devstorage.full_control')
        http = credentials.authorize(httplib2.Http(memcache))
        self.gcs_service = build('storage', 'v1', http=http, developerKey=DEVELOPER_KEY)

        self.gcs_service.BUCKET = BUCKET

        return function(self, *args, **kwargs)

    return _decorated


class MainHandler(webapp2.RequestHandler):
    @ValidateGCSWithCredential
    def get(self):
        fields_to_return = 'nextPageToken,items(bucket,name,metadata(my-key))'
        req = self.gcs_service.objects().list(bucket=self.gcs_service.BUCKET, fields=fields_to_return, maxResults=42)

        # while req is not None:
        #     resp = req.execute()
        #     print json.dumps(resp, indent=2)
        #     req = self.gcs_service.objects().list_next(req, resp)

        resp = req.execute()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(json.dumps(resp, indent=2))


class UploadHandler(webapp2.RequestHandler):
    @ValidateGCSWithCredential
    def get(self):
        object_name = "hello_gcs.txt"
        media = MediaIoBaseUpload(StringIO("hello gcs"), mimetype='text/plain')
        uploader = self.gcs_service.objects().insert(bucket=self.gcs_service.BUCKET, body={
            'name': object_name.encode('utf8')
        }, media_body=media)
        resp = uploader.execute()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(json.dumps(resp, indent=2))


routes = [
    ('/upload', UploadHandler),
    ('/', MainHandler),
]

router = webapp2.WSGIApplication(routes, debug=True)
