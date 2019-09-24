# Map-to-ASCII

Generates ASCII maps from regular Google (or any other provider) maps. Just run `py main.py -d` and see the result by yourself.

### Arguments:
  * `-d` / `--debug`: displays the different images
  * `-p` / `--path`: path to the image (default: `test.png`)
  * `-x` / `--width`: Width of the final image (default: `100`)
  * `-y` / `--height`: Height of the final image (dafault: `100`)

### Libraries used:
  * OpenCV
  * Numpy
  * libtcod (ASCII display)


### TODO:
  * Query maps API to get the image
  * Other characters than # for the ASCII map
