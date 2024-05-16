


import numpy as np
from PIL import Image
from decimal import Decimal, getcontext

def bcps_encode(image_path, secret_message, output_path):

    img = Image.open(image_path)
    width, height = img.size
    secret_message_binary = ''.join(format(ord(char), '08b') for char in secret_message)
    img_gray = img.convert('L')
    img_array = np.array(img_gray)
    bit_planes = [np.bitwise_and(img_array, 2**i) for i in range(8)]
    complexities = [np.mean(np.abs(np.diff(plane))) for plane in bit_planes]
    threshold = sum(complexities) / len(complexities)
    encoded_bit_planes = []
    for i, plane in enumerate(bit_planes):
        if complexities[i] > threshold:
            encoded_plane = np.where(plane > 0, plane | 1, plane)
        else:
            encoded_plane = plane
        encoded_bit_planes.append(encoded_plane)
    encoded_img_array = sum(encoded_bit_planes)
    encoded_img = Image.fromarray(encoded_img_array.astype('uint8'))
    encoded_img.save(output_path)

def bcps_decode(image_path):

    encoded_img = Image.open(image_path)
    encoded_img_array = np.array(encoded_img)

    bit_planes = [np.bitwise_and(encoded_img_array, 2**i) for i in range(8)]

    complexities = [np.mean(np.abs(np.diff(plane))) for plane in bit_planes]

    threshold = sum(complexities) / len(complexities)

    extracted_bits = [plane & 1 for index, plane in enumerate(bit_planes) if complexities[index] > threshold]

    extracted_message_binary = ''
    for i in range(encoded_img_array.shape[0]):  
        for j in range(encoded_img_array.shape[1]):  
            extracted_bit = 0
            for plane in extracted_bits:
                extracted_bit |= plane[i, j]
            extracted_message_binary += str(extracted_bit)  
            if len(extracted_message_binary) % 8 == 0:
                break

   
    padding_length = 8 - (len(extracted_message_binary) % 8)
    extracted_message_binary += '0' * padding_length

  
    extracted_message = ''.join(chr(int(extracted_message_binary[i:i+8], 2)) for i in range(0, len(extracted_message_binary), 8))

    return extracted_message


image_path = '/content/drive/MyDrive/Colab Notebooks/testing.jpg'
secret_message = 'H'
output_path = "/content/drive/MyDrive/Colab Notebooks/testingaziz4.jpg"
encoded_image = bcps_encode(image_path, secret_message,output_path)
encoded_image_path = '/content/drive/MyDrive/Colab Notebooks/testingaziz4.jpg'
decoded_message = bcps_decode(encoded_image_path)
print(decoded_message)
