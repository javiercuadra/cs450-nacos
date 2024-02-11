# Automated Microsegmentation Policy Generation 
# for Cloud-Native Applications Using Service Discovery
# 
# Randy Truong, Javier Cuadra, David Hu (+ NU LIST) 
# Northwestern University 
# 10 February 2024 

import os 
import sys 
import json 
import modules
from collections import defaultdict 
import xml.etree.ElementTree as ET 
from typing import * 

def main(): 
    pass 

if (__name__ == "__main__"):  
    if (len(sys.argv) < 2): 
        raise Exception("[ERROR]: Please add a valid input file\nUsage: python3 main.py <filename>\n") 

    filename = sys.argv[1]

    # ... 

    main()



