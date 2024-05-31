import numpy as np
from PIL import Image

def bcps_encode(image_path, secret_message, output_path):
    img = Image.open(image_path)
    width, height = img.size

    # Convert the secret message to binary
    secret_message_binary = ''.join(format(ord(char), '08b') for char in secret_message)

    img_gray = img.convert('L')
    img_array = np.array(img_gray)

    # Extract the bit planes
    bit_planes = [np.bitwise_and(img_array, 2**i) for i in range(8)]

    # Calculate complexities
    complexities = [np.mean(np.abs(np.diff(plane.astype(np.int16)))) for plane in bit_planes]
    threshold = sum(complexities) / len(complexities)

    # Find the bit plane to encode
    complex_planes = [i for i, complexity in enumerate(complexities) if complexity > threshold]
    if not complex_planes:
        raise ValueError("No suitable bit plane found for encoding.")
    bit_plane_to_encode = complex_planes[0]

    # Flatten the bit plane to encode the message
    plane = bit_planes[bit_plane_to_encode]
    flat_plane = plane.flatten()

    # Embed the secret message into the bit plane
    message_index = 0
    for i in range(len(flat_plane)):
        if message_index >= len(secret_message_binary):
            break
        flat_plane[i] = (flat_plane[i] & ~1) | int(secret_message_binary[message_index])
        message_index += 1

    # Reshape the bit plane back and update the bit planes
    bit_planes[bit_plane_to_encode] = flat_plane.reshape(plane.shape)

    # Combine the bit planes to form the encoded image array
    encoded_img_array = np.zeros_like(img_array)
    for i in range(8):
        encoded_img_array += bit_planes[i] * (2 ** i)

    # Save the encoded image
    encoded_img = Image.fromarray(encoded_img_array.astype('uint8'))
    encoded_img.save(output_path)

### Corrected Decoding Function

def bcps_decode(image_path):
    encoded_img = Image.open(image_path)
    encoded_img_array = np.array(encoded_img)

    # Extract the bit planes
    bit_planes = [np.bitwise_and(encoded_img_array, 2**i) for i in range(8)]

    # Calculate complexities
    complexities = [np.mean(np.abs(np.diff(plane.astype(np.int16)))) for plane in bit_planes]
    threshold = sum(complexities) / len(complexities)

    # Identify the bit plane used for encoding
    complex_planes = [i for i, complexity in enumerate(complexities) if complexity > threshold]
    if not complex_planes:
        raise ValueError("No suitable bit plane found for decoding.")
    bit_plane_to_decode = complex_planes[0]

    # Flatten the bit plane for decoding
    plane = bit_planes[bit_plane_to_decode]
    flat_plane = plane.flatten()

    # Extract the secret message bits
    secret_bits = [str(flat_plane[i] & 1) for i in range(len(flat_plane))]

    # Convert bits to characters
    secret_message_binary = ''.join(secret_bits)
    secret_message_chars = [secret_message_binary[i:i+8] for i in range(0, len(secret_message_binary), 8)]

    # Stop at the delimiter and construct the message
    secret_message = ''
    for char in secret_message_chars:
        if char == '11111110':  # Delimiter
            break
        secret_message += chr(int(char, 2))

    return secret_message

# Usage example
image_path = '/content/drive/MyDrive/Colab Notebooks/testing.jpg'
secret_message = 'H'
output_path = "/content/drive/MyDrive/Colab Notebooks/testingaziz15.jpg"
bcps_encode(image_path, secret_message, output_path)
decoded_message = bcps_decode(output_path)
print(decoded_message)
