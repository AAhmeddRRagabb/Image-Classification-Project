# Image Classification Project
This project provides hands-on experience in Machine Learning (ML) through the task of image classification. The primary goal is to classify images of Muslim shikhs using multiple ML algorithms, including Logistic Regression, Decision Tree, Random Forest, and Support Vector Machines.


## The Workflow
1. **Image Collection:** Downloaded public images of well-known shikhs using Python’s `icrawler` library, which streamlined the process of gathering a large dataset for classification.
   
2. **Image Processing with OpenCV:** Leveraged the OpenCV library to load, process, and clean images. In particular, OpenCV’s Haar cascades were used for detecting faces and eyes, simplifying the shikh detection process.
   * [Face Detection](https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_frontalface_default.xml)
   * [Eye Detection](https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_eye.xml)
     
3. **Manual Cleaning:** Removed unsuitable images such as those showing different individuals, poor-quality images, or irrelevant content (downloaded by the crawler) to ensure high-quality training data.
   
4. **Feature Extraction with Wavelet Transform:** Applied wavelet transformation to extract key facial features such as eyes and nose. The implementation was adapted from solutions found on Stack Overflow.
  
5. **Model Training & Evaluation:** Trained multiple ML models on the cleaned dataset using GridSearchCV. Results showed that Logistic Regression and Support Vector Machine models achieved an accuracy of 93%. However, performance was weaker for certain individuals — e.g., El-Hossary — due to limited variety in their training images.
   
6. **Model Deployment:** Served the trained model through a Flask application, paired with a simple UI built using HTML & CSS, and enhanced with JavaScript for interactive functionality.


## Additional Features
Integrated a free LLM from [OpenRouter.ai](https://openrouter.ai/) to generate brief informational text about the classified shikh. This enhances the user experience by providing context along with the classification result.



Image-Classification-Project/
│
├── classification.ipynb                # Training & evaluation
│
├── utils/                               # Standalone scripts & detection files
│   └── open_CV_cascades/                # Haar cascade XMLs
│
├── server/                              # Flask backend + frontend
│   ├── app.py                           # Flask app entry point
│   ├── static/                          # Static assets
│   │   ├── css/                         # Stylesheets
│   │   ├── js/                          # JavaScript
│   │   ├── img/                         # UI images
│   │   └── test-images/                 # Test images
│   ├── templates/                       # HTML templates
│   └── utils/                           # Backend helpers
│       ├── champion_model/              # Best-performing trained model
│       ├── open_CV_cascades/            # Haar cascade XMLs
│       ├── classification.py            # Inference logic
│       ├── llm_details.py                # LLM integration
│       └── shikhs.json                   # Class labels
│
├── models/                              # Trained ML models
│
├── data/                                # Dataset
│   ├── images/                          # Raw images
│   ├── faces/                           # Auto-processed images
│   └── faces_after_manual_cleaning/     # Final dataset
│
└── README.md                            # Documentation



---
---
* Additional Resources
  [ML Image Classification](https://www.youtube.com/playlist?list=PLeo1K3hjS3uvaRHZLl-jLovIjBP14QTXc)
---
---
***ALHAMDULILLAH***
   

  
