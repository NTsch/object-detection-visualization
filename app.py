from flask import Flask, render_template
import os

app = Flask(__name__)

# Define the path to your annotation files
annotation_dir = 'static/annotations'  # Update this path to the directory containing your annotation files
image_dir = 'static/ground_truth'  # Path to the ground truth images
class_names = open('static/classes.txt').read().splitlines()

def read_annotations(image_filename):
    annotation_file = os.path.join(annotation_dir, os.path.splitext(image_filename)[0] + '.txt')
    
    if os.path.exists(annotation_file):
        with open(annotation_file, 'r') as f:
            lines = f.read().splitlines()
        annotations = [list(map(float, line.split())) for line in lines]
    else:
        annotations = []

    return annotations

ground_truth_data = []

for image_filename in os.listdir(image_dir):
    if image_filename.endswith('.jpg'):
        annotations = read_annotations(image_filename)
        ground_truth_data.append({'image': image_filename, 'annotations': annotations})

@app.route('/')
def index():
    return render_template('index.html', ground_truth_data=ground_truth_data, class_names=class_names)

if __name__ == '__main__':
    app.run(debug=True)
