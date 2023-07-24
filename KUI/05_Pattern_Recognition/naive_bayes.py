import argparse
from PIL import Image
import numpy as np
import os
import csv
import math

def setup_arg_parser():
    parser = argparse.ArgumentParser(description='Learn and classify image data.')
    parser.add_argument('train_path', type=str, help='path to the training data directory')
    parser.add_argument('test_path', type=str, help='path to the testing data directory')
    parser.add_argument("-o", metavar='filepath', 
                        default='classification.dsv',
                        help="path (including the filename) of the output .dsv file with the results")
    return parser


def main():
    parser = setup_arg_parser()
    args = parser.parse_args()
    
    print('Training data directory:', args.train_path)
    print('Testing data directory:', args.test_path)
    print('Output file:', args.o)
    print("Running Naive Bayes classifier")
    
    training_data = []
    training_answers = {}

    # Load the training answers from the dsv file
    for fname in os.listdir(args.train_path):
        if fname.endswith('.dsv'):
            path = os.path.join(args.train_path, fname)
            with open(path, mode='r') as inp:
                reader = csv.reader(inp, delimiter=':')
                training_answers = {rows[0]:rows[1] for rows in reader}

    # Load the training images and associate them with their labels
    for fname in os.listdir(args.train_path):
        if fname.endswith('.png'):
            path = os.path.join(args.train_path, fname)
            image_vector = np.array(Image.open(path)).astype(int).flatten()
            training_data.append((image_vector, training_answers[fname]))

    class_counts = {}
    feature_counts = {}

    for image_vector, label in training_data:
        # Count the occurrences of each class
        class_counts[label] = class_counts.get(label, 0) + 1

        # Count the occurrences of each pixel value for each class
        for pixel_position, pixel_value in enumerate(image_vector):
            feature_counts[(label, pixel_position, pixel_value)] = feature_counts.get((label, pixel_position, pixel_value), 0) + 1

    total_instances = sum(class_counts.values())
    output_dict = {}

    # Load test images and perform Naive Bayes classification
    for fname in os.listdir(args.test_path):
        path = os.path.join(args.test_path, fname)
        if fname.endswith('.png'):
            image_vector = np.array(Image.open(path)).astype(int).flatten()

            max_log_prob = float('-inf')
            max_label = None

            # Calculate log probabilities for each class
            for label in class_counts.keys():
                log_prior = math.log(class_counts[label]) - math.log(total_instances)
                log_likelihood = 0
                for pixel_position, pixel_value in enumerate(image_vector):
                    log_likelihood += math.log(feature_counts.get((label, pixel_position, pixel_value), 0) + 1) / (class_counts[label] + len(image_vector))
                log_prob = log_prior + log_likelihood
                if log_prob > max_log_prob:
                    max_log_prob = log_prob
                    max_label = label

            output_dict[fname] = max_label

    # Write the classification results to the output file
    with open(args.o, 'w') as f:
        for key in output_dict.keys():
            f.write("%s:%s\n"%(key, output_dict[key]))
        
if __name__ == "__main__":
    main()
