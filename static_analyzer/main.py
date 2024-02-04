import sys

from nacos_go_sdk_parser_types import Service

import parse_files
import parse_wrapper

def find_services(files, wrapper_name, wrapper_data):
  service_dict = {}
  for file in files:
    with open(file, 'r', encoding='utf-8') as f:
      lines = f.readlines()
      for i, line in enumerate(lines):
        if wrapper_name in line:
          print(f"Found {wrapper_name} in {file}")
          args = line.split(wrapper_name)[1].split('(')[1].split(')')[0].split(',')
          args = [arg.strip() for arg in args if arg.strip()]

          map = wrapper_data.wrapper_to_sdk_index_map
          serviceName = args[map["ServiceName"]]
          ip = args[map["Ip"]]
          port = args[map["Port"]]

          service = Service(serviceName, ip, port)
          service_dict[serviceName] = service
  return service_dict


if __name__ == "__main__":
  directory_path = "./example"

  if len(sys.argv) == 2:
    directory_path = sys.argv[1]
    print(f"Provided file path: {directory_path}")

  print(f"Find all go files located within {directory_path}")
    # Replace with the path to your repository
  go_files = parse_files.find_go_files(directory_path)

  print("\n\nPrinting all go file paths in the repository.")
  for file_path in go_files:
      print(file_path)

  print("\n\nBeginning to filter go_files from to only contain files that import nacos-sdk-go:")
  nacos_go_files = parse_files.filter_files_with_nacos_import(go_files)

  print("\n\nPrinting all filtered go file paths in the repository.")
  for file_path in nacos_go_files:
      print(file_path)

  func_dict = parse_wrapper.find_wrappers(nacos_go_files[1])

  service_dict = {}

  for key, value in func_dict.items():
    print(f"Here is the function, {key}, that wraps around the sdk function {value.sdk_func_call}. It contains the following arguments: {value.wrapper_params}")
    func_wrapper_files = parse_wrapper.filter_files_with_func_wrappers(go_files, key)
    print(f"\n\nPrinting all filtered go file paths containing func_wrapper {key} in the repository.")
    for file_path in func_wrapper_files:
        print(file_path)


    service_dict.update(find_services(func_wrapper_files, key, value))


  for k, v in service_dict.items():
    print(f"The service {k} is located at {v.ip}:{v.port}")
