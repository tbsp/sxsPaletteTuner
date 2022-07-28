
import tkinter as tk
from tkinter import filedialog as fd
from PIL import ImageTk, Image

from systems import gbc

def applyFilter(image, colorMapping, scaleList, filterFunc=None):
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b = [scaleList[x] for x in colorMapping[pixels[i, j]]]
            if filterFunc:
                pixels[i, j] = filterFunc((r, g, b))
            else:
                pixels[i, j] = (r, g, b)

    return image


class FilteredImageFrame(tk.Frame):
	def __init__(self, systemImage, scaleVar, filterNames, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)

		self.systemImage = systemImage
		self.scaleVar = scaleVar

		self.imageLabel = tk.Label(self)
		self.imageLabel.pack(side=tk.TOP)

		self.filterValue = tk.StringVar(value=filterNames[0])
		self.filterValue.trace('w', self.updateImage)

		optionMenu = tk.OptionMenu(self, self.filterValue, *filterNames)
		optionMenu.pack(side=tk.TOP)

	def updateImage(self, *args):
		filterName = self.filterValue.get()

		image = self.systemImage.copy()

		# Create dict of color replacements for fast replacement
		colorMapping = {}
		for colorFrame in self.master.master.colorFrames:
			origR, origG, origB = colorFrame.originalRGB

			colorMapping[(origR, origG, origB)] = colorFrame.getRGB()

		# Next apply the filter
		if filterName in gbc.FILTER_ARGS:
			filterArgs = gbc.FILTER_ARGS[filterName]
		
		if filterArgs:
			image = applyFilter(image, colorMapping, *filterArgs)

		# Scale image
		width, height = image.size
		scale = self.scaleVar.get()
		image = image.resize((width*scale, height*scale), Image.NEAREST)

		# Update image on panel
		imageTK = ImageTk.PhotoImage(image)
		self.imageLabel.configure(image=imageTK)
		self.imageLabel.image = imageTK # some trick to avoid GC (https://stackoverflow.com/a/3482156)

			

class PaletteTunerApp(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.rawImage = None
		self.systemImage = None
		self.filteredImageFrames = []

		self.title("Side-by-Side Palette Tuner")

		self.geometry("1100x900")

		topFrame = tk.Frame(self)
		topFrame.pack(side=tk.TOP)

		loadButton = tk.Button(topFrame, text='Load Image', command=self.load_button)
		loadButton.pack(side=tk.LEFT)

		scaleLabel = tk.Label(topFrame, text='Scale:')
		scaleLabel.pack(side=tk.LEFT, padx=5)

		scaleValues = ['1', '2', '3', '4', '5']
		self.scaleVar = tk.IntVar(value=scaleValues[1])

		scaleOption = tk.OptionMenu(topFrame, self.scaleVar, *scaleValues)
		scaleOption.pack(side=tk.LEFT)

		countLabel = tk.Label(topFrame, text='Filter Count:')
		countLabel.pack(side=tk.LEFT, padx=5)

		countValues = ['1', '2', '3', '4', '5', '6']
		self.countVar = tk.IntVar(value=countValues[2])

		countOption = tk.OptionMenu(topFrame, self.countVar, *countValues)
		countOption.pack(side=tk.LEFT)

		self.imageFrame = tk.Frame(self)
		self.imageFrame.pack(side=tk.TOP)

		# Create parent for color frames
		self.colorFrame = tk.Frame(self)
		self.colorFrame.pack(side=tk.TOP)
		self.colorFrames = []

		self.createFitlerFrames()

		self.scaleVar.trace('w', self.updateFilteredImages)
		self.countVar.trace('w', self.createFitlerFrames)

	def load_button(self):
		filename = fd.askopenfilename()
		if filename:
			# Clear out old image/controls
			for widget in self.colorFrames:
				widget.destroy()

			self.rawImage = Image.open(filename)

			# Pre-convert image to system color space for faster updates
			self.systemImage = self.rawImage.copy()
			pixels = self.systemImage.load()
			for i in range(self.systemImage.size[0]):
				for j in range(self.systemImage.size[1]):
					pixels[i,j] = gbc.reduceFunc(pixels[i,j])

			self.updateColorControls()
			self.updateFilteredImages()

	def createFitlerFrames(self, *args):

		oldCount = len(self.filteredImageFrames)
		newCount = self.countVar.get()

		# Remove extra old excess frames
		while len(self.filteredImageFrames) > newCount:
			widget = self.filteredImageFrames[-1]
			self.filteredImageFrames.remove(widget)
			widget.destroy()

		filterNames = list(gbc.FILTER_ARGS.keys())

		while len(self.filteredImageFrames) < newCount:
			frame = FilteredImageFrame(self.systemImage, 
									   self.scaleVar,
									   filterNames,
									   master=self.imageFrame)
			frame.pack(side=tk.LEFT, padx=10)
			self.filteredImageFrames.append(frame)

		if newCount != oldCount:
			self.updateFilteredImages()

	def updateFilteredImages(self, *args):

		if self.systemImage:
			self.images = []
			for i in range(self.countVar.get()):
				frame = self.filteredImageFrames[i]
				frame.systemImage = self.systemImage
				frame.updateImage()

	def updateColorControls(self):
		colors = self.systemImage.getcolors()

		for index, (__, colorRGB) in enumerate(colors):
			colorFrame = gbc.ColorEditingFrame(colorRGB, master=self.colorFrame)
			colorFrame.pack(side=tk.TOP)
			self.colorFrames.append(colorFrame)

		
if __name__ == '__main__':

	app = PaletteTunerApp()
	app.mainloop()
