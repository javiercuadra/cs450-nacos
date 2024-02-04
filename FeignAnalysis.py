import os
from collections import defaultdict
import yaml
import xml.etree.ElementTree as ET

# Two dir variables are used because some projects store all service information in one directory and implement the Feign remote calling interface of all services in another directory.
root_dir = "/Users/davidhu0/Downloads/demo.nacos 2" # Scan the entire project to obtain the relationship between the Feign client interface and the corresponding called service

service_dir  = "/Users/davidhu0/Downloads/demo.nacos 2" # Process each service directory: 1. Get the current service name 2. Get the Feign client of which services are called by the current service


service =[]
global interface
global interface_service
interface_service = {}
interface = []

label_service = {}

def handle_properties(file):
    service_info = {}
    dictname = {}
    try:
        for line in file.readlines():
            line = line.strip().replace('\n', '')
            if line.find("#") != -1:
                line = line[0:line.find('#')]
            if line.find("=") > 0:
                strs = line.split('=')
                strname = strs[0].strip()
                value = strs[1].strip()
                dictname[strname] = value
                if strname.find('spring.application.name') > 0:
                    service_info['service_name'] = value
                if strname.find('discovery.ip') > 0:
                    service_info['service_ip'] = value
    except UnicodeDecodeError: # 二进制文件不要
        pass # Fond non-text data
    return service_info


def get_service_inteface(dir):
    for foldername, subfolders, filenames in os.walk(dir):
        if 'src' in subfolders and 'main' in os.listdir(os.path.join(foldername, 'src')):
            for subfoldername, _, subfilenames in os.walk(os.path.join(foldername, 'src', 'main')):
                if 'java' in subfoldername:
                    for java_foldername, java_subfolders, java_filenames in os.walk(subfoldername):
                        for java_files in java_filenames:
                            if java_files.endswith('.java'):
                                with open(os.path.join(java_foldername, java_files), 'r') as f:
                                    FeignFlag = 0
                                    lineId = 0
                                    nouse = 0
                                    for line in f.readlines():
                                      # Process single-line and multi-line comments
                                        if line.find("//") != -1:
                                            line = line[0:line.find('//')]#Comments may appear behind the code
                                        if '/*' in line or line.startswith('/*'):
                                            if '"'  not in line or "'" not in line:
                                                nouse = 1
                                        if '*/' in line or line.startswith('*/'):
                                            if '"' not in line or "'" not in line:
                                                nouse = 0
                                        if nouse == 1:
                                            continue
                                        if line != '':
                                            lineId += 1
                                        if "@FeignClient" in line:
                                            FeignFlag = lineId
                                            if 'value' in line:
                                                lines = line.split('value')
                                                value = lines[1].strip().split('"')[1]
                                            elif 'name' in line:
                                                lines = line.split('name')
                                                value = lines[1].strip().split('"')[1]
                                            elif '=' not in line:
                                                lines = line.split('(')
                                                value = lines[1].strip().split('"')[1]
                                        if 'interface' in line and FeignFlag > 0 and lineId == (FeignFlag+1):#It is possible that the first line imports that package or something.
                                            lines = line.split('interface')
                                            interface_name = lines[1].strip().split('{')[0].strip()
                                            interface.append(interface_name)
                                            interface_service[interface_name] = value
def get_service_name(service_dir):
    global service_name
    service_name = ''
    for foldername, subfolders, filenames in os.walk(service_dir):
        if 'src' in subfolders and 'main' in os.listdir(os.path.join(foldername, 'src')):
            if os.path.isfile(os.path.join(foldername, 'pom.xml')): # Take out the artifactId in pom.xml
                tree = ET.parse(os.path.join(foldername, 'pom.xml'))
                root = tree.getroot()
                for child in root:
                    if 'artifactId' in child.tag:
                        artifact_id = child.text
            for subfoldername, _, subfilenames in os.walk(os.path.join(foldername, 'src', 'main')):
                if 'resources' in subfoldername:
                    for file in subfilenames:
                        service_name_tmp = ''
                        if '.yml' not in file and '.yaml' not in file and '.properties' not in file:
                            continue
                        if file.endswith('.yml') or file.endswith('.yaml'):
                            yml_file = os.path.join(subfoldername, file)
                            with open(yml_file, 'r') as f:
                                try:
                                    application_yaml = yaml.load(f.read(), Loader=yaml.FullLoader) #yml contains other characters, safe_load will cause problems.
                                    if application_yaml == None:
                                        continue
                                    service_name_tmp = application_yaml.get('spring', {}).get('application', {}).get('name', {})
                                except :
                                    with open(yml_file, 'r') as f:
                                        spring_line_id = 0
                                        application_line_id = 0
                                        data = f.readlines()
                                        lineId = 0
                                        for line in data:
                                            lineId += 1
                                            if line.startswith('spring:'):
                                                spring_line_id = lineId
                                            elif line.startswith('  application:') and lineId == (spring_line_id + 1):
                                                application_line_id = lineId
                                            elif line.startswith('    name:') and lineId == (application_line_id + 1):
                                                if '@artifactId@' in line:
                                                    service_name_tmp = artifact_id
                                                else:
                                                    # line = line.split('name:')
                                                    service_name_tmp = line.split('name:')[1].strip()
                        if file.endswith('.properties'):
                            properties_file = os.path.join(subfoldername, file)
                            with open(properties_file, 'r', encoding='gbk') as f:
                                service_info = handle_properties(f)
                                if service_info:
                                    service_name_tmp = service_info['service_name']
                        if service_name_tmp != {} and service_name_tmp != '':
                            service_name = service_name_tmp
                            service.append(service_name)


def get_interface_calls(service_dir):
    for foldername, subfolders, filenames in os.walk(service_dir):
        if 'src' in subfolders and 'main' in os.listdir(os.path.join(foldername, 'src')):
            for subfoldername, _, subfilenames in os.walk(os.path.join(foldername, 'src', 'main')):
                if 'java' in subfoldername:
                    for java_foldername, java_subfolders, java_filenames in os.walk(subfoldername):
                        for java_files in java_filenames:
                            if java_files.endswith('.java'):
                                with open(os.path.join(java_foldername, java_files), 'r') as f:
                                    lastAutowired = 0
                                    nouse = 0
                                    lineId = 0
                                    for line in f.readlines():
                                        if line.find("//") != -1:
                                            line = line[0:line.find('//')]
                                        if '/*' in line or line.startswith('/*'):
                                            if '"'  not in line or "'" not in line:
                                                nouse = 1
                                        if '*/' in line or line.startswith('*/'):
                                            if '"' not in line or "'" not in line:
                                                nouse = 0
                                        if nouse == 1:
                                            continue
                                        if line != '':
                                            lineId += 1
                                        if '@Autowired' in line or '@Inject' in line or '@NonNull' in line or '@Resource' in line:
                                            lastAutowired = int(lineId)
                                        if lastAutowired > 0:
                                            for interfaceClient in interface:
                                                if interfaceClient in line:
                                                    if interface_service[interfaceClient] == service_name:  # 自己调自己
                                                        continue
                                                    elif interface_service[interfaceClient] not in service_calls[service_name]:
                                                        service_calls[service_name].append(interface_service[interfaceClient])
                                                    lastAutowired = 0

def get_service_label(dir):
    global  service_label
    service_label = {}
    for foldername, subfolders, filenames in os.walk(dir):
        for file in filenames:
            if file.endswith('.yaml'):
                yml_file = os.path.join(dir, file)
                with open(yml_file, 'r') as f:
                    try:
                        # application_yaml = yaml.load_all(f)
                        application_yaml = yaml.load_all(f.read(), Loader=yaml.FullLoader)
                        # print(application_yaml, type(application_yaml))
                        if application_yaml == None:
                            continue
                        for i in application_yaml:
                            # print(i)
                            # print(i.get('kind',{}))
                            if 'Deployment' in i.get('kind',{}) :
                                service_label = i.get('spec', {}).get('template', {}).get('metadata', {}).get('labels', {})
                                # print('111')
                                # print(service_label)
                    except:
                        with open(yml_file, 'r') as f:
                            data = f.readlines()

                            print('open deployment yaml error!')
                            print(data)
                        # with open(yml_file, 'r') as f:
                        #     spring_line_id = 0
                        #     application_line_id = 0
                        #     data = f.readlines()
                        #     lineId = 0
                        #     for line in data:
                        #         lineId += 1
                        #         if line.startswith('metadata:'):
                        #             spring_line_id = lineId
                        #         elif line.startswith('  labels:') and lineId == (spring_line_id + 2):
                        #             application_line_id = lineId
                        #         elif line.startswith('    app:') and lineId == (application_line_id + 1):
                        #             service_label = line.split('app:')[1].strip()

        break #只取每个服务第一层目录下的deployment.yaml

def generate_policy(service_calls, dir):
    for i in all_service_calls:
        policy = {
            'apiVersion': 'networking.k8s.io/v1',
            'kind': 'NetworkPolicy',
            'metadata': {'name': ''},
            'spec': {
                'podSelector':
                    {'matchLabels':
                         {'app': ''}},
                'policyTypes': ['Egress'],
                'egress': [{
                    'to': [
                    ]}]}}
        policy['metadata']['name'] = i
        policy['spec']['podSelector']['matchLabels'] = label_service[i]
        for j in all_service_calls[i][i]:
            app = {}
            matchLabels = {}
            podSelector = {}
            # app['app'] = label_service[j]
            matchLabels['matchLabels'] = label_service[j]
            podSelector['podSelector'] = matchLabels
            policy['spec']['egress'][0]['to'].append(podSelector)
        filename = i + '-polic`y.yaml'
        filename = os.path.join(dir, filename)
        if service_calls == {}:
            return
        try:
            with open(filename, "x", encoding='utf-8') as f:
                yaml.dump(data=policy, stream=f, allow_unicode=True)
        except FileExistsError:
            with open(filename, "w", encoding='utf-8') as f:
                f.truncate()  # 清空内容
                yaml.dump(data=policy, stream=f, allow_unicode=True)



get_service_inteface(root_dir) #Get the binding relationship between the called service and the feign client under the entire project
interface = list(set(interface))
all_service_calls = defaultdict(list)
for _, subfolders, _ in os.walk(service_dir):
    for subdir in subfolders:
        current_service = os.path.join(service_dir, subdir)
        if os.path.isfile(current_service):  # Not a folder
            continue
        service_calls = defaultdict(list)
        get_service_name(current_service)
        if service_name == '':
            continue
        get_service_inteface(current_service) # Get it again under the current project, because the Feign client under the service may have the same name.
        interface = list(set(interface))
        get_interface_calls(current_service)
        all_service_calls[service_name] = service_calls
        get_service_label(current_service)
        if service_label != {}:
            label_service[service_name] = service_label
    break

print(service)
#print(all_service_calls)
# print("XXXXX")
# print(label_service)
# Because all service directories need to be scanned to obtain the complete service name-label
# generate_policy(all_service_calls, service_dir)
