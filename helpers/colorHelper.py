
class colorHelper:
    def __init__(self, c, a = 1):
        if isinstance(c, tuple):
            self.r, self.g, self.b = c
        elif isinstance(c, str):
            (self.r, self.g, self.b) = self.getColors(c)
        self.a = a
        
    
    def getTuple(self):
        return (self.r, self.g, self.b)
        
        
    def getTransparence(self):
        return self.a 
        
        
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
            "snow": (255, 250, 250)
        }
        return colors[color]
        

"""rosybrown":,
"lightcoral":,
"indianred":,
"brown":,
"firebrick":,
"maroon":,
"darkred":,
"mistyrose":,
"salmon":,
"tomato":,
"darksalmon":,
"coral":,
"orangered":,
"lightsalmon":,
"sienna":,
"seashell":,
"chocolate":,
"saddlebrown":,
"sandybrown":,
"peachpuff":,
"peru":,
"linen":,
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
