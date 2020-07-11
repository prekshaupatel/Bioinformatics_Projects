import support

import tensorflow as tf
from tensorflow.keras import layers
import keras

batch_size = 32
num_classes = 2
img_height = 1024
img_width = 1024

def main():
    support.set_environment()
    train_data_dir = "../data/train"
    test_data_dir = "../data/test"
    val_data_dir = "../data/val"

    train_data = support.get_data(train_data_dir, img_height, img_width, batch_size)
    test_data = support.get_data(test_data_dir, img_height, img_width, batch_size)
    val_data = support.get_data(val_data_dir, img_height, img_width, batch_size)

    model = tf.keras.Sequential([
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes)
    ])    

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy'])

    model.fit(
        train_data,
        batch_size=batch_size,
        validation_data=val_data,
        epochs=3)

    test_loss, test_acc = model.evaluate(test_data)
    print('test_acc:', test_acc, 'test_loss', test_loss)

main()


