import os
from os import listdir
from PIL import Image as Img
from numpy import asarray
from numpy import expand_dims
from keras.models import load_model
import cv2
from mtcnn import MTCNN
import pickle
import numpy as np

MyFaceNetModel = load_model("model/facenet_keras.h5")
knowing_faces_path = 'images/knowing_faces/'
mtcnn_detector = MTCNN()


def update_dataset():
    database = {}

    for file_name in listdir(knowing_faces_path):
        file_path = knowing_faces_path + file_name
        photo = cv2.imread(file_path)

        output = mtcnn_detector.detect_faces(photo)
        temp = []

        if len(output) > 0:
            temp = output[0]

        if temp:
            x1, y1, w, h = temp['box']
            x2, y2 = x1 + w, y1 + h

        gbr_frame = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
        gbr_frame = Img.fromarray(gbr_frame)
        gbr_array = asarray(gbr_frame)

        found_face = gbr_array[y1:y2, x1:x2]

        found_face = Img.fromarray(found_face)
        found_face = found_face.resize((160, 160))
        found_face = asarray(found_face)

        found_face = found_face.astype('float32')
        mean, std = found_face.mean(), found_face.std()
        found_face = (found_face - mean) / std

        found_face = expand_dims(found_face, axis=0)
        sign = MyFaceNetModel.predict(found_face)

        database[os.path.splitext(file_name)[0]] = sign

    data_file = open("database/data.pkl", "wb")
    pickle.dump(database, data_file)
    data_file.close()


def face_recognition(output, frame):
    my_file = open("database/data.pkl", "rb")
    database = pickle.load(my_file)
    my_file.close()
    x1, y1, w, h = output['box']
    x2, y2 = x1 + w, y1 + h

    gbr_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gbr_frame = Img.fromarray(gbr_frame)
    gbr_array = asarray(gbr_frame)

    found_face = gbr_array[y1:y2, x1:x2]

    found_face = Img.fromarray(found_face)
    found_face = found_face.resize((160, 160))
    found_face = asarray(found_face)

    found_face = found_face.astype('float32')
    mean, std = found_face.mean(), found_face.std()
    found_face = (found_face - mean) / std

    found_face = expand_dims(found_face, axis=0)
    sign = MyFaceNetModel.predict(found_face)

    min_dist = 100
    identity = ' '
    for k, value in database.items():
        dist = np.linalg.norm(value - sign)
        if dist < min_dist:
            min_dist = dist
            identity = k

    return identity
