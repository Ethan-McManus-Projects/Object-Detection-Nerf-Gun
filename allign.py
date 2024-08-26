import os
import pandas as pd
import argparse

def clean_csv_and_images(csv_path, image_dir):
    # Read the CSV file, skipping the first line
    df = pd.read_csv(csv_path, skiprows=1)

    # Get the list of image filenames (without extensions)
    image_filenames = {os.path.splitext(f)[0] for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))}

    # Get the list of filenames from the CSV (assuming the first column contains the filenames)
    csv_filenames = set(df.iloc[:, 0])

    # Find filenames that are in the CSV but not in the image directory
    missing_images = csv_filenames - image_filenames

    # Find filenames that are in the image directory but not in the CSV
    missing_csv_entries = image_filenames - csv_filenames

    # Calculate the number of remaining rows and images after deletion
    remaining_csv_rows = len(df) - len(missing_images)
    remaining_images = len(image_filenames) - len(missing_csv_entries)

    # Check if deletions would result in fewer than 10 lines in the CSV or fewer than 10 files in the image directory
    if remaining_csv_rows < 10 or remaining_images < 10:
        print("Error: Deletion would result in fewer than 10 lines in the CSV or fewer than 10 files in the image directory.")
        return

    # Remove rows from the CSV that do not have corresponding images
    df = df[~df.iloc[:, 0].isin(missing_images)]

    # Remove images that do not have corresponding CSV entries
    for missing_image in missing_csv_entries:
        os.remove(os.path.join(image_dir, missing_image + '.jpg'))  # Assuming images are in .jpg format

    # Save the updated CSV file
    df.to_csv(csv_path, index=False)

    print(f"Removed {len(missing_images)} entries from the CSV file.")
    print(f"Removed {len(missing_csv_entries)} images from the directory.")

def main():
    parser = argparse.ArgumentParser(description="Clean CSV and image directory.")
    parser.add_argument('--csv_path', type=str, required=True, help='Path to the CSV file')
    parser.add_argument('--image_dir', type=str, required=True, help='Path to the image directory')
    args = parser.parse_args()

    clean_csv_and_images(args.csv_path, args.image_dir)

if __name__ == '__main__':
    main()