# Enables the usage of a interface that presents a photograph with two 
# buttons that with one you select the image and with the other it 
# computes the output.

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image  

class PhotoSelector:
    def __init__(self):
        self.root = tk.Tk()

        # Title of the window
        self.root.title("Photo Selector")
        # Size of the window
        self.root.geometry('800x250')
        self.file_path = None

        # Include picture
        image1 = Image.open("Object_Detection\mrcnn\logo.jpg").resize((250, 250), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image1)
        label1 = tk.Label(image=test).place(x=0, y=0)

        # Include background color
        self.root['background'] = '#6CD9FF'

        # Include text
        lbl = tk.Label(self.root, text="Selecciona el archivo deseado:", font=("Dubai", 30),bg="#6CD9FF", fg="#0F2D92")
        lbl.place(x=270, y=0)
        
        # Create a button to select a photo
        self.select_button = tk.Button(self.root, text="1. Seleccionar imagen",font=("Dubai", 20),bg="#0F2D92", fg="#FFFFFF", command=self.select_photo)
        self.select_button.place(x=280, y=70)
        
        # Create a button to close the interface (show result)
        self.close_button = tk.Button(self.root, text="2. Mostrar resultado",font=("Dubai", 20),bg="#0F2D92", fg="#FFFFFF", command=self.root.destroy)
        self.close_button.place(x=460, y=160)
        
        self.root.mainloop()
    
    def select_photo(self):
        # Open a file dialog to select a photo
        file_path = filedialog.askopenfilename(initialdir="/", title="Select Photo", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        
        if file_path:
            self.file_path = file_path
            print(f"Selected photo: {self.file_path}")

