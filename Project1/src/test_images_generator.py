import numpy as np
from PIL import Image

def generate_stripes():
    size = 256
    stripe_size = 16

    image_vertical = np.zeros((size, size), dtype=np.uint8)
    for i in range(0, size, stripe_size * 2):
        image_vertical[i:i+stripe_size, :] = 255

    Image.fromarray(image_vertical).save('stripes_vertical.png')

    image_horizontal = np.zeros((size, size), dtype=np.uint8)
    for i in range(0, size, stripe_size * 2):
        image_horizontal[:, i:i+stripe_size] = 255

    Image.fromarray(image_horizontal).save('stripes_horizontal.png')