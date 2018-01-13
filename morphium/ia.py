import os
import logging
import boto
from boto.s3.connection import OrdinaryCallingFormat
import mimetypes
from datetime import datetime

from morphium.util import env, TAG_LATEST

log = logging.getLogger(__name__)
config = {}


class InternetArchive(object):
    """A scraper archive on the internet archive. This is called when a
    scraper has generated a file which needs to be backed up to a
    bucket."""

    def __init__(self, item=None, prefix=None):
        self.tag = datetime.utcnow().date().isoformat()
        self.item = item or env('ia_item')
        self.prefix = prefix
        self.access_key = env('ia_access_key_id')
        self.secret_key = env('ia_secret_access_key')

    @property
    def bucket(self):
        if not hasattr(self, '_bucket'):
            config = self.item is not None
            config = config and self.access_key is not None
            config = config and self.secret_key is not None
            if not config:
                log.warning("No Internet Archive config, skipping upload.")
                self._client = None
                return None

            conn = boto.connect_s3(self.access_key, self.secret_key,
                                   host='s3.us.archive.org',
                                   is_secure=False,
                                   calling_format=OrdinaryCallingFormat())
            if not conn.lookup(self.item, validate=False):
                conn.create_bucket(self.item)
            self._bucket = conn.get_bucket(self.item)
        return self._bucket

    def upload_file(self, source_path, file_name=None, mime_type=None):
        """Upload a file to the given bucket."""
        if self.bucket is None:
            return

        if file_name is None:
            file_name = os.path.basename(source_path)

        if mime_type is None:
            mime_type, _ = mimetypes.guess_type(file_name)
            mime_type = mime_type or 'application/octet-stream'

        date_name = os.path.join(self.tag, file_name)
        copy_name = os.path.join(TAG_LATEST, file_name)
        for key_name in (date_name, copy_name):
            if self.prefix is not None:
                key_name = os.path.join(self.prefix, key_name)
            log.info("Uploading [%s]: %s", self.item, key_name)
            key = self.bucket.get_key(key_name)
            if key is None:
                key = self.bucket.new_key(key_name)
            key.content_type = mime_type
            key.set_contents_from_filename(source_path,
                                           policy='public-read')    
        return key.generate_url(84600, query_auth=False)
