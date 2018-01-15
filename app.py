import io
import os
from flask import Flask, request, g
from flask import send_file, render_template
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.models import load_model
from number_of_islands import Graph
#import matplotlib.pyplot as plt
#plt.use('Agg')

app = Flask(__name__, instance_relative_config=True)



# Preload our model
print("Loading model")
model = load_model('UNET_model_400400_bu4.h5', compile=False)
graph = tf.get_default_graph()

def ml_predict(image):
    with graph.as_default():
        # Add a dimension for the batch
        prediction = model.predict(image[None, :, :, :])
    prediction = prediction.reshape((400,400, -1))
    return prediction



@app.route('/')
def home():
	return render_template('index.html')


THRESHOLD = 0.5
img_rows, img_cols = 400, 400

@app.route('/predict', methods=['POST'])
def predict():
    # Load image
    image = request.files['file']
    image = Image.open(image)
    img = np.array(image).astype('float32')

    # crop only to relevant pixels
    img = img[:img_rows, :img_cols]

    res = model.predict(img.reshape(1, img_rows, img_cols, 1))
    g = Graph(img_rows, img_cols, res.reshape(img_rows, img_cols))


    # Append transparency 4th channel to the 3 RGB image channels.
    print('image array: ', np.array(image).shape)
    print('result array: ', res.shape)
    # plt.figure()
    # plt.imshow(img)
    # plt.imshow(res.reshape(img_rows, img_cols), alpha=0.6)
    #
    # byte_io = io.BytesIO()
    #
    # plt.savefig(byte_io)
    # byte_io.seek(0)
    # return send_file(byte_io, mimetype='image/png')
    app_result = {'roofs': str(g.countIslands())}
    print(str(g.countIslands()))
    return render_template('result.html', roofs=app_result['roofs'])
    # transparent_image = np.append(np.array(image), res.reshape(400, 400)*255., axis=-1)
    # transparent_image = Image.fromarray(transparent_image)
    # transparent_image = transparent_image.convert('RGB')


    # Send back the result image to the client
    # byte_io = io.BytesIO()
    # transparent_image.save(byte_io, 'PNG')
    # byte_io.seek(0)
    # return send_file(byte_io, mimetype='image/png')

# @app.route('/')
# def homepage():
#     return render_template('index.html')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
