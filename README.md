# AI-Waste-Classification-Recycling-Recommendation-System-
This project is an AI-powered waste management system that classifies waste images using a MobileNetV2 deep learning model and recommends relevant recycling companies based on the predicted waste type.  The application is built using Python, TensorFlow/Keras, and Streamlit, making it lightweight, interactive, and deployment-ready.

#Overview
Manual waste segregation is time-consuming, unsafe, and highly dependent on human expertise. This project leverages a trained MobileNetV2-based deep learning model to classify waste images and provide instant predictions through a simple and interactive web interface.

Users can either upload an image from their device or capture an image using a camera, making the system practical and user-friendly.

#Model Details
Model Architecture: MobileNetV2 (Transfer Learning)
Framework: TensorFlow / Keras
Task: Multi-class Image Classification
Optimizer: Adam
Loss Function: Categorical Crossentropy

#Technology Stack
Python
TensorFlow
Keras
Streamlit
OpenCV
NumPy
Pillow

####Dataset Details
Recycling Companies Dataset (companies.xlsx)
Column Name	Description
Company_Names	Name of recycling company
Waste_Needed	Type of waste accepted
Location	Company location
Website	Official website

#####How the System Works

1.User uploads an image of waste

2.Image is preprocessed and passed to MobileNetV2 model

3.Model predicts the waste category

4.Relevant recycling companies are fetched from the dataset

5.Results are displayed with company details and website links

####Future Enhancements

Location-based company filtering

###User authentication

Integration with real-time municipal APIs

Multi-language support

####Author

Gayatri Adatiya
AI & Data Science Student

###License

This project is for educational and academic purposes.

