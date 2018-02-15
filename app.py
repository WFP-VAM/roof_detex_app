import os
from flask import Flask, request
from flask import send_file, render_template
from PIL import Image
import numpy as np
from tensorflow.python.keras.models import load_model
from number_of_islands import Graph
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
app = Flask(__name__, instance_relative_config=True)


def output_showcase(img, res, img_rows, img_cols, islands):
    # generate image with result
    fig = plt.figure(figsize=(5, 5), dpi=300)
    ax = fig.add_subplot(111)
    ax.imshow(img.astype('uint8'))
    ax.imshow(res.reshape(img_rows, img_cols) * 100, alpha=0.3, cmap='gray')
    ax.set_title('huts detected: {}'.format(islands))

    output = io.BytesIO()
    plt.savefig(output, dpi=fig.dpi)
    output.seek(0)

    return send_file(output, mimetype='image/png')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.files['file'].filename == '':
        return 'No selected file'

    # Load image
    image = request.files['file']
    image = Image.open(image).convert('RGB')

    img = np.array(image).astype('float32')

    img_rows, img_cols = img.shape[0], img.shape[1]

    # crop image, score and create output
    height, width = 256, 256

    im_list = []  # the crops will go here
    huts_list = []  # the huts for each image go here
    composite = np.zeros((img_rows, img_cols)) # the result from each crop will be stored here.

    for i in range(img_rows // height):
        for j in range(img_cols // width):
            # print (i,j)
            box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
            im_crop = image.crop(box)
            im_list.append(im_crop)

            im_crop = np.array(im_crop).astype('float32')
            res = model.predict(im_crop.reshape(1, im_crop.shape[0], im_crop.shape[1], 3))

            g = Graph(height, width, res.reshape(im_crop.shape[0], im_crop.shape[1]))
            huts_list.append(g.countIslands())

            composite[j * width:(j + 1) * width, i * height:(i + 1) * height] = res.reshape(height, width)

    # generate image with result
    return output_showcase(img, composite, img_rows, img_cols, sum(huts_list))


if __name__ == '__main__':

    # Preload our model
    print(("* Loading Keras model and Flask starting server..."
            "please wait until server has fully started"))

    model = load_model('model.h5', compile=False)

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
