from nacos_go_sdk_parser_types import SDKFunctionWrapperMapping

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


  return function_dict
