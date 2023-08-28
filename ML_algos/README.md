# Overview
<br>

## Complete Multimodal Flow-chart:
![Multimodal_Flowchart](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/ed5edc8e-1a43-4d84-8d3a-f3ed4681f891)

<br>
<br>

## Model Architecture for CNN Classification into Contact, Non-Contact
![Model_Architecture_CNN_classsification](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/deb9c234-6b30-4909-a612-22b43a371d01)

<br>

## Model Architecture for CNN Classification into left, right direction

![Model_Architecture_CNN_classsification](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/deb9c234-6b30-4909-a612-22b43a371d01)


### Note: Here left direction implies that the object was brought in contact with the whisker array from the left direction and vice-versa for the right direction.

<br>

## Model Architecture for CNN regression to obtain x,y coordinates of the object with respect to the Whisker Robot.

![Model_Architecture_CNN_regression](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/dc5dd455-ff9d-4038-824d-8d169a346c98) 
<br>
<br>
<br>

# Background:
1) The CNN classification model for contact/non-contact prediction is trained on the entire dataset, excluding the suspicious  <br>
data and NaN values. <br>
2) The CNN classification model for left/right direction prediction is trained on only trustworthy contact data.  <br>

3a) A separate neural network (CNN model in this case) is trained for x-coordinate, y-coordinate of object prediction, trained     <br>
only on left direction trustworthy contact data.
b) A separate neural network (CNN model in this case) is trained for x-coordinate, y-coordinate of object prediction, trained     <br>
only on right direction trustworthy contact data.  <br>
<br>
<br>

# Guidelines:
1) Firstly, run the classification code for contact/non-contact, classification model code for direction, regression model code for x,y coordinates, <br>
in any order. Each of the model codes saves checkpoints (weights) at regular intervals of epochs. Evaluate the model during training and testing by <br> 
looking at the accuracy and loss across epochs. Based on the performance pick a checkpoint when the model performs best and is neither underfitting <br>
nor overfitting. Higher the accuracy and lower the loss indicates better performance. Performing well on training data and bad on test indicates overfitting <br>
Performing poorly on training usually indicates underfitting.

2) After having picked checkpoints for each of the 4 neural networks/ ML models, use these in the multimodal code to make the ultimate predictions. <br>

<br>

# How to run the code?

## ML model for contact/ non-contact classification:

`python3 CNN_.ipynb`  --> To run the CNN classification code for contact/ non-contact, save checkpoints, and evaluate the model.

## ML model for left/ right classification:
`python3 CNN_.ipynb`  --> To run the CNN classification code for left direction/ right direction, save checkpoints, and evaluate the model.

## ML model to predict x,y coordinates:
`python3 CNN_.ipynb`  --> To run the CNN regression code for left direction/ right direction, save checkpoints, and evaluate the model.

## Multimodal Code:
`python3 CNN_merge.ipynb`  --> To run the CNN multimodal code.

## Random testing:
`python3 CNN_testing.ipynb`  --> To run the random testing code for placing the peg at random positions and testing (making predictions).