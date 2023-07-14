import os
import shutil
import subprocess
from tqdm import tqdm

input_directory = "./"
output_directory = "output"
pdb2pdbqt_path = "/path/to/AutoDockTools/Utilities24"
pdb2pdbqt_script = os.path.join(pdb2pdbqt_path, "prepare_ligand4.py")

# Membuat direktori output
if os.path.exists(output_directory):
    shutil.rmtree(output_directory)
os.makedirs(output_directory)

# Mendapatkan daftar file dalam direktori input_directory
file_list = os.listdir(input_directory)
sdf_files = [filename for filename in file_list if filename.endswith(".sdf")]

# Menggunakan tqdm untuk membuat progress bar
for filename in tqdm(sdf_files, desc="Processing sdf database"):
    sdf = os.path.splitext(os.path.basename(filename))[0]
    command = f"obabel {os.path.join(input_directory, filename)} -osdf -O {os.path.join(output_directory, sdf)}.sdf -m"
    subprocess.run(command, shell=True)

# Mengganti nama file SDF
sdf_files = [f for f in os.listdir(output_directory) if f.endswith(".sdf")]
os.chdir(output_directory)
for sdf_file in tqdm(sdf_files, desc="Rename SDF file"):
    with open(sdf_file, 'r') as f:
        new_name = f.readline().strip()
    os.rename(sdf_file, new_name + ".sdf")
os.chdir("..")

# Konversi sdf ke pdb
sdf_files = [filename for filename in os.listdir(output_directory) if filename.endswith(".sdf")]
os.chdir(output_directory)
for sdf_file in tqdm(sdf_files, desc="Converting SDF to PDB"):
    new_name = os.path.splitext(sdf_file)[0]
    command = f"obabel {sdf_file} -opdb -O {new_name}.pdb -h"
    subprocess.run(command, shell=True)
    os.remove(sdf_file)
os.chdir("..")

# Konversi pdb ke pdbqt
def get_pdb_files(directory):
    pdb_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdb"):
            pdb_files.append(os.path.join(directory, filename))
    return pdb_files

os.chdir(output_directory)
pdb_files =  os.listdir()
for pdb_file in tqdm(pdb_files, desc="Converting PDB to PDBQT"):
    command = f"{pdb2pdbqt_script} -l {pdb_file}"
    subprocess.run(command, shell=True)
    os.remove(pdb_file)
os.chdir("..")
print("done")
print("The script written by La Ode Aman, laode_aman@ung.ac.id")
