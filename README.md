# roof_detex_app
deployed on Heroku: https://roof-detex-app.herokuapp.com/

This is the application that embeds the model trained [here](https://github.com/WFP-VAM/roof_detex) in a Flask webapp.

It accepts from the user a raster, crops it, scores each crop and recomposes the results as the original ratser for download. The automatically downloaded .tif with the results can be easily overlayed onto the original raster.
