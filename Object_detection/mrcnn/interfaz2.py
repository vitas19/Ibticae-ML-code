# Enables the usage of a interface that presents a photograph with two 
# buttons that with one you select the image and with the other it 
# computes the output.


import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import patches
from matplotlib.figure import Figure
import numpy as np


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

        # Include picture in the left top corner
        image1 = Image.open("Object_Detection\mrcnn\logo.jpg").resize((80, 80), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image1)
        label1 = tk.Label(image=test).place(x=0, y=0)

        # Include picture as a background
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

            # Create the tick when an image has been selected
            lbl = tk.Label(self.root, text=" ✓ ", font=("Dubai", 15),bg="#0F2D92", fg="#FFFFFF")
            lbl.place(x=20, y=550)

            # Create a PhotoImage object from the selected photo
            photo = Image.open(self.file_path).resize((500, 350), Image.ANTIALIAS)
            photo_image = ImageTk.PhotoImage(photo)

            # Create a Label widget to display the photo
            image_label = tk.Label(self.root, image=photo_image)
            image_label.place(x=400, y=125)

            # Position image in front of other objects
            photo_image.lift()


    def process_file(self):
        # Call the callback function with the selected file path
        if self.file_path:
            visual = self.callback(self.file_path)
            N = visual[0]
            y1 = visual[1]
            x1 = visual[2]
            y2 = visual[3]
            x2 = visual[4]
            caption = visual[5]
            masked_image = visual[6]

        # Create a Figure object and add the image to it using Matplotlib
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        # Turn off the axis
        ax.set_axis_off()
        # Remove padding
        fig.tight_layout(pad=0)

        # Add the rectangles and text to the infered photos
        for i in range(N):
            color = "red"
            p = patches.Rectangle((x1[i], y1[i]), x2[i] - x1[i], y2[i] - y1[i], linewidth=4,
                                alpha=0.7, #linestyle="dashed",
                                edgecolor=color, facecolor='none')
            ax.add_patch(p)
            ax.text(x1[i], y1[i] + 8, caption[i],
                        color='w', size=11, backgroundcolor="black")

            ax.imshow(masked_image.astype(np.uint8))
        
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()

        # Get a Tkinter.Canvas object from the FigureCanvasTkAgg object and pack it to display it in the Tkinter window
        canvas.get_tk_widget().place(x=400, y=90)
