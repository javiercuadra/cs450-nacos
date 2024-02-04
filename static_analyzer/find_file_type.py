import os
from typing import List

def find_file_type(starting_directory: str, file_type: str) -> List[str]:
  """
  Recursively searches for and lists all files of a specified type within a given directory.

  This function traverses the specified directory and all its subdirectories to find files
  with the given file extension (file_type). It builds and returns a list of the full paths
  to each of these files.

  Args:
      starting_directory (str): The path of the directory from which to start the search.
      file_type (str): The file extension to search for, without the leading dot. For example,
                        use 'go' to search for Go files, 'py' for Python files, etc.

  Returns:
      List[str]: A list containing the full paths to all files found with the specified
                  file extension. If no such files are found, the list will be empty.
  """
  go_file_paths = []

  # Iterate through all items inside the starting_directory
  for root, dirs, files in os.walk(starting_directory):

    # Iterate through each file in the starting_directory
    for file in files:

      # Check if the file is of the type provided
      if not file.endswith(f".{file_type}"):
        continue

      # Generate the entire filepath for the given file and add it to the list
      full_path = os.path.join(root, file)
      go_file_paths.append(full_path)

    # Iterate through all directories in the starting_directory
    for directory in dirs:

      # Add any new files of the specified type within the subdirectory
      go_file_paths.extend(find_file_type(os.path.join(root, directory), file_type))

  return go_file_paths
