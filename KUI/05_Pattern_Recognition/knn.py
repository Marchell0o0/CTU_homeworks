import argparse
from PIL import Image
import numpy as np
import os
import csv


def setup_arg_parser():
    parser = argparse.ArgumentParser(description='Learn and classify image data.')
    parser.add_argument('train_path', type=str, help='path to the training data directory')
    parser.add_argument('test_path', type=str, help='path to the testing data directory')
    parser.add_argument('-k', type=int, 
                        help='run k-NN classifier (if k is 0 the code may decide about proper K by itself')
    parser.add_argument("-o", metavar='filepath', 
                        default='classification.dsv',
                        help="path (including the filename) of the output .dsv file with the results")
    return parser

def euclidean_distance(a, b):
    return np.sqrt(np.sum(np.square(a - b)))

def get_image_vectors_from_folder(folder):
    image_vectors = np.array()
    for filename in os.listdir(folder):
        if filename.endswith('.png'):
            image_vector = np.array(Image.open(os.path.join(folder, filename))).astype(int).flatten()
            np.append(images, image_vector)
    return image_vectors


def main():
    parser = setup_arg_parser()
    args = parser.parse_args()
    
    print('Training data directory:', args.train_path)
    print('Testing data directory:', args.test_path)
    print('Output file:', args.o)
    
    print(f"Running k-NN classifier with k={args.k}")

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

    output_dict = {}

    # Load test images and perform k-NN classification
    for fname in os.listdir(args.test_path):
        path = os.path.join(args.test_path, fname)
        if "png" in fname:
            image_vector = np.array(Image.open(path)).astype(int).flatten()
            distances = [(euclidean_distance(image_vector, train_vector), train_label)
                         for train_vector, train_label in training_data]
            distances.sort()  # sorts in ascending order of distance
            neighbors = distances[:args.k]  # get k nearest neighbors
            labels = [label for _, label in neighbors]
            output_dict[fname] = max(set(labels), key=labels.count)  # store majority class in dictionary

    # Write the classification results to the output file
    with open(args.o, 'w') as f:
        for key in output_dict.keys():
            f.write("%s:%s\n"%(key, output_dict[key]))
        
        
if __name__ == "__main__":
    main()
    
