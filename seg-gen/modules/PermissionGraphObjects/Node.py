# Node.py
#
# Helper class for creating a `Node` object 
#
# Randy Truong 
# Northwestern University 
# 11 February 2024 

# Add Enum support 
from enum import Enum 

class NodeType(Enum): 
    SERVICE_NODE   = 1 
    VERSION_NODE   = 2

class Node: 
    # Node.__init__()
    def __init__(self, serviceName: str, nodeType: int, version: str) -> None: 
        """
        desc: 
        - Initializes a `Node` object for the `PermissionGraph` object 
        """
        try: 
            NodeType(nodeType)
        except: 
            raise ValueError(f"[ERROR] Invalid nodeType {nodeType}")

        self.serviceName = serviceName 
        self.type = nodeType 
        self.version = version
        self.bAdjList: defaultdict = {} 
        self.rAdjList: defaultdict = {} 
        pass 

    # Node.addBelongingEdge()
    def addBelongingEdge(self, node: Node) -> None: 
        """
        desc: 
        - Adds a belonging edge to the current node 
        """

        # If `node.nodeType` is not VERSION_NODE -> Error 
        if (node.type != 2):
            raise Error(f"[DEBUG] Attempted to add a non-version node to {self.serviceName}") 
        
        self.bAdjList[node.version] = node
        pass 

    # Node.addRequestEdge()
    def addRequestEdge(self, node: Node) -> None: 
        """
        desc: 
        - Adds a request edge to the current node 
        """

        if (node.type != 1): 
            raise Exception(f"[DEBUG] Attempted to add a request edge\ 
                        to non-service node {node.serviceName}")

        self.rAdjList[node] = node 
        pass





