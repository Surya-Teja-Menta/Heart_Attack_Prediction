import os
import argparse
import warnings
import pandas as pd
import numpy as np
from sklearn.metrics import recall_score,precision_score,f1_score
from sklearn.ensemble import ExtraTreesClassifier 
from sklearn.svm import SVC
from sklearn.preprocessing import *
from urllib.parse import urlparse
from get_data import read_params
import joblib,json,pickle
import mlflow


def eval_metrics(actual,pred):
    recall=recall_score(actual, pred)
    precision=precision_score(actual,pred)
    f1=f1_score(actual,pred)
    return recall,precision,f1


def train_and_evaluate(config_path):
    config=read_params(config_path)
    test_data_path=config['split_data']['test_path']
    train_data_path=config['split_data']['train_path']
    random_state=config['base']['random_state']
    model_dir=config['model_dir']
    mm=StandardScaler()


   
    target=[config['base']['target_col']]
    train=pd.read_csv(train_data_path,sep=',')
    test=pd.read_csv(test_data_path,sep=',')
    train_y=train[target]
    test_y=test[target]
    train_x=train.drop(target,axis=1)
    train_x=train_x.drop('Unnamed: 0',axis=1)
    test_x=test.drop(target,axis=1)
    test_x=test_x.drop('Unnamed: 0',axis=1)
    trainm=mm.fit_transform(train_x)
    testm=mm.transform(test_x)
    train=pd.DataFrame(trainm,columns=train_x.columns)
    test=pd.DataFrame(testm,columns=test_x.columns)
    n_estimators=10
    max_depth=5
    mlflow_config=config['mlflow_config']
    remote_server_url=mlflow_config['remote_server_url']
    mlflow.set_tracking_uri(remote_server_url)
    mlflow.set_experiment(mlflow_config['experiment_name'])
    with mlflow.start_run(run_name=mlflow_config['run_name']) as mlops:


        lr=ExtraTreesClassifier(n_estimators=config['estimators']['ExtraTreeClassifier']['params']['n_estimators'],max_depth=config['estimators']['ExtraTreeClassifier']['params']['max_depth'])
        lr.fit(train,train_y)
        predicted_qualities=lr.predict(test_x)
    
    
        (precision,recall,f1)= eval_metrics(test_y,predicted_qualities)
        print("Extra Tree Classifier model model :" )
        print("  Precision: %s" % precision)
        print("  Recall: %s" % recall)
        print("  F1 Score: %s" % f1)
        mlflow.log_param('n_estimators',n_estimators)
        mlflow.log_param('max_depth',max_depth)
        mlflow.log_metric('Precision',precision)
        mlflow.log_metric('Recall',recall)
        mlflow.log_metric('F1_Score',f1)
        
        tracking_url_type_store=urlparse(mlflow.get_artifact_uri()).scheme
        if tracking_url_type_store!='file':
            mlflow.sklearn.log_model(lr,'model',registered_model_name=mlflow_config['registered_model'])
        else:
            mlflow.sklearn.load_model(lr,'model')

        
        


if __name__ == '__main__':
    args=argparse.ArgumentParser()
    args.add_argument("--config",default='params.yaml')
    parsed_args=args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)