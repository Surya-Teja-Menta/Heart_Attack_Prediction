from flask import Flask,render_template,request,jsonify
import os, yaml,joblib,pickle
#from sklearn.externals import joblib
import numpy as np

params_path='params.yaml'
webapp_root='webapp'
static_dir=os.path.join(webapp_root,'static')
template_dir=os.path.join(webapp_root,'templates')
app=Flask(__name__, static_folder=static_dir,template_folder=template_dir)

def read_params(config_path):
    with open(config_path) as yaml_file:
        config=yaml.safe_load(yaml_file)
    return config
def conv(data):
    l,f=data[0][8],data[0]
    f=f[:8]
    l=float(l)
    f=[int(i) for i in f]
    f.append(l)
    data[0]=f
    return data

def predict(data):
    config=read_params(params_path)
    model_dir_path=config['webapp_model_dir']
    #model=joblib.load_model(model_dir_path)
    with open('pickle_model','rb') as file:
        pickle_file=pickle.load(file)
    prediction=pickle_file.predict(data)
    s=''
    if prediction[0]>=0.5:
        s='Positive'
    else:
        s='Negative'

    return s









@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        try:
            if request.form:
                data=dict(request.form)
                data=[list(data.values())]
                #data=conv(data)
                data=[list(map(float,data[0]))]
                response=predict(data)
                return render_template('index.html',response=response)
            elif request.json:
                response=api_response(request)
                return jsonify(response)

        except Exception as e:
            print(e)
            error={"error":"Something went wrong"}
            return render_template("404.html",error=error)

    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
