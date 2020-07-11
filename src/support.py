import os
import ssl
from keras.preprocessing.image import ImageDataGenerator


def set_environment():
    """
    Set the environment
    """
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification 
        ssl._create_default_https_context = _create_unverified_https_context

def get_data(path, img_height, img_width, batch_size):
    """
    INPUT: 
           path - Path to directory with subdirectories with images
           img_height - height of image to be resized
           img_width - width of image to be resized 
           batch_size - the batch size
    OUTPUT: Returns a tensorflow.python.keras.preprocessing.image.DirectoryIterator object
    """
    data_gen = ImageDataGenerator(rescale = 1./255)
    raw_data = data_gen.flow_from_directory(
        path,
        seed=123,
        target_size=(img_height, img_width),
        batch_size= batch_size,
        class_mode = "categorical",
        color_mode= "grayscale"
    )
    return raw_data
