

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