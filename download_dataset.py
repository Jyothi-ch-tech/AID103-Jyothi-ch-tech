"""
Download Plant Disease Dataset from Kaggle
"""
import os
import sys

try:
    from kaggle.api.kaggle_api_extended import KaggleApi
    
    print("Initializing Kaggle API...")
    api = KaggleApi()
    api.authenticate()
    
    print("Downloading dataset: new-plant-diseases-dataset")
    print("This may take a few minutes (around 2GB)...")
    
    # Download to current directory
    api.dataset_download_files(
        'vipoooool/new-plant-diseases-dataset',
        path='.',
        unzip=True
    )
    
    print("\n✅ Dataset downloaded successfully!")
    print("Location: ./New Plant Diseases Dataset(Augmented)/")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure kaggle.json is in C:\\Users\\chara\\.kaggle\\")
    print("2. Try: pip install --upgrade kaggle")
    print("3. Restart PowerShell and try again")
    sys.exit(1)
