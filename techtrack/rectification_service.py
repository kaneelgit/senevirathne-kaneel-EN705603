import os
import cv2
import argparse
import numpy as np
from modules.rectification.augmentation import horizontal_flip, vertical_flip, gaussian_blur, resize_image, convert_to_grayscale, adjust_brightness, adjust_contrast
from modules.rectification.hard_negative_mining import sample_hard_negatives

def augment_image(image):

    augmentations = [
        horizontal_flip,
        vertical_flip,
        lambda img: gaussian_blur(img, kernel_size=(5, 5)),
        lambda img: resize_image(img, size=(416, 416)),
        convert_to_grayscale,
        lambda img: adjust_brightness(img, beta=50),
        lambda img: adjust_contrast(img, alpha=1.5)
    ]
    
    augmented_images = []
    for augmentation in augmentations:
        augmented_image = augmentation(image)
        augmented_images.append(augmented_image)
    
    return augmented_images

def process_images(prediction_dir: str, annotation_dir: str, output_dir: str, num_samples: int = 10, iou_threshold: float = 0.5):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    sorted_results = sample_hard_negatives(prediction_dir, annotation_dir, num_samples, iou_threshold)
    
    # Process each selected image
    for i, (image_dir, (loss, pred_path, ann_path)) in enumerate(sorted_results):
        image = cv2.imread(image_dir)
        if image is None:
            print(f"Error loading image {image_dir}")
            continue
        
        # Perform augmentations
        augmented_images = augment_image(image)
        
        # Save augmented images
        for j, aug_image in enumerate(augmented_images):
            aug_image_path = os.path.join(output_dir, f"{os.path.basename(image_dir).split('.')[0]}_aug_{j}.jpg")
            cv2.imwrite(aug_image_path, aug_image * 255)  # Ensure image is in range [0, 255]
            print(f"Saved augmented image {aug_image_path}")

def main():
    parser = argparse.ArgumentParser(description="Rectification service for hard negative mining and image augmentation.")
    
    # Adding arguments for command-line inputs
    parser.add_argument('--prediction_dir', required=True, help='Path to the directory containing prediction files.')
    parser.add_argument('--annotation_dir', type=str, required=True, help='Path to the directory containing annotation files.')
    parser.add_argument('--output_dir', type=str, required=True, help='Path to the directory where augmented images will be saved.')
    parser.add_argument('--num_samples', type=int, default=10, help='Number of hard negatives to sample and augment.')
    parser.add_argument('--iou_threshold', type=float, default=0.5, help='IoU threshold for selecting hard negatives.')
    
    # Parsing command-line arguments
    args = parser.parse_args()
    
    # Call the image processing function with the parsed arguments
    process_images(
        prediction_dir=args.prediction_dir,
        annotation_dir=args.annotation_dir,
        output_dir=args.output_dir,
        num_samples=args.num_samples,
        iou_threshold=args.iou_threshold
    )

if __name__ == "__main__":
    main()

