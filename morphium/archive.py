import os
import logging
import boto3
import mimetypes
from datetime import datetime

from morphium.util import env, TAG_LATEST

log = logging.getLogger(__name__)
config = {}


class Archive(object):
    """A scraper archive on S3. This is called when a scraper has generated a
    file which needs to be backed up to a bucket."""

    def __init__(self, bucket=None, prefix=None):
        self.tag = datetime.utcnow().date().isoformat()
        self.bucket = bucket or env('aws_bucket')
        self.prefix = prefix or 'data'

    @property
    def client(self):
        if not hasattr(self, '_client'):
            if self.bucket is None:
                log.warning("No $AWS_BUCKET, skipping upload.")
                self._client = None
                return None
            access_key = env('aws_access_key_id')
            if access_key is None:
                log.warning("No $AWS_ACCESS_KEY_ID, skipping upload.")
                self._client = None
                return None
            secret_key = env('aws_secret_access_key')
            if secret_key is None:
                log.warning("No $AWS_SECRET_ACCESS_KEY, skipping upload.")
                self._client = None
                return None

            session = boto3.Session(aws_access_key_id=access_key,
                                    aws_secret_access_key=secret_key)
            self._client = session.client('s3')
        return self._client

    def upload_file(self, source_path, file_name=None, mime_type=None):
        """Upload a file to the given bucket."""
        if self.client is None:
            return

        if file_name is None:
            file_name = os.path.basename(source_path)

        if mime_type is None:
            mime_type, _ = mimetypes.guess_type(file_name)
            mime_type = mime_type or 'application/octet-stream'

        key_name = os.path.join(self.prefix, self.tag, file_name)
        log.info("Uploading [%s]: %s", self.bucket, key_name)
        args = {
            'ContentType': mime_type,
            'ACL': 'public-read',
        }
        self.client.upload_file(source_path, self.bucket, key_name,
                                ExtraArgs=args)
        copy_name = os.path.join(self.prefix, TAG_LATEST, file_name)
        copy_source = {'Key': key_name, 'Bucket': self.bucket}
        self.client.copy(copy_source, self.bucket, copy_name,
                         ExtraArgs=args)
        return 'http://%s/%s' % (self.bucket, key_name)
