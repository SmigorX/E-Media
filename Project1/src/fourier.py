import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def plot_fourier_transform(image_path: str, save_path: str | None = None) -> None:
    try:
        image = Image.open(image_path).convert('L')
    except Exception as e:
        print(f"Error loading image by PIL: {e}")
        return

    image_array = np.array(image)
    fourier_transform = np.fft.fft2(image_array)

    fourier_shifted = np.fft.fftshift(fourier_transform)

    magnitude_spectrum = 20 * np.log(np.abs(fourier_shifted) + 1)

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(image_array, cmap='gray')
    plt.title('Original Image (Grayscale)')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(magnitude_spectrum, cmap='gray')
    plt.title('Magnitude Spectrum (Log Scale)')
    plt.axis('off')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        print(f"  Fourier transform saved to: {save_path}")
        plt.close()
    else:
        plt.show()
