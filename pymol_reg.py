import pandas as pd
from pymol import cmd
import numpy as np
import re
def _create_reg_label(selection, object_name, label, color):
    cmd.pseudoatom(object=object_name + '_label', selection=selection, name=object_name ,label=label, state=0,color=color)
    cmd.set("label_color",color, object_name + '_label')
    cmd.set("label_outline_color","black", object_name + '_label')
    cmd.set("label_size", "24",object_name + '_label')
    cmd.set("label_font_id", "7",object_name + '_label')

def _create_reg_object(selection,reg_df,scale, color,n_terms,property):
    norm_reg = np.multiply(list(reg_df['REG']/reg_df['REG'].iloc[0]),scale)
    if (reg_df['REG'] < 0).values.any():
        sign = 'neg'
    elif  (reg_df['REG'] > 0).values.any():
        sign = 'pos'
    count = 0
    for i, val in reg_df.iloc[:n_terms].iterrows() :
        atom_pair = re.search("(\()(.*?)(\))", val['TERM']).group(0)
        temp = re.split(r"[(,)]", atom_pair)
        prop = val['TERM'].split('(')[0]
        obj_name = f"{prop}_{temp[1]}_{temp[2]}_{selection}"
        atom_index = re.findall('[0-9]+',atom_pair)
        atom1 = atom_index[0]
        atom2 = atom_index[1]
        cmd.select(name = f"temp_sele",selection = f'i. {atom1} i. {atom2}', domain=selection)
        cmd.distance( obj_name, selection1 = f"i. {atom1} in {selection}",selection2 = f" i. {atom2} in {selection}")
        cmd.hide("labels",obj_name)
        cmd.color(color=color,selection=obj_name)
        cmd.set("dash_gap",str((1/scale)/norm_reg[count]),obj_name)
        cmd.set("dash_width",str(norm_reg[count]),obj_name)
        _create_reg_label(f"temp_sele", obj_name ,str(round(val['REG'],1)),color)
        cmd.delete("temp_sele")
        cmd.group(obj_name + '_group', obj_name)
        cmd.group(obj_name + '_group', obj_name + "_label")
        cmd.group(f"{property}_{sign}_{selection}",obj_name + '_group')
        count += 1
    cmd.group(f"{property}_{selection}",f"{property}_{sign}_{selection}")

def pymol_reg(selection='all',reg_file=None, property='Einter', segment='1', n_terms = 3, pos_color='red', neg_color='green', scale=5.0):
    n_terms = int(n_terms)
    scale = float(scale)
    reg_df = pd.read_excel(reg_file, sheet_name= f'{property}_seg_{segment}')
    reg_pos = reg_df[['TERM','REG']][reg_df['REG'] > 0].iloc[::-1]
    reg_neg = reg_df[['TERM','REG']][reg_df['REG'] < 0]
    _create_reg_object(selection,reg_pos,scale,pos_color,n_terms,property)
    _create_reg_object(selection,reg_neg,scale,neg_color,n_terms,property)

cmd.extend('pymol_reg', pymol_reg)