import os, yaml,joblib,pickle,json
from sklearn.preprocessing import *
import pandas as pd
import numpy as np

params_path='params.yaml'
schema_path=os.path.join('prediction_service','schema.json')

def read_params(config_path):
    with open(config_path) as yaml_file:
        config=yaml.safe_load(yaml_file)
    return config

def get_schema(schema_path=schema_path):
    with open(schema_path) as json_file:
        schema=json.load(json_file)
    return schema

def predict(data):
    config=read_params(params_path)
    with open('prediction_service/model/heart-svm.pkl','rb') as file:
        pickle_file=pickle.load(file)
    prediction=pickle_file.predict(data)

    s=''
    if prediction[0]>=0.5:
        s='Positive'
    else:
        s='Negative'

    return s

def api_response(request):

    try:
        data=np.array([list(request.json.values())])
        response=predict(data)
        response={"response":response}
        return response
    except Exception as e:
        print(e)
        error={'error':'Something went wrong'}
        return error

def form_response(dict_request):
    data=dict_request
    data=[list(map(float,data))]
    response=predict(data)
    return response