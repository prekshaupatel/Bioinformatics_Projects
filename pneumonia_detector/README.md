<h1>Pneumonia Detector</h1>

The detector is a neural network model built using <a href="https://www.tensorflow.org/">TensorFlow (v2.2.0 or above)</a> and <a href="https://keras.io/">Keras</a> modules in python3. 
To train the model chest x-rays of normal individuals and pneumonia patients were obtained from <a href="https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia">kaggle</a>. The data had been split into 3 - training, validation, and test datasets. A <a href="https://www.tensorflow.org/api_docs/python/tf/keras/Sequential">neural network</a> was trained and validated. Hyperparameters including image size, batch size, and number of epochs were tuned. 

<h3>Running the Model</h3>

To run the code, download the data from <a href="https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia">kaggle</a> and save the directory as 'pneumonia_detector/data'.

To run the code, make sure you have installed TensorFlow (v2.2.0 or above). If not, run the following command on your commandline:

```
pip install tensorflow
```

Once you have the required libraries, run the code from the src folder.

```
cd src
python3 neural_network.py
```

<h3>References</h3>

* <a href="https://machinelearningmastery.com/pooling-layers-for-convolutional-neural-networks/">A Gentle Introduction to Pooling Layers for Convolutional Neural Networks</a>
