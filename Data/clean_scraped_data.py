import csv
import os
import shutil

input_file = 'Compiled_scraped_data.csv'
output_file = 'clean_scraped_data.csv'

with open(input_file, mode='r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    cleaned_data = []
    for row in csv_reader:
        # Check your conditions here
        if (not row['Area'] and row['Height control'] == "Subject to detailed evaluation") or (not row['GPR'].strip()):
                continue
        cleaned_data.append(row)

# Write the cleaned data to a new CSV file
with open(output_file, mode='w', encoding='utf-8', newline='') as csv_file:
    fieldnames = ['Index', 'Address', 'GPR', 'Area', 'Dwelling Units', 'LRA', 'Height control', 'Max dwelling units',
                  'Road setback', '', '']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(cleaned_data)

folders = ['Area', 'Site plan', 'Zoom']
for folder in folders:
    # Constants
    input_csv = 'clean_scraped_data.csv'
    source_folder = os.path.join('Compiled_screenshots', f"{folder}")
    destination_folder = os.path.join('Compiled_screenshots', f"{folder}_cleaned")

    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Get the list of Index values from clean_scraped_data.csv
    with open(input_csv, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        index_values = [row['Index'] for row in csv_reader]

    # Copy the images
    for index_val in index_values:
        source_image = os.path.join(source_folder, f"{index_val}_area.png")

        if os.path.exists(source_image):
            destination_image = os.path.join(destination_folder, f"{index_val}_{folder.lower()}.png")
            shutil.copy(source_image, destination_image)
        else:
            print(f"Image not found for Index {index_val}.")