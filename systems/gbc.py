
import tkinter as tk
from tkinter.colorchooser import askcolor

def rgb2hex(rgb):
    return "#%02x%02x%02x" % rgb  

def rgb2hexGB(rgb):
    """Convert 15bit RGB to GB 15bit hex value"""
    return '%04x' % ((int(rgb[0])) +
                     (int(rgb[1]) << 5) +
                     (int(rgb[2]) << 10))

def gb2rgb(rgb):
    """Convert 15bit RGB to 24bit RGB"""
    return (rgb[0]*8, rgb[1]*8, rgb[2]*8)

def reduceFunc(rgb):
    return (int(rgb[0]/8), int(rgb[1]/8), int(rgb[2]/8))

def scaleChannel(x):
    return (x << 3) | (x >> 2)

CGB_CURVE = [0,6,12,20,28,36,45,56,66,76,88,100,113,125,137,149,161,172,182,192,202,210,218,225,232,238,243,247,250,252,254,255]
def scaleChannelWithCurveCGB(x):
    return CGB_CURVE[x]

AGB_CURVE = [0,3,8,14,20,26,33,40,47,54,62,70,78,86,94,103,112,120,129,138,147,157,166,176,185,195,205,215,225,235,245,255]
def scaleChannelWithCurveAGB(x):
    return AGB_CURVE[x]

SGB_CURVE = [0,2,5,9,15,20,27,34,42,50,58,67,76,85,94,104,114,123,133,143,153,163,173,182,192,202,211,220,229,238,247,255]
def scaleChannelWithCurveSGB(x):
    return SGB_CURVE[x]

def emulateHardwareCGB(rgb):

    gamma = 2.2

    r, g, b = rgb

    newG = pow((pow(g / 255.0, gamma) * 3 + pow(b / 255.0, gamma)) / 4, 1 / gamma) * 255
    newR = r
    newB = b

    return (int(newR), int(newG), int(newB))

def emulateHardwareAGB(rgb):

    gamma = 2.2

    r, g, b = rgb

    newG = pow((pow(g / 255.0, gamma) * 5 + pow(b / 255.0, gamma)) / 6, 1 / gamma) * 255
    newR = r
    newB = b

    return (int(newR), int(newG), int(newB))

def preserveBrightnessCGB(rgb):

    gamma = 1.6 # emulate hardware and preserve brightness

    r, g, b = rgb

    newG = pow((pow(g / 255.0, gamma) * 3 + pow(b / 255.0, gamma)) / 4, 1 / gamma) * 255
    newR = r
    newB = b

    oldMax = max(r, max(g, b))
    newMax = max(newR, max(newG, newB))

    if newMax != 0:
        ratio = oldMax / newMax
        newR = newR * ratio
        newG = newG * ratio
        newB = newB * ratio

    oldMin = min(r, min(g, b))
    newMin = min(newR, min(newG, newB))

    if newMin != 255:
        ratio = (255 - oldMin) / (255 - newMin)
        newR = 255 - (255 - newR) * ratio
        newG = 255 - (255 - newG) * ratio
        newB = 255 - (255 - newB) * ratio
    
    return (int(newR), int(newG), int(newB))

def preserveBrightnessAGB(rgb):

    gamma = 1.6 # emulate hardware and preserve brightness

    r, g, b = rgb

    newG = pow((pow(g / 255.0, gamma) * 5 + pow(b / 255.0, gamma)) / 6, 1 / gamma) * 255
    newR = r
    newB = b

    oldMax = max(r, max(g, b))
    newMax = max(newR, max(newG, newB))

    if newMax != 0:
        ratio = oldMax / newMax
        newR = newR * ratio
        newG = newG * ratio
        newB = newB * ratio

    oldMin = min(r, min(g, b))
    newMin = min(newR, min(newG, newB))

    if newMin != 255:
        ratio = (255 - oldMin) / (255 - newMin)
        newR = 255 - (255 - newR) * ratio
        newG = 255 - (255 - newG) * ratio
        newB = 255 - (255 - newB) * ratio
    
    return (int(newR), int(newG), int(newB))


def reduceContrastCGB(rgb):

    gamma = 2.2

    r, g, b = rgb

    newG = pow((pow(g / 255.0, gamma) * 3 + pow(b / 255.0, gamma)) / 4, 1 / gamma) * 255
    newR = r
    newB = b

    newR = newR * 7/8 + (g+b)/16
    newG = newG * 7/8 + (r+b)/16
    newB = newB * 7/8 + (r+g)/16

    newR = newR * (220 - 40) / 255 + 40
    newG = newG * (224 - 36) / 255 + 36
    newB = newB * (216 - 32) / 255 + 32

    return (int(newR), int(newG), int(newB))

def reduceContrastAGB(rgb):

    gamma = 2.2

    r, g, b = rgb

    newG = pow((pow(g / 255.0, gamma) * 5 + pow(b / 255.0, gamma)) / 6, 1 / gamma) * 255
    newR = r
    newB = b

    newR = newR * 7/8 + (g+b)/16
    newG = newG * 7/8 + (r+b)/16
    newB = newB * 7/8 + (r+g)/16

    newR = newR * (224 - 40) / 255 + 20
    newG = newG * (220 - 36) / 255 + 18
    newB = newB * (216 - 32) / 255 + 16

    return (int(newR), int(newG), int(newB))


def lowContrastCGB(rgb):

    gamma = 2.2

    r, g, b = rgb

    newG = pow((pow(g / 255.0, gamma) * 3 + pow(b / 255.0, gamma)) / 4, 1 / gamma) * 255
    newR = r
    newB = b

    r = newR
    g = newR
    b = newR

    newR = newR * 7/8 + (g+b)/16
    newG = newG * 7/8 + (r+b)/16
    newB = newB * 7/8 + (r+g)/16

    newR = newR * (162 - 45) / 255 + 45
    newG = newG * (167 - 41) / 255 + 41
    newB = newB * (157 - 38) / 255 + 38

    return (int(newR), int(newG), int(newB))

def lowContrastAGB(rgb):

    gamma = 2.2

    r, g, b = rgb

    newG = pow((pow(g / 255.0, gamma) * 5 + pow(b / 255.0, gamma)) / 6, 1 / gamma) * 255
    newR = r
    newB = b

    r = newR
    g = newR
    b = newR

    newR = newR * 7/8 + (g+b)/16
    newG = newG * 7/8 + (r+b)/16
    newB = newB * 7/8 + (r+g)/16

    newR = newR * (167 - 27) / 255 + 27
    newG = newG * (165 - 24) / 255 + 24
    newB = newB * (157 - 22) / 255 + 22

    return (int(newR), int(newG), int(newB))

def harshRealityFilter(image, colorMapping):
	"""Return the passed image to look like 'reality'"""
	pixels = image.load()
	for i in range(image.size[0]):
		for j in range(image.size[1]):
			r, g, b = colorMapping[pixels[i, j]]

			# Taken directly from SameBoy
			r = r * 7/8 + (g+b)/16
			g = g * 7/8 + (r+b)/16
			b = b * 7/8 + (r+g)/16

			if False: # AGB
				pass
			else:
				r = r*(162-45)/255+45
				g = g*(167-41)/255+41
				b = b*(157-38)/255+38
			
			pixels[i, j] = (int(r),
			 				int(g),
			  				int(b))

	return image


FILTER_ARGS = {'Disabled': (scaleChannelWithCurveCGB, None),

               'Correct Curves (CGB)': (scaleChannelWithCurveCGB, None),
               'Emulate Hardware (CGB)': (scaleChannelWithCurveCGB, emulateHardwareCGB),
               'Preserve Brightness (CGB)': (scaleChannelWithCurveCGB, preserveBrightnessCGB),
               'Reduce Contrast (CGB)': (scaleChannelWithCurveCGB, reduceContrastCGB),
               'Harsh Reality (CGB)': (scaleChannelWithCurveCGB, lowContrastCGB),          

               'Correct Curves (AGB)': (scaleChannelWithCurveAGB, None),
               'Emulate Hardware (AGB)': (scaleChannelWithCurveAGB, emulateHardwareAGB),
               'Preserve Brightness (AGB)': (scaleChannelWithCurveAGB, preserveBrightnessAGB),
               'Reduce Contrast (AGB)': (scaleChannelWithCurveAGB, reduceContrastAGB),
               'Harsh Reality (AGB)': (scaleChannelWithCurveAGB, lowContrastAGB),
               }


class ColorEditingFrame(tk.Frame):
    def __init__(self, colorRGB, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.originalRGB = colorRGB

        self.rVar = tk.IntVar(self, colorRGB[0])
        self.gVar = tk.IntVar(self, colorRGB[1])
        self.bVar = tk.IntVar(self, colorRGB[2])

        self.hexVar = tk.StringVar(self, rgb2hexGB(colorRGB))

        self.setButton = tk.Button(self, bg=rgb2hex(gb2rgb(colorRGB)), text='     ', command=self.buttonSetColor)
        self.setButton.pack(side=tk.LEFT)

        vcmd = self.register(self.intValidate)

        rLabel = tk.Label(self, text='R:')
        rLabel.pack(side=tk.LEFT)
        rEntry = tk.Entry(self, textvariable=self.rVar, width=5, validate='all', validatecommand=(vcmd, '%P'))
        rEntry.pack(side=tk.LEFT)
        rScale = tk.Scale(self, variable=self.rVar, from_=0, to_=31,
                          orient=tk.HORIZONTAL, showvalue=False)
        rScale.pack(side=tk.LEFT)

        gLabel = tk.Label(self, text='G:')
        gLabel.pack(side=tk.LEFT)
        gEntry = tk.Entry(self, textvariable=self.gVar, width=5, validate='all', validatecommand=(vcmd, '%P'))
        gEntry.pack(side=tk.LEFT)
        gScale = tk.Scale(self, variable=self.gVar, from_=0, to_=31,
                          orient=tk.HORIZONTAL, showvalue=False)
        gScale.pack(side=tk.LEFT)

        bLabel = tk.Label(self, text='B:')
        bLabel.pack(side=tk.LEFT)
        bEntry = tk.Entry(self, textvariable=self.bVar, width=5, validate='all', validatecommand=(vcmd, '%P'))
        bEntry.pack(side=tk.LEFT)
        bScale = tk.Scale(self, variable=self.bVar, from_=0, to_=31,
                          orient=tk.HORIZONTAL, showvalue=False)
        bScale.pack(side=tk.LEFT)

        hexLabel = tk.Label(self, text='Hex')
        hexLabel.pack(side=tk.LEFT)
        hexEntry = tk.Entry(self, textvariable=self.hexVar, width=10)
        hexEntry.pack(side=tk.LEFT)

        copyButton = tk.Button(self, text='Copy', command=self.copyHex)
        copyButton.pack(side=tk.LEFT)

        self.rVar.trace('w', self.master.master.updateFilteredImages)
        self.gVar.trace('w', self.master.master.updateFilteredImages)
        self.bVar.trace('w', self.master.master.updateFilteredImages)

        self.rVar.trace('w', self.updateHexValue)
        self.gVar.trace('w', self.updateHexValue)
        self.bVar.trace('w', self.updateHexValue)

    def intValidate(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def buttonSetColor(self, *args):
        result = askcolor()

        if result:
            colorRGB, colorHex = result
            self.rVar.set(int(colorRGB[0]/8))
            self.gVar.set(int(colorRGB[1]/8))
            self.bVar.set(int(colorRGB[2]/8))

            self.setButton.configure(bg=colorHex)

    def getRGB(self):
        """Get a safe RGB tuple"""
        try:
            r = sorted([0, self.rVar.get(), 31])[1]
        except tk.TclError:
            r = 0
        try:
            g = sorted([0, self.gVar.get(), 31])[1]
        except tk.TclError:
            g = 0
        try:
            b = sorted([0, self.bVar.get(), 31])[1]
        except tk.TclError:
            b = 0

        return (r, g, b)

    def updateHexValue(self, *args):
        self.hexVar.set(rgb2hexGB(self.getRGB()))

    def copyHex(self, *args):
        hex = self.hexVar.get()

        self.clipboard_clear()
        self.clipboard_append(hex)
