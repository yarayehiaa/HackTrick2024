import cv2
import numpy as np

def rotate_image(image, angle):
    # Rotate the image by the specified angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def remove_patch(test_case:tuple) -> list:
    
    combined_image_array , patch_image_array = test_case
    combined_image = np.array(combined_image_array,dtype=np.uint8)
    patch_image = np.array(patch_image_array,dtype=np.uint8)

    # Convert images to grayscale
    base_gray = cv2.cvtColor(combined_image_array, cv2.COLOR_BGR2GRAY)
    patch_gray = cv2.cvtColor(patch_image_array, cv2.COLOR_BGR2GRAY)

    # Initialize variables to store the best match parameters
    best_match_loc = None
    best_match_angle = 0
    best_match_scale = 1
    best_match_score = -np.inf
    angles = [0, 90, 180, 270]

    # Loop through different scales
    for scale in np.linspace(0.1, 2.00, 150):
        scaled_patch = cv2.resize(patch_gray, None, fx=scale, fy=scale)

        # Loop through different angles (0 to 270 degrees)
        for angle in angles:
            rotated_patch = rotate_image(scaled_patch, angle)

            # Check if rotated patch dimensions exceed base image dimensions
            if rotated_patch.shape[0] > base_gray.shape[0] or rotated_patch.shape[1] > base_gray.shape[1]:
                break

            # Find the match between base image and rotated patch
            result = cv2.matchTemplate(base_gray, rotated_patch, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            # Update best match if the current match has a higher score
            if max_val > best_match_score:
                best_match_loc = max_loc
                best_match_angle = angle
                best_match_scale = scale
                best_match_score = max_val

    # Extract patch dimensions
    patch_height, patch_width = patch_gray.shape

    # Set a confidence threshold
    confidence_threshold = 0.6

    # Create a mask to remove the patch if confidence is high enough
    mask = np.zeros_like(base_gray)
    if best_match_score > confidence_threshold:
        scaled_patch = cv2.resize(patch_gray, None, fx=best_match_scale+0.1, fy=best_match_scale+0.1)
        rotated_patch = rotate_image(scaled_patch, best_match_angle)
        mask[best_match_loc[1]:best_match_loc[1]+rotated_patch.shape[0], 
             best_match_loc[0]:best_match_loc[0]+rotated_patch.shape[1]] = 255

    # Remove the patch from the base image using the mask
    base_image_removed = cv2.inpaint(base_image, mask.astype(np.uint8), inpaintRadius=3, flags=cv2.INPAINT_TELEA)

    return base_image_removed