Create Environment

```bash
conda create -n Heart python==3.7 -y
```

Activate env
```bash
conda activate Heart
```
Create a Requirements File and add requirements
Install the Requirements
```bash
pip install -r requirements.txt
```

Download the dataset from

https://www.kaggle.com/rashikrahmanpritom/heart-attack-analysis-prediction-dataset

Initiate Git
```bash
git init
```
Initiate dvc
```bash
dvc init
```

Add data to dvc
```bash
dvc add data_given/heart.csv
```

Add Everything to git

```bash
git add . && git commit -m "Added Successfully"
```

Connecting to Remote github

```bash
git add . && git commit -m "Updated Successfully"
```

```bash
git remote add origin https://github.com/Surya-Teja-Menta/Heart_Attack_Prediction
```

```bash
git branch -M main
```

```bash
git push origin main
```
tox command
```bash
tox
```
Rebuilding Tox
```bash
tox -r
```
pytest command
```bash
pytest -v
```
setup commands 
```bash
pip install -e
``` 
Building our Own Package
```bash
python setup.py sdist bdist_wheel
```
Final App: https://heart-attack-3.herokuapp.com/
