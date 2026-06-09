import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def plot_fourier_transform(image_path: str) -> None:
    # 1. Load the image and convert to grayscale ('L')
    try:
        image = Image.open(image_path).convert('L') # L = R * 0.299 + G * 0.587 + B * 0.114
    except Exception as e:
        print(f"Error loading image by PIL: {e}")
        return
    
    image_array = np.array(image)
    # 2. Compute the 2D Fourier Transform
    fourier_transform = np.fft.fft2(image_array) # We receive an array of complex numbers

    # 3. Shift the zero-frequency component to the center
    fourier_shifted = np.fft.fftshift(fourier_transform) # Shift the zero-frequency component to the center of the spectrum for better display

    # 4. Compute the magnitude spectrum using logarithmic scaling (amplitude differences are too large to display directly)
    magnitude_spectrum = 20 * np.log(np.abs(fourier_shifted) + 1)  # Adding 1 to avoid log(0)

    # 5. Display via Matplotlib
    plt.figure(figsize=(12, 6))

    # Original image
    plt.subplot(1, 2, 1)
    plt.imshow(image_array, cmap='gray')
    plt.title('Original Image (Grayscale)')
    plt.axis('off')

    # Magnitude spectrum
    plt.subplot(1, 2, 2)
    plt.imshow(magnitude_spectrum, cmap='gray')
    plt.title('Magnitude Spectrum (Log Scale)')
    plt.axis('off')

    plt.tight_layout()
    plt.show()
