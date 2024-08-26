# generate_tfrecord.py

import argparse

def main(args):
    # Your existing code here
    # Example:
    # process_tfrecord(args.x, args.l, args.o)
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate TFRecord files.')
    parser.add_argument('-x', '--xml_dir', help='Path to the folder where the input .xml files are stored.', required=True)
    parser.add_argument('-l', '--labels_path', help='Path to the labels (.pbtxt) file.', required=True)
    parser.add_argument('-o', '--output_path', help='Path of output TFRecord (.record) file.', required=True)
    args = parser.parse_args()
    main(args)