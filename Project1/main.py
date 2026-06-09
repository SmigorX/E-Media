from src.loader import load_png_image
from src.ihdr import read_IHDR_chunk, print_IHDR_info
from src.idat import read_IDAT_chunks, print_IDAT_info
from src.plte import read_PLTE_chunks, print_PLTE_info
from src.iend import read_IEND_chunk, print_IEND_info
from src.chunks import read_all_chunks, print_all_chunks
from src.fourier import plot_fourier_transform
from src.test_images_generator import generate_stripes

def main():

    image_path = './test.png'  
    image_bytes = load_png_image(image_path)

    print("\n--- 1. Scanning file structure ---")
    chunks = read_all_chunks(image_bytes)
    print_all_chunks(chunks)

    print("\n--- 2. Validating IHDR chunk ---")
    ihdr_info = read_IHDR_chunk(image_bytes)
    print_IHDR_info(ihdr_info)

    print("\n--- 3. Analyzing IDAT chunks ---")
    idat_chunks = [chunk for chunk in chunks if chunk["type"] == "IDAT"]
    if idat_chunks:
        idat_info = read_IDAT_chunks(idat_chunks)
        print_IDAT_info(idat_info)
    else:
        print("  No IDAT chunks found in the PNG file.")

    print("\n--- 4. Analyzing PLTE chunks ---")
    plte_chunks = [chunk for chunk in chunks if chunk["type"] == "PLTE"]
    if plte_chunks:
        plte_info = read_PLTE_chunks(plte_chunks)
        print_PLTE_info(plte_info)
    else:
        print("  No PLTE chunks found in the PNG file.")

    print("\n--- 5. Validating IEND chunk ---")
    iend_valid = read_IEND_chunk(image_bytes, chunks[-1]["start_index"])
    print_IEND_info(iend_valid)
    
    print("\n--- 6. Fourier Transform Analysis ---")
    plot_fourier_transform(image_path)

    # Test for the successful Fourier Transform
    #generate_stripes()
    #plot_fourier_transform('./stripes_vertical.png')
    #plot_fourier_transform('./stripes_horizontal.png')


if __name__ == "__main__":
    main()