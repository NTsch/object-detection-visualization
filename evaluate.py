import os

# evaluates True Positives, False Positives, and False Negatives by comparing ground truth labels and predicted labels
# requires 2 directories with gt labels and pred labels

def check_iou_class(box1, box2):
    # Calculate Intersection over Union (IoU) between two bounding boxes
    class1, x1, y1, w1, h1, conf = [float(x) for x in box1.split()]
    class2, x2, y2, w2, h2 = [float(x) for x in box2.split()]

    intersection_area = max(0, min(x1 + w1, x2 + w2) - max(x1, x2)) * max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
    union_area = w1 * h1 + w2 * h2 - intersection_area

    iou = intersection_area / (union_area + 1e-6)  # Adding a small epsilon to avoid division by zero
    same_class = class1 == class2
    return iou, same_class

def evaluate(pred_lines, gt_lines, iou_threshold=0.5, confidence_threshold=0.5):
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for pred_line in pred_lines:
        #class1, x1, y1, w1, h1, conf = [float(x) for x in pred_line.split()]
        match_found = False
        for gt_line in gt_lines:
            #class2, x2, y2, w2, h2 = [float(x) for x in gt_line.split()]
            iou, same_class = check_iou_class(pred_line, gt_line)
            if iou >= iou_threshold and same_class:
                match_found = True
                break
        if match_found:
            true_positives += 1
        else:
            false_positives += 1
    
    # Calculate false negatives
    false_negatives = len(gt_lines) - true_positives
    return [true_positives, false_positives, false_negatives]

def eval_all():
    # results_directory = "yolov5/runs/detect/exp6/labels/"
    # gt_directory = "yolov5_data_set/labels/test/"
    results_directory = "labels/pred"
    gt_directory = "labels/gt"
    all_results = []
    
    for result_file in os.listdir(results_directory):
        with open(os.path.join(results_directory, result_file), 'r') as file1:
            pred_lines = file1.readlines()
            with open(os.path.join(gt_directory, result_file), 'r') as file2:
                gt_lines = file2.readlines()
                result = evaluate(pred_lines, gt_lines)
                result.insert(0, result_file)
                all_results.append(result)
    
    return all_results 

#print(eval_all())