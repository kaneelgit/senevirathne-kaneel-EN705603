"""
Author - Kaneel Senevirathne
Date - 10/02/2024

Applying transformations to a images.
"""
import cv2
import numpy as np

def horizontal_flip(image):
    flipped_image = cv2.flip(image, 1)  
    return flipped_image

def gaussian_blur(image, kernel_size=(5, 5), sigma=0):
    blurred_image = cv2.GaussianBlur(image, kernel_size, sigma)
    return blurred_image

def resize_image(image, size=(416, 416)):
    resized_image = cv2.resize(image, size)
    return resized_image

def rotate_image(image, angle=45):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, M, (w, h))
    return rotated_image

def adjust_brightness(image, brightness_factor=1.2):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.convertScaleAbs(v, alpha=brightness_factor)
    final_hsv = cv2.merge((h, s, v))
    bright_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return bright_image

def translate_image(image, shift_x=50, shift_y=30):
    (h, w) = image.shape[:2]
    M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
    shifted_image = cv2.warpAffine(image, M, (w, h))
    return shifted_image
