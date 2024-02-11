# Node.py
#
# Helper class for creating a `Node` object 
#
# Randy Truong 
# Northwestern University 
# 11 February 2024 

class Node: 
    def __init__(self, serviceName: str, nodeType: str): 
        self.serviceName = serviceName 
        self.nodeType = nodeType 
        self.adjList = {} 
        return None 



