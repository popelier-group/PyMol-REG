# PyMol_REG

Visualisation of REG results through PyMol GUI.
This repository contains the Plugin 'pymol_reg.py' for PyMol (tested on version 2.5.0 Open-Source).
This adds the functionality of visualising a Relative Energy Gradient (REG) analysis output from the [REG.py](https://github.com/FabioFalcioni/REG.py) library. This mainly works with the Interacting Quantum Atoms (IQA) topological partitioning.

# Requirements

- [PyMol](https://github.com/schrodinger/pymol-open-source)
- [numpy](https://numpy.org/)
- [pandas](https://pandas.org/)

# Usage

To load the `pymol_reg.py` script as a PyMol plugin, please follow this [link](https://pymolwiki.org/index.php/Plugins).
Otherwise, simply type

- `run path/to/pymol_reg.py`
  to load it in the current PyMol session.

## Variables

1. **selection** : object/geometry of the reaction analyzed with the REG methodology uploaded in PyMol.
2. **reg_file** : path to the REG.xlsx file output from the REG.py library.
3. **property** : IQA property that is present in the REG.xlsx file. This depends on which properties have been analyzed with the REG.py library. Examples are "Vxc", "Vcl" and "Einter".
4. **segment** : segment number to consider for the REG values of the previously defined property. (default=1)
5. **n_terms** : number of REG terms to visualize, positive and negative. (default=3)
6. **pos_color** : color for the positive REG values. (default=red)
7. **neg_color** : color for the negative REG values. (default=green)
8. **scale** : scaling value to make visualization easier. (default=5.0)

# To do

- Add a QTWidget in PyMol GUI
