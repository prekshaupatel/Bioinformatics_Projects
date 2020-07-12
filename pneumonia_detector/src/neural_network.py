import support
import tensorflow as tf
from tensorflow.keras import layers
import keras
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np

batch_size = 32
num_classes = 2
img_height = 256
img_width = 256
Epochs = 30

def main():
    support.set_environment()
    train_data_dir = "../data/train"
    test_data_dir = "../data/test"
    val_data_dir = "../data/val"

    train_data = support.get_data(train_data_dir, img_height, img_width, batch_size)
    test_data = support.get_data(test_data_dir, img_height, img_width, batch_size)
    val_data = support.get_data(val_data_dir, img_height, img_width, batch_size)

    print("\nTraining Model...")
    model = tf.keras.Sequential([
        layers.Conv2D(32, 3, activation='relu'),
        layers.AveragePooling2D(),
        layers.Conv2D(32, 3, activation='relu'),
        layers.AveragePooling2D(),
        layers.Conv2D(16, 3, activation='relu'),
        layers.AveragePooling2D(),
        layers.Flatten(),
        layers.Dense(1024, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(1, activation='sigmoid')
    ])    
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy'])

    H = model.fit(
        train_data,
        batch_size=batch_size,
        validation_data=val_data,
        epochs=Epochs)

    print("Testing Model...")
    print("Writing test result to ../output/test_results.txt")
    f = open("../output/test_results.txt", 'w')
    
    test_loss, test_acc = model.evaluate(test_data)
    w_str = 'Test Accuracy: ' + str(test_acc) + ' Test Loss: ' + str(test_loss) + '\n'
    f.write(w_str)

    
    test_y = test_data.labels
    pred_y = model.predict(test_data)

    for i in range(len(pred_y)):
        if pred_y[i] > 0.5:
            pred_y[i] = 1
        else:
            pred_y[i] = 0

    label_names = ["" for i in range(len(test_data.class_indices))]
    for i in test_data.class_indices:
        label_names[test_data.class_indices[i]] = i
        
    f.write(classification_report(test_y, pred_y,target_names=label_names))

    
    cm = confusion_matrix(test_y, pred_y)
    total = sum(sum(cm))
    acc = (cm[0, 0] + cm[1, 1]) / total
    sensitivity = cm[0, 0] / (cm[0, 0] + cm[0, 1])
    specificity = cm[1, 1] / (cm[1, 0] + cm[1, 1])
    
    #print(cm)
    f.write("\nAccuracy: {:.4f}".format(acc))
    f.write("\nSensitivity: {:.4f}".format(sensitivity))
    f.write("\nSpecificity: {:.4f}\n".format(specificity))

    f.close()
    
    N = Epochs
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
    plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
    plt.title("Training Loss and Accuracy on Pneumonia Dataset")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")
    plt.savefig("../output/plot.png", dpi=1000)

    model.save("../output/pnemonia.model", save_format="h5")

    
main()


