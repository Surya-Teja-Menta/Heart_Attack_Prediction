import os
import argparse
import warnings
import pandas as pd
import numpy as np
from sklearn.metrics import recall_score,precision_score,f1_score
from sklearn.ensemble import ExtraTreesClassifier 
from sklearn.svm import SVC
from sklearn.preprocessing import *
from get_data import read_params
import joblib,json,pickle

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
    print(train.head())
    print(test.head())
    

    lr=ExtraTreesClassifier()
    lr.fit(train,train_y)
    predicted_qualities=lr.predict(test_x)
  
  
    (rmse,mae,r2)= eval_metrics(test_y,predicted_qualities)
    print("Extra Tree Classifier model model :" )
    print("  Precision: %s" % rmse)
    print("  Recall: %s" % mae)
    print("  F1 Score: %s" % r2)
    score_file=config['reports']['scores']
    params_file=config['reports']['params']

    with open(score_file,'w') as f:
        scores={
            'Precison':rmse,
            'Recall':mae,
            'F1_score':r2
        }
        json.dump(scores,f,indent=4)
    

    model_path=os.path.join(model_dir,"model.joblib")
    joblib.dump(lr,model_path)
    model_path=os.path.join(model_dir,"heart_model")
    with open('heart_model','wb') as file:
        pickle.dump(lr,file)


if __name__ == '__main__':
    args=argparse.ArgumentParser()
    args.add_argument("--config",default='params.yaml')
    parsed_args=args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)