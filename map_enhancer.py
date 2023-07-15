import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_image(img, output_image_path,l):

    # Apply median filtering to reduce noise
    blurred_img = cv2.medianBlur(img,5)

    # Create a 1x1 kernel for morphological operations
    kernel = np.ones((l,l), np.uint8)

    # Perform erosion and dilation operations
    erosion = cv2.erode(blurred_img, kernel, iterations=1)
    output = cv2.dilate(erosion, kernel, iterations=1)

    # Apply median filtering to the output image
    blurred_output = cv2.medianBlur(output, 5)

    # Save the processed image
    cv2.imwrite(output_image_path, blurred_output)

    # Display the original and processed images
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(blurred_output, cv2.COLOR_BGR2RGB))
    plt.title('Processed Image')

    plt.show()
    return blurred_img
input_image_path = 'knn.png'
output_image_path = 'output.png'
img = cv2.imread(input_image_path)
# process_image(process_image(process_image(process_image(img, output_image_path,3), output_image_path,3), output_image_path,3), output_image_path,80)
process_image(img, 'output1.png',2)
process_image(cv2.imread('output1.png'), 'output2.png',15)
process_image(cv2.imread('output2.png'), 'output3.png',80)


plt.subplot(1, 2, 1)
plt.imshow(cv2.imread('output1.png'))
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(cv2.imread('output1.png'), cv2.COLOR_BGR2RGB))
plt.title('Processed Image')