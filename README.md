# Roof Detector App

### What is this?
This is an simple web application that can be used to count structures in IDP or refugees camps from very high resolution satellite images. 
It:
- allows a user to load a 3-band raster in a web UI;
- crops the raster into smaller tiles;
- scores each tile;
- composes the results as the original ratser;
- download the results or view in-browser.

The model used to detect the huts from the image is a CNN trained [here](https://github.com/WFP-VAM/roof_detex).

### How to use
You can pull from Docker Hub:
```
docker pull lriches/roof_detex_app
```

and run:
```buildoutcfg
docker run -t -p 5000:5000 roof_detex
```

Navigate to `localhost:5000` to find the UI.
