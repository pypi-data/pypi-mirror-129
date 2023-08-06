from ctypes import *
import threading
import json
import os

class MyBuffer(threading.local):
  def __init__(self):
    self.buf = create_string_buffer(65535)
    self.bufSize = sizeof(self.buf)
    #print("Created new Buffer {}".format(self.buf))

tls_var = MyBuffer()

from .G2Exception import TranslateG2ModuleException, G2ModuleNotInitialized, G2ModuleGenericException

def resize_return_buffer(buf_, size_):
  """  callback function that resizes return buffer when it is too small
  Args:
  size_: size the return buffer needs to be
  """
  try:
    if not tls_var.buf:
      #print("New RESIZE_RETURN_BUF {}:{}".format(buf_,size_))
      tls_var.buf = create_string_buffer(size_)
      tls_var.bufSize = size_
    elif (tls_var.bufSize < size_):
      #print("RESIZE_RETURN_BUF {}:{}/{}".format(buf_,size_,tls_var.bufSize))
      foo = tls_var.buf
      tls_var.buf = create_string_buffer(size_)
      tls_var.bufSize = size_
      memmove(tls_var.buf, foo, sizeof(foo))
  except AttributeError:
      #print("AttributeError RESIZE_RETURN_BUF {}:{}".format(buf_,size_))
      tls_var.buf = create_string_buffer(size_)
      #print("Created new Buffer {}".format(tls_var.buf))
      tls_var.bufSize = size_
  return addressof(tls_var.buf)
  


class G2Config(object):
    """G2 config module access library

    Attributes:
        _lib_handle: A boolean indicating if we like SPAM or not.
        _resize_func_def: resize function definiton
        _resize_func: resize function pointer
        _module_name: CME module name
        _ini_file_name: name and location of .ini file
    """
    def init(self, module_name_, ini_file_name_, debug_=False):
        """  Initializes the G2 config module engine
        This should only be called once per process.
        Args:
            moduleName: A short name given to this instance of the config module
            iniFilename: A fully qualified path to the G2 engine INI file (often /opt/senzing/g2/python/G2Module.ini)
            verboseLogging: Enable diagnostic logging which will print a massive amount of information to stdout
        """
        self._module_name = self.prepareStringArgument(module_name_)
        self._ini_file_name = self.prepareStringArgument(ini_file_name_)
        self._debug = debug_

        if self._debug:
            print("Initializing G2 Config")

        self._lib_handle.G2Config_init.argtypes = [c_char_p, c_char_p, c_int]
        ret_code = self._lib_handle.G2Config_init(self._module_name,
                                 self._ini_file_name,
                                 self._debug)

        if self._debug:
            print("Initialization Status: " + str(ret_code))

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def initV2(self, module_name_, ini_params_, debug_=False):

        self._module_name = self.prepareStringArgument(module_name_)
        self._ini_params = self.prepareStringArgument(ini_params_)
        self._debug = debug_

        if self._debug:
            print("Initializing G2 Config")

        self._lib_handle.G2Config_init_V2.argtypes = [c_char_p, c_char_p, c_int]
        ret_code = self._lib_handle.G2Config_init_V2(self._module_name,
                                 self._ini_params,
                                 self._debug)

        if self._debug:
            print("Initialization Status: " + str(ret_code))

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def __init__(self):
        # type: () -> None
        """ G2Config class initialization
        """

        try:
          if os.name == 'nt':
            self._lib_handle = cdll.LoadLibrary("G2.dll")
          else:
            self._lib_handle = cdll.LoadLibrary("libG2.so")
        except OSError as ex:
          print("ERROR: Unable to load G2.  Did you remember to setup your environment by sourcing the setupEnv file?")
          print("ERROR: For more information see https://senzing.zendesk.com/hc/en-us/articles/115002408867-Introduction-G2-Quickstart")
          print("ERROR: If you are running Ubuntu or Debian please also review the ssl and crypto information at https://senzing.zendesk.com/hc/en-us/articles/115010259947-System-Requirements")
          raise G2ModuleGenericException("Failed to load the G2 library")

        self._resize_func_def = CFUNCTYPE(c_char_p, c_char_p, c_size_t)
        self._resize_func = self._resize_func_def(resize_return_buffer)


    def prepareStringArgument(self, stringToPrepare):
        # type: (str) -> str
        """ Internal processing function """

        #handle null string
        if stringToPrepare == None:
            return None
        #if string is unicode, transcode to utf-8 str
        if type(stringToPrepare) == str:
            return stringToPrepare.encode('utf-8')
        #if input is bytearray, assumt utf-8 and convert to str
        elif type(stringToPrepare) == bytearray:
            return stringToPrepare.decode().encode('utf-8')
        elif type(stringToPrepare) == bytes:
            return str(stringToPrepare).encode('utf-8')
        #input is already a str
        return stringToPrepare


    def clearLastException(self):
        """ Clears the last exception
        """

        self._lib_handle.G2Config_clearLastException.restype = None
        self._lib_handle.G2Config_clearLastException.argtypes = []
        self._lib_handle.G2Config_clearLastException()

    def getLastException(self):
        """ Gets the last exception
        """

        self._lib_handle.G2Config_getLastException.restype = c_int
        self._lib_handle.G2Config_getLastException.argtypes = [c_char_p, c_size_t]
        self._lib_handle.G2Config_getLastException(tls_var.buf,sizeof(tls_var.buf))
        resultString = tls_var.buf.value.decode('utf-8')
        return resultString

    def getLastExceptionCode(self):
        """ Gets the last exception code
        """

        self._lib_handle.G2Config_getLastExceptionCode.restype = c_int
        self._lib_handle.G2Config_getLastExceptionCode.argtypes = []
        exception_code = self._lib_handle.G2Config_getLastExceptionCode()
        return exception_code

    def create(self):
        """ Creates a new config handle from the stored template
        """
        self._lib_handle.G2Config_create.restype = c_void_p
        configHandle = self._lib_handle.G2Config_create()
        if configHandle == None:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)
        return configHandle

    def load(self,jsonConfig):
        """ Creates a new config handle from a json config string
        """
        _jsonConfig = self.prepareStringArgument(jsonConfig)
        self._lib_handle.G2Config_load.restype = c_void_p
        self._lib_handle.G2Config_load.argtypes = [c_char_p]
        configHandle = self._lib_handle.G2Config_load(_jsonConfig)
        if configHandle == None:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)
        return configHandle

    def close(self,configHandle):
        """ Closes a config handle
        """
        self._lib_handle.G2Config_close.argtypes = [c_void_p]
        self._lib_handle.G2Config_close(configHandle)

    def save(self,configHandle,response):
        """ Saves a config handle
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_save.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_save(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def listDataSources(self,configHandle,response):
        """ lists a set of data sources
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listDataSources.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listDataSources(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def listDataSourcesV2(self,configHandle,response):
        """ lists a set of data sources
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listDataSources_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listDataSources_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def listEntityClassesV2(self,configHandle,response):
        """ lists a set of entity classes
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listEntityClasses_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listEntityClasses_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def listEntityTypesV2(self,configHandle,response):
        """ lists a set of entity types
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listEntityTypes_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listEntityTypes_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def addDataSource(self,configHandle,dataSourceCode):
        """ Adds a data source
        """
        _dataSourceCode = self.prepareStringArgument(dataSourceCode)
        self._lib_handle.G2Config_addDataSource.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_addDataSource(configHandle,_dataSourceCode)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def addDataSourceWithID(self,configHandle,dataSourceCode,id):
        """ Adds a data source
        """
        _dataSourceCode = self.prepareStringArgument(dataSourceCode)
        self._lib_handle.G2Config_addDataSourceWithID.argtypes = [c_void_p, c_char_p, c_int]
        ret_code = self._lib_handle.G2Config_addDataSourceWithID(configHandle,_dataSourceCode,id)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def addDataSourceV2(self,configHandle,inputJson,response):
        """ Adds a data source
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_addDataSource_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_addDataSource_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def addEntityClassV2(self,configHandle,inputJson,response):
        """ Adds a entity class
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_addEntityClass_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_addEntityClass_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def addEntityTypeV2(self,configHandle,inputJson,response):
        """ Adds a entity type
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_addEntityType_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_addEntityType_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def deleteDataSourceV2(self,configHandle,inputJson):
        """ Deletes a data source
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_deleteDataSource_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_deleteDataSource_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def deleteEntityClassV2(self,configHandle,inputJson):
        """ Deletes an entity class
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_deleteEntityClass_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_deleteEntityClass_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def deleteEntityTypeV2(self,configHandle,inputJson):
        """ Deletes an entity type
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_deleteEntityType_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_deleteEntityType_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def listFeatureElementsV2(self,configHandle,response):
        """ lists the set of feature elements
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listFeatureElements_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listFeatureElements_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def getFeatureElementV2(self,configHandle,inputJson,response):
        """ get a feature element
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_getFeatureElement_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_getFeatureElement_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def addFeatureElementV2(self,configHandle,inputJson,response):
        """ Adds a feature element
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_addFeatureElement_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_addFeatureElement_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def deleteFeatureElementV2(self,configHandle,inputJson):
        """ Deletes a feature element
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_deleteFeatureElement_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_deleteFeatureElement_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def listFeatureClassesV2(self,configHandle,response):
        """ lists the set of feature classes
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listFeatureClasses_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listFeatureClasses_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)


        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def listFeaturesV2(self,configHandle,response):
        """ lists the set of features
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listFeatures_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listFeatures_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def getFeatureV2(self,configHandle,inputJson,response):
        """ get a feature
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_getFeature_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_getFeature_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def addFeatureV2(self,configHandle,inputJson,response):
        """ Adds a feature
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_addFeature_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_addFeature_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def deleteFeatureV2(self,configHandle,inputJson):
        """ Deletes a feature
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_deleteFeature_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_deleteFeature_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def addElementToFeatureV2(self,configHandle,inputJson):
        """ Adds an element to a feature
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_addElementToFeature_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_addElementToFeature_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def deleteElementFromFeatureV2(self,configHandle,inputJson):
        """ Deletes an element from a feature
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_deleteElementFromFeature_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_deleteElementFromFeature_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def listFeatureStandardizationFunctionsV2(self,configHandle,response):
        """ lists the set of standardization functions
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listFeatureStandardizationFunctions_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listFeatureStandardizationFunctions_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def listFeatureExpressionFunctionsV2(self,configHandle,response):
        """ lists the set of expression functions
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listFeatureExpressionFunctions_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listFeatureExpressionFunctions_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def listFeatureComparisonFunctionsV2(self,configHandle,response):
        """ lists the set of comparison functions
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listFeatureComparisonFunctions_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listFeatureComparisonFunctions_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def listFeatureDistinctFunctionsV2(self,configHandle,response):
        """ lists the set of distinct functions
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listFeatureDistinctFunctions_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listFeatureDistinctFunctions_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def listFeatureStandardizationFunctionCallsV2(self,configHandle,response):
        """ lists the set of feature standardization function calls
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listFeatureStandardizationFunctionCalls_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listFeatureStandardizationFunctionCalls_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def getFeatureStandardizationFunctionCallV2(self,configHandle,inputJson,response):
        """ get a feature standardization function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_getFeatureStandardizationFunctionCall_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_getFeatureStandardizationFunctionCall_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def addFeatureStandardizationFunctionCallV2(self,configHandle,inputJson,response):
        """ Adds a feature standardization function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_addFeatureStandardizationFunctionCall_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_addFeatureStandardizationFunctionCall_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def deleteFeatureStandardizationFunctionCallV2(self,configHandle,inputJson):
        """ Deletes a feature standardization function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_deleteFeatureStandardizationFunctionCall_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_deleteFeatureStandardizationFunctionCall_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def listFeatureExpressionFunctionCallsV2(self,configHandle,response):
        """ lists the set of feature expression function calls
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listFeatureExpressionFunctionCalls_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listFeatureExpressionFunctionCalls_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def getFeatureExpressionFunctionCallV2(self,configHandle,inputJson,response):
        """ get a feature expression function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_getFeatureExpressionFunctionCall_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_getFeatureExpressionFunctionCall_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def addFeatureExpressionFunctionCallV2(self,configHandle,inputJson,response):
        """ Adds a feature expression function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_addFeatureExpressionFunctionCall_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_addFeatureExpressionFunctionCall_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def deleteFeatureExpressionFunctionCallV2(self,configHandle,inputJson):
        """ Deletes a feature expression function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_deleteFeatureExpressionFunctionCall_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_deleteFeatureExpressionFunctionCall_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def addFeatureExpressionFunctionCallElementV2(self,configHandle,inputJson):
        """ Adds an element to a feature expression function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_addFeatureExpressionFunctionCallElement_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_addFeatureExpressionFunctionCallElement_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def deleteFeatureExpressionFunctionCallElementV2(self,configHandle,inputJson):
        """ Deletes an element from a feature expression function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_deleteFeatureExpressionFunctionCallElement_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_deleteFeatureExpressionFunctionCallElement_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def listFeatureComparisonFunctionCallsV2(self,configHandle,response):
        """ lists the set of feature comparison function calls
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listFeatureComparisonFunctionCalls_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listFeatureComparisonFunctionCalls_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def getFeatureComparisonFunctionCallV2(self,configHandle,inputJson,response):
        """ get a feature comparison function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_getFeatureComparisonFunctionCall_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_getFeatureComparisonFunctionCall_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def addFeatureComparisonFunctionCallV2(self,configHandle,inputJson,response):
        """ Adds a feature comparison function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_addFeatureComparisonFunctionCall_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_addFeatureComparisonFunctionCall_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def deleteFeatureComparisonFunctionCallV2(self,configHandle,inputJson):
        """ Deletes a feature comparison function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_deleteFeatureComparisonFunctionCall_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_deleteFeatureComparisonFunctionCall_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def addFeatureComparisonFunctionCallElementV2(self,configHandle,inputJson):
        """ Adds an element to a feature comparison function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_addFeatureComparisonFunctionCallElement_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_addFeatureComparisonFunctionCallElement_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def deleteFeatureComparisonFunctionCallElementV2(self,configHandle,inputJson):
        """ Deletes an element from a feature comparison function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_deleteFeatureComparisonFunctionCallElement_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_deleteFeatureComparisonFunctionCallElement_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def listFeatureDistinctFunctionCallsV2(self,configHandle,response):
        """ lists the set of feature distinct function calls
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listFeatureDistinctFunctionCalls_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listFeatureDistinctFunctionCalls_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def getFeatureDistinctFunctionCallV2(self,configHandle,inputJson,response):
        """ get a feature distinct function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_getFeatureDistinctFunctionCall_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_getFeatureDistinctFunctionCall_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def addFeatureDistinctFunctionCallV2(self,configHandle,inputJson,response):
        """ Adds a feature distinct function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_addFeatureDistinctFunctionCall_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_addFeatureDistinctFunctionCall_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def deleteFeatureDistinctFunctionCallV2(self,configHandle,inputJson):
        """ Deletes a feature distinct function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_deleteFeatureDistinctFunctionCall_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_deleteFeatureDistinctFunctionCall_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def addFeatureDistinctFunctionCallElementV2(self,configHandle,inputJson):
        """ Adds an element to a feature distinct function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_addFeatureDistinctFunctionCallElement_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_addFeatureDistinctFunctionCallElement_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def deleteFeatureDistinctFunctionCallElementV2(self,configHandle,inputJson):
        """ Deletes an element from a feature distinct function call
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_deleteFeatureDistinctFunctionCallElement_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_deleteFeatureDistinctFunctionCallElement_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

    def listAttributeClassesV2(self,configHandle,response):
        """ lists the set of attribute classes
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listAttributeClasses_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listAttributeClasses_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value


    def listAttributesV2(self,configHandle,response):
        """ lists the set of attributes
        """
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_listAttributes_V2.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_listAttributes_V2(configHandle,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def getAttributeV2(self,configHandle,inputJson,response):
        """ get an attribute
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_getAttribute_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_getAttribute_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def addAttributeV2(self,configHandle,inputJson,response):
        """ Adds an attribute
        """
        _inputJson = self.prepareStringArgument(inputJson)
        responseBuf = c_char_p(addressof(tls_var.buf))
        responseSize = c_size_t(tls_var.bufSize)
        self._lib_handle.G2Config_addAttribute_V2.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2Config_addAttribute_V2(configHandle,_inputJson,
                                             pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)

        response += responseBuf.value

    def deleteAttributeV2(self,configHandle,inputJson):
        """ Deletes an attribute
        """
        _inputJson = self.prepareStringArgument(inputJson)
        self._lib_handle.G2Config_deleteAttribute_V2.argtypes = [c_void_p, c_char_p]
        ret_code = self._lib_handle.G2Config_deleteAttribute_V2(configHandle,_inputJson)

        if ret_code == -1:
            raise G2ModuleNotInitialized('G2Config has not been succesfully initialized')
        elif ret_code < 0:
            self._lib_handle.G2Config_getLastException(tls_var.buf, sizeof(tls_var.buf))
            raise TranslateG2ModuleException(tls_var.buf.value)


    def destroy(self):
        """ Uninitializes the engine
        This should be done once per process after init(...) is called.
        After it is called the engine will no longer function.

        Args:

        Return:
            None
        """

        self._lib_handle.G2Config_destroy()

