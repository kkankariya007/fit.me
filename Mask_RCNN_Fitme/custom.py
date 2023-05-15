import os
import sys
import json
import datetime
import numpy as np
import skimage.draw
import cv2
from mrcnn.visualize import display_instances
import matplotlib.pyplot as plt

# Root directory of the project
ROOT_DIR = "F:\Mask_RCNN_Fitme"

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import model as modellib, utils

# Path to trained weights file
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# Directory to save logs and model checkpoints, if not provided
# through the command line argument --logs
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")



class CustomConfig(Config):
    """Configuration for training on the custom  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "object"

    # We use a GPU with 24GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 4

    # Number of classes (including background)
    NUM_CLASSES = 1 + 60  # Background + phone,laptop and mobile

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 10

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9

############################################################
#  Dataset
############################################################

class CustomDataset(utils.Dataset):

    def load_custom(self, dataset_dir, subset):
        # Add classes. We have only one class to add.
        self.add_class("object", 1, "0,null")
        self.add_class("object", 2, "1,accessories")
        self.add_class("object", 3, "2,bag")
        self.add_class("object", 4, "3,belt")
        self.add_class("object", 5, "4,blazer")
        self.add_class("object", 6, "5,blouse")
        self.add_class("object", 7, "6,bodysuit")
        self.add_class("object", 8, "7,boots")
        self.add_class("object", 9, "8,bra")
        self.add_class("object", 10, "9,bracelet")
        self.add_class("object", 11, "10,cape")
        self.add_class("object", 12, "11,cardigan")
        self.add_class("object", 13, "12,clogs")
        self.add_class("object", 14, "13,coat")
        self.add_class("object", 15, "14,dress")
        self.add_class("object", 16, "15,earrings")
        self.add_class("object", 17, "16,flats")
        self.add_class("object", 18, "17,glasses")
        self.add_class("object", 19, "18,gloves")
        self.add_class("object", 20, "19,hair")
        self.add_class("object", 21, "20,hat")
        self.add_class("object", 22, "21,heels")
        self.add_class("object", 23, "22,hoodie")
        self.add_class("object", 24, "23,intimate")
        self.add_class("object", 25, "24,jacket")
        self.add_class("object", 26, "25,jeans")
        self.add_class("object", 27, "26,jumper")
        self.add_class("object", 28, "27,leggings")
        self.add_class("object", 29, "28,loafers")
        self.add_class("object", 30, "29,necklace")
        self.add_class("object", 31, "30,panties")
        self.add_class("object", 32, "31,pants")
        self.add_class("object", 33, "32,pumps")
        self.add_class("object", 34, "33,purse")
        self.add_class("object", 35, "34,ring")
        self.add_class("object", 36, "35,romper")
        self.add_class("object", 37, "36,sandals")
        self.add_class("object", 38, "37,scarf")
        self.add_class("object", 39, "38,shirt")
        self.add_class("object", 40, "39,shoes")
        self.add_class("object", 41, "40,shorts")
        self.add_class("object", 42, "41,skin")
        self.add_class("object", 43, "42,skirt")
        self.add_class("object", 44, "43,sneakers")
        self.add_class("object", 45, "44,socks")
        self.add_class("object", 46, "45,stockings")
        self.add_class("object", 47, "46,suit")
        self.add_class("object", 48, "47,sunglasses")
        self.add_class("object", 49, "48,sweater")
        self.add_class("object", 50, "49,sweatshirt")
        self.add_class("object", 51, "50,swimwear")
        self.add_class("object", 52, "51,t-shirt")
        self.add_class("object", 53, "52,tie")
        self.add_class("object", 54, "53,tights")
        self.add_class("object", 55, "54,top")
        self.add_class("object", 56, "55,vest")
        self.add_class("object", 57, "56,wallet")
        self.add_class("object", 58, "57,watch")
        self.add_class("object", 59, "58,wedges")
        self.add_class("object", 60, "59,plazo")


        # Train or validation dataset?
        assert subset in ["train", "val"]
        dataset_dir = os.path.join(dataset_dir, subset)

        # Load annotations
        # VGG Image Annotator saves each image in the form:
        # { 'filename': '28503151_5b5b7ec140_b.jpg',
        #   'regions': {
        #       '0': {
        #           'region_attributes': {},
        #           'shape_attributes': {
        #               'all_points_x': [...],
        #               'all_points_y': [...],
        #               'name': 'polygon'}},
        #       ... more regions ...
        #   },
        #   'size': 100202
        # }
        # We mostly care about the x and y coordinates of each region
        annotations1 = json.load(open('F:/Mask_RCNN_Fitme/Dataset/train/annotations_VGG.json'))
        # print(annotations1)
        annotations = list(annotations1.values())  # don't need the dict keys

        # The VIA tool saves images in the JSON even if they don't have any
        # annotations. Skip unannotated images.
        annotations = [a for a in annotations if a['regions']]
        
        # Add images
        for a in annotations:
            # print(a)
            # Get the x, y coordinaets of points of the polygons that make up
            # the outline of each object instance. There are stores in the
            # shape_attributes (see json format above)
            polygons = [r['shape_attributes'] for r in a['regions']] 
            objects = [s['region_attributes']['name'] for s in a['regions']]
            print("objects:",objects)


            #name_dict = {"laptop": 1,"tab": 2,"phone": 3}
            name_dict = {"0,null": 1,
                         "1,accessories": 2,
                         "2,bag":3,
                         "3,belt":4,
                         "4,blazer":5,
                         "5,blouse":6,
                         "6,bodysuit":7,
                         "7,boots":8,
                         "8,bra":9,
                         "9,bracelet":10,
                         "10,cape":11,
                         "11,cardigan":12,
                         "12,clogs":13,
                         "13,coat":14,
                         "14,dress":15,
                         "15,earrings":16,
                         "16,flats":17,
                         "17,glasses":18,
                         "18,gloves":19,
                         "19,hair":20,
                         "20,hat":21,
                         "21,heels":22,
                         "22,hoodie":23,
                         "23,intimate":24,
                         "24,jacket":25,
                         "25,jeans":26,
                         "26,jumper":27,
                         "27,leggings":28,
                         "28,loafers":29,
                         "29,necklace":30,
                         "30,panties":31,
                         "31,pants":32,
                         "32,pumps":33,
                         "33,purse":34,
                         "34,ring":35,
                         "35,romper":36,
                         "36,sandals":37,
                         "37,scarf":38,
                         "38,shirt":39,
                         "39,shoes":40,
                         "40,shorts":41,
                         "41,skin":42,
                         "42,skirt":43,
                         "43,sneakers":44,
                         "44,socks":45,
                         "45,stockings":46,
                         "46,suit":47,
                         "47,sunglasses":48,
                         "48,sweater":49,
                         "49,sweatshirt":50,
                         "50,swimwear":51,
                         "51,t-shirt":52,
                         "52,tie":53,
                         "53,tights":54,
                         "54,top":55,
                         "55,vest":56,
                         "56,wallet":57,
                         "57,watch":58,
                         "58,wedges":59,
                         "59,plazo":60,
                         } #,"xyz": 3}





            # key = tuple(name_dict)
            num_ids = [name_dict[a] for a in objects]
     
            # num_ids = [int(n['Event']) for n in objects]
            # load_mask() needs the image size to convert polygons to masks.
            # Unfortunately, VIA doesn't include it in JSON, so we must read
            # the image. This is only managable since the dataset is tiny.
            print("numids",num_ids)
            image_path = os.path.join(dataset_dir, a['filename'])
            image = skimage.io.imread(image_path)
            height, width = image.shape[:2]

            self.add_image(
                "object",  ## for a single class just add the name here
                image_id=a['filename'],  # use file name as a unique image id
                path=image_path,
                width=width, height=height,
                polygons=polygons,
                num_ids=num_ids
                )

    def load_mask(self, image_id):
        """Generate instance masks for an image.
       Returns:
        masks: A bool array of shape [height, width, instance count] with
            one mask per instance.
        class_ids: a 1D array of class IDs of the instance masks.
        """
        # If not a Dog-Cat dataset image, delegate to parent class.
        image_info = self.image_info[image_id]
        if image_info["source"] != "object":
            return super(self.__class__, self).load_mask(image_id)

        # Convert polygons to a bitmap mask of shape
        # [height, width, instance_count]
        info = self.image_info[image_id]
        if info["source"] != "object":
            return super(self.__class__, self).load_mask(image_id)
        num_ids = info['num_ids']
        mask = np.zeros([info["height"], info["width"], len(info["polygons"])],
                        dtype=np.uint8)
        for i, p in enumerate(info["polygons"]):
            # Get indexes of pixels inside the polygon and set them to 1
            rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
            
            mask[rr, cc, i] = 1

        # Return mask, and array of class IDs of each instance. Since we have
        # one class ID only, we return an array of 1s
        # Map class names to class IDs.
        num_ids = np.array(num_ids, dtype=np.int32)
        return mask, num_ids #np.ones([mask.shape[-1]], dtype=np.int32)

    def image_reference(self, image_id):
        """Return the path of the image."""
        info = self.image_info[image_id]
        if info["source"] == "object":
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)
def train(model):
    """Train the model."""
    # Training dataset.
    dataset_train = CustomDataset()
    dataset_train.load_custom("F:/Mask_RCNN_Fitme/dataset", "train")
    dataset_train.prepare()

    # Validation dataset
    dataset_val = CustomDataset()
    dataset_val.load_custom("F:/Mask_RCNN_Fitme/dataset", "val")
    dataset_val.prepare()

    # *** This training schedule is an example. Update to your needs ***
    # Since we're using a very small dataset, and starting from
    # COCO trained weights, we don't need to train too long. Also,
    # no need to train all layers, just the heads should do it.
    print("Training network heads")
    model.train(dataset_train, dataset_val,
                learning_rate=config.LEARNING_RATE,
                epochs=10,
                layers='heads')
				
				
				
config = CustomConfig()
model = modellib.MaskRCNN(mode="training", config=config,
                                  model_dir=DEFAULT_LOGS_DIR)

weights_path = COCO_WEIGHTS_PATH
        # Download weights file
if not os.path.exists(weights_path):
  utils.download_trained_weights(weights_path)

model.load_weights(weights_path, by_name=True, exclude=[
            "mrcnn_class_logits", "mrcnn_bbox_fc",
            "mrcnn_bbox", "mrcnn_mask"])

train(model)	
