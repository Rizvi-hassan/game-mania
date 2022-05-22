from tkinter import *
from PIL import ImageTk, Image

root = Tk()

button = Button(root, text="Click me!")
image = Image.open("bg1.jpg")
image = image.resize((100, 70), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image) # make sure to add "/" not "\"
button.config(image=img, text = "CLICK ME", font = "consolas 14 bold")
button.pack() # Displaying the button

root.mainloop()