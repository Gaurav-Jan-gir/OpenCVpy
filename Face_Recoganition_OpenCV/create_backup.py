import shutil
import os
import pandas as pd


def create_backup(data_dir, excel_file, backup_dir):
    os.makedirs(backup_dir, exist_ok=True)
    
    # Backup Excel file
    backup_excel(excel_file, backup_dir)
    
    # Backup .npy files
    backup_npy(data_dir, backup_dir)
    
    # Export Excel to CSV
    csv_file = os.path.join(backup_dir, 'data_backup.csv')
    export_csv(excel_file, csv_file)

def remove_backup(backup_dir):
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
    else:
        print(f"Backup directory '{backup_dir}' does not exist.")

def restore_backup(backup_dir, data_dir, excel_file):
    if not os.path.exists(backup_dir):
        print(f"Backup directory '{backup_dir}' does not exist.")
        return
    
    # Restore Excel file
    restore_excel(excel_file, backup_dir)
    
    # Restore .npy files
    restore_npy(data_dir, backup_dir)

def restore_excel(excel_file, backup_dir):
    excel_dir = os.path.join(backup_dir, 'excel')
    if os.path.exists(excel_dir):
        for file in os.listdir(excel_dir):
            if file == os.path.basename(excel_file):
                shutil.copy(os.path.join(excel_dir, file), excel_file)
                print(f"Restored Excel file to {excel_file}")
                return
    print(f"No Excel backup found in {excel_dir}")

def restore_npy(data_dir, backup_dir):
    npy_dir = os.path.join(backup_dir, 'npy')
    if os.path.exists(npy_dir):
        for file in os.listdir(npy_dir):
            if file.endswith('.npy'):
                shutil.copy(os.path.join(npy_dir, file), os.path.join(data_dir, file))
                print(f"Restored {file} to {data_dir}")
    else:
        print(f"No .npy backup found in {npy_dir}")

def backup_excel(excel_file, backup_dir):
    excel_dir = os.path.join(backup_dir, 'excel')
    os.makedirs(excel_dir, exist_ok=True)
    if os.path.exists(excel_file):
        file_name = os.path.basename(excel_file)
        shutil.copy(excel_file, os.path.join(excel_dir, file_name))

def backup_npy(data_dir, backup_dir):
    npy_dir = os.path.join(backup_dir, 'npy')
    os.makedirs(npy_dir, exist_ok=True)
    for file in os.listdir(data_dir):
        if file.endswith('.npy'):
            shutil.copy(os.path.join(data_dir, file), os.path.join(npy_dir, file))

def export_csv(excel_file, csv_file):
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        df.to_csv(csv_file, index=False)