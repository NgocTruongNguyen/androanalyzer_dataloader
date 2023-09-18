# Import necessary libraries
from urllib import request
import os
import zipfile
import pandas as pd
import tempfile  # Import the tempfile module

# Create a temporary directory for storing the ZIP file
temp_dir = tempfile.mkdtemp()


# Define the default and backup server URLs for downloading the dataset
default_server_url = "https://s3-hcm-r1.longvan.net/19414866-malware-dataset/lv_truong/AndroidMalware_AllDataset4Paper.zip"
backup_server_url = "https://19414866-malware-dataset.s3-hcm-r1.longvan.net/lv_truong/AndroidMalware_AllDataset4Paper.zip"

# Specify the path for the downloaded ZIP file in the temporary directory
zip_file_path = os.path.join(temp_dir, "AndroidMalware_AllDataset4Paper.zip")

# Check if the ZIP file already exists, if not, attempt to download it
if not os.path.exists(zip_file_path):
    try:
        # Try to download from the default server URL
        request.urlretrieve(default_server_url, zip_file_path)
    except:
        # If the default server fails, try the backup server URL
        request.urlretrieve(backup_server_url, zip_file_path)

# Function to load data from the ZIP file by name
def load_data(name, train_set=True):
    """
    Load data from a specified CSV file within a ZIP archive.

    Args:
        name (str): The name of the dataset or file to be loaded.
        train_set (bool, optional): A boolean flag indicating whether to load the training set (default) or testing set.

    Returns:
        pandas.DataFrame: A DataFrame containing the loaded data.
    """
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        try:
            # Try to open and read the specified CSV file from the ZIP archive
            with zip_file.open(f'{name}.csv') as csv_file:
                return pd.read_csv(csv_file)
        except Exception as error:
            if name == 'AndroAnalyzer':
                if train_set:
                    with zip_file.open(f'MiniMalDroid2020/AndroAnalyzer/AndroAnalyzer_train.csv') as csv_file:
                        return pd.read_csv(csv_file)
                else:
                    with zip_file.open(f'MiniMalDroid2020/AndroAnalyzer/AndroAnalyzer_test.csv') as csv_file:
                        return pd.read_csv(csv_file)
            # Handle any exceptions and print an error message
            print(error)

# Function to get SHA256 data by class name
def get_sha256(class_name, train_set=True):
    """
    Retrieve SHA256 data by class name from either the training or testing set.

    Args:
        class_name (str): The name of the class for which SHA256 data is requested.
        train_set (bool, optional): A boolean flag indicating whether to retrieve data from the training set (default) or testing set.

    Returns:
        list: A list of SHA256 strings associated with the specified class.
    """
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        try:
            if train_set:
                with zip_file.open(f'MiniMalDroid2020/SHA256/train_set/{class_name}') as data_file:
                    # Read and decode the data as UTF-8 and split it into lines
                    return data_file.read().decode('utf-8').splitlines()
            else:
                with zip_file.open(f'MiniMalDroid2020/SHA256/test_set/{class_name}') as data_file:
                    # Read and decode the data as UTF-8 and split it into lines
                    return data_file.read().decode('utf-8').splitlines()
        except Exception as error:
            print(error)

# Function to get a list of dataset names
def get_list_dataset():
    """
    Get a list of dataset names available in the ZIP archive.

    Returns:
        list: A list of dataset names.
    """
    # Print and return a list of dataset names
    return ['AndroVul', 'Bataci', 'Drebin-215', 'Malgenome-215', 'AndroAnalyzer']

# Function to get a list of class names
def get_classname():
    """
    Get a list of class names.

    Returns:
        list: A list of class names.
    """
    # Print and return a list of class names
    return ['Adware', 'Banking', 'Benign', 'Riskware', 'SMS']

if __name__ == "__main__":
    print("Wellcome to AndroAnalyzer Dataset!!!")