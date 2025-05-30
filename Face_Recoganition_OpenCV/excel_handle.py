from openpyxl import Workbook, load_workbook , utils
from datetime import datetime
import time
import sys
import os

class Excel_handle:
    def __init__(self,path):
        self.path = path
        self.wb = self.create_excel_file()
        if self.wb is None:
            print("Failed to create or load the Excel file. Exiting...")
            sys.exit(1)
        self.ws = self.wb.active

    def create_excel_file(self):   
        if not os.path.exists(self.path):
            wb = Workbook()
            ws = wb.active
            ws.title = "User Data"
            ws.append(["ID", "Name", "Confidence","Count"])
            ws.column_dimensions['A'].width = len("ID")+3
            ws.column_dimensions['B'].width = len("Name")+3
            ws.column_dimensions['C'].width = len("Confidence")+3
            ws.column_dimensions['D'].width = len("Count")+3
            wb.save(self.path)
            wb.close()
        try:
            wb = load_workbook(self.path)
        except Exception as e:
            print(f"Error loading Excel File: {e}")
            print("Do you want to delete the existing file and create a new one? (y/n)")
            choice = input().strip().lower()
            if choice == 'y':
                time.sleep(1)
                try:
                    os.remove(self.path)
                except PermissionError as e:
                    print(f"Permission Error: {e}. Please close the file and try again.")
                    return None
                return self.create_excel_file()
            else:
                return None
        return wb
    
    def get_row_number(self, ws,id):
        for rn in range(2, ws.max_row + 1):  # Start from row 2 (skip header)
            cell_value = ws.cell(row=rn, column=1).value  # ID is in column 1
            if cell_value == id:
                return rn
        return None
    

    def write_to_excel(self,name, id, confidence,tg):
        row_num = self.get_row_number(self.ws, id)
        dt = datetime.now().strftime("%d/%m/%Y") + " - " + datetime.now().strftime("%H:%M:%S")
        confidence = round((1-confidence) * 100, 2)  # Convert to percentage
        if row_num is None:
            self.ws.append([id, name, confidence, 1,dt])
            self.ws.column_dimensions['A'].width = max(len(str(id))+3,self.ws.column_dimensions['A'].width)
            self.ws.column_dimensions['B'].width = max(len(name)+3,self.ws.column_dimensions['B'].width)
            self.ws.column_dimensions['C'].width = max(len(str(confidence))+3,self.ws.column_dimensions['C'].width)
            self.ws.column_dimensions['D'].width = max(len(str(1))+3,self.ws.column_dimensions['D'].width)
            self.ws.column_dimensions['E'].width = max(len(dt)+3,self.ws.column_dimensions['E'].width)
        else:
            
            count = self.ws.cell(row=row_num, column=4).value
            if self.timeGapInSeconds(self.ws.cell(row=row_num, column=4+count).value, dt) < tg:
                print("Duplicate entry detected. Skipping...")
                return
            self.ws.cell(row=row_num, column=3).value = min(self.ws.cell(row=row_num, column=3).value, confidence)
            cl = utils.get_column_letter(5+count)
            self.ws.cell(row=row_num, column=4).value = count + 1
            self.ws.cell(row=row_num, column=5+count).value = dt
            self.ws.column_dimensions[cl].width = max(len(dt),self.ws.column_dimensions[cl].width)
        self.wb.save(self.path)
        
    def timeGapInSeconds(self, old_time, new_time):
        old_time = datetime.strptime(old_time, "%d/%m/%Y - %H:%M:%S")
        new_time = datetime.strptime(new_time, "%d/%m/%Y - %H:%M:%S")
        return (new_time - old_time).total_seconds()