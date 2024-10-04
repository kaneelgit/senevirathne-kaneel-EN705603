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

def vertical_flip(image):
    flipped_image = cv2.flip(image, 0) 
    return flipped_image

def convert_to_grayscale(image):
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    return grayscale_image


def adjust_brightness(image, brightness_range=(0.5, 1.5)):
    factor = np.random.uniform(brightness_range[0], brightness_range[1])
    bright_image = cv2.convertScaleAbs(image, alpha=factor, beta=0)  
    return bright_image
