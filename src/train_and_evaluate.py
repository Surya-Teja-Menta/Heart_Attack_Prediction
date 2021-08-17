import os
import argparse
import warnings
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from sklearn.linear_model import ElasticNet
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from get_data import read_params
from sklearn.dummy import DummyClassifier
import joblib,json,pickle
from mlxtend.classifier import StackingCVClassifier

def eval_metrics(actual,pred):
    rmse=np.sqrt(mean_squared_error(actual, pred))
    mae=mean_absolute_error(actual,pred)
    r2=r2_score(actual,pred)
    return rmse,mae,r2


def train_and_evaluate(config_path):
    config=read_params(config_path)
    test_data_path=config['split_data']['test_path']
    train_data_path=config['split_data']['train_path']
    random_state=config['base']['random_state']
    model_dir=config['model_dir']

    kernel=config['estimators']['SVC']['params']['kernel']
    C=config['estimators']['SVC']['params']['C']
    target=[config['base']['target_col']]
    train=pd.read_csv(train_data_path,sep=',')
    test=pd.read_csv(test_data_path,sep=',')
    scaler=StandardScaler()
    train_y=train[target]
    print("train_Y",len(train_y))
    test_y=test[target]
    train_x=train.drop(target,axis=1)
    train_x=train_x.drop('Unnamed: 0',axis=1)

    test_x=test.drop(target,axis=1)
    test_x=test_x.drop('Unnamed: 0',axis=1)

    lr=SVC(kernel=kernel,C=C)
    lr.fit(train_x,train_y)
    predicted_qualities=lr.predict(test_x)
  
  
    (rmse,mae,r2)= eval_metrics(test_y,predicted_qualities)
    print("SVC model (kernel=%s, C=%s):" % (kernel, C))
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)
    score_file=config['reports']['scores']
    params_file=config['reports']['params']

    with open(score_file,'w') as f:
        scores={
            'rmse':rmse,
            'mae':mae,
            'r2':r2
        }
        json.dump(scores,f,indent=4)
    with open(params_file,'w') as f:
        params={
            'kernel':kernel,
            'C':C,
        }
        json.dump(params,f,indent=4)

    model_path=os.path.join(model_dir,"model.joblib")
    joblib.dump(lr,model_path)
    model_path=os.path.join(model_dir,"pheart_model")
    with open('heart_model','wb') as file:
        pickle.dump(lr,file)


if __name__ == '__main__':
    args=argparse.ArgumentParser()
    args.add_argument("--config",default='params.yaml')
    parsed_args=args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)