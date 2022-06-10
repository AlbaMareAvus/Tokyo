import cv2
from mtcnn import MTCNN
# import torch
# from facenet_pytorch import MTCNN

detector = MTCNN()
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def mtcnn_face_detection(frame):
    output = detector.detect_faces(frame)
    temp = []

    if len(output) > 0:
        temp = output[0]

    if temp:
        x, y, w, h = temp['box']
        cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=(255, 200, 100), thickness=2)

    return frame


# from facenet_pytorch import MTCNN
# import torch
# import cv2
#
# if torch.cuda.is_available():
#     device = torch.device('cuda')
# else:
#     device = torch.device('cpu')
# capture = cv2.VideoCapture(0)
# detector = MTCNN(margin=40, select_largest=False, post_process=False, device='cuda:0')
#
# while True:
#     ret, frame = capture.read()
#     if not ret:
#         print("fail to grab frame, try again")
#         break
#
#     output = detector.detect(frame)
#
#     cv2.imshow('win', frame)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# capture.release()
# cv2.destroyAllWindows()


def haarcascade_face_detection(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 15, 200), 3)
    return frame
