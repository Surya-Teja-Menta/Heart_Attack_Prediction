import os

dirs=[
    os.path.join('data','raw'),
    os.path.join('data','processed'),
    'notebooks',
    'saved_models',
    'src'

]

for di in dirs:
    os.makedirs(di,exist_ok=True)
    with open(os.path.join(di,'.gitkeep'),'w') as f:
        pass
file_=[
    "dvc.yaml",
    "params.yaml",
    '.gitignore',
    os.path.join('src','__init__.py')    


]
for fi in file_:
    with open(fi,'w') as f:
        pass