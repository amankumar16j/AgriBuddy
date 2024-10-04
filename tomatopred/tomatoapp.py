import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Load your trained model
model = load_model("D:/smartindia/tomatopred/tomatopred1.h5")

def preprocess_frame(frame):
    # Resize frame to the input size expected by your model (e.g., 256x256)
    frame_resized = cv2.resize(frame, (256, 256))
    frame_array = img_to_array(frame_resized)
    frame_array = np.expand_dims(frame_array, axis=0)
    frame_array /= 255.0  # Normalize to [0, 1]
    return frame_array

# Define the color range for object detection (e.g., detecting green)
lower_bound = np.array([35, 100, 100])  # Lower bound of green in HSV
upper_bound = np.array([85, 255, 255])  # Upper bound of green in HSV

# Start capturing video from the default camera (0)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame for prediction
    preprocessed_frame = preprocess_frame(frame)
    prediction = model.predict(preprocessed_frame)

    dict={0:'Tomato___Bacterial_spot',
 1:'Tomato___Early_blight',
 2:'Tomato___Late_blight',
 3:'Tomato___Leaf_Mold',
 4:'Tomato___Septoria_leaf_spot',
 5:'Tomato___Spider_mites Two-spotted_spider_mite',
 6:'Tomato___Target_Spot',
 7:'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
 8:'Tomato___Tomato_mosaic_virus',
9: 'Tomato___healthy'}
    
    # Display the result on the frame
    # if prediction[0][0] > 0.5:  # Assuming binary classification
    #     label = "Diseased"
    # else:
    #     label = "Healthy"
    pred_class=np.argmax(prediction,axis=1)[0]
    if pred_class in dict:
        label=dict[pred_class]
    else:
        label="Cannot detect the disease please try by uploading image"
    
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame with the bounding box and label
    cv2.imshow('Live Feed Prediction', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
