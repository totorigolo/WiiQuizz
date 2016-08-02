
class colorHelper:
    def __init__(self, c, a = 1):
        color = {"red":(255, 0, 0), "green":(0, 255, 0), "blue":(0,0, 255), "black":(0, 0, 0), "white":(255, 255, 255), "yellow":(255, 255, 0), "cyan":(0, 255, 255), "magenta": (255, 0, 255)}
        if isinstance(c, tuple):
            self.r, self.g, self.b = c
        elif isinstance(c, str):
            (self.r, self.g, self.b) = color[c]
        self.a = a
        
    
    def getTuple(self):
        return (self.r, self.g, self.b)
        
        
    def getTransparence(self):
        return self.a 
        
        
    def isTransparent(self):
        if 0 <= self.a < 1:
            return True
        return False
        
        

        