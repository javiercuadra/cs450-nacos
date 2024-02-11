# Modules 
`ManifestParser`: returns a 
`PermissionEngine`:  
`PolicyGeneratorEngine`: 

# Expected Workflow 
1. After generating a JSON manifest file of the service invocations 
for a given application (that utilizes a microservice architecture), 
the user will input the JSON file into `main.py` 
2. The `ManifestParser` is a wrapper around the `json` library. It will 
take the inputted JSON file and turn it into a dictionary 
3. The `PermisisonEngine` is will generate a `PermissionGraph` object that represents 
the permission relations between various services. 
4. Utilizing the `PermissionGraph` object, the `PolicyGenerator` module will 
generate microsegmentation policies.


