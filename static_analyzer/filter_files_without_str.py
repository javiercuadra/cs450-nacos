from typing import List

def remove_single_line_comments(line: str) -> str:
  """Remove single-line comments from a line of code."""
  comment_index = line.find("//")
  if comment_index != -1:
    return line[:comment_index]
  return line

def is_within_multiline_comment(line: str, inside_multiline_comment: bool) -> bool:
  """Check and toggle the multi-line comment state based on the current line."""
  if '/*' in line and '*/' in line:
    return inside_multiline_comment  # Comment starts and ends on the same line
  if '/*' in line:
    return True  # Entering a multi-line comment
  if '*/' in line:
    return False  # Exiting a multi-line comment
  return inside_multiline_comment

def contains_key_string(line: str, key_str: str) -> bool:
  """Check if the line contains the key string excluding function definitions."""
  return key_str in line and "func" not in line

def filter_files_without_str(files: List[str], key_str: str) -> List[str]:
  """
  Filter files that contain a specific key string outside of comments.

  Args:
      files (List[str]): A list of file paths to check.
      key_str (str): The key string to search for in each file.

  Returns:
      List[str]: A list of file paths that contain the key string outside of comments.
  """
  filtered_files = []
  for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as file:
      inside_multiline_comment = False
      for line in file:
        line = remove_single_line_comments(line)
        inside_multiline_comment = is_within_multiline_comment(line, inside_multiline_comment)

        if inside_multiline_comment or not contains_key_string(line, key_str):
          continue

        filtered_files.append(file_path)
        break  # Found the key string, no need to check further in this file

  return filtered_files
