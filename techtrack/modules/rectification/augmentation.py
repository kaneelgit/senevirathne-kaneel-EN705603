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
    image = image * 255.
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    return grayscale_image / 255.


def adjust_brightness(image, beta):
    image = image * 255.
    bright_image = cv2.convertScaleAbs(image, alpha=1, beta=beta)

    return bright_image / 255.

def adjust_contrast(image, alpha):
    image = image * 255.
    contrast_image = cv2.convertScaleAbs(image, alpha=alpha, beta=0)
    return contrast_image / 255.