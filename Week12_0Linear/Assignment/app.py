
# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle
import pandas as pd
from pandas.core.common import flatten
from sklearn.preprocessing import StandardScaler


app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            crim = float(request.form['CRIM'])
            #print(crim)
            zn = float(request.form['ZN'])
            #print(zn)
            indus = float(request.form['INDUS'])
            #print(indus)
            nox = float(request.form['NOX'])
            #print(nox)
            rm = float(request.form['RM'])
            #print(rm)
            age = float(request.form['AGE'])
            #print(age)
            dis = float(request.form['DIS'])
            #print(dis)
            rad = float(request.form['RAD'])
            #print(rad)
            tax = float(request.form['TAX'])
            #print(tax)
            ptratio = float(request.form['PTRATIO'])
            #print(ptratio)
            b = float(request.form['B'])
            #print(b)
            lstat = float(request.form['LSTAT'])
            #print(lstat)
            is_chas = request.form['chas']
            if (is_chas == 'yes'):
                chas = 1
            else:
                chas = 0
            #print(chas)
            data = [crim,zn,indus,chas,nox,rm,age,dis,rad,tax,ptratio,b,lstat]
            df = pd.DataFrame(data)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(df)
            #Flatten the list
            X_scaled_flat_list =list(flatten(X_scaled))
            #X_scaled_flat_list = [item for sublist in X_scaled for item in sublist]
            #print(X_scaled_flat_list)
            filename = 'finalized_predict_model.pickle'
            loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # predictions using the loaded model file
            prediction=loaded_model.predict([X_scaled_flat_list])
            print('prediction is', prediction)
            # # showing the prediction results in a UI
            return render_template('results.html',prediction=prediction)
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')



if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app