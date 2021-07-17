from flask import Response
from flask import Flask, render_template, request
from flask_cors import CORS,cross_origin
from logistic_predict import predObj


logistic_app = Flask(__name__)
app = logistic_app
@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


class ClientApi:

    def __init__(self):
        self.predObj = predObj()

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def predictRoute():
    if request.method == 'POST':
        try:
         #reading the inputs given by the user
            age = float(request.form['age'])
            estimated_salary = float(request.form['estimated_salary'])
            data = {'age':age,'EstimatedSalary':estimated_salary}
            pred = predObj()
            result = pred.predict_log(data)
            print('Customer:',result)
            # showing the prediction results in a UI
            return render_template('results.html', Result=result)
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'

@app.route("/predict_postman", methods=['POST'])
def predictRoute_1():
    try:
        if request.json['data'] is not None:
            data = request.json['data']
            print('data is:     ', data)
            pred = predObj()
            res = pred.predict_log(data)
            print('result is        ', res)
            return Response(res)
    except ValueError:
        return Response("Value not found")
    except Exception as e:
        print('exception is   ', e)
        return Response(e)

#Data input via postman
# {
#   "data": [
#     {
#       "Age": 19,
#       "EstimatedSalary":19000
#       }
#   ]}

if __name__ == "__main__":
    clntApp = ClientApi()
    host = '0.0.0.0'
    port = 5000
    app.run(debug=True)
    #httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    #httpd.serve_forever()