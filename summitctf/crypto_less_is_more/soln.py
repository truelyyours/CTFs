from pathlib import Path
from ast import literal_eval
import base64

directory = Path('.')

files = []
file_content = []

for filenames in directory.iterdir():
    if str(filenames) == 'soln.py':
        continue
    file_content.append(filenames.read_text().strip())
    files.append(str(filenames))

flags = []
signs = []
key_matrix = []

for content in file_content:
    temp = content.split('\n')
    flags.append(temp[0].split(': ')[-1])
    signs.append(temp[1].split(': ')[-1])
    key_matrix.append(temp[2].split(': ')[-1])

print(len(flags))
key_set = set(key_matrix)
key_list = []
# for k in key_matrix:
#     key_list.append(list(literal_eval(k)))
signs_set = set(signs)
print("KEYS and SIGNS: ", key_set, signs_set)

print("SIGNS COUNT: 109079140092091089174200", signs.count('109079140092091089174200'))
print("SIGNS COUNT: 109079140093091089174200", signs.count('109079140093091089174200'))

sign_intrest = '109079140093091089174200'
ind = signs.index(sign_intrest)
key_intrest = literal_eval(key_matrix[ind])
flag_intrest = base64.b64decode(flags[ind])
print("KEY: ", key_intrest)
print("FLAG: ", flag_intrest, flags[ind])

# FLAG: SummitCTF{secret_nb6azvfm5t3e}

