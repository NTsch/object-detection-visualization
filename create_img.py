import os
from PIL import Image, ImageDraw, ImageFont

# Function to parse the bounding box data from a text file
def parse_bbox_file(bbox_file_path):
    bounding_boxes = []
    with open(bbox_file_path, 'r') as file:
        for line in file:
            values = line.strip().split()
            if len(values) == 5:
                class_id, center_x, center_y, width, height = map(float, values)
                bounding_boxes.append((class_id, center_x, center_y, width, height))
    return bounding_boxes

# Function to load class names from the "classes.txt" file
def load_class_names(class_file_path):
    class_names = []
    with open(class_file_path, 'r') as file:
        for line in file:
            class_names.append(line.strip())
    return class_names

# Function to assign unique colors to class IDs
def assign_colors_to_classes(class_names):
    colors = []
    for i in range(len(class_names)):
        # Generate a unique color for each class
        hue = i / len(class_names)
        rgb = [int(255 * c) for c in colorsys.hsv_to_rgb(hue, 1, 1)]
        colors.append(tuple(rgb))
    return colors

# Function to superimpose bounding boxes on an image with class names
def superimpose_bounding_boxes(image_path, bounding_boxes, class_names, colors, output_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    for box in bounding_boxes:
        class_id, center_x, center_y, width, height = box
        image_width, image_height = image.size
        x_min = int((center_x - width / 2) * image_width)
        y_min = int((center_y - height / 2) * image_height)
        x_max = int((center_x + width / 2) * image_width)
        y_max = int((center_y + height / 2) * image_height)

        # Draw bounding box
        draw.rectangle([x_min, y_min, x_max, y_max], outline=colors[int(class_id)], width=5)

        # Display class name
        # class_name = class_names[int(class_id)]
        # text_width, text_height = draw.textsize(class_name, font)
        # draw.rectangle([x_min, y_min, x_min + text_width + 4, y_min + text_height], fill=colors[int(class_id)])
        # draw.text((x_min + 2, y_min), class_name, fill="white", font=font)

    image.save(output_path)

import colorsys

# Input folders
image_folder = 'static/ground_truth'
annotation_folder = 'static/annotations'

# Output folder for annotated images
output_folder = 'static/annotated_ground_truth'

# Path to the "classes.txt" file
class_file_path = 'static/classes.txt'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load class names and assign colors
class_names = load_class_names(class_file_path)
colors = assign_colors_to_classes(class_names)

# Loop through all JPG images in the ground_truth folder
for image_filename in os.listdir(image_folder):
    if image_filename.endswith('.jpg'):
        image_path = os.path.join(image_folder, image_filename)
        annotation_filename = os.path.splitext(image_filename)[0] + '.txt'
        annotation_path = os.path.join(annotation_folder, annotation_filename)
        output_path = os.path.join(output_folder, image_filename)

        # Parse bounding box data
        bounding_boxes = parse_bbox_file(annotation_path)

        # Superimpose bounding boxes with class names and save the result
        superimpose_bounding_boxes(image_path, bounding_boxes, class_names, colors, output_path)

print("Processing complete. Annotated images are saved in the 'static/annotated_images' folder.")

