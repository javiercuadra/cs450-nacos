from nacos_go_sdk_parser_types import SDKFunctionWrapperMapping
from typing import List

def find_wrappers(file):
  function_dict = {}
  with open(file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if 'func' in line and "{" in line:  # Simplistic check for function definition
          parts = line.split('func')[1].split('(')
          func_name = parts[0].strip()  # Function name
          args_part = parts[1].split(')')[0]  # Arguments part
          func_args = args_part.split(',')  # Splitting arguments by comma
          func_args = [arg.strip() for arg in func_args if arg.strip()]  # Cleaning and filtering empty arguments
          continue
        if "RegisterInstance" in line:
          # print(f"Found RegisterInstance with wrapper function {func_name} and args {func_args}")

          for j in range(i, len(lines)):
            if "ServiceName" in lines[j]:
              serviceName_var = lines[j].split(":")[1].split(",")[0].strip()
            if "Ip" in lines[j]:
              ip_var =lines[j].split(":")[1].split(",")[0].strip()
            if "Port" in lines[j]:
              port_var = lines[j].split(":")[1].split(",")[0].strip()

          wrapper_to_sdk_index_map= {}
          for i, arg in enumerate(func_args):
            if serviceName_var in arg:
              wrapper_to_sdk_index_map["ServiceName"] = i
            if ip_var in arg:
              wrapper_to_sdk_index_map["Ip"] = i
            if port_var in arg:
              wrapper_to_sdk_index_map["Port"] = i

          dict_node = SDKFunctionWrapperMapping(func_name, func_args, "RegisterInstance", wrapper_to_sdk_index_map)
          function_dict[func_name] = dict_node
          # print(f"Function: {dict_node.wrapper_name}, Args: {dict_node.wrapper_params}, SDK Call: {dict_node.sdk_func_call}, Index Map: {dict_node.wrapper_to_sdk_index_map}")



          # Process the node or print it here
          # Example: print(f"Function: {dict_node.name}, Args: {dict_node.args}, SDK Call: {dict_node.sdk_call}")

        # if "}" in line:  # Simplistic check for the end of a function block
        #   inside_func = False  # Reset flags as we exit a function block

  return function_dict

def filter_files_with_func_wrappers(go_files: List[str], func_wrapper: str) -> List[str]:
    """
    Filter .go files that import nacos-sdk-go.

    Args:
        go_files (list): A list of .go file paths to check.

    Returns:
        list: A list of file paths that import nacos-sdk-go.
    """
    nacos_import_files = []
    nacos_import_str = func_wrapper
    for file_path in go_files:
      with open(file_path, 'r', encoding='utf-8') as file:
        inside_multiline_comment = False
        for line in file:
          # Check for and handle single-line comments
          single_line_comment_index = line.find("//")
          if single_line_comment_index != -1:
            line = line[:single_line_comment_index]  # Exclude the comment part

          # Check for the start or end of multi-line comments
          if '/*' in line:
            inside_multiline_comment = True
            # Check if end of comment is on the same line, and adjust accordingly
            if '*/' in line:
              inside_multiline_comment = False
              # Remove the comment block from the line
              start = line.find('/*')
              end = line.find('*/') + 2
              line = line[:start] + line[end:]
            else:
              continue  # Skip the rest of the line processing for multi-line comment start
          elif '*/' in line:
            inside_multiline_comment = False
            continue  # Skip the rest of the line processing for multi-line comment end

          if inside_multiline_comment:
            continue  # Skip processing lines inside multi-line comments

          # After handling comments, check if the line contains the nacos-sdk-go import
          if nacos_import_str in line and not "func" in line:
            nacos_import_files.append(file_path)
            break  # Found the import, no need to check further in this file
    return nacos_import_files
