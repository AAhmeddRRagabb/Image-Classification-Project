# -------------------------------------------------------------------
# This module is to build supportive functions to the server module
# Those functions will facilitate the model prediction process
# --------------------------------------------------------------------------------------------------------------------------------------

import numpy as np
import cv2
import pywt
import json
import pickle
from pathlib import Path

# --------------------------------------------------------------------------------------------------------------------------------------

base = Path(__file__).parent

# Reading the classes and the model

# Read the Json Classes
def load_json_classes():
    path_to_classes = base / f'shikhs.json'
    with open(path_to_classes, 'r', encoding = 'utf-8') as f:
        return (json.load(f))


# Read the model
def load_model():
    path_to_model = base / f'models/SVMClassifier.pickle'
    with open(path_to_model, 'rb') as model:
        return (pickle.load(model))

# --------------------------------------------------------------------------------------------------------------------------------------


# Detecting important visual details (eyes, nose, ...)
def w2d(img, mode = 'haar', level = 1):
    imArray = img

    if imArray is None:  
        raise FileNotFoundError(f"Image not found or unreadable at")
    
    # Gray Scale
    imArray = cv2.cvtColor(imArray, cv2.COLOR_BGR2GRAY)
    imArray = np.float32(imArray)

    # Normalize pixel values to range [0, 1]
    imArray /= 255

    # Decompose the image using Discrete Wavelet transform -> returns (cA, (cH1, cV1, cD1), ..., (cHn, cVn, cDn))
    # cA: low frequencies
    # cH, cV, cD -> horizontal, vertical, and diagonal details
    coeffs = pywt.wavedec2(imArray, mode, level = level)

    # Removes low freq info
    coeffs_h = list(coeffs)
    coeffs_h[0] *= 0

    # Reconstructs the image
    imArray_h = pywt.waverec2(coeffs_h, mode)
    imArray_h *= 255
    imArray_h = np.uint8(imArray_h)

    return imArray_h
# --------------------------------------------------------------------------------------------------------------------------------------

# Define functions to extract the faces from the images
def get_face(image_path):
    '''
    The functions captures the face of a given character image

    Args:
        image_path (str): The path to the image

    Returns:
        roi_color (np.array(m_pixles, n_pixles, 3)): The region of interest (the face)
    '''

    face_cascade_path = base / "opencv_cascades" / "haarcascade_frontalface_default.xml"
    eye_cascade_path = base / "opencv_cascades" / "haarcascade_eye.xml"
    
    face_cascade = cv2.CascadeClassifier(str(face_cascade_path))
    eye_cascade = cv2.CascadeClassifier(str(eye_cascade_path))

    img = cv2.imread(image_path)
    
    if img is None:
        raise FileNotFoundError(f"Image not found or unreadable at {Path(image_path).resolve()}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

    # Detecting the face region
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y: y+h, x:x+w]

        # Checking if it is a valid photo (a photo with 2+ eyes for a 1+ character)
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if (len(eyes)) >= 2:
            return check_face(roi_color)
        else:
            raise ValueError('Err1')
        


# Check the face 
def check_face(face):
    if face is None:
        raise ValueError('Err2')
    else:
        return face
# --------------------------------------------------------------------------------------------------------------------------------------


# Prepare the image for prediction
def prepare_the_image(img):
    # Scaling and Extracting the important features
    scalled_raw_img = cv2.resize(img, (32, 32))
    img_har = w2d(img, 'db1', 5)
    scalled_img_har = cv2.resize(img_har, (32, 32))

    # Stacking both images to train the model on them
    combined_img = np.vstack((
        scalled_raw_img.reshape(32*32*3, 1),
        scalled_img_har.reshape(32*32, 1)
    ))

    len_img_arr = 32 * 32 * 3 + 32 * 32
    final_img = combined_img.reshape(1, len_img_arr).astype(float)

    return final_img

# --------------------------------------------------------------------------------------------------------------------------------------

# Prediction Function
def classify(file_path, model):
    try:
        # Preprocessing the image to align with the training process
        face = get_face(file_path)
        
        test_img = prepare_the_image(face)

        # Predicting
        cls  = model.predict(test_img.reshape(1, -1))[0]
        prob = model.predict_proba(test_img.reshape(1, -1))[0]

        return cls, prob
    except Exception as e:
        raise ValueError(e)



# --------------------------------------------------------------------------------------------------------------------------------------


    
    
    