# import cv2
# import numpy as np

# # Load the image
# chicken_img = cv2.imread('suspicious_chicken.png')

# # Convert the image to grayscale
# gray_chicken = cv2.cvtColor(chicken_img, cv2.COLOR_BGR2GRAY)

# # Create a binary mask where white pixels are 255 and non-white pixels are 0
# _, binary_mask = cv2.threshold(gray_chicken, 254, 255, cv2.THRESH_BINARY)

# # Invert the mask so that non-white pixels are 255 and white pixels are 0
# inverted_mask = cv2.bitwise_not(binary_mask)

# # Convert the inverted mask back to 3-channel to match the original image
# inverted_mask_3ch = cv2.cvtColor(inverted_mask, cv2.COLOR_GRAY2BGR)

# # Use the mask to set non-white pixels to black in the original image
# result = cv2.bitwise_and(chicken_img, inverted_mask_3ch)

# # Save the result
# cv2.imwrite('chicken_image_nonwhite_to_black.png', result)

# # Display the result
# cv2.imshow('Result', result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2
import numpy as np

def overlay_images(base_image_path, overlay_image_path, x_offset, y_offset, output_path):
    # Load the base image
    base_image = cv2.imread(base_image_path)
    
    # Load the overlay image
    overlay_image = cv2.imread(overlay_image_path)
    
    # Get the dimensions of the overlay image
    h, w = overlay_image.shape[:2]
    
    # Define the region of interest (ROI) in the base image where the overlay will be placed
    roi = base_image[y_offset:y_offset+h, x_offset:x_offset+w]
    
    # Create a mask of the overlay image by converting to grayscale and then thresholding
    gray_overlay = cv2.cvtColor(overlay_image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_overlay, 1, 255, cv2.THRESH_BINARY)
    
    # Create the inverse mask
    mask_inv = cv2.bitwise_not(mask)
    
    # Black out the area of the base image that will be replaced by the overlay
    base_image_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    
    # Take only the region of the overlay image that has non-black pixels
    overlay_fg = cv2.bitwise_and(overlay_image, overlay_image, mask=mask)
    
    # Put the overlay image on the base image
    dst = cv2.add(base_image_bg, overlay_fg)
    
    # Put the result back into the original image
    base_image[y_offset:y_offset+h, x_offset:x_offset+w] = dst
    
    # Save the result
    cv2.imwrite(output_path, base_image)
    
    # Display the result
    cv2.imshow('Overlay Result', base_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def overlay_and_filter_red(base_image_path, overlay_image_path, x_offset, y_offset, output_path):

    # Load the base image

    base_image = cv2.imread(base_image_path)

    

    # Load the overlay image

    overlay_image = cv2.imread(overlay_image_path)

    

    # Get the dimensions of the overlay image

    h, w = overlay_image.shape[:2]

    

    # Define the region of interest (ROI) in the base image where the overlay will be placed

    roi = base_image[y_offset:y_offset+h, x_offset:x_offset+w]

    

    # Create a mask of the overlay image by converting to grayscale and then thresholding

    gray_overlay = cv2.cvtColor(overlay_image, cv2.COLOR_BGR2GRAY)

    _, mask = cv2.threshold(gray_overlay, 1, 255, cv2.THRESH_BINARY)

    

    # Create the inverse mask

    mask_inv = cv2.bitwise_not(mask)

    

    # Black out the area of the base image that will be replaced by the overlay

    base_image_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    

    # Take only the region of the overlay image that has non-black pixels

    overlay_fg = cv2.bitwise_and(overlay_image, overlay_image, mask=mask)

    

    # Put the overlay image on the base image

    dst = cv2.add(base_image_bg, overlay_fg)

    

    # Put the result back into the original image

    base_image[y_offset:y_offset+h, x_offset:x_offset+w] = dst

    

    # Convert the image to HSV color space

    hsv = cv2.cvtColor(base_image, cv2.COLOR_BGR2HSV)

    

    # Define range for red color in HSV

    lower_red_1 = np.array([0, 120, 70])

    upper_red_1 = np.array([10, 255, 255])

    lower_red_2 = np.array([170, 120, 70])

    upper_red_2 = np.array([180, 255, 255])

    

    # Create masks for red color

    mask_red_1 = cv2.inRange(hsv, lower_red_1, upper_red_1)

    mask_red_2 = cv2.inRange(hsv, lower_red_2, upper_red_2)

    mask_red = cv2.bitwise_or(mask_red_1, mask_red_2)

    

    # Invert the mask to keep non-red areas

    mask_non_red = cv2.bitwise_not(mask_red)

    

    # Convert the mask to 3-channel

    mask_non_red_3ch = cv2.cvtColor(mask_non_red, cv2.COLOR_GRAY2BGR)

    

    # Apply the mask to keep only non-red areas

    result = cv2.bitwise_and(base_image, mask_non_red_3ch)

    

    # Save the result

    cv2.imwrite(output_path, result)

    

    # Display the result

    cv2.imshow('Filtered Result', result)

    cv2.waitKey(0)

    cv2.destroyAllWindows()


# Example usage
base_image_path = 'suspicious_chicken.png'
overlay_image_path = 'treasure map.png'
x_offset = 0  # Adjust this to position the overlay horizontally
y_offset = 0  # Adjust this to position the overlay vertically
# output_path = 'overlay_result.png'
output_path = 'filtered_overlay_result.png'

# overlay_images(base_image_path, overlay_image_path, x_offset, y_offset, output_path)
overlay_and_filter_red(base_image_path, overlay_image_path, x_offset, y_offset, output_path)