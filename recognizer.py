from sklearn import svm
from sklearn import cross_validation
from sklearn.externals import joblib
import os
import numpy as np
from PIL import Image
# import Pillow

class GridRecognizer:
    def __init__(self):
        self.training_data = []
        self.target_values = []
        self.svc = svm.SVC(gamma=0.001, kernel='linear', C=100)
        self.downscale_res = (32, 32)

    def _load(self, path, target_value):
        training_imgs = os.listdir(path)
        for f in training_imgs:
            img = Image.open(path+'/'+f)
            img = img.resize(self.downscale_res, Image.BILINEAR)
            self.training_data.append(np.array(img.getdata()).flatten())
            self.target_values.append(target_value)

    def load(self):
        self._load('training/player', 2)
        self._load('training/enemy', 1)
        self._load('training/boss', 1)
        self._load('training/empty', 0)

    def train(self):
        if os.path.isfile('svc.dat'):
            self.svc = joblib.load('svc.dat')
        else:
            self.load()
            np_data = np.array(self.training_data)
            print (np.array(self.training_data))
            np_values = np.array(self.target_values)
            self.svc.fit(np_data, np_values)
            joblib.dump(self.svc, 'svc.dat', compress=9)

    def predict(self, image):
        resized_img = image.resize(self.downscale_res, Image.BILINEAR)
        np_img = (np.array(resized_img.getdata()).flatten())
        np_img = np.array(np_img).reshape(1,-1)
        return int(self.svc.predict(np_img))


