import pandas as pd
from pymol import cmd
import numpy as np
def create_label(selection, object_name, label, color):
    cmd.pseudoatom(object=object_name + '_label', selection=selection, name=object_name ,label=label, state=0,color=color)
    cmd.set("label_color",color, object_name + '_label')
    cmd.set("label_outline_color","black", object_name + '_label')
    
def reg_comparison(selection='all',file1=None, file2=None, property='Einter', segment='1', n_terms=10, energy_threshold=10.0):
    n_terms = int(n_terms)
    reg_df = pd.read_excel(file1, sheet_name= f'{property}_seg_{segment}')
    
    reg_pos = df_1[df_1['REG'] > 0]
    reg_neg = df_1[df_1['REG'] < 0]
    reg_pos['REG'] = reg_pos['REG'].apply(lambda x: x/reg_pos['REG'].iloc[-1])
    reg_neg['REG'] = reg_neg['REG'].apply(lambda x: x/reg_neg['REG'].iloc[0])
    print(reg_pos)
    import re
    for item in list(diff_pos_sorted.items()):
        atom_pair = re.search("(\()(.*?)(\))", item[0]).group(0)
        temp = re.split(r"[(,)]", atom_pair)
        obj_name = f"{temp[1]}_{temp[2]}"
        atom_index = re.findall('[0-9]+',atom_pair)
        atom1 = atom_index[0]
        atom2 = atom_index[1]
        if item[1][1] > float(energy_threshold):
            cmd.select(name = f"temp_sele",selection = f'i. {atom1} i. {atom2}')
            cmd.distance( obj_name, selection1 = f'(i. {atom1})',selection2 = f'(i. {atom2})')
            cmd.color(color='red',selection=obj_name)
            cmd.set("dash_gap","0.3",obj_name)
            cmd.set("dash_width","8.0",obj_name)
            cmd.hide("labels",obj_name)
            create_label(f"temp_sele", obj_name ,str(round(item[1][1],1)),'red')
            cmd.delete("temp_sele")
        elif item[1][1] < -float(energy_threshold):
            cmd.select(name = f"temp_sele",selection = f'i. {atom1} i. {atom2}')
            cmd.distance( obj_name, selection1 = f'(i. {atom1})',selection2 = f'(i. {atom2})')
            cmd.color(color='green',selection=obj_name)
            cmd.set("dash_gap","0.3",obj_name)
            cmd.set("dash_width","8.0",obj_name)
            cmd.hide("labels",obj_name)
            create_label(f"temp_sele", obj_name ,str(round(item[1][1],1)),'green')
            cmd.delete("temp_sele")

cmd.extend('reg_comparison',reg_comparison)