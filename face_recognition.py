import os
from os import listdir
from PIL import Image as Img
from numpy import asarray
from numpy import expand_dims
from keras.models import load_model
import cv2
from mtcnn import MTCNN
import pickle

MyFaceNet = load_model("model/facenet_keras.h5")
knowing_faces_path = 'images/knowing_faces/'
detector = MTCNN()


def update_dataset():
    database = {}

    for filename in listdir(knowing_faces_path):
        file_path = knowing_faces_path + filename
        photo = cv2.imread(file_path)

        output = detector.detect_faces(photo)
        temp = []

        if len(output) > 0:
            temp = output[0]

        if temp:
            x1, y1, w, h = temp['box']
            x2, y2 = x1 + w, y1 + h

        gbr = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
        gbr = Img.fromarray(gbr)
        gbr_array = asarray(gbr)

        face = gbr_array[y1:y2, x1:x2]

        face = Img.fromarray(face)
        face = face.resize((160, 160))
        face = asarray(face)

        face = face.astype('float32')
        mean, std = face.mean(), face.std()
        face = (face - mean) / std

        face = expand_dims(face, axis=0)
        signature = MyFaceNet.predict(face)

        database[os.path.splitext(filename)[0]] = signature

    data_file = open("data.pkl", "wb")
    pickle.dump(database, data_file)
    data_file.close()

