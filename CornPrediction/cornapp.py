import cv2
import numpy as np
import tensorflow
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array


def preprocess_frame(frame):
    # Resize frame to 256x256 to match your model's input size
    frame_resized = cv2.resize(frame, (256, 256))
    
    # Convert frame to array and preprocess it
    frame_array = img_to_array(frame_resized)
    frame_array = np.expand_dims(frame_array, axis=0)
    frame_array /= 255.0  # Normalize to [0, 1]
    
    return frame_array

model = load_model("D:/smartindia/CornPrediction/cornprediction.h5")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Preprocess the frame
    preprocessed_frame = preprocess_frame(frame)
    
    # Predict
    prediction = model.predict(preprocessed_frame)
    
    dict={
    0: 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    1: 'Corn_(maize)___Common_rust_', 
    2: 'Corn_(maize)___Northern_Leaf_Blight',
    3: 'Corn_(maize)___healthy',
}
    
    # Display the result on the frame
    # if prediction[0][0] > 0.5:  # Assuming binary classification
    #     label = "Diseased"
    # else:
    #     label = "Healthy"
    pred_class=np.argmax(prediction,axis=1)[0]
    label=dict[pred_class]
    
    print(label)
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Camera Feed', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
