import numpy as np
import argparse
import tensorflow as tf
import cv2
import time
import subprocess
import sys

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile

# Global variable to hold the current class detected
current_class_detected = None

def load_model(model_path):
    model = tf.saved_model.load(model_path)
    return model


def run_inference_for_single_image(model, image):
    image = np.asarray(image)
    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis,...]
    
    # Run inference
    output_dict = model(input_tensor)

    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(output_dict.pop('num_detections'))
    output_dict = {key: value[0, :num_detections].numpy()
                   for key, value in output_dict.items()}
    output_dict['num_detections'] = num_detections

    # detection_classes should be ints.
    output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)
   
    # Handle models with masks:
    if 'detection_masks' in output_dict:
        # Reframe the the bbox mask to the image size.
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                                    output_dict['detection_masks'], output_dict['detection_boxes'],
                                    image.shape[0], image.shape[1])      
        detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5, tf.uint8)
        output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()
    
    return output_dict


def check_with_pause(detection_classes, detection_scores, threshold=0.6):
    global current_class_detected
    
    # Filter detection_classes based on the threshold
    filtered_classes = [detection_classes[i] for i in range(len(detection_scores)) if detection_scores[i] >= threshold]
    print(f"Detection classes after filtering: {filtered_classes}")  # Debug print
    
    if len(filtered_classes) == 1:
        print(f"Current class detected: {current_class_detected}")  # Debug print
        if current_class_detected != filtered_classes[0]:
            current_class_detected = filtered_classes[0]
            print(f"Updated current class detected: {current_class_detected}")  # Debug print
            return
        if current_class_detected == filtered_classes[0]:
            print('DETECTED PROPER: ', current_class_detected)
            subprocess.run(['python', 'C:/Users/ethan/notebooksmlprojects/.ipynb_checkpoints/arduinoConnectScript.py'])
            sys.exit()
            current_class_detected = None
            return
        else:
            current_class_detected = None
            return
    else:
        current_class_detected = None
        return

def run_inference(model, category_index, cap):
    while True:
        ret, image_np = cap.read()
        # Actual detection.
        output_dict = run_inference_for_single_image(model, image_np)
        
        # Call check_with_pause with detection_classes
        if(current_class_detected != None):
            time.sleep(3)
            # Uncomment this line for proper running
            check_with_pause(output_dict['detection_classes'], output_dict['detection_scores'])
        else:
            check_with_pause(output_dict['detection_classes'], output_dict['detection_scores'])
        
        # Visualization of the results of a detection.
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            category_index,
            instance_masks=output_dict.get('detection_masks_reframed', None),
            use_normalized_coordinates=True,
            line_thickness=8)
        cv2.imshow('object_detection', cv2.resize(image_np, (800, 600)))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detect objects inside webcam videostream')
    parser.add_argument('-m', '--model', type=str, required=True, help='Model Path')
    parser.add_argument('-l', '--labelmap', type=str, required=True, help='Path to Labelmap')
    args = parser.parse_args()

    detection_model = load_model(args.model)
    category_index = label_map_util.create_category_index_from_labelmap(args.labelmap, use_display_name=True)

    cap = cv2.VideoCapture(0)
    run_inference(detection_model, category_index, cap)

# python .\detect_from_webcam.py -m ssd_mobilenet_v2_320x320_coco17_tpu-8\saved_model -l .\data\mscoco_label_map.pbtxt

# python "C:\Users\ethan\notebooksmlprojects\.ipynb_checkpoints\runFromWebcam.py" -m "C:\Users\ethan\notebooksmlprojects\.ipynb_checkpoints\savedModelFolder\saved_model" -l "C:\Users\ethan\notebooksmlprojects\labelmap.pbtxt"