import os
import shutil

def backup_data(source_dir, backup_dir):
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source directory {source_dir} does not exist.")

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(backup_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

def backup_file(source_file, backup_dir):
    if not os.path.exists(source_file):
        raise FileNotFoundError(f"Source file {source_file} does not exist.")

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    shutil.copy2(source_file, os.path.join(backup_dir, os.path.basename(source_file)))

def remove_backup(backup_dir):
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
    else:
        print(f"Backup directory {backup_dir} does not exist, nothing to remove.")

def restore_backup(backup_dir, target_dir):
    if not os.path.exists(backup_dir):
        raise FileNotFoundError(f"Backup directory {backup_dir} does not exist.")

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for item in os.listdir(backup_dir):
        s = os.path.join(backup_dir, item)
        d = os.path.join(target_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)