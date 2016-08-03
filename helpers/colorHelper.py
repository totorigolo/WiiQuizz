# coding: utf8

class colorHelper:
    def __init__(self, c, a = 1):
        if isinstance(c, tuple):
            self.r, self.g, self.b = c
        elif isinstance(c, str):
            (self.r, self.g, self.b) = self.getColors(c)
        self.a = a
        
    
    def getTuple(self):
        return (self.r, self.g, self.b)
        
        
    def getTransparency(self):
        return self.a 
        
    
    def setTransparency(self, val):
        self.a = val
        
        
    def lighten(self, val):
        self.r += val
        self.g += val
        self.b += val
        if self.r > 255:
            self.r = 255
        if self.g > 255:
            self.g = 255
        if self.b > 255:
            self.b = 255
        if self.r < 0:
            self.r = 0
        if self.g < 0:
            self.g = 0
        if self.b < 0:
            self.b = 0
        
        
    def darken(self, val):
        self.lighten(-val)
        
        
    def isTransparent(self):
        if 0 <= self.a < 1:
            return True
        return False
        
        
    def getColors(self, color):
        colors = {
            "red":(255, 0, 0), 
            "green":(0, 255, 0), 
            "blue":(0,0, 255), 
            "black":(0, 0, 0), 
            "white":(255, 255, 255), 
            "yellow":(255, 255, 0), 
            "cyan":(0, 255, 255), 
            "magenta": (255, 0, 255),
            "darkgrey": (105, 105, 105),
            "grey": (128, 128, 128),
            "dimgrey": (169, 169, 169),
            "silver": (192, 192, 192),
            "lightgrey": (211, 211, 211),
            "gainsboro": (220, 220, 220),
            "whitesmoke": (245, 245, 245),
            "snow": (255, 250, 250),
            "rosybrown":(188, 143, 143),
            "lightcoral":(240, 128, 128),
            "indianred":(205, 92, 92),
            "brown":(165, 42, 42),
            "firebrick":(178, 34, 34),
            "maroon":(128, 0, 0),
            "darkred":(139, 0, 0),
            "mistyrose":(255, 228, 225),
            "salmon":(250, 128, 114),
            "tomato":(255, 999, 71),
            "darksalmon":(233, 150, 122),
            "coral":(255, 127, 80),
            "orangered":(255, 69, 0),
            "lightsalmon":(255, 160, 122),
            "sienna":(160, 82, 45),
            "seashell":(255, 245, 238),
            "chocolate":(210, 105, 30),
            "saddlebrown":(139, 69, 19),
            "sandybrown":(250, 164, 96),
            "peachpuff":(255, 218, 185),
            "peru":(205, 133, 63),
            "lightskyblue": (135, 206, 250),
            "skyblue": (135, 206, 235),
            "darkblue": (0, 0, 139)
        }
        return colors[color]
        

"""linen":,
"bisque":,
"darkorange":,
"burlywood":,
"antiquewhite":,
"tan":,
"navajowhite":,
"blanchedalmond":,
"papayawhip":,
"moccasin":,
"orange":,
"wheat":,
"oldlace":,
"floralwhite":,
"darkgoldenrod":,
"goldenrod":,
"cornsilk":,
"gold":,
"lemonchiffon":,
"khaki":,
"palegoldenrod":,
"darkkhaki":,
"ivory":,
"beige":,
"lightyellow":,
"lightgoldenrodyellow":,
"olive":,
"olivedrab":,
"yellowgreen":,
"darkolivegreen":,
"greenyellow":,
"chartreuse":,
"lawngreen":,
"sage":"""
