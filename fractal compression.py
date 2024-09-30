from PIL import Image
import numpy as np


# Function to break image into smaller blocks
def split_image(image, block_size):
    width, height = image.size
    blocks = []
    for i in range(0, width, block_size):
        for j in range(0, height, block_size):
            block = image.crop((i, j, i + block_size, j + block_size))
            blocks.append(block)
    return blocks


# Function to compare two blocks and calculate similarity (using Mean Squared Error)
def compare_blocks(block1, block2):
    arr1 = np.array(block1).astype(np.float32)
    arr2 = np.array(block2).astype(np.float32)
    return np.mean((arr1 - arr2) ** 2)


# Function to compress the image using fractal similarity
def fractal_compress(image, block_size=8, tolerance=100):
    blocks = split_image(image, block_size)
    compressed = []

    # For each block, find a similar block and store transformation instead
    for i in range(len(blocks)):
        current_block = blocks[i]
        for j in range(i + 1, len(blocks)):
            similar_block = blocks[j]
            if compare_blocks(current_block, similar_block) < tolerance:
                compressed.append((j, 'repeat'))  # Store index of similar block
                break
        else:
            compressed.append((i, current_block))  # Store original block if no match found

    return compressed


# Function to reconstruct the image from compressed data
def fractal_decompress(compressed, block_size, image_size):
    width, height = image_size
    decompressed_image = Image.new('RGB', (width, height))

    for i, data in enumerate(compressed):
        x = (i % (width // block_size)) * block_size
        y = (i // (width // block_size)) * block_size

        if data[1] == 'repeat':
            ref_block_index = data[0]
            decompressed_image.paste(decompressed_image.crop(
                ((ref_block_index % (width // block_size)) * block_size,
                 (ref_block_index // (width // block_size)) * block_size,
                 (ref_block_index % (width // block_size)) * block_size + block_size,
                 (ref_block_index // (width // block_size)) * block_size + block_size)),
                (x, y)
            )
        else:
            decompressed_image.paste(data[1], (x, y))

    return decompressed_image


# Example usage:
image = Image.open('glacier.jpg').convert('RGB')  # Load your image (glacier example)
# Adjusting the block size and tolerance for better results
compressed_data = fractal_compress(image, block_size=4, tolerance=50)  # Smaller block size and higher tolerance
reconstructed_image = fractal_decompress(compressed_data, block_size=4, image_size=image.size)

# Save or show the reconstructed image
reconstructed_image.save('improved_reconstructed_glacier.jpg')
reconstructed_image.show()

