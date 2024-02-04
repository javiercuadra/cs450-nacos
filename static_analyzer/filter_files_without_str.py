from typing import List

def remove_single_line_comments(line: str) -> str:
  """
  Removes single-line comments from a given line of code.

  If a single-line comment is detected (marked by "//"), everything after
  this marker in the line is removed. If no comment is found, the line is
  returned unchanged.

  Args:
      line (str): The line of code from which to remove single-line comments.

  Returns:
      str: The line of code with single-line comments removed.
  """
  comment_index = line.find("//")
  if comment_index != -1:
    return line[:comment_index]
  return line

def is_within_multiline_comment(line: str, inside_multiline_comment: bool) -> bool:
  """
  Determines if the current line is within a multi-line comment block.

  This function checks the current line for the start ("/*") or end ("*/")
  of a multi-line comment. The state of being inside a multi-line comment
  is toggled based on these markers. If both markers are present on the same
  line, it's assumed the line starts and ends a comment within itself, and
  the state remains unchanged.

  Args:
      line (str): The current line of code to check.
      inside_multiline_comment (bool): The current state indicating whether
                                        the parsing is inside a multi-line comment block.

  Returns:
      bool: True if the current or subsequent lines are within a multi-line
            comment block, False otherwise.
  """
  if '/*' in line and '*/' in line:
    return inside_multiline_comment  # Comment starts and ends on the same line
  if '/*' in line:
    return True  # Entering a multi-line comment
  if '*/' in line:
    return False  # Exiting a multi-line comment
  return inside_multiline_comment

def contains_key_string(line: str, key_str: str) -> bool:
  """
  Checks if a given line contains a specified key string, excluding function definitions.

  This function searches for the presence of a specific key string within the line,
  but ignores any occurrences within function definitions to focus only on use cases
  outside of these definitions.

  Args:
      line (str): The line of code to search.
      key_str (str): The key string to look for in the line.

  Returns:
      bool: True if the key string is found outside of function definitions, False otherwise.
  """
  return key_str in line and "func" not in line

def filter_files_without_str(files: List[str], key_str: str) -> List[str]:
  """
  Filters a list of files to find those that contain a specified key string outside of comments.

  This function iterates through each provided file, reading its content to determine
  if the key string is present outside of both single-line and multi-line comments.
  Files that contain the key string under these conditions are included in the returned list.

  Args:
      files (List[str]): A list of paths to files to be scanned.
      key_str (str): The key string to search for within the files.

  Returns:
      List[str]: A list of paths to files that contain the key string outside of comments.
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
