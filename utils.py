def output_showcase(img, res, img_rows, img_cols, islands):
    # generate image with result
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from io import BytesIO
    from flask import send_file
    fig = plt.figure(figsize=(5, 5), dpi=300)
    ax = fig.add_subplot(111)
    ax.imshow(img.astype('uint8'))
    ax.imshow(res.reshape(img_rows, img_cols) * 100, alpha=0.3, cmap='gray')
    ax.set_title('huts detected: {}'.format(islands))

    output = BytesIO()
    plt.savefig(output, dpi=fig.dpi)
    output.seek(0)

    return send_file(output, mimetype='image/png')


def tifgenerator(outfile, raster, array):

    import gdal

    print('-> writing: ', outfile)
    # create empty raster from the original one

    band = raster.GetRasterBand(1)
    arr = band.ReadAsArray()
    [cols, rows] = arr.shape

    output_raster = gdal.GetDriverByName('GTiff').Create(outfile, rows, cols, 1,
                                                         gdal.GDT_Float32)  # Open the file
    output_raster.SetGeoTransform(raster.GetGeoTransform())  # Specify its coordinates
    output_raster.SetProjection(raster.GetProjection())

    output_raster.GetRasterBand(1).SetNoDataValue(-99)

    print(array.shape)

    output_raster.GetRasterBand(1).WriteArray(array)  # Writes my array to the raster

    output_raster.FlushCache()  # saves to disk!!