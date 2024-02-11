# Edge.py
# 
# Helper class for creating an `Edge` object 
# 
# Randy Truong 
# Northwestern University 
# 11 February 2024 

class Edge: 
    def __init__(self, src: str, dst: str, edgeType: str):  
        self.src = src 
        self.edgeType = edgeType 
        self.dst = dst 
        return None 

