import cv2

input_path = "Project/Resources/human.jpg" 
output_path = "Project/Resources/human_hd.jpg"
image = cv2.imread(input_path)


hd_width = 1280
hd_height = 720


resized_image = cv2.resize(image, (hd_width, hd_height))


cv2.imwrite(output_path, resized_image)

print(f"Resized image saved as {output_path}")
