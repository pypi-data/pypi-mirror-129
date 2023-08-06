from ctypes import *
import threading
import json
import os

tls_var = threading.local()

from csv import reader as csvreader

from .G2Exception import TranslateG2ModuleException, G2ModuleNotInitialized, G2ModuleGenericException

def resize_return_buffer(buf_, size_):
  """  callback function that resizs return buffer when it is too small
  Args:
  size_: size the return buffer needs to be
  """
  try:
    if (sizeof(tls_var.buf) < size_) :
      tls_var.buf = create_string_buffer(size_)
  except AttributeError:
      tls_var.buf = create_string_buffer(size_)
  return addressof(tls_var.buf)


class G2Engine(object):
    """G2 engine access library

    Attributes:
        _lib_handle: A boolean indicating if we like SPAM or not.
        _resize_func_def: resize function definiton
        _resize_func: resize function pointer
        _engine_name: CME engine name
        _ini_file_name: name and location of .ini file
    """
    def init(self, engine_name_, ini_file_name_, debug_=False, configID = 1):
        """  Initializes the G2 engine
        This should only be called once per process.  Currently re-initializing the G2 engin
        after a destroy requires unloaded the class loader used to load this class.
        Args:
            engineName: A short name given to this instance of the engine
            iniFilename: A fully qualified path to the G2 engine INI file (often /opt/senzing/g2/python/G2Module.ini)
            verboseLogging: Enable diagnostic logging which will print a massive amount of information to stdout

        Returns:
            int: 0 on success
        """

        self._engine_name = engine_name_
        self._ini_file_name = ini_file_name_
        self._debug = debug_
        if self._debug:
            print("Initializing G2 engine")

        resize_return_buffer(None, 65535)

        self._lib_handle.G2_init.argtypes = [c_char_p, c_char_p, c_int]
        retval = self._lib_handle.G2_init(self._engine_name.encode('utf-8'),
                                 self._ini_file_name.encode('utf-8'),
                                 self._debug)

        if self._debug:
            print("Initialization Status: " + str(retval))

        if retval == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        elif retval < 0:
            raise G2ModuleGenericException("Failed to initialize G2 Engine")

        if type(configID) == bytearray:
            cID = c_longlong(0)
            self._lib_handle.G2_getActiveConfigID.argtypes = [POINTER(c_longlong)]
            ret_code = self._lib_handle.G2_getActiveConfigID(cID)
            if ret_code == -2:
                self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
                self._lib_handle.G2_clearLastException()
                raise TranslateG2ModuleException(tls_var.buf.value)
            elif ret_code < 0:
                raise G2ModuleGenericException("ERROR_CODE: " + str(ret_code))
            for i in bytes(cID.value):
                configID.append(i)
        else:
            ret_code = 0
        return min(ret_code, retval)



    def __init__(self):
        # type: () -> None
        """ G2Engine class initialization
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

    def primeEngine(self):
        retval = self._lib_handle.G2_primeEngine()
        if self._debug:
            print("Initialization Status: " + str(retval))

        if retval == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        elif retval < 0:
            raise G2ModuleGenericException("Failed to initialize G2 Engine")
        return retval

    def process(self, input_umf_):
        # type: (str) -> None
        """ Generic process function without return
        This method will send a record for processing in g2.

        Args:
            record: An input record to be processed. Contains the data and control info.

        Return:
            None
        """

        if type(input_umf_) == str:
            input_umf_string = input_umf_.encode('utf-8')
        elif type(input_umf_) == bytearray:
            input_umf_string = str(input_umf_)
        else:
            input_umf_string = input_umf_
        resize_return_buffer(None, 65535)
        self._lib_handle.G2_process.argtypes = [c_char_p]
        self._lib_handle.G2_process.restype = c_int
        ret_code = self._lib_handle.G2_process(input_umf_string)
        if ret_code == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        elif ret_code < 0:
            raise G2ModuleGenericException("ERROR_CODE: " + str(ret_code))

    def processWithResponse(self, input_umf_):
        """ Generic process function that returns results
        This method will send a record for processing in g2. It is a synchronous
        call, i.e. it will wait until g2 actually processes the record, and then
        optionally return any response message.

        Args:
            record: An input record to be processed. Contains the data and control info.
            response: If there is a response to the message it will be returned here.
                     Note there are performance benefits of calling the process method
                     that doesn't need a response message.

        Return:
            str: The response in G2 JSON format.
        """

        # type: (str) -> str
        """  resolves an entity synchronously
        Args:
            input_umf_: G2 style JSON
        """
        if type(input_umf_) == str:
            input_umf_string = input_umf_.encode('utf-8')
        elif type(input_umf_) == bytearray:
            input_umf_string = str(input_umf_)
        else:
            input_umf_string = input_umf_
        resize_return_buffer(None, 65535)
        responseBuf = c_char_p(None)
        responseSize = c_size_t(0)
        self._lib_handle.G2_processWithResponseResize.argtypes = [c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2_processWithResponseResize(input_umf_string,
                                                                 pointer(responseBuf),
                                                                 pointer(responseSize),
                                                                 self._resize_func)
        if ret_code == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        elif ret_code == -1:
            raise G2ModuleNotInitialized('G2Engine has not been succesfully initialized')

        return responseBuf.value.decode('utf-8')

    def checkRecord(self, input_umf_, recordQueryList):
        # type: (str,str,str) -> str
        """ Scores the input record against the specified one
        Args:
            input_umf_: A JSON document containing the attribute information
                   for the observation.
            dataSourceCode: The data source for the observation.
            recordID: The ID for the record

        Return:
            str: The response in G2 JSON format.
        """

        if type(input_umf_) == str:
            input_umf_string = input_umf_.encode('utf-8')
        elif type(input_umf_) == bytearray:
            input_umf_string = str(input_umf_)
        else:
            input_umf_string = input_umf_
        resize_return_buffer(None, 65535)
        responseBuf = c_char_p(None)
        responseSize = c_size_t(0)
        self._lib_handle.G2_checkRecord.argtypes = [c_char_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2_checkRecord(input_umf_string,
                                                   recordQueryList,
                                                   pointer(responseBuf),
                                                   pointer(responseSize),
                                                   self._resize_func)
        if ret_code == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        elif ret_code == -1:
            raise G2ModuleNotInitialized('G2Engine has not been succesfully initialized')

        return responseBuf.value.decode('utf-8')

    def getExportHandle(self, exportType, max_match_level):
        # type: (str, int) -> c_void_p
        """ Generate a CSV or JSON export
        This is used to export entity data from known entities.  This function
        returns an export-handle that can be read from to get the export data
        in the requested format.  The export-handle should be read using the "G2_fetchNext"
        function, and closed when work is complete. If CSV, the first output row returned
        by the export-handle contains the CSV column headers as a string.  Each
        following row contains the exported entity data.

        Args:
            exportType: CSV or JSON
            max_match_level: The match-level to specify what kind of entity resolves
                         and relations we want to see.
                             1 -- same entities
                             2 -- possibly same entities
                             3 -- possibly related entities
                             4 -- disclosed relationships
        Return:
            c_void_p: handle for the export
        """
        g2ExportFlags = 0
        if max_match_level == 1:
            # Include match-level 1
            g2ExportFlags = 4
        elif max_match_level == 2:
            # Include match-level 1,2
            g2ExportFlags = 12
        elif max_match_level == 3:
            # Include match-level 1,2,3
            g2ExportFlags = 28
        elif max_match_level == 4:
            # Include match-level 1,2,3,4
            g2ExportFlags = 60
        else:
            g2ExportFlags = 0
        g2ExportFlags = g2ExportFlags | 3
        if exportType == 'CSV':
            self._lib_handle.G2_exportCSVEntityReport.restype = c_void_p
            exportHandle = self._lib_handle.G2_exportCSVEntityReport(g2ExportFlags)
        else:
            self._lib_handle.G2_exportJSONEntityReport.restype = c_void_p
            exportHandle = self._lib_handle.G2_exportJSONEntityReport(g2ExportFlags)
        return exportHandle

    def exportCSVEntityReport(self, max_match_level):
        return self.getExportHandle('CSV', max_match_level)

    def exportJSONEntityReport(self, max_match_level):
        return self.getExportHandle('JSON', max_match_level)

    def fetchNext(self, exportHandle):
        # type: (c_void_p) -> str
        """ Fetch a record from an export
        Args:
            exportHandle: handle from generated export

        Returns:
            str: Record fetched, empty if there is no more data
        """

        resultString = ""
        resize_return_buffer(None,65535)
        self._lib_handle.G2_fetchNext.argtypes = [c_void_p, c_char_p, c_size_t]
        rowData = self._lib_handle.G2_fetchNext(c_void_p(exportHandle),tls_var.buf,sizeof(tls_var.buf))
        while rowData:
            resultString += tls_var.buf.value.decode('utf-8')
            if resultString[-1] == '\n':
                resultString = resultString[0:-1]
                break
            else:
                rowData = self._lib_handle.G2_fetchNext(c_void_p(exportHandle),tls_var.buf,sizeof(tls_var.buf))
        return resultString

    def fetchCsvExportRecord(self, exportHandle, csvHeaders = None):
        # type: (c_void_p, str) -> str
        """ Fetch a CSV record from an export.
        Args:
            exportHandle: handle from generated export
            csvHeaders: CSV header record

        Returns:
            dict: Record fetched using the csvHeaders as the keys.
                  None if no more data is available.
        """
        resultString = self.fetchNext(exportHandle)
        if resultString:
            csvRecord = next(csvreader([resultString]))
            if csvHeaders:
                csvRecord = dict(list(zip(csvHeaders, csvRecord)))
        else:
            csvRecord = None
        return csvRecord


    def closeExport(self, exportHandle):
        self._lib_handle.G2_closeExport(c_void_p(exportHandle))

    def prepareStringArgument(self, stringToPrepare):
        # type: (str) -> str
        """ Internal processing function """

        if stringToPrepare == None:
            return None
        #if string is unicode, transcode to utf-8 str
        if type(stringToPrepare) == str:
            return stringToPrepare.encode('utf-8')
        #if input is bytearray, assumt utf-8 and convert to str
        elif type(stringToPrepare) == bytearray:
            return str(stringToPrepare)
        #input is already a str
        return stringToPrepare

    def addRecord(self,dataSourceCode,recordId,jsonData,loadId=None):
        # type: (str,str,str,str) -> int
        """ Loads the JSON record
        Args:
            dataSourceCode: The data source for the observation.
            recordID: The ID for the record
            jsonData: A JSON document containing the attribute information
                   for the observation.
            loadID: The observation load ID for the record, can be null and will default to dataSourceCode

        Return:
            int: 0 on success
        """

        _dataSourceCode = self.prepareStringArgument(dataSourceCode)
        _loadId = self.prepareStringArgument(loadId)
        _recordId = self.prepareStringArgument(recordId)
        _jsonData = self.prepareStringArgument(jsonData)
        resize_return_buffer(None, 65535)
        ret_code = self._lib_handle.G2_addRecord(_dataSourceCode,_recordId,_jsonData,_loadId)
        if ret_code == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        elif ret_code < 0:
            raise G2ModuleGenericException("ERROR_CODE: " + str(ret_code))
        return ret_code

    def addRecordWithReturnedRecordID(self,dataSourceCode,recordID,jsonData,loadId=None):
        # type: (str,str,str,str) -> int
        """ Loads the JSON record
        Args:
            dataSourceCode: The data source for the observation.
            recordID: A memory buffer for returning the recordID
            jsonData: A JSON document containing the attribute information
                   for the observation.
            loadID: The observation load ID for the record, can be null and will default to dataSourceCode

        Return:
            int: 0 on success
        """

        _dataSourceCode = self.prepareStringArgument(dataSourceCode)
        _loadId = self.prepareStringArgument(loadId)
        _jsonData = self.prepareStringArgument(jsonData)
        resultString = ""
        resize_return_buffer(None, 65535)
        self._lib_handle.G2_addRecordWithReturnedRecordID.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_size_t]
        ret_code = self._lib_handle.G2_addRecordWithReturnedRecordID(_dataSourceCode,_jsonData,_loadId, tls_var.buf, sizeof(tls_var.buf))
        if ret_code == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        elif ret_code < 0:
            raise G2ModuleGenericException("ERROR_CODE: " + str(ret_code))
        resultString = str(tls_var.buf.value.decode('utf-8'))
        for i in resultString:
            recordID.append(i)
        return ret_code



    def replaceRecord(self,dataSourceCode,recordId,jsonData,loadId=None):
        # type: (str,str,str,str) -> int
        """ Replace the JSON record, loads if doesn't exist
        Args:
            dataSourceCode: The data source for the observation.
            recordID: The ID for the record
            jsonData: A JSON document containing the attribute information
                   for the observation.
            loadID: The load ID for the record, can be null and will default to dataSourceCode

        Return:
            int: 0 on success
        """

        _dataSourceCode = self.prepareStringArgument(dataSourceCode)
        _loadId = self.prepareStringArgument(loadId)
        _recordId = self.prepareStringArgument(recordId)
        _jsonData = self.prepareStringArgument(jsonData)
        resize_return_buffer(None, 65535)
        ret_code = self._lib_handle.G2_replaceRecord(_dataSourceCode,_recordId,_jsonData,_loadId)
        if ret_code == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        elif ret_code < 0:
            raise G2ModuleGenericException("ERROR_CODE: " + str(ret_code))
        return ret_code

    def deleteRecord(self,dataSourceCode,recordId,loadId=None):
        # type: (str,str,str) -> int
        """ Delete the record
        Args:
            dataSourceCode: The data source for the observation.
            recordID: The ID for the record
            loadID: The load ID for the record, can be null and will default to dataSourceCode

        Return:
            int: 0 on success
        """

        _dataSourceCode = self.prepareStringArgument(dataSourceCode)
        _loadId = self.prepareStringArgument(loadId)
        _recordId = self.prepareStringArgument(recordId)
        resize_return_buffer(None, 65535)
        ret_code = self._lib_handle.G2_deleteRecord(_dataSourceCode,_recordId,_loadId)
        if ret_code == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        elif ret_code < 0:
            raise G2ModuleGenericException("ERROR_CODE: " + str(ret_code))
        return ret_code


    def searchByAttributes(self,jsonData,response):
        # type: (str,bytearray) -> int
        """ Find records matching the provided attributes
        Args:
            jsonData: A JSON document containing the attribute information to search.
            response: A bytearray for returning the response document; if an error occurred, an error response is stored here.
        Return:
            int: 0 upon success, other for error.
        """
        _jsonData = self.prepareStringArgument(jsonData)
        resize_return_buffer(None, 65535)
        responseBuf = c_char_p(None)
        responseSize = c_size_t(0)
        self._lib_handle.G2_searchByAttributes.argtypes = [c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2_searchByAttributes(_jsonData,
                                                                 pointer(responseBuf),
                                                                 pointer(responseSize),
                                                                 self._resize_func)
        if ret_code == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        stringRet = str(tls_var.buf.value.decode('utf-8'))
        for i in stringRet:
            response.append(i)
        return ret_code

    def getEntityByEntityID(self,entityID,response):
        # type: (int,bytearray) -> int
        """ Find the entity with the given ID
        Args:
            entityID: The entity ID you want returned.  Typically referred to as
                      ENTITY_ID in JSON results.
            response: A bytearray for returning the response document; if an error occurred, an error response is stored here.

        Return:
            int: 0 upon success, other for error.
        """

        resize_return_buffer(None, 65535)
        responseBuf = c_char_p(None)
        responseSize = c_size_t(0)
        self._lib_handle.G2_getEntityByEntityID.argtypes = [c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2_getEntityByEntityID(entityID,
                                                                 pointer(responseBuf),
                                                                 pointer(responseSize),
                                                                 self._resize_func)
        if ret_code == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        stringRet = str(tls_var.buf.value.decode('utf-8'))
        for i in stringRet:
            response.append(i)
        return ret_code

    def getEntityByRecordID(self,dsrcCode,recordId,response):
        # type: (str,str,bytearray) -> int
        """ Get the entity containing the specified record
        Args:
            dataSourceCode: The data source for the observation.
            recordID: The ID for the record
            response: A bytearray for returning the response document; if an error occurred, an error response is stored here.

        Return:
            int: 0 upon success, other for error.
        """

        _dsrcCode = self.prepareStringArgument(dsrcCode)
        _recordId = self.prepareStringArgument(recordId)
        resize_return_buffer(None, 65535)
        responseBuf = c_char_p(None)
        responseSize = c_size_t(0)
        self._lib_handle.G2_getEntityByRecordID.argtypes = [c_char_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2_getEntityByRecordID(_dsrcCode,_recordId,
                                                                 pointer(responseBuf),
                                                                 pointer(responseSize),
                                                                 self._resize_func)
        if ret_code == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        stringRet = str(responseBuf.value.decode('utf-8'))
        for i in stringRet:
            response.append(i)
        return ret_code

    def getRecord(self,dsrcCode,recordId,response):
        # type: (str,str,bytearray) -> int
        """ Get the specified record
        Args:
            dataSourceCode: The data source for the observation.
            recordID: The ID for the record
            response: A bytearray for returning the response document; if an error occurred, an error response is stored here.

        Return:
            int: 0 upon success, other for error.
        """

        _dsrcCode = self.prepareStringArgument(dsrcCode)
        _recordId = self.prepareStringArgument(recordId)
        resize_return_buffer(None, 65535)
        responseBuf = c_char_p(None)
        responseSize = c_size_t(0)
        self._lib_handle.G2_getRecord.argtypes = [c_char_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2_getRecord(_dsrcCode,_recordId,
                                                                 pointer(responseBuf),
                                                                 pointer(responseSize),
                                                                 self._resize_func)
        if ret_code == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        stringRet = str(responseBuf.value.decode('utf-8'))
        for i in stringRet:
            response.append(i)
        return ret_code

    def stats(self):
        # type: () -> object
        """ Retrieve the workload statistics for the current process.
        Resets them after retrieved.

        Args:

        Return:
            object: JSON document with statistics
        """

        resize_return_buffer(None, 65535)
        responseBuf = c_char_p(None)
        responseSize = c_size_t(0)
        self._lib_handle.G2_stats.argtypes = [POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2_stats(pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)
        if ret_code == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        elif ret_code == -1:
            raise G2ModuleNotInitialized('G2Engine has not been succesfully initialized')

        return str(responseBuf.value.decode('utf-8'))


    def getLastException(self):
        responseBuf = c_char_p(None)
        responseSize = c_size_t(256)
        ret_code = self._lib_handle.G2_getLastException(responseBuf, responseSize)
        return str(responseBuf.value)

    def getLastExceptionCode(self):
        return self._lib_handle.G2_getLastExceptionCode(tls_var.buf, sizeof(tls_var.buf))

    def clearLastException(self):
        self._lib_handle.G2_clearLastException()

    def exportConfig(self,response, configID=1):
        # type: (bytearray) -> int
        """ Retrieve the G2 engine configuration

        Args:
            response: A bytearray for returning the response document; if an error occurred, an error response is stored here.

        Return:
            int: 0 upon success, other for error.
        """

        resize_return_buffer(None, 65535)
        responseBuf = c_char_p(None)
        responseSize = c_size_t(0)
        self._lib_handle.G2_exportConfig.argtypes = [POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        ret_code = self._lib_handle.G2_exportConfig(pointer(responseBuf),
                                             pointer(responseSize),
                                             self._resize_func)
        if ret_code == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        elif ret_code < 0:
            raise G2ModuleGenericException("ERROR_CODE: " + str(ret_code))
        stringRet = str(responseBuf.value.decode('utf-8'))
        for i in stringRet:
            response.append(i)

        if type(configID) == bytearray:
            cID = c_longlong(0)
            self._lib_handle.G2_getActiveConfigID.argtypes = [POINTER(c_longlong)]
            ret_code2 = self._lib_handle.G2_getActiveConfigID(cID)
            if ret_code2 == -2:
                self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
                self._lib_handle.G2_clearLastException()
                raise TranslateG2ModuleException(tls_var.buf.value)
            elif ret_code2 < 0:
                raise G2ModuleGenericException("ERROR_CODE: " + str(ret_code2))
            for i in bytes(cID.value):
                configID.append(i)
        else:
            ret_code2 = 0
        return min(ret_code, ret_code2)


    def getActiveConfigID(self, configID):
        # type: (bytearray) -> object
        """ Retrieve the active config ID for the G2 engine

        Args:
            configID: A bytearray for returning the identifier value for the config

        Return:
            int: 0 upon success, other for error.
        """

        cID = c_longlong(0)
        self._lib_handle.G2_getActiveConfigID.argtypes = [POINTER(c_longlong)]
        ret_code = self._lib_handle.G2_getActiveConfigID(cID)
        if ret_code == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        elif ret_code < 0:
            raise G2ModuleGenericException("ERROR_CODE: " + str(ret_code))
        for i in bytes(cID.value):
            configID.append(i)
        return ret_code


    def getRepositoryLastModifiedTime(self, lastModifiedTime):
        # type: (bytearray) -> object
        """ Retrieve the last modified time stamp of the entity store repository

        Args:
            lastModifiedTime: A bytearray for returning the last modified time of the data repository

        Return:
            int: 0 upon success, other for error.
        """

        lastModifiedTimeStamp = c_longlong(0)
        self._lib_handle.G2_getRepositoryLastModifiedTime.argtypes = [POINTER(c_longlong)]
        ret_code = self._lib_handle.G2_getRepositoryLastModifiedTime(lastModifiedTimeStamp)
        if ret_code == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        elif ret_code < 0:
            raise G2ModuleGenericException("ERROR_CODE: " + str(ret_code))
        for i in bytes(lastModifiedTimeStamp.value):
            lastModifiedTime.append(i)
        return ret_code

    def purgeRepository(self, reset_resolver_=True):
        # type: (bool) -> None
        """ Purges the G2 repository

        Args:
            reset_resolver: Re-initializes the engine.  Should be left True.

        Return:
            None
        """

        resize_return_buffer(None, 65535)
        retval = self._lib_handle.G2_purgeRepository()
        if retval == -2:
            self._lib_handle.G2_getLastException(tls_var.buf, sizeof(tls_var.buf))
            self._lib_handle.G2_clearLastException()
            raise TranslateG2ModuleException(tls_var.buf.value)
        elif retval == -1:
            raise G2ModuleNotInitialized('G2Engine has not been succesfully initialized')

        if reset_resolver_ == True:
            self.restart()

    def restart(self):
        """  Internal function """
        moduleName = self._engine_name
        iniFilename = self._ini_file_name
        self.destroy()
        self.init(moduleName, iniFilename, False)

    def destroy(self):
        """ Uninitializes the engine
        This should be done once per process after init(...) is called.
        After it is called the engine will no longer function.

        Args:

        Return:
            None
        """

        return self._lib_handle.G2_destroy()

