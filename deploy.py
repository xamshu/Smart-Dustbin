!git clone https://github.com/xamshu/Smart-Dustbin.git


import numpy as np
import pandas as pd
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        os.path.join(dirname, filename)
import os
from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
IMAGE_SIZE = [224, 224]

train_path = "/content/Smart-Dustbin/DATASET/TRAIN/"
valid_path = "/content/Smart-Dustbin/DATASET/TEST/"
# Import the Resnet50 architecture
resnet = ResNet50(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)
for layer in resnet.layers:
    layer.trainable = False

#Finding numbers of the class
folders = glob('/content/Smart-Dustbin/DATASET/TRAIN/*')
x = Flatten()(resnet.output)
prediction = Dense(len(folders), activation='softmax')(x)

model = Model(inputs=resnet.input, outputs=prediction)
model.summary()

model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

#creating test dataset
training_set = train_datagen.flow_from_directory('/content/Smart-Dustbin/DATASET/TRAIN/',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('/content/Smart-Dustbin/DATASET/TEST/',
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'categorical')
from tensorflow.keras.callbacks import ModelCheckpoint
MODEL_DIR = "/content/Smart-Dustbin/"

if not os.path.exists(MODEL_DIR):  #If the directory does not exist, create it.
    os.makedirs(MODEL_DIR)
checkpoint = ModelCheckpoint(filepath=os.path.join(MODEL_DIR, "model-{epoch:02d}.h5"), save_best_only=True)

#fit the model
r = model.fit_generator(
  training_set,
  validation_data=test_set,
  epochs=20,
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)
# loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()
#plt.savefig('LossVal_loss_eff')

# accuracy
plt.plot(r.history['accuracy'], label='train acc')
plt.plot(r.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()
#plt.savefig('AccVal_acc_eff')
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Dropout, Flatten, Dense, BatchNormalization
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.utils.vis_utils import plot_model
from glob import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import cv2
from tensorflow.keras.models import load_model

model.save('resnet.h5')

y_pred = model.predict(test_set)
y_pred

import numpy as np
y_pred = np.argmax(y_pred, axis=1)
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
model=load_model('resnet.h5')
# test data to check model and predict
img = image.load_img('/content/Smart-Dustbin/DATASET/TEST/O/O_12577.jpg', target_size = (224, 224))
img = image.img_to_array(img)
img = np.expand_dims(img, axis = 0)
result = model.predict(img)
training_set.class_indices

if result[0][0] == 1:
    prediction = 'Inorganic'
else:
    prediction = 'Organic'