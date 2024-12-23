import cv2
import numpy as np
import sys
import os

symbols_list = ["#", "-", "*", ".", "+", "o"]
threshold_list = np.linspace(0, 255, len(symbols_list) + 1)[:-1]  # 动态生成阈值

def print_out_ascii(array, output_file=None):
    """Prints or saves the coded image with symbols"""
    ascii_art = []
    for row in array:
        ascii_row = "".join(symbols_list[int(e) % len(symbols_list)] for e in row)
        ascii_art.append(ascii_row)

    if output_file:
        with open(output_file, 'w') as f:
            f.write("\n".join(ascii_art))
        print(f"ASCII art saved to {output_file}")
    else:
        for line in ascii_art:
            print(line)

def img_to_ascii(image, scale_width=20, scale_height=40):
    """Returns the numeric coded image"""
    height, width = image.shape
    new_width = max(1, int(width / scale_width))  # 防止宽度为 0
    new_height = max(1, int(height / scale_height))  # 防止高度为 0

    resized_image = cv2.resize(image, (new_width, new_height))
    thresh_image = np.zeros(resized_image.shape)

    for i, threshold in enumerate(threshold_list):
        thresh_image[resized_image > threshold] = i
    return thresh_image

if __name__ == "__main__":
    # Step 1: 提示用户输入图片路径
    if len(sys.argv) < 2:
        print("No image path provided.")
        image_path = input("Please enter the path to the image file (or press Enter to use 'sample_image.png'): ").strip()
        if not image_path:
            image_path = "sample_image.png"  # Default image path
    else:
        image_path = sys.argv[1]

    # Step 2: 验证图片路径是否存在
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' does not exist.")
        sys.exit(1)

    # Step 3: 尝试加载图片
    try:
        image = cv2.imread(image_path, 0)  # Load image in grayscale
        if image is None:
            raise FileNotFoundError(f"Unable to load image at {image_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Step 4: 转换图片为 ASCII 艺术
    ascii_art = img_to_ascii(image)

    # Step 5: 输出结果到文件或屏幕
    output_file = "ascii_art.txt"
    print_out_ascii(ascii_art, output_file=output_file)

    print(f"ASCII art has been saved to '{output_file}'.")
