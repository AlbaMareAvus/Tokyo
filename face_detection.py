import cv2
from mtcnn import MTCNN

detector = MTCNN()

capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read()

    output = detector.detect_faces(frame)

    for single_output in output:
        x, y, w, h = single_output['box']
        cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=(255, 200, 100), thickness=2)

    cv2.imshow('win', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyWindow()


"""
from facenet_pytorch import MTCNN
import torch
import cv2

if torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')

capture = cv2.VideoCapture(0)
detector = MTCNN(keep_all=True, device=device)

while True:
    ret, frame = capture.read()
    if not ret:
        print("fail to grab frame, try again")
        break

    output = detector.detect(frame)

    cv2.imshow('win', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
"""

"""import cv2

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam.
cap = cv2.VideoCapture(0)

while True:
    # Read the frame
    _, frame = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 15, 200), 3)
    # Display
    cv2.imshow('Frame', frame)
    # Stop if escape key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()"""
