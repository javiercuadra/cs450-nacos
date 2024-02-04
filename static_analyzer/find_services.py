from typing import List, Dict, Tuple
from nacos_go_sdk_parser_types import SDKFunctionWrapperMapping, Service

def __extract_args(line: str, wrapper_name: str) -> List[str]:
  """_summary_

  Args:
      line (str): _description_
      wrapper_name (str): _description_

  Returns:
      List[str]: _description_
  """

  # The line is of the form `... wrapper_name(arg_1, ..., arg_n)`
  # Split the line to get the arguments and strip them of whitespace
  args = line.split(wrapper_name)[1].split('(')[1].split(')')[0].split(',')
  args = [arg.strip() for arg in args if arg.strip()]

  return args

def __map_args_to_parameter(args: List[str], index_map: Dict[str, int]) -> Tuple[str, str, str]:
  """
  Maps arguments to their corresponding service parameters based on an index mapping.

  This function takes a list of arguments and an index mapping dictionary to extract
  specific service parameters: the service name, IP address, and port number. The index
  map specifies the positions of these parameters within the args list. This is useful
  for dynamically extracting parameter values from a list when the order of values is
  known only at runtime.

  Args:
      args (List[str]): A list of strings representing various parameters, from which
                        the service name, IP address, and port number need to be extracted.
      index_map (Dict[str, int]): A dictionary mapping parameter names ("ServiceName", "Ip",
                                    "Port") to their respective indexes in the `args` list.

  Returns:
      Tuple[str, str, str]: A tuple containing the service name, IP address, and port number,
                              extracted based on the provided index mapping.
  """

  serviceName = args[index_map["ServiceName"]]
  ip = args[index_map["Ip"]]
  port = args[index_map["Port"]]

  return (serviceName, ip, port)

def find_services(files: List[str], wrapper_name: str, wrapper_data: SDKFunctionWrapperMapping):
  """
  Identifies services registered through wrapper functions in the given files.

  This function scans a list of files for occurrences of a specified wrapper function
  and attempts to extract service registration details (service name, IP, and port)
  based on the arguments passed to that wrapper function. The extraction is guided
  by a mapping of wrapper function parameters to SDK function call parameters,
  contained in `wrapper_data`. Each identified service is stored in a dictionary
  keyed by service name.

  Args:
      files (List[str]): A list of paths to Go source files to be scanned for service
                          registration calls.
      wrapper_name (str): The name of the wrapper function to look for in the files,
                          which is expected to make the SDK service registration call.
      wrapper_data (SDKFunctionWrapperMapping): An instance containing metadata about
                          the wrapper function, including a mapping of parameter names
                          to their expected positions in the argument list.

  Returns:
      Dict[str, Service]: A dictionary mapping service names to `Service` objects,
                          each representing a service identified in the scanned files.
                          The `Service` object contains the service name, IP address,
                          and port number extracted from the wrapper function calls.
  """

  service_dict: Dict[str, Service] = {}

  # Iterate through all the files
  for file in files:

    # Read the file
    with open(file, 'r', encoding='utf-8') as f:
      lines = f.readlines()

      # Iterate through all the lines in the file
      for _, line in enumerate(lines):

        # Check if the wrapper function is in the line
        if wrapper_name not in line:
          continue

        # Extract arguments from line
        args = __extract_args(line, wrapper_name)

        # Extract the argument value at the index for its parameter name.
        index_map = wrapper_data.wrapper_to_sdk_index_map
        service_name, ip, port = __map_args_to_parameter(args, index_map)

        # Create and store the found  service
        service_dict[service_name] = Service(service_name, ip, port)

  return service_dict
