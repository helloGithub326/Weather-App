from tkinter import Canvas
from PIL import ImageTk

class staticImage(Canvas):
    def __init__(self, parent, image, col, row, color, padx, pady):
        super().__init__(master=parent, background=color, bd=0, highlightthickness=0, relief='ridge', width=100, height=100)
        self.grid(column=col, row=row, sticky='nsew', padx=padx, pady=pady)
        
        self.image = image
        self.imageTk = ImageTk.PhotoImage(self.image)
        self.imageRatio = self.image.size[0] / self.image.size[1]
        
        self.canvasWidth = 0
        self.canvasHeight = 0
        self.imageWidth = 0
        self.imageHeight = 0
        
        self.bind('<Configure>', self.resize)
        
    def resize(self, event=None):
        canvasRatio = event.width / event.height
        self.canvasWidth = event.width
        self.canvasHeight = event.height
        
        if canvasRatio > self.imageRatio:
            self.imageHeight = int(self.canvasHeight)
            self.imageWidth = int(self.imageHeight * self.imageRatio)
        else:
            self.imageWidth = int(self.canvasWidth)
            self.imageHeight = int(self.imageWidth / self.imageRatio)
            
        self.updateImage()
        
    def updateImage(self, newImage=None):
        self.delete('all')
        if newImage:
            image = newImage
            self.image = image
        else:
            image = self.image
        if (self.imageWidth, self.imageHeight) != (0,0):
            resizedImage = image.resize((self.imageWidth, self.imageHeight))
            self.imageTk = ImageTk.PhotoImage(resizedImage)
            self.create_image((self.canvasWidth/2), (self.canvasHeight/2), image=self.imageTk)
        
class animatedImage(Canvas):
    def __init__(self, parent, images, col, row, color):
        super().__init__(master=parent, background=color, bd=0, highlightthickness=0, relief='ridge')
        self.grid(column=col, row=row, sticky='nsew')
        
        self.images = images
        self.frameIndex = 0
        self.imageTk = ImageTk.PhotoImage(self.images[self.frameIndex])
        self.imageRatio = self.images[self.frameIndex].size[0] / self.images[self.frameIndex].size[1]
        
        self.canvasWidth = 0
        self.canvasHeight = 0
        self.imageWidth = 0
        self.imageHeight = 0
        
        self.bind('<Configure>', self.resize)
        self.after(42, self.animate)
        
    def animate(self):
        self.frameIndex += 1
        if self.frameIndex >= len(self.images):
            self.frameIndex = 0
        self.updateImage()
        self.after(42, self.animate)
        
    def resize(self, event=None):
        canvasRatio = event.width / event.height
        self.canvasWidth = event.width
        self.canvasHeight = event.height
        
        if canvasRatio > self.imageRatio:
            self.imageHeight = int(self.canvasHeight)
            self.imageWidth = int(self.imageHeight * self.imageRatio)
        else:
            self.imageWidth = int(self.canvasWidth)
            self.imageHeight = int(self.imageWidth / self.imageRatio)
            
        self.updateImage()
        
    def updateImage(self):
        self.delete('all')
        if (self.imageWidth, self.imageHeight) != (0,0):
            resizedImage = self.images[self.frameIndex].resize((self.imageWidth, self.imageHeight))
            self.imageTk = ImageTk.PhotoImage(resizedImage)
            self.create_image((self.canvasWidth/2), (self.canvasHeight/2), image=self.imageTk)