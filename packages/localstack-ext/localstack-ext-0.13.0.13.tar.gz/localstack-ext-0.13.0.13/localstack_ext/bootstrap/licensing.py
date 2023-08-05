import base64
FRuPW=None
FRuPD=Exception
FRuPI=True
FRuPh=str
FRuPX=len
FRuPV=bytes
FRuPJ=False
FRuPb=int
FRuPc=range
FRuPG=ValueError
FRuPv=object
import json
import logging
import os
import sys
import traceback
from localstack import config as localstack_config
from localstack.constants import ENV_PRO_ACTIVATED
from localstack.utils.common import load_file,md5,now_utc
from localstack.utils.common import safe_requests as requests
from localstack.utils.common import str_insert,str_remove,to_bytes,to_str
from localstack_ext import __version__,config
from localstack_ext.bootstrap.decryption import DecryptionHandler,init_source_decryption
from localstack_ext.config import ROOT_FOLDER
ENV_PREPARED={}
MAX_KEY_CACHE_DURATION_SECS=60*60*24
LOG=logging.getLogger(__name__)
ENV_LOCALSTACK_API_KEY="LOCALSTACK_API_KEY"
TEST_AUTH_HEADERS=FRuPW
class KeyActivationError(FRuPD):
 def __init__(self,message:FRuPh=FRuPW):
  self.message=message
class CachedKeyError(KeyActivationError):
 pass
class InvalidKeyError(KeyActivationError):
 pass
class InvalidDecryptionKeyError(KeyActivationError):
 pass
def read_api_key(raise_if_missing=FRuPI):
 key=(os.environ.get(ENV_LOCALSTACK_API_KEY)or "").strip()
 if not key and raise_if_missing:
  raise FRuPD("Unable to retrieve API key. Please configure $%s in your environment"%ENV_LOCALSTACK_API_KEY)
 return key
def truncate_api_key(api_key:FRuPh):
 return '"%s..."(%s)'%(api_key[:3],FRuPX(api_key))
def fetch_key()->FRuPV:
 api_key=read_api_key()
 if api_key=="test":
  return b"test"
 data={"api_key":api_key,"version":__version__}
 try:
  logging.getLogger("py.warnings").setLevel(logging.ERROR)
  result=requests.post("%s/activate"%config.API_URL,json.dumps(data),verify=FRuPJ)
  if result.status_code>=400:
   content=result.content
   content_type=result.headers.get("Content-Type")
   if result.status_code==403:
    message=json.loads(to_str(content))["message"]
    raise InvalidKeyError("Activation key %s is invalid or expired! Reason: %s"%(truncate_api_key(api_key),message))
   raise KeyActivationError('Received error activating key (code %s): ctype "%s" - %s'%(result.status_code,content_type,content))
  key_base64=json.loads(to_str(result.content))["key"]
  cache_key_locally(api_key,key_base64)
 except InvalidKeyError:
  raise
 except FRuPD as e:
  if log_license_issues():
   api_key=FRuPh(api_key_configured()or "")
   LOG.warning("Error activating API key %s: %s %s"%(truncate_api_key(api_key),e,traceback.format_exc()))
   LOG.warning("Looking for cached key as fallback...")
  key_base64=load_cached_key(api_key)
 finally:
  logging.getLogger("py.warnings").setLevel(logging.WARNING)
 decoded_key=base64.b64decode(key_base64)
 return decoded_key
def cache_key_locally(api_key,key_b64):
 configs=localstack_config.load_config_file()
 timestamp=FRuPh(FRuPb(now_utc()))
 key_raw=to_str(base64.b64decode(key_b64))
 for i in FRuPc(FRuPX(timestamp)):
  key_raw=str_insert(key_raw,i*2,timestamp[i])
 key_b64=to_str(base64.b64encode(to_bytes(key_raw)))
 configs["cached_key"]={"timestamp":FRuPb(timestamp),"key_hash":md5(api_key),"key":key_b64}
 localstack_config.save_config_file(configs)
 return configs
def load_cached_key(api_key):
 configs=localstack_config.load_config_file()
 cached_key=configs.get("cached_key")
 if not cached_key:
  raise CachedKeyError("Could not find cached key")
 if cached_key.get("key_hash")!=md5(api_key):
  raise CachedKeyError("Cached key was created for a different API key")
 now=now_utc()
 if(now-cached_key["timestamp"])>MAX_KEY_CACHE_DURATION_SECS:
  raise CachedKeyError("Cached key expired")
 timestamp=FRuPh(cached_key["timestamp"])
 key_raw=to_str(base64.b64decode(cached_key["key"]))
 for i in FRuPc(FRuPX(timestamp)):
  assert key_raw[i]==timestamp[i]
  key_raw=str_remove(key_raw,i)
 key_b64=to_str(base64.b64encode(to_bytes(key_raw)))
 return key_b64
def enable_file_decryption(key:FRuPV):
 decryption_handler=DecryptionHandler(key)
 try:
  file_name=f"{ROOT_FOLDER}/localstack_ext/utils/common.py.enc"
  encrypted_file_content=load_file(file_name,mode="rb")
  file_content=decryption_handler.decrypt(encrypted_file_content)
  if "import" not in to_str(file_content):
   raise FRuPG("Decryption resulted in invalid python file!")
 except FRuPD:
  raise InvalidDecryptionKeyError("Error while trying to validate decryption key!")
 init_source_decryption(decryption_handler)
def check_require_pro():
 if config.REQUIRE_PRO:
  LOG.error("Unable to activate API key, but $REQUIRE_PRO is configured - quitting.")
  sys.exit(1)
def prepare_environment():
 class OnClose(FRuPv):
  def __exit__(self,*args,**kwargs):
   ENV_PREPARED["finalized"]=FRuPI
  def __enter__(self,*args,**kwargs):
   pass
 if not ENV_PREPARED.get("finalized"):
  try:
   key=fetch_key()
   if not key:
    raise FRuPD("Unable to fetch and validate API key from environment")
   if to_str(key)!="test":
    enable_file_decryption(key)
    LOG.info("Successfully activated API key")
   else:
    LOG.info("Using test API key")
   os.environ[ENV_PRO_ACTIVATED]="1"
  except KeyActivationError as e:
   if log_license_issues():
    LOG.warning(e.message)
   check_require_pro()
  except FRuPD as e:
   if log_license_issues():
    LOG.warning("Unable to activate API key: %s %s"%(e,traceback.format_exc()))
   check_require_pro()
 return OnClose()
def log_license_issues():
 return api_key_configured()and localstack_config.is_env_not_false("LOG_LICENSE_ISSUES")
def api_key_configured():
 return read_api_key(raise_if_missing=FRuPJ)
def is_logged_in():
 configs=localstack_config.load_config_file()
 login_info=configs.get("login")
 if not login_info:
  return FRuPJ
 return FRuPI
def get_auth_headers():
 if TEST_AUTH_HEADERS:
  return TEST_AUTH_HEADERS
 configs=localstack_config.load_config_file()
 login_info=configs.get("login")
 if login_info:
  auth_token=login_info["token"]
  if not auth_token.startswith("%s "%login_info["provider"]):
   auth_token="%s %s"%(login_info["provider"],auth_token)
  return{"authorization":auth_token}
 api_key=read_api_key(raise_if_missing=FRuPJ)
 if api_key:
  return{"ls-api-key":api_key,"ls-version":__version__}
 raise FRuPD("Please log in first")
# Created by pyminifier (https://github.com/liftoff/pyminifier)
