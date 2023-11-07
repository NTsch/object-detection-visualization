import create_img
import os
import subprocess
from flask import Flask, render_template

app = Flask(__name__)

# Function to get the list of image filenames in a directory
def get_image_filenames(directory):
    image_filenames = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_filenames.append(filename)
    return image_filenames
    
if not os.path.exists('static/annotated_ground_truth') or not os.listdir('static/annotated_ground_truth'):
    create_img.create_annotated_ground_truth()

@app.route('/')
def display_images():
    annotated_images = get_image_filenames('static/annotated_ground_truth')
    prediction_images = get_image_filenames('static/predictions')

    # Pair each annotated image with a prediction image of the same name
    image_pairs = [(annotated, prediction) for annotated in annotated_images for prediction in prediction_images if annotated == prediction]

    return render_template('index.html', image_pairs=image_pairs)

if __name__ == '__main__':
    app.run(debug=True)