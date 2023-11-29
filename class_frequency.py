import os
import yaml
import matplotlib.pyplot as plt
import numpy as np

def parse_labels(folder_path, class_mapping):
    class_counts = {class_name: 0 for class_name in class_mapping.values()}
    total_labels = 0
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            total_labels += 1
            with open(os.path.join(folder_path, filename), 'r') as file:
                lines = file.readlines()
                for line in lines:
                    class_label = line.split()[0]
                    class_name = class_mapping.get(int(class_label), 'Unknown')
                    class_counts[class_name] += 1

    # Normalize frequencies by dividing by the total number of label files
    class_counts_normalized = {class_name: count / total_labels for class_name, count in class_counts.items()}
    return class_counts_normalized

def plot_bar_chart(class_counts, title, output_filename=None):
    classes, counts = zip(*class_counts.items())
    x = np.arange(len(classes))

    plt.bar(x, counts, align='center')
    plt.xticks(x, classes, rotation=45, ha='right')  # Rotate class names for better visibility
    plt.xlabel('Class')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.gcf().subplots_adjust(bottom=0.25)
    # Save the plot if output_filename is provided
    if output_filename:
        plt.savefig(output_filename)

    plt.show()

# Load class mapping from YAML file
with open("labels/data.yaml", 'r') as yaml_file:
    class_mapping = yaml.safe_load(yaml_file)['names']

folder1_path = "labels/noe_gt_full"
folder2_path = "labels/fr_pred"

class_counts_folder1 = parse_labels(folder1_path, class_mapping)
class_counts_folder2 = parse_labels(folder2_path, class_mapping)

plot_bar_chart(class_counts_folder1, 'Class Frequency per Charter in 500 Lower Austrian Charters', 'no_plot.png')
plot_bar_chart(class_counts_folder2, 'Class Frequency per Charter in 300 French Charters', 'fr_plot.png')
