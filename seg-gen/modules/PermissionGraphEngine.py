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
                       }
     ] 
     
""" 

import os 
import sys 
import json 
from PermissionGraphObjects.Node import Node 
from PermissionGraphObjects.Edge import Edge 
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
                    List of 

        - `defaultdict self.rawGraph`: 
                    List of all nodes N_{s} and N_{v} within G 

        - `defaultdict self.serviceGraph`: 
                    Hierarchal mapping of N_{s} and N_{v} within G 
        """
        manifests.sort(key = lambda a: a["service"]) 

        self.manifests: List[defaultdict] = manifests 
        self.rawGraph: defaultdict = {} 
        self.serviceGraph: defaultdict = {} 
        self.sortedGraph = []
        return None 

    # mapServiceNode() 
    def mapServiceNode(self, manifest: defaultdict) -> None: 
        """
        params: 
        - None 

        desc:
        Creates a service node as well as creates a corresponding 
        """
        serviceName, versionName, requests = (manifest["service"], 
                                              manifest["version"], 
                                              manifest["requests"])
        # Init Service Node Object 
        currentNode = Node(serviceName, 1) # 1 == SERVICE_NODE
        self.serviceGraph[serviceName] = currentNode
        pass

    # mapVersionNode()
    def mapVersionNode(self, manifest: defaultdict) -> None: 
        """

        desc: 
        Creates a version node for a given service node 
        """
        serviceName, versionName, requests = (manifest["service"], 
                                              manifest["version"], 
                                              manifest["requests"])
        
        # Find corresponding service node 
        try: 
            serviceNode = self.serviceGraph[serviceName] 
        except: 
            raise Exception(f"[DEBUG] Tried to add a version node\
                    without a service node {serviceName}")


        # Init Version Node Object 
        currentNode = Node(serviceName, 2) # 2 == VERSION_NODE
        self.serviceGraph[serviceName].addBelongingEdge()
        pass

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

        # Remark: The permission graph is generated utilizing 
        # the following attributes: 
        # 
        # G = (N_{s}, N_{v}, E_{b}, E_{r}) where 
        # 
        #   N_{s} (Service Node):    
        #     Generic service for microservice architecture  
        #   N_{v} (Version Node):    
        #     Variation of N_{s} that can be invoked with varying permissions 
        #   E_{b} (Belonging Edge):  
        #     An edge that connects N_{v} with its corresponding N_{s}
        #   E_{r} (Request Edge):    
        #     An edge that connects N_{s1} with another N_{s2} 
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

    def dfs(self, curr: defaultdict, visited: set, 
            path: set, finalSort: set) -> bool: 
        # Base Case 0: If visited -> return None 
        if (curr in visited): 
            return True 

        # Base Case 1: If in same path -> return False 
        if (curr in path): 
            return False 

        # Recurse through the rest of the graph 
        for nei in adjList[curr]: 
            dfs(curr=, visited=, path= )

        
        return True 

        

    # TODO topSort()
    def topSort(self) -> None: 
        """ 
        params: 
        - None 

        returns: 
        - None 
        
        desc: 
        - Performs a topological sorting of the service names and 
        their version
        """ 
        
        finalSort: List[tuple] = [] 
        path: set = set(), visited: set = set()

        for node in graph: 
            if (not dfs(node, visited, path, finalSort)): 
                return False 

        return True 

    # renderGraph()
    def renderGraph(self) -> None: 
        pass 


