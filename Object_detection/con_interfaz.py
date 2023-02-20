# INTENTO DE IMPLEMETAR UNA INTERFAZ

# Esta con visualize (mostrando las mascaras)

import mrcnn
import mrcnn.config
import mrcnn.model
import mrcnn.visualize
import cv2
import os
import matplotlib.pyplot as plt
from mrcnn.interfaz import PhotoSelector


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
# Download the mask_rcnn_coco.h5 file from this link: https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5
model.load_weights(filepath=r"Object_Detection\mrcnn\mask_rcnn_coco.h5", by_name=True)

# Load the image
image = cv2.imread(photo_selector.file_path)

# load the input image, convert it from BGR to RGB channel
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Perform a forward pass of the network to obtain the results
r = model.detect([image], verbose=0)

# Get the results for the first image.
r = r[0]


if 40 in r['class_ids']:
    # Visualize the detected objects.
    visual = mrcnn.visualize.display_instances(image=image, 
                                    boxes=r['rois'], 
                                    masks=r['masks'], 
                                    class_ids=r['class_ids'], 
                                    class_names=CLASS_NAMES, 
                                    scores=r['scores'])

else:
    visual = mrcnn.visualize.no_bottle(image=image)

