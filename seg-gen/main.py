# Automated Microsegmentation Policy Generation 
# for Cloud-Native Applications Using Service Discovery
#
# Randy Truong, Javier Cuadra, David Hu (+ NU LIST) 
# Northwestern University 
# 10 February 2024 

import os 
from collections import defaultdict 
# import yaml 
import xml.etree.ElementTree as ET 
from typing import * 

# Generating Policies: 
# - If 

class GeneratePolicy: 
    def __init__(self, serviceCall: List[str]) -> None: 
        """
        params: 
        - serviceCalls: An array of string arrays 

        """
        self.serviceMeta: defaultdict = { 
                                         'name' : '' # TODO: Should we include 
                                                     # other service metadata? (ip addr's + ports, etc.)
                                         } 

        self.policySpecification: defaultdict = {} # TODO: Research microsegmentation 
                                                   # policy generation for service discovery


        self.finalPolicy: defaultdict = {  
                                         'apiVersion' : 'nacos/v2', 
                                         'policyType' : 'NetworkPolicy', 
                                         'metadata'   : self.serviceMetadata,
                                         'spec'       : self.policySpecification
                                         } 

        self.serviceCalls: List[str] = serviceCalls 
        return None 

    # TODO generateMetadata()
    def generateMetadata(self) -> None: 
        """ 
        params: None 

        desc: 
        - From the instance's `serviceCalls`, generate policy's 
        """
        # Base Case: Not exists any serviceCalls 
        if (not self.serviceCalls): 
            raise Exception("[ERROR]: No parsable service calls.")

        
        # Notes: 
        # - Why does policy['metadata']['name'] take in a list?
        

        

        pass 

    # TODO generatePolicy()
    def generatePolicy(self) -> None: 
        """
        params: None

        desc: 
        - Given a list of service calls, generate a policy from a `policyTemplate` 
        """
        # Base Case: Not exists any serviceCalls 
        if (not self.serviceCalls): 
            raise Exception("[ERROR]: No parsable service calls.")


        pass 

    # TODO dump()
    def dump(self) -> None: 
        """
        params: None

        desc: 
        - 
        """
        # Base Case: Not exists any serviceCalls 
        if (not self.serviceCalls): 
            raise Exception("[ERROR]: No parsable service calls.")

        try:  
            with open(filename, "x", encoding="utf-8") as f: 
                yaml.dump(data=self.finalPolicy, stream=f, allow_unicode=True) 
        except FileExistsError: 
            with open(filename, "w", encoding="utf-8") as f: 
                f.truncate() 
                yaml.dump(data=self.finalPolicy, stream=f, allow_unicode=True) 

        pass 


def main(): 
    pass 

if (__name__ == "__main__"):  
    main()



