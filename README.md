# Printed-Text-recognition-and-conversion

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

The aim was to make a software that can recognize text from the scanned document images, 
and store it electronically in a format(.txt) so that the users can edit the text or locate any word or phrase.

## Methods used:

 * Image Processing:
   <ol>
    <li>Binarization</li>
    <li>Skew-Correction</li>
   </ol>
 * Segmentation 
   <ol>
    <li>Line segmentation</li>
    <li>Character segmentation</li>
   </ol>
 * The training is done using CNN model.

## To install
The language used is Python3
  
  ### Required libraries
  ```sh
      Numpy
      OpenCV
      Sklearn
      Scikit
      Tensorflow
      PyQt4
```
  ### To run through GUI
  ```sh
      python gui.py      
```
  ### To run on CLI
  ```sh
      python main.py     
```
