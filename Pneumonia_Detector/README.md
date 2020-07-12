<h1>Pneumonia Detector</h1>

The detector is a neural network model built using <a href="https://www.tensorflow.org/">TensorFlow (v2.2.0 or above)</a> and <a href="https://keras.io/">Keras</a> modules in python3. 
To train the model chest x-rays of normal individuals and pneumonia patients were obtained from <a href="https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia">kaggle</a>. The data had been split into 3 - training, validation, and test datasets. A <a href="https://www.tensorflow.org/api_docs/python/tf/keras/Sequential">neural network</a> was trained and validated. Parameters including model layers and number of epochs were tuned. 

<h3>Running the Model</h3>

To run the code, download the data from <a href="https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia">kaggle</a> and save the directory as 'pneumonia_detector/data'.

To run the code, make sure you have installed TensorFlow (v2.2.0 or above). If not, run the following command on your commandline:

```
$ pip install tensorflow
```

Once you have the required libraries, make sure you have the neccessary directories in your 'pneumonia_detector' directory. 

```
$ ls
README.md data  output  src
$ ls data
test  train val
```

Once the environment is setup, run the code from the src folder. 

```
$ cd src
$ python3 neural_network.py
```

The code saves the output, including the test accuracy and the corresponding analysis, in the 'output' directory. On an average, this code gives a test accuracy of 0.74.



