# Image Classification Project
This project offers hands-on experience in Machine Learning (ML) through the task of image classification. The primary goal is to classify images of Muslim shikhs using multiple ML algorithms, including logistic regression, decision tree, random forest, and support vector machines. The project was accomplished taking a several sequential steps, described below:- 
1. Downloading public images (for public shikhs) using python `icrawler` library which eased the process of downloading several images for the classificaion project.
2. Using the `OpenCV` library to load, process, and clean the images. The library was very useful and helped to extract the face area and the eyes from the image symplifying the process of detecting shikhs.
   * [Face Detection](https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_frontalface_default.xml)
   * [Eye Detection](https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_eye.xml)
3. After that, some images were not suitable for the project such as images for different persons, images with very poor quality, and etc. Those images have been manually cleaned in order to produce a high-performance model.
4. Using the `wavelet` transformation to extract useful info from the image such as eyes, nose, and etc. The code are sourced from `StackOverFlow`.
5. After that, several (ML) models are trained on the cleaned faces with the GridSearchCV. Results revealed that `LogisticRegression` & `SupportVectorMachine` models achieved a very good accuracy of 93%. However, the model found to perform poorly on certain character, who is `El-Hossary`, and that's due to the lack of different images since the majority of his training images were similar.
6. The final step, was to serving this model using `Flask` environment ...
