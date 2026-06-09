from src.loader import load_png_image
from src.ihdr import read_IHDR_chunk, print_IHDR_info
from src.chunks import read_all_chunks, print_all_chunks
from src.fourier import plot_fourier_transform
from src.test_images_generator import generate_stripes

def main():

    # Test for the successful Fourier Transform
    #generate_stripes()
    #plot_fourier_transform('./stripes_vertical.png')
    #plot_fourier_transform('./stripes_horizontal.png')

    image_path = './test.png'  
    image_bytes = load_png_image(image_path)

    ihdr_info = read_IHDR_chunk(image_bytes)
    print_IHDR_info(ihdr_info)

    chunks = read_all_chunks(image_bytes)
    print_all_chunks(chunks)

    plot_fourier_transform(image_path)

if __name__ == "__main__":
    main()