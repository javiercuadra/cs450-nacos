import os
from typing import List

def find_go_files(starting_directory: str) -> List[str]:
  """
  Traverse a directory and return a list of file paths for all .go files.

  Args:
      directory (str): The root directory to start the search from.

  Returns:
      list: A list of file paths for .go files.
  """
  go_file_paths = []
  for root, dirs, files in os.walk(starting_directory):
    for file in files:
      if file.endswith(".go"):
        full_path = os.path.join(root, file)
        go_file_paths.append(full_path)
    for directory in dirs:
      go_file_paths.extend(find_go_files(directory))
  return go_file_paths

def filter_files_with_nacos_import(go_files: List[str]) -> List[str]:
    """
    Filter .go files that import nacos-sdk-go.

    Args:
        go_files (list): A list of .go file paths to check.

    Returns:
        list: A list of file paths that import nacos-sdk-go.
    """
    nacos_import_files = []
    nacos_import_str = "github.com/nacos-group/nacos-sdk-go/clients"
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
          if nacos_import_str in line:
            nacos_import_files.append(file_path)
            break  # Found the import, no need to check further in this file
    return nacos_import_files
