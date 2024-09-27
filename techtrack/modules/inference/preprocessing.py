"""
Author - Kaneel Senevirathne
Date - 09/27/2024

Developing a preprocessing module that reads a video from a file and preprocesses videos to the 
object_detection_module for inference. 

"""

import cv2
import numpy as np

def capture_video(video_path: str, drop_rate: int = 10):
    """
    Takes in video path, and yeild rate (default 10) and yeilds the frames after preprocessing
    """

    #open video
    video = cv2.VideoCapture(video_path)

    #check if open
    if not video.isOpened():
        raise("Video didn't succesfully open")
        
    #iterate through frames and yeild
    frame_number = 0
    batch = []

    while True:
        ret, frame = video.read()

        #exit loop if no more frames
        if not ret:
            break
        
        if frame_number % drop_rate == 0:

            #preprocess frame
            frame_processed = cv2.dnn.blobFromImage(frame,
                                scalefactor = 1/255.,
                                size = (416, 416),
                                mean = (0, 0, 0),
                                swapRB = True,
                                crop = False
            )

            batch.append(frame_processed)

        if len(batch) == drop_rate:
            #convert the list to the correct format of images
            squeezed_batch = [np.squeeze(img, axis=0) for img in batch]
            final_batch = np.stack(squeezed_batch, axis=0)      
            yield final_batch
            batch = [] #collect next batch

        frame_number += 1

    #yeild the left over stuff
    if batch:
        squeezed_batch = [np.squeeze(img, axis=0) for img in batch]
        final_batch = np.stack(squeezed_batch, axis=0)      
        yield final_batch