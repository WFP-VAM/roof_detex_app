import os
from flask import Flask, request
from flask import send_file, render_template
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.models import load_model
from number_of_islands import Graph
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import io
app = Flask(__name__, instance_relative_config=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    # Load image
    params = request.form

    img_rows, img_cols = int(params['row pixels']), int(params['column pixels'])

    image = request.files['file']
    image = Image.open(image)

    img = np.array(image).astype('float32')

    res = model.predict(img.reshape(1, img_rows, img_cols, 3))
    g = Graph(img_rows, img_cols, res.reshape(img_rows, img_cols))

    # generate image with result
    fig = plt.figure(figsize=(5, 5), dpi=300)
    ax = fig.add_subplot(111)
    ax.imshow(img.astype('uint8'))
    ax.imshow(res.reshape(img_rows, img_cols)*100, alpha=0.3, cmap='gray')
    ax.set_title('huts detected: {}'.format(g.countIslands()))

    output = io.BytesIO()
    plt.savefig(output, dpi=fig.dpi)
    output.seek(0)

    return send_file(output, mimetype='image/png')


if __name__ == '__main__':

    # Preload our model
    print(("* Loading Keras model and Flask starting server..."
            "please wait until server has fully started"))

    model = load_model('model_ft2.h5', compile=False)
    graph = tf.get_default_graph()

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
