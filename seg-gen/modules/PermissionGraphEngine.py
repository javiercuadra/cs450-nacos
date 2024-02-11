# PermissionEngine.py: AutoArmor Permission Graph Generation Engine 
# 
# Automated Microservice Policy Generation 
# for Cloud-Native Applications Using Service 
# Discovery 
# 
# Given a parsed manifest file. Generate a directed acyclic 
# graph representation of a microservice architecture-
# based application. 
#
# Randy Truong 
# Northwestern University 
# 10 February 2024 

""" 
Example of rawGraph: 
    [ node1: { 
              "type":, 
              "version": , 
              "adjList": , 
              }, 
      node2: { 
              "type": , 
              "version": , 
              "adjList" , 
              }, 
      node3: {
              "type": , 
              "version": , 
              "adjList": , 
              }, 
      node4: { 
              "type": , 
              "version": , 
              "adjList" , 
              }, 
      node5: { 
              "type": , 
              "version: , 
              "adjList" , 
              }, 
    ] 

Example of serviceGraph:   
    [  
      "serviceNode1": {
                        "adjList": [] 
                       }, 
      "serviceNode2": {
                        "adjList": [] 
                       }, 
      "serviceNode3": { 
                        "adjList": [] 
                       }, 
      "serviceNode4": {
                        "adjList": [] 
                       }, 
    ] 
     
""" 

import os 
import sys 
import json 
import PermissionGraphObjects.Node, PermissionGraphObjects.Edge
from collections import defaultdict
from typing import * 

class PermissionGraph: 
    def __init__(self, manifests: List[defaultdict]) -> None: 
        """
        params:  
        - defaultdict manifestDict: This is a dictionary version 
        of the parsed manifest file. 
        
        returns: 
        - None 

        desc: 
        - Constructor for `PermissionGraph` object 

        attributes: 
        - `List[defaultdict] PermissionGraph.manifests`: 
        - `defaultdict self.rawGraph`: List of all nodes N_{s} and N_{v} within G 
        - `defaultdict self.serviceGraph`: Hierarchal mapping of N_{s} and N_{v} within G 
        """
        manifests.sort(key = lambda a: a["service"]) 

        self.manifests: List[defaultdict] = manifests 
        self.rawGraph: defaultdict = {} 
        self.serviceGraph: defaultdict = {} 
        return None 

    def mapManifest(self, manifest: defaultdict, makeServiceNode: bool) -> None: 
        """ 
        params: 
        - defaultdict manifest: A manifest file 
        - bool makeServiceNode: Determines whether or not we should make (i) a 
        service node or (ii) a verison node 
        """ 
        serviceName, versionName, requests = (manifest["service"], 
                                              manifest["version"], 
                                              manifest["requests"])

        match makeServiceNode: 
            # Case 1: (makeServiceNode == 1) -> Add entry into service graph + 
            # make node in raw graph + add edges 
            case True: 
                if (serviceName in self.serviceGraph):   
                    return None 

                else: 
                    self.serviceGraph[serviceName]: defaultdict = {"adjList" : {} 
                                                                   } # adjList 
                    self.rawGraph[serviceName]: defaultdict = {"version": [], 
                                                               "adjList": []
                                                               }
                    self.mapRequests(serviceName, versionName, requests)
            # Case 2: (makeServiceNode == 0) -> Create version node + add edges 
            case False: 
                if (serviceName not in self.serviceGraph 
                    or serviceName not in self.rawGraph): 
                    raise Exception(f"No entry exists for {serviceName}")

                else: 
                    node = {"version": versionName, 
                            "adjList": []
                            }
                    self.serviceGraph[serviceName]["children"].append(node) 
                    self.mapRequests(serviceName, versionName, requests)
        return None 

    # TODO mapRequests() 
    def mapRequests(self, serviceName: str, version: str, requests: List[defaultdict]) -> None: 
        """
        params: 
        - str serviceName: The name of the service that we are adding nodes to 
        - str version: The version of the service that we are adding nodes to 

        returns: 
        - None 

        desc: 
        This is a function that maps requests as one of two edges in the permission 
        graph: 
        - E_{b}: Belonging Edge (Edge that connects a version node to a service node) 
        - E_{r}: Request Edge (Edge that connects a service to another service) 
        """

        if (serviceName not in self.serviceGraph 
            or serviceName not in self.rawGraph): 
            raise Exception(f"No entry exists for {serviceName}")

        else: 
            pass
            # service = self.serviceGraph[serviceName][
            # self.

        

        pass 

    # generateGraph() 
    def generateGraph(self) -> None: 
        """ 
        params: 
        - None 

        returns: 
        - None 

        desc: 
        - Generates permission graph from the `PermissionGraph.manifest` dict
        """ 

        # Remark: The permission graph is generated utilizing the following 
        # attributes: 
        # 
        # G = (N_{s}, N_{v}, E_{b}, E_{r}) where 
        # 
        #   N_{s} (Service Node):    Generic service for microservice architecture  
        #   N_{v} (Version Node):    Variation of N_{s} that can be invoked with varying permissions 
        #   E_{b} (Belonging Edge):  An edge that connects N_{v} with its corresponding N_{s}
        #   E_{r} (Request Edge):    An edge that connects N_{s1} with another N_{s2} 
        # 
        # Plan: 
        #   1. Generate overarching service node
        #   2. Generate corresponding version nodes 

        match len(manifests): 
            # Case 1: len(manifests) == 0 -> Throw exception 
            case 0: 
                raise Exception("No manifests/services found.")

            # Case 2: len(manifests) == 1 -> Create service node and attach version + edges
            case 1: 
                service = self.manifests[0]
                self.mapManifest(service, True)
                self.mapManifest(service, False) 

            # Case 3: Create multiple service nodes 
            case _: 
                formerService: str = "null" 

                for m in manifests: 

                    service: str = m["service"] 
                    requests: List[defaultdict] = m["requests"] 
                    # Not in service graph -> Create service node + version node + edges 
                    if (service != formerService): 
                        self.mapManifest(service, True) 
                        self.mapManifest(service, False) 
                        # self.mapRequests() 

                    # Otherwise -> Create new version node 
                    else: 
                        self.mapManifest(service, False) 
                        # self.mapRequests()

        pass 

    # TODO topSort()
    def topSort(self) -> None: 
        """ 
        params: 
        - None 

        returns: 
        - None 
        
        desc: 
        - Performs a topological sorting of the 
        """ 
        pass 


