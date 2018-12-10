from flask import Flask, request
from flask import send_file, render_template
import os
import numpy as np
from tensorflow.python.keras.models import load_model
from scipy import ndimage
from utils import tifgenerator, output_showcase
import gdal
from PIL import Image

app = Flask(__name__, instance_relative_config=True)


@app.route('/')
def home():
    return render_template('index.html')


# need to take raster as input
# metadata from raster
@app.route('/predict', methods=['POST'])
def predict():

    print('loading model...')
    model_type = request.form['model_type']
    if model_type == 'vam':
        model = model_vam
    elif model_type == 'spacenet_vam':
        model = model_spacenet_vam


    print('loading file...')
    # inputs
    file = request.files['file']

    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    file.save(os.path.join('tmp', 'input_raster'))

    src = gdal.Open(os.path.join('tmp', 'input_raster'))  #src = gdal.Open('../roof_detex/VAM_data/rasters/bawargana_26apr2017_comp_crop.tif')

    img = src.ReadAsArray().astype('uint8').swapaxes(0,2).swapaxes(0,1)
    rs_height, rs_width = img.shape[0], img.shape[1]
    image = Image.fromarray(img)#, mode='RGB')

    # crop, score and compose
    # crop image, score and create output
    height, width = 256, 256

    im_list = []  # the crops will go here
    huts_list = []  # the huts for each image go here
    composite = np.zeros((rs_height, rs_width))  # the result from each crop will be stored here.
    print(rs_height, rs_width)
    for i in range(rs_height // height):
        for j in range(rs_width // width):
            print('scoring crop...')
            box = (j * width, i * height, (j + 1) * width, (i + 1) * height)  # find box coordinates
            im_crop = image.crop(box)  # crop images
            im_list.append(im_crop)  # append to the list of images to be scored

            im_crop = np.array(im_crop).astype('float32')  # convert from PIL to array
            res = model.predict((im_crop / 255.).reshape(1, im_crop.shape[0], im_crop.shape[1], 3))

            blobs, number_of_blobs = ndimage.measurements.label(
                ndimage.binary_fill_holes(res.reshape(im_crop.shape[0], im_crop.shape[1]).astype(int)))
            huts_list.append(number_of_blobs)

            # add to tiled
            tg_shape = composite[i * height:(i + 1) * height, j * width:(j + 1) * width].shape
            composite[i * height:(i + 1) * height, j * width:(j + 1) * width] = \
                res[:, :tg_shape[0], :tg_shape[1], :].reshape(tg_shape[0], tg_shape[1])

    print('Number of blobls:', np.sum(huts_list))

    # prepare raster
    outfile = 'tmp/output.tif'
    tifgenerator(outfile=outfile, raster=src, array=composite)

    if request.form["action"] == "download":
        print('sending file to client.')
        return send_file(outfile,
                         mimetype='image/tiff',
                         as_attachment=True,
                         attachment_filename="predictions.tif")

    elif request.form["action"] == "preview":
        print('loading preview...')
        return output_showcase(img, composite, img.shape[0], img.shape[1], sum(huts_list))


if __name__ == '__main__':

    # Preload our model
    print(("* Loading Keras model and Flask starting server..."
            "please wait until server has fully started"))

    model_vam = load_model('model/model_vam.h5', compile=False)
    model_spacenet_vam = load_model('model/model_spacenet_VAM.h5', compile=False)

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)