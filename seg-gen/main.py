# Automated Microsegmentation Policy Generation 
# for Cloud-Native Applications Using Service Discovery
# 
# Randy Truong, Javier Cuadra, David Hu (+ NU LIST) 
# Northwestern University 
# 10 February 2024 

# Necessary Imports
import os 
import sys 
import json 
from collections import defaultdict 
from typing import * 

# Custom Imports :)
from modules.ManifestParser import ManifestParser
from modules.PermissionGraphEngine import PermissionGraph
from modules.PolicyGeneratorEngine import PolicyGenerator



# import xml.etree.ElementTree as ET 

def main(filename: str): 
    parser = ManifestParser(filename)
    parser.parse()
    # print(parser.finalDict["requests"])

if (__name__ == "__main__"):  
    if (len(sys.argv) < 2): 
        raise Exception("[ERROR]: Please add a valid input file\nUsage: python3 main.py <filename>\n") 

    filename = sys.argv[1]

    # ... 

    main(filename)



