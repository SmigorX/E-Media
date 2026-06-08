from src.loader import load_png_image
from src.ihdr import read_IHDR_chunk, print_IHDR_info

def main():
    image_path = './test.png'  
    image_bytes = load_png_image(image_path)

    ihdr_info = read_IHDR_chunk(image_bytes)
    print_IHDR_info(ihdr_info)

if __name__ == "__main__":
    main()