import cv2

# 画像を読み込む
input_path = "Project/Resources/human.jpg"  # 画像のパスを指定
output_path = "Project/Resources/human_hd.jpg"
image = cv2.imread(input_path)

# フルHDのサイズ
hd_width = 1280
hd_height = 720

# 画像をリサイズ
resized_image = cv2.resize(image, (hd_width, hd_height))

# リサイズ後の画像を保存
cv2.imwrite(output_path, resized_image)

print(f"Resized image saved as {output_path}")
