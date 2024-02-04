from typing import Dict, List, Tuple
from nacos_go_sdk_parser_types import SDKFunctionWrapperMapping
import re

def parse_function_definition(line: str) -> Tuple[str, List[str]]:
  """
  Parses a function definition from a line of code.

  Extracts the function's name and its arguments from a given line assumed to contain
  a function definition following the Go syntax.

  Args:
      line (str): A line of code containing a function definition.

  Returns:
      Tuple[str, List[str]]: A tuple containing the name of the function and a list of its arguments.
  """
  parts = line.split('func')[1].split('(')
  func_name = parts[0].strip()
  args_part = parts[1].split(')')[0]
  func_args = [arg.strip() for arg in args_part.split(',') if arg.strip()]
  return func_name, func_args

def find_service_params(lines: List[str], start_index: int, sdk_call) -> Dict[str, str]:
  """
  Extracts service parameter assignments from code lines following a function definition.

  Scans lines of code starting from a given index to find assignments for specific service
  parameters: ServiceName, Ip, and Port. Assumes these parameters are assigned in a straightforward
  manner in the lines immediately following the identified function definition.

  Args:
      lines (List[str]): All lines of code from the file being analyzed.
      start_index (int): The index in `lines` to start the search from, usually the line
                          following a wrapper function definition.
      sdk_call (str): The name of the SDK call being wrapped by the identified functions.

  Returns:
      Dict[str, str]: A dictionary mapping parameter names ("ServiceName", "Ip", "Port")
                      to their assigned values in the code.
  """
  # Defines the params needed  for different SDK calls
  if sdk_call == "RegisterInstance":
    service_params = {"ServiceName": "", "Ip": "", "Port": ""}
  elif sdk_call == "SelectInstance":
    service_params = {"ServiceName": ""}

  for line in lines[start_index:]:
    for param in service_params.keys():
      if param in line:
        service_params[param] = line.split(":")[1].split(",")[0].strip()
  return service_params

def map_args_to_indices(func_args: List[str], service_params: Dict[str, str]) -> Dict[str, int]:
  """
  Maps function arguments to indices based on service parameter assignments.

  Given a list of function arguments and a dictionary of service parameters with their
  assigned values, this function maps each service parameter to the index of the argument
  it corresponds to. If the service parameter value is a string, it is directly assigned.

  Args:
      func_args (List[str]): The arguments of the wrapper function.
      service_params (Dict[str, str]): Service parameters and their assigned values.

  Returns:
      Dict[str, int]: A dictionary mapping service parameter names to indices in the
                      wrapper function's argument list.
  """
  index_map = {}
  for param, value in service_params.items():
    # if the value is a string, it is directly assigned
    if re.match(r'"([^"]*)"', value):
      index_map[param] = value
      continue
    for i, arg in enumerate(func_args):
      if value in arg:
        index_map[param] = i
  return index_map


def find_wrappers(files: List[str], sdk_call: str) -> Dict[str, SDKFunctionWrapperMapping]:
  """
  Identifies functions in a Go file that act as wrappers for the 'RegisterInstance' SDK call.

  Analyzes a given Go source file to find functions that wrap the 'RegisterInstance' call,
  extracting their names, arguments, and mappings of these arguments to specific service
  parameters (ServiceName, Ip, Port). Each identified wrapper function and its associated
  data is stored in a dictionary.

  Args:
      file (str): The path to the Go source file to be analyzed.
      sdk_call (str): The name of the SDK call to be wrapped by the identified functions.

  Returns:
      Dict[str, SDKFunctionWrapperMapping]: A dictionary where keys are the names of wrapper
                                            functions and values are SDKFunctionWrapperMapping
                                            objects containing detailed information about each
                                            wrapper function and its association with the
                                            'RegisterInstance' SDK call.
  """
  function_dict = {}
  for file in files:
    with open(file, 'r', encoding='utf-8') as f:
      lines = f.readlines()
      func_name, func_args = "", []
      for i, line in enumerate(lines):
        if 'func' in line and "{" in line:
          func_name, func_args = parse_function_definition(line)
        if sdk_call in line and func_name:  # Ensure func_name is not empty
          service_params = find_service_params(lines, i, sdk_call)
          wrapper_to_sdk_index_map = map_args_to_indices(func_args, service_params)
          dict_node = SDKFunctionWrapperMapping(func_name, func_args, sdk_call, wrapper_to_sdk_index_map)
          function_dict[func_name] = dict_node
  return function_dict
