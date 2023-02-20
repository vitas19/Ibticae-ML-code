# PROGRAMA COGE VIDEO DESDE LA CÁMARA DEL ORDENADOR Y ANALIZA FOTOGRAMA POR FOTOGRAMA
# DEVUELVE FOTOS (NO VIDEO COMPILADO)


import mrcnn
import mrcnn.config
import mrcnn.model
import mrcnn.visualize
import mrcnn.interfaz
import cv2
import os
import matplotlib.pyplot as plt



# load the class label names from disk, one label per line
# CLASS_NAMES = open("coco_labels.txt").read().strip().split("\n")


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

img_array = []
i=-0.5 

#cap = cv2.VideoCapture(r"Object_Detection\mrcnn\video1_recor1.mp4")
cap = cv2.VideoCapture(0)
success, image = cap.read()
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(length)

print("SIGUE ACTIALIZANDO")


while success:
    # Get the full path to the file
    #file_path = os.path.join(directory, filename)

    # Load the image

    #image = cv2.imread(image)


    # load the input image, convert it from BGR to RGB channel
    #image = cv2.imread("dron1.png")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width,layers = image.shape
    size = (width, height)
    out = cv2.VideoWriter('prueba.avi', cv2.VideoWriter_fourcc(*'DIVX'),15,size)
    # Perform a forward pass of the network to obtain the results
    r = model.detect([image], verbose=0)

    # Get the results for the first image.
    r = r[0]

    print(r['class_ids'])

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


    print(len(img_array))
    #print(length)
    i+=0.5
    print(i)




#print(len(img_array))
#print(length)

    