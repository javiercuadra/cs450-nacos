import sys
from typing import Dict, List

from nacos_go_sdk_parser_types import Service, SDKFunctionWrapperMapping

from parse_files import find_go_files, filter_files_with_nacos_import
from parse_wrapper import find_wrappers, filter_files_with_func_wrappers
from find_services import find_services

def define_directory_path() -> str:
  """
  Determines the directory path for analysis.

  This function checks if the user has provided a directory path as a command-line argument.
  If a path is provided, it uses that path. Otherwise, it defaults to using "./example" as
  the directory path. This is primarily used to set up the initial directory for parsing or
  analysis, allowing for optional user input to specify the directory.

  The function also prints the determined directory path to the console.

  Returns:
      str: The determined directory path to be used for parsing or analysis.
  """

  # Default directory if user just wants to test our parser
  directory_path: str = "./example"

  # Check if user gave a different directory
  if len(sys.argv) == 2:
    directory_path = sys.argv[1]

  print(f"Provided directory path: {directory_path}")
  return directory_path

def find_all_go_files(directory_path: str) -> List['str']:
  """
  Searches for and lists all Go (.go) files within a specified directory.

  This function traverses the given directory path and all its subdirectories
  to find files with the '.go' extension. It leverages the `find_go_files`
  function to perform the actual search. Each found file path is printed to
  the console. This is useful for identifying all Go source files in a project
  or a specific part of a project.

  Args:
      directory_path (str): The root directory path from which the search
                            for Go files will begin.

  Returns:
      List[str]: A list of file paths, each pointing to a discovered Go file.
  """
  print(f"\n\nFinding all Go files located within {directory_path}")
  go_files: List[str] = find_go_files(directory_path)

  for file_path in go_files:
    print(file_path)

  return go_files

def find_nacos_files(go_files: List['str']) -> List['str']:
  """
  Filters a list of Go file paths to identify those that use Nacos SDK's service discovery functions.

  This function examines each provided Go file to determine if it contains imports or usage
  of the Nacos SDK for Go, specifically focusing on service discovery functions. It leverages
  the `filter_files_with_nacos_import` function to perform the actual filtering. Each file path
  that is determined to use the Nacos SDK is printed to the console. This function is useful
  for isolating parts of a Go project that interact with Nacos service discovery, facilitating
  analysis or modification of those interactions.

  Args:
      go_files (List[str]): A list of file paths, each pointing to a Go source file.

  Returns:
      List[str]: A list of file paths, each pointing to a Go file that uses Nacos SDK's
                  service discovery functions. If no such files are found, the list will be empty.
  """
  print("\n\nFinding all Go files that use nacos_sdk_go's service discovery functions")
  nacos_go_files: List['str'] = filter_files_with_nacos_import(go_files)

  for file_path in nacos_go_files:
      print(file_path)

  return nacos_go_files

def find_wrapper_functions(nacos_files: List['str']) -> Dict[str, SDKFunctionWrapperMapping]:
  """
    Identifies and maps wrapper functions to their corresponding SDK function calls
    within a list of specified Go files that use Nacos SDK.

    This function searches through the given list of Go files, identifying functions
    that act as wrappers to the 'RegisterInstance' call in the Nacos SDK. It compiles
    a mapping of these wrapper functions, detailing their parameters, the specific SDK
    call they wrap, and a parameter index map for further analysis.

    Args:
        nacos_files (List[str]): A list of file paths, each pointing to a Go file
                                 suspected to contain Nacos SDK function calls.

    Returns:
        Dict[str, SDKFunctionWrapperMapping]: A dictionary where each key is the name of
                                              a wrapper function and the value is an
                                              SDKFunctionWrapperMapping object containing
                                              detailed mapping information for that wrapper.
                                              This includes parameters of the wrapper, the
                                              SDK function call it wraps, and a parameter
                                              index mapping.
    """

  print("\n\nFinding all function wrappers for RegisterInstance")
  sdk_function_wrapper_mappings: Dict[str, SDKFunctionWrapperMapping] = find_wrappers(nacos_files)

  for wrapper, mapping in sdk_function_wrapper_mappings.items():
    print(f"Function: {wrapper}:")
    print(f"    Parameters: {mapping.wrapper_params},")
    print(f"    SDK Call: {mapping.sdk_func_call},")
    print(f"    Index Map: {mapping.wrapper_to_sdk_index_map}")

  return sdk_function_wrapper_mappings

def find_registered_services(sdk_function_wrapper_mappings: Dict[str, SDKFunctionWrapperMapping]) -> Dict[str, Service]:
  """
    Identifies services registered in the provided directory by analyzing the
    SDK function wrapper mappings.

    This function iterates over a dictionary of SDK function wrapper mappings
    to find Go files that contain calls to these wrapper functions. It then
    identifies the services being registered through these wrapper functions
    and compiles a dictionary of these services, keyed by service name.

    Args:
        sdk_function_wrapper_mappings (Dict[str, SDKFunctionWrapperMapping]): A dictionary
            where keys are names of wrapper functions and values are SDKFunctionWrapperMapping
            objects, which contain details about the wrapper functions and their SDK calls.

    Returns:
        Dict[str, Service]: A dictionary of identified services, where each key is the
            name of a service and each value is a Service object containing the service's
            name, IP address, and port number.

  """

  service_dict: Dict[str, Service] = {}

  print("\n\nFind all the services registered in this directory")
  for key, value in sdk_function_wrapper_mappings.items():

    # Search for Go files containing the wrapper function
    wrapper_function_files: List[str] = filter_files_with_func_wrappers(go_files, key)

    # Identify and store the services resgistered
    service_dict.update(find_services(wrapper_function_files, key, value))

  for k, v in service_dict.items():
    print(f"{k} is located at {v.ip}:{v.port}")

if __name__ == "__main__":
  # Define the directory to run the parser on
  directory_path = define_directory_path()

  # Locate all Go files in the directory
  go_files = find_all_go_files(directory_path)

  # Filter out files that use Nacos service discovery
  nacos_files = find_nacos_files(go_files)

  # Find all function wrappers for registering functions
  sdk_function_wrapper_mappings: Dict[str, SDKFunctionWrapperMapping] = find_wrapper_functions(nacos_files[1])

  # Find all services registered in the repository
  service_dict = find_registered_services(sdk_function_wrapper_mappings)
