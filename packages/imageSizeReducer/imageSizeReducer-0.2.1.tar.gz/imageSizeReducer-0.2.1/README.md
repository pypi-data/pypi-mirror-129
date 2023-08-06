# Image Size Reducer

Image Size Reducer is a package created for reducing image size for fast uploading and processing.

## Steps

- Specify image path
- Specify quality 1-100
- Specify path where you want to save

## Installation

Image Size Reducer requires [python3](https://www.python.org/downloads/) to run.

```sh
pip install imageSizeReducer
```
## Usage

> Image Size Reducer

```python
from imageSizeReducer import imageSizeReducer

actualImage = "path/to/img.jpg"
pathToSave = "path/to/img.jpg"
quality=95

imageSizeReducer.resize(actualImage, quality, pathToSave)

# output - {'message': 'successfully completed image resize', 'actual-image-path': '/home/bramhesh/Downloads/20.jpg', 'quality-specified': 50, 'path-to-image': '/home/bramhesh/20.jpg'}
# output - {'message': 'image resize process failed', 'error': FileNotFoundError(2, 'No such file or directory'), 'actual-image-path': '/home/bramhesh/Downloads/2.jpg', 'quality-specified': 50, 'path-to-image': '/home/bramhesh/20.jpg'}
# output - {'message': 'image resize process failed', 'error': ValueError('unknown file extension: '), 'actual-image-path': '/home/bramhesh/Downloads/20.jpg', 'quality-specified': '/home/bramhesh/20.jpg', 'path-to-image': 50}
```
