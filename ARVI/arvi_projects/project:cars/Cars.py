from keras.applications.resnet50 import ResNet50
from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, Flatten
from keras.models import Model
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

def get_model(cls=100):
    feature_extractor = ResNet50(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    flat = Flatten()(feature_extractor.output)
    # d = Dense(nb_classes*2, activation='relu')(flat)
    # d = Dense(nb_classes, activation='softmax')(d)
    print(np.shape(flat),'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    d = Dense(cls, activation='softmax')(flat)
    m = Model(inputs=feature_extractor.input, outputs=d)

    for layer in m.layers[:-8]:
        layer.trainable = False

    m.compile(
        optimizer=SGD(lr=0.01, momentum=0.9),
        loss='categorical_crossentropy',
        metrics=['accuracy'])
    m.summary()
    return m

nb_classes = 514

model = get_model(cls=nb_classes)

for layer in model.layers[:-14]:
        layer.trainable = False

model.compile(optimizer=SGD(lr=0.001, momentum=0.9),
        loss='categorical_crossentropy',
        metrics=['accuracy'])


# model.load_weights('weights_finetuned.h5')

img_height = 224
img_width = 224
batch_size = 32

train_dir = 'data/cartrain/'
test_dir = 'data/cartest/'


train_gen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_gen = ImageDataGenerator(rescale=1./255)

train_generator = train_gen.flow_from_directory(
    train_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

test_generator = test_gen.flow_from_directory(
    test_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

model.fit_generator(
    generator=train_generator,
    validation_data= test_generator,
    validation_steps=8,
    steps_per_epoch=42,
    nb_epoch=42,
    callbacks=[ModelCheckpoint('weights_finetuned.h5', save_best_only=True, monitor='val_loss')])

model.save_weights('weights_finetuned.h5')