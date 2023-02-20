# INTENTO DE HACER QUE SOLO MUESTRE LAS BOTELLAS 

# IMPORTANTE LEER ESTO:
# Esta ahora puesto en visualize2 (que no muestra las máscaras),
# se puede cambiar facilmente a visualize para que si las muestre

import mrcnn
import mrcnn.config
import mrcnn.model
import mrcnn.visualize2
import cv2
import os
import matplotlib.pyplot as plt
from mrcnn.interfaz import PhotoSelector
import numpy as np


# Create an instance of the PhotoSelector class
photo_selector = PhotoSelector()

# Print the file path of the selected photo
if photo_selector.file_path:
    print(f"Selected photo path: {photo_selector.file_path}")
else:
    print("No photo selected.")



# load the class label names from disk, one label per line
CLASS_NAMES = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

class SimpleConfig(mrcnn.config.Config):
    # Give the configuration a recognizable name
    NAME = "coco_inference"
    
    # set the number of GPUs to use along with the number of images per GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

	# Number of classes = number of classes + 1 (+1 for the background). The background class is named BG
    NUM_CLASSES = len(CLASS_NAMES)

# Initialize the Mask R-CNN model for inference and then load the weights.
# This step builds the Keras model architecture.
model = mrcnn.model.MaskRCNN(mode="inference", config=SimpleConfig(), model_dir=os.getcwd())

# Load the weights into the model.
model.load_weights(filepath=r"Object_Detection\mrcnn\mask_rcnn_coco.h5", by_name=True)


# Load the image
image = cv2.imread(photo_selector.file_path)


# load the input image, convert it from BGR to RGB channel
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Perform a forward pass of the network to obtain the results
r = model.detect([image], verbose=0)

# Get the results for the first image.
r = r[0]

# Initialize to create new arrays with only bottles detected
new_class_ids=[]
new_scores= []
new_rois = []
new_masks = []

# Append all the bottle information
counter = 0
for i in r['class_ids']:
    if i == 40:
        new_class_ids.append(i)
        new_scores.append(r['scores'][counter])
        new_rois.append(r['rois'][counter])
        new_masks.append(r['masks'][:, :,counter])
    
    counter += 1


if len(new_class_ids) > 0:
    # Perform the necessary changes to the new arrays in order to obtain 
    # the needed specifications
    new_class_ids = np.array(new_class_ids)

    new_rois = np.array(new_rois)

    new_masks = np.array(new_masks)
    dim1, dim2, dim3 = new_masks.shape
    new_masks = new_masks.reshape(dim2, dim3, dim1)

    # Visualize the detected objects.
    visual = mrcnn.visualize2.display_instances(image=image, 
                                    boxes=new_rois, 
                                    masks=new_masks, 
                                    class_ids=new_class_ids, 
                                    class_names=CLASS_NAMES, 
                                    scores=new_scores)

else:
    visual = mrcnn.visualize2.no_bottle(image=image)
