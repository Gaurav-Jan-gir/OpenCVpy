import Interface_excel as Interface
import sys
import create_backup as backup
import os

backup_dir = os.path.join(os.getcwd(), 'backup')
data_dir = os.path.join(os.getcwd(), 'data')

if __name__ == "__main__":
    excel_path = os.path.join(os.getcwd(),'data', 'data.xlsx')
    config_path = 'config.json'
    
    if len(sys.argv) > 1:
        if sys.argv[1]:
            excel_path = sys.argv[1]
            if not os.path.exists(excel_path):
                print(f"Excel file '{excel_path}' does not exist.")
                if input("Do you want to continue with the default path? (y/n): ").strip().lower() != 'y':
                    sys.exit(1)
            if not excel_path.endswith('.xlsx'):
                print(f"Invalid file format for '{excel_path}'.")
                if input("Do you want to continue with the default path? (y/n): ").strip().lower() != 'y':
                    sys.exit(1)
            
    if len(sys.argv) >2 and sys.argv[2]:  # Fix: Add () for method call
        config_path = sys.argv[2]

    try:
         backup.create_backup(data_dir, excel_path,backup_dir)
    except Exception as e:
        print(f"An error occurred while creating backup: {e}")
        if input("Do you want to continue without backup? (y/n): ").strip().lower() != 'y':
            sys.exit(1)
    try:
        Interface.interFace(excel_path , config_path)
        backup.remove_backup(backup_dir)
    except Exception as e:
            print(f"An error occurred: {e}")
            print("Please check the configuration and try again.")
            if input("Do you want to restore backup? (y/n): ").strip().lower() != 'y':
                backup.restore_backup(backup_dir, data_dir, excel_path)
            sys.exit(1)