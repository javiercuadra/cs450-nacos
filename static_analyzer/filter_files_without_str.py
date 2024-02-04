from typing import List

def filter_files_without_str(files: List[str], key_str: str) -> List[str]:
    """
    Filter .go files that import nacos-sdk-go.

    Args:
        go_files (list): A list of .go file paths to check.

    Returns:
        list: A list of file paths that import nacos-sdk-go.
    """
    nacos_import_files = []
    nacos_import_str = key_str
    for file_path in files:
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
