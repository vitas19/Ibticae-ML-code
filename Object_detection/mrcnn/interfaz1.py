# Enables the usage of a interface that presents a photograph with two 
# buttons that with one you select the image and with the other it 
# computes the output.

import tkinter as tk
from tkinter import filedialog, Canvas
from PIL import ImageTk, Image  
import matplotlib.pyplot as plt

class PhotoSelector:
    def __init__(self, callback):
        self.root = tk.Tk()

        # Title of the window
        self.root.title("Photo Selector")
        # Size of the window
        self.root.geometry('1000x600')
        self.file_path = None
        self.callback = callback
  
        # Include background color
        white_frame = tk.Frame(bd=0, highlightthickness=0, background="white")
        blue_frame = tk.Frame(bd=0, highlightthickness=0, background='#6CD9FF')
        white_frame.place(x=300, y=0, width=1200, height=800, anchor="nw")
        blue_frame.place(x=0, y=0, width=300, height=800, anchor="nw")


        # Include picture
        image1 = Image.open("Object_Detection\mrcnn\logo.jpg").resize((80, 80), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image1)
        label1 = tk.Label(image=test).place(x=0, y=0)

        # Include picture
        photo_image = Image.open("Object_Detection\mrcnn\logo1.png").resize((700, 600), Image.ANTIALIAS)
        test2 = ImageTk.PhotoImage(photo_image)
        label2 = tk.Label(image=test2).place(x=300, y=0)

        # Include text
        lbl = tk.Label(self.root, text="AI Object Detection", font=("Dubai", 15),bg="#6CD9FF", fg="#0F2D92")
        lbl.place(x=100, y=30)
        
        # Create a button to select a photo
        self.select_button = tk.Button(self.root, text=" Importar archivo ",font=("Dubai", 20),bg="#0F2D92", fg="#FFFFFF", command=self.select_photo)
        self.select_button.place(x=40, y=100)
        
        # Create a button to inference
        self.process_button = tk.Button(self.root, text="   Inferir   ",font=("Dubai", 20),bg="#0F2D92", fg="#FFFFFF", command=self.process_file, state=tk.DISABLED)
        self.process_button.place(x=90, y=200)

        # Create a button to close the interface
        self.close_button = tk.Button(self.root, text=" Cerrar ", font=("Dubai", 15),bg="#0F2D92", fg="#FFFFFF", command=self.root.destroy)
        self.close_button.place(x=200, y=530)

        self.root.mainloop()
    
    def select_photo(self):
        # Open a file dialog to select a photo
        file_path = filedialog.askopenfilename(initialdir="/", title="Select Photo", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        
        if file_path:
            self.file_path = file_path
            self.process_button.config(state=tk.NORMAL)
            print(f"Selected photo: {self.file_path}")

            lbl = tk.Label(self.root, text=" ✓ ", font=("Dubai", 15),bg="#0F2D92", fg="#FFFFFF")
            lbl.place(x=20, y=550)

            # Create a PhotoImage object from the selected photo
            photo = Image.open(self.file_path).resize((500, 350), Image.ANTIALIAS)
            photo_image = ImageTk.PhotoImage(photo)

            # Create a Label widget to display the photo
            image_label = tk.Label(self.root, image=photo_image)
            image_label.place(x=400, y=125)

            # position image in front of other objects
            photo_image.lift()


    def process_file(self):
        # Call the callback function with the selected file path
        if self.file_path:
            visual = self.callback(self.file_path)


        # Display the visual image
        if visual is not None:
            from PIL import Image, ImageTk
            plt.show()
            visual = Image.open(visual).resize((400, 300), Image.ANTIALIAS)
            visual_image = ImageTk.PhotoImage(visual)
  
            # Create a Label widget to display the photo
            visual_label = tk.Label(self.root, image=visual_image)
            visual_label.place(x=0, y=150)

            visual_image.lift()

