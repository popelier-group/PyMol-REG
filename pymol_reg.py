import pandas as pd
from pymol import cmd
import numpy as np
def _create_label(selection, object_name, label, color):
    cmd.pseudoatom(object=object_name + '_label', selection=selection, name=object_name ,label=label, state=0,color=color)
    cmd.set("label_color",color, object_name + '_label')
    cmd.set("label_outline_color","black", object_name + '_label')
    cmd.set("label_size", "24",object_name + '_label')
    cmd.set("label_font_id", "7",object_name + '_label')
    
def pymol_reg(selection='all',reg_file=None, property='Einter', segment='1', n_terms = 3, pos_color='red', neg_color='green'):
    n_terms = int(n_terms)
    reg_df = pd.read_excel(reg_file, sheet_name= f'{property}_seg_{segment}')
    reg_pos = reg_df[['TERM','REG']][reg_df['REG'] > 0].iloc[::-1]
    reg_neg = reg_df[['TERM','REG']][reg_df['REG'] < 0]
    import re
    norm_pos = np.multiply(list(reg_pos['REG']/reg_pos['REG'].iloc[0]),5)
    norm_neg = np.multiply(list(reg_neg['REG']/reg_neg['REG'].iloc[0]),5)
    count = 0
    for i, val in reg_pos.iloc[:n_terms].iterrows() :
        atom_pair = re.search("(\()(.*?)(\))", val['TERM']).group(0)
        temp = re.split(r"[(,)]", atom_pair)
        prop = val['TERM'].split('(')[0]
        obj_name = f"{prop}_{temp[1]}_{temp[2]}"
        atom_index = re.findall('[0-9]+',atom_pair)
        atom1 = atom_index[0]
        atom2 = atom_index[1]
        cmd.select(name = f"temp_sele",selection = f'i. {atom1} i. {atom2}', domain=selection)
        cmd.distance( obj_name, selection1 = f"i. {atom1} in {selection}",selection2 = f" i. {atom2} in {selection}")
        cmd.color(color=pos_color,selection=obj_name)
        cmd.set("dash_gap",str(0.5/norm_pos[count]),obj_name)
        cmd.set("dash_width",str(norm_pos[count]),obj_name)
        cmd.hide("labels",obj_name)
        _create_label(f"temp_sele", obj_name ,str(round(val['REG'],1)),pos_color)
        cmd.delete("temp_sele")
        count += 1
    count= 0
    for i, val in reg_neg.iloc[:n_terms].iterrows() :
        atom_pair = re.search("(\()(.*?)(\))", val['TERM']).group(0)
        temp = re.split(r"[(,)]", atom_pair)
        prop = val['TERM'].split('(')[0]
        obj_name = f"{prop}_{temp[1]}_{temp[2]}"
        atom_index = re.findall('[0-9]+',atom_pair)
        atom1 = atom_index[0]
        atom2 = atom_index[1]
        cmd.select(name = f"temp_sele",selection = f'i. {atom1} i. {atom2}', domain=selection)
        cmd.distance( obj_name, selection1 = f"i. {atom1} in {selection}",selection2 = f" i. {atom2} in {selection}")
        cmd.color(color=neg_color,selection=obj_name)
        cmd.set("dash_gap",str(0.5/norm_neg[count]),obj_name)
        cmd.set("dash_width",str(norm_neg[count]),obj_name)
        cmd.hide("labels",obj_name)
        _create_label(f"temp_sele", obj_name ,str(round(val['REG'],1)),neg_color)
        cmd.delete("temp_sele")
        count += 1

cmd.extend('pymol_reg', pymol_reg)