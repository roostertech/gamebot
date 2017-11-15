from sklearn import svm
from sklearn import cross_validation
from sklearn.externals import joblib
import os
import numpy as np
from PIL import Image


# import Pillow

class Recognizer:
    def __init__(self, name, downscale=True, downscale_res=(32,32)):
        self.training_data = []
        self.target_values = []
        self.svc = svm.SVC(gamma=0.001, kernel='linear', C=100)
        self.downscale_res = downscale_res
        self.name = name
        self.downscale = downscale

    def load(self, path, target_value, verbose=False):
        training_imgs = os.listdir(path)
        for f in training_imgs:
            if verbose:
                print "%s -> %d" % (f, target_value)
            img = Image.open(path + '/' + f)
            if self.downscale:
                img = img.resize(self.downscale_res, Image.BILINEAR)
            self.training_data.append(np.array(img.getdata()).flatten())
            self.target_values.append(target_value)

    # def load(self):
    #     self._load('training/player', 2)
    #     self._load('training/enemy', 1)
    #     self._load('training/boss', 1)
    #     self._load('training/empty', 0)

    def train(self):
        if os.path.isfile('svc-%s.dat' % self.name):
            self.svc = joblib.load('svc-%s.dat' % self.name)
        else:
            # self.load()
            np_data = np.array(self.training_data)
            print (np.array(self.training_data))
            np_values = np.array(self.target_values)
            self.svc.fit(np_data, np_values)
            joblib.dump(self.svc, 'svc-%s.dat' % self.name, compress=9)

    def predict(self, image):
        if self.downscale:
            image = image.resize(self.downscale_res, Image.BILINEAR)
        np_img = (np.array(image.getdata()).flatten())
        np_img = np.array(np_img).reshape(1, -1)
        return int(self.svc.predict(np_img))
