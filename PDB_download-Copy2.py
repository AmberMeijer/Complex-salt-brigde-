#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, tempfile
import subprocess, signal
import time
import csv
from yasara import macro, disk


# In[2]:


#yasara_exe_path = r"C:\Program Files\yasara\YASARA.exe"
yasara_exe_path = r"C:\Program Files\yasara\YASARA.exe"
csv_path = "pdb_all.csv"
#out_path = r'C:\Users\amber\Downloads\pyPDBdownloader\pyPDBdownloader\output'


# In[3]:


def files_to_download(csv_path):
    out = []
    with open(csv_path, newline='') as csvfile:
        fields = ['filename', 'anchor', 'res1', 'res2', 'subunit', 'anchor_name']
        reader = csv.DictReader(csvfile, fields, delimiter =';')
        for row in reader:
            if row['filename'] != 'filename':
                out.append(row)
    return out


# In[4]:


def set_custom_macro(filename, anchor, res1, res2, subunit, anchor_name):
    p = str(os.path.abspath(os.path.join(os.getcwd(), 'output', filename+subunit+'_'+anchor+'_'+anchor_name+'_'+res1+'_'+res2+'.pdb')))
    macro = """
            LoadPDB {0}, download=yes;
            SelectAll;
            UnselectMol {4};
            DelMol selected;
            SelectAll;
            UnselectRes {1} {2} {3};
            DelAtom selected;
            DelHydAll;
            DelAtom CA CB N C O Res Arg;
            DelAtom CA CB N C O Res Glu;
            DelAtom CA N C O Res Asp;
            DelAtom CA CB CG N C O Res Lys;
            AddhydAll;
            style=stick;
            SavePDB {0}, {5}, Format=PDB, Transform=Yes;
            Clear
            """.format(filename, anchor, res1, res2, subunit, p).split(";")
    macro = [command.strip() for command in macro]
    return macro


# In[ ]:


i = 0
timeframe = 60
sheet = files_to_download(csv_path)
print('Started downloading .pbg files for {0} different names'.format(len(sheet)))
print('Maximum runtime: {0} minutes        Max. endtime: {1}'.format(len(sheet)*timeframe/60, time.time()+len(sheet)*timeframe))
for row in sheet:
    i += 1
    entry = set_custom_macro(row['filename'], row['anchor'], row['res1'], row['res2'], row['subunit'], row['anchor_name'])
    temp = os.path.join(os.getcwd(), 'somefile.mcr')
    with open(temp, 'w') as f:
        for line in entry:
            f.write(line+'\n')
    command = yasara_exe_path +" -txt " + temp
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    t_end = time.time() + timeframe
    success = None
    while time.time() < t_end:
        if os.path.exists(os.path.join(os.getcwd(), 'output', row['filename']+row['subunit']+'_'+row['anchor']+'_'+row['anchor_name']+'_'+row['res1']+'_'+row['res2']+'.pdb')):
            print('    {0}/{1} -- {2} -- Sucessfully downloaded'.format(i, len(sheet), row['filename']))
            time.sleep(1)
            success = True
            break
    if not success:
        print('    {0}/{1} -- {2} -- ERROR: timeout of 30 seconds exeeded'.format(i, len(sheet), row['filename']))
    process.kill()


# In[ ]:





# In[ ]:




