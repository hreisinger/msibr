# MSIBR
MSIBR is the conjoining join to the paper [paper name] (paper url). This code will generate Serpent2 input files with a standard file format. There may be problems using Linux.


## File System
**Main Folder**

- Python Files
  - generate_serpent.py: Main file to create input decks | calls deck.py
  - calculateSlit.py: Converts the variable blanket fraction into the slit width between graphite hexagons
  - deck.py: Organizes input deck and outputs string | calls lattice.py, surfs.py, cells.py, materials.py, reprocessing.py
  - cells.py: Cell creation
  - lattice.py: Lattice creation
  - materials.py: Material definitions
  - surfs.py: Surface creation
  - reprocessing.py: If toggeled will create a reprocessing scheme
  - runAll.py: A simple file which loops through all the current input decks (should be inside the main run folder)
- Run Folders
  - Folder: variable1[0]
    - Folder: variable2[0]
    
        Input File: MSiBR.inp (variable1[0], variable2[0])
    - Folder: variable2[1]

        Input File: MSiBR.inp (variable1[0], variable2[1])
    - ...
    - Folder: variable2[-1]
  - Folder: variable1[1]
  - ...
  - Folder: variable1[-1]
  - runAll.py

