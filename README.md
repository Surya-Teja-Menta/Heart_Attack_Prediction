Create Environment

'''bash
conda create -n Heart python==3.7 -y
'''

Activate env
'''bash
conda activate Heart
'''
Create a Requirements File and add requirements
Install the Requirements
'''bash
pip install -r requirements.txt
'''

Download the dataset from

https://www.kaggle.com/rashikrahmanpritom/heart-attack-analysis-prediction-dataset

git init

dvc init

dvc add data_given/heart.csv

git add . && git commit -m "Added Successfully"

