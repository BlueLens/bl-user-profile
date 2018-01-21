from __future__ import print_function
import os
import pickle
import time
import redis
from multiprocessing import Process
from stylelens_user.user_logs import UserLogs
from bluelens_log import Logging

REDIS_USER_OBJECT_HASH = 'bl:user:object:hash'
REDIS_USER_OBJECT_QUEUE = 'bl:user:object:queue'
REDIS_USER_IMAGE_HASH = 'bl:user:image:hash'
REDIS_FEED_IMAGE_HASH = 'bl:feed:image:hash'

REDIS_LOG_SEARCH_IMAGE_FILE_QUEUE = 'bl:log:search:image:file'
REDIS_LOG_SEARCH_IMAGE_ID_QUEUE = 'bl:log:search:image:id'
REDIS_LOG_SEARCH_OBJECT_ID_QUEUE = 'bl:log:search:object:id'

REDIS_USER_PROFILE_IMAGE_FILE_SEARCH_QUEUE = 'bl:user:profile:image:file:search'
REDIS_USER_PROFILE_IMAGE_INDEX_SEARCH_QUEUE = 'bl:user:profile:image:index:search'
REDIS_USER_PROFILE_OBJECT_ID_SEARCH_QUEUE = 'bl:user:profile:object:id:search'

REDIS_SERVER = os.environ['REDIS_SEARCH_SERVER']
REDIS_PASSWORD = os.environ['REDIS_SEARCH_PASSWORD']

DB_USER_LOG_USER = os.environ['DB_USER_LOG_USER']
DB_USER_LOG_HOST = os.environ['DB_USER_LOG_HOST']
DB_USER_LOG_PORT = os.environ['DB_USER_LOG_PORT']
DB_USER_LOG_NAME = os.environ['DB_USER_LOG_NAME']
DB_USER_LOG_PASSWORD = os.environ['DB_USER_LOG_PASSWORD']

rconn = redis.StrictRedis(REDIS_SERVER, decode_responses=False, port=6379, password=REDIS_PASSWORD)
options = {
  'REDIS_SERVER': REDIS_SERVER,
  'REDIS_PASSWORD': REDIS_PASSWORD
}
log = Logging(options, tag='bl-user-profile')

def profile_image_file_search(rconn):
  while True:
    key, value = rconn.blpop([REDIS_USER_PROFILE_IMAGE_FILE_SEARCH_QUEUE])
    if value is not None:
      image = pickle.loads(value)
      # objects = image.get('objects')
      # if objects is not None:
      #   for o in objects:



if __name__ == '__main__':
  try:
    log.info("start bl-user-profile:1")
    Process(target=profile_image_file_search, args=(rconn,)).start()
    # Process(target=profile_image_index_search, args=(rconn,)).start()
    # Process(target=profile_object_id_search, args=(rconn,)).start()
  except Exception as e:
    log.error(str(e))
