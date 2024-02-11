# ManifestParser.py: AutoArmor JSON manifest file for Automated 
# Policy Generation for "Automatic Policy Generation for Inter-Service 
# Access Control of Microservices" 
# 
# Description
# This is a file for parsing a JSON-based manifest file. It simply just 
# returns a defaultdict object that represents the JSON-based manifest 
# file.
# 
# Randy Truong 
# Northwestern University 
# 10 February 2024 

import os 
import sys 
import json 
from collections import defaultdict
from typing import *  # import typing because I like type hints, but I also like python 


class ManifestParser: 
    def __init__(self, rawManifestFile) -> None: 
        """
        params: 
        - str rawManifestFile: The name of a JSON-based manifest file. 

        returns: 
        - None 
        """
        self.rawManifestFile: str = rawManifestFile
        self.finalDict: defaultdict = {}

        return None 

    def parse(self) -> None: 
        """  
        params: 
        - None 

        returns: 
        - None 
        """ 
        path: str = self.rawManifestFile

        if (not os.path.isfile(path)): 
            raise Exception("Not a valid file path.")

        with open(path, "r") as f: 
            f: str = f.read()
            self.finalDict = json.loads(f)

        return None 

