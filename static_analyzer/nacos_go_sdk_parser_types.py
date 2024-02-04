from typing import List, Dict

class SDKFunctionWrapperMapping:
  '''
  Represents the mapping between an SDK function call and its wrapper function.

  This class stores detailed information about a wrapper function, including its
  name, parameters, the SDK function it calls, and a mapping between the indices
  of wrapper function parameters and SDK function call parameters. This is useful
  for analyzing and managing how SDK functions are utilized within higher-level
  wrapper functions in the codebase.

  Attributes:
      wrapper_name (str): The name of the wrapper function.
      wrapper_params (List[str]): A list of parameter names for the wrapper function.
      sdk_func_call (str): The name of the SDK function being called.
      wrapper_to_sdk_index_map (Dict[str, int]): A dictionary mapping parameter names
          from the wrapper function to their corresponding indices in the SDK function
          call parameters.


  """
  '''

  def __init__(self, wrapper_name, wrapper_params, sdk_func_call, wrapper_to_sdk_index_map):
    """
    Initializes a new instance of the Service class.

    Args:
        wrapper_name (str): The name of the wrapper function.
        wrapper_params (List[str]): The parameters of the wrapper function.
        sdk_func_call (str): The name of the SDK function call.
        wrapper_to_sdk_index_map (Dict[str, int]): Mapping of wrapper function parameters
            to SDK function call parameters by index.
    """
    self.wrapper_name: str = wrapper_name
    self.wrapper_params: List[str] = wrapper_params
    self.sdk_func_call: str = sdk_func_call
    self.wrapper_to_sdk_index_map: Dict[str, int] = wrapper_to_sdk_index_map

class Service:
  """
  Represents a service with networking details.

  This class is designed to encapsulate the essential attributes of a network service,
  including its name, IP address, and port number. It provides a structured way to
  manage and access the service's networking details throughout the application.

  Attributes:
      service_name (str): The name of the service.
      ip (str): The IP address of the service.
      port (str): The port number on which the service is running.
  """

  def __init__(self, service_name, ip, port):
    """
    Initializes a new instance of the Service class.

    Args:
        service_name (str): The name of the service.
        ip (str): The IP address of the service.
        port (str): The port number on which the service is running.
    """
    self.service_name: str = service_name
    self.ip: str = ip
    self.port: str = port
