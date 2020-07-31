import sys
import os

if len(sys.argv) < 3:
    raise Exception("Please provide a file name root and an increment (Usage: python rename_files.py file_name_root 2)")
    
if not sys.argv[2].isnumeric():
    raise Exception("Please provide a number for the increment (Usage: python rename_files.py file_name_root 2)")

file_root = sys.argv[1]
files = os.listdir()
dds_files = []

for file in files:
    if file.endswith(".dds") and file[-7]=="_": # Bit hacky to check the presence of the '_'
        dds_files.append(file)
        
if len(dds_files) < 0:
    raise Exception("No matching dds files found")
        
if len(dds_files) > 99:
    raise Exception("Can not handle more than 99 dds files in folder")
    
for file in dds_files:
    og_file_number = int(file[-6:-4])
    new_file_number = str(og_file_number + int(sys.argv[2]))
    if len(new_file_number) < 2:
        new_file_number = "0" + new_file_number
    new_file_name = file[:-6] + new_file_number + file[-4:]
    print(new_file_name)