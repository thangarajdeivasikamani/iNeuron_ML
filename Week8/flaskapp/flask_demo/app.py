from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# create the home or route ( like locahost:poprt)
# whenever call the route call the home_page method.
# Inside the template we have simple html code
# Inside the css will be store style,color & other required
@app.route('/', methods=['GET', 'POST']) # To render Homepage
def home_page():
    # render_template is default mehtod render the result
    return render_template('index.html')
# Inside the route we are calling math operation.
@app.route('/math', methods=['POST'])  # This will be called from UI
def math_operation():
    # If form send the POST method & then request from send num1 & Num2 data
    # Here request & return
    # We need to display the return result so here we are using result html page.
    # we can show the display even text,json format.
    # Here form help send the data ( Mean application)
    # Core calculaiton happen in python.
    # Then result we are displaying
    if (request.method=='POST'):
        # Call the request default method
        operation=request.form['operation']
        num1=int(request.form['num1'])
        num2 = int(request.form['num2'])
        if(operation=='add'):
            r=num1+num2
            result= 'the sum of '+str(num1)+' and '+str(num2) +' is '+str(r)
        if (operation == 'subtract'):
            r = num1 - num2
            result = 'the difference of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(r)
        if (operation == 'multiply'):
            r = num1 * num2
            result = 'the product of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(r)
        if (operation == 'divide'):
            r = num1 / num2
            result = 'the quotient when ' + str(num1) + ' is divided by ' + str(num2) + ' is ' + str(r)
        return render_template('results.html',result=result)
# I need to check with POST man,
# Supouse the need this output & re-use
# we can send the data in json format & display the result in json format
# Ensure  that while posting the json query in post man body the drop down selected as Json( Bellow Setting)
# Reference: https://pythonise.com/series/learning-flask/working-with-json-in-flaskhttps://pythonise.com/series/learning-flask/working-with-json-in-flaskhttps://pythonise.com/series/learning-flask/working-with-json-in-flaskhttps://pythonise.com/series/learning-flask/working-with-json-in-flaskhttps://pythonise.com/series/learning-flask/working-with-json-in-flask
@app.route('/via_postman', methods=['POST']) # for calling the API from Postman/SOAPUI
def math_operation_via_postman():
    if (request.method=='POST'):
        operation=request.json['operation']
        num1=int(request.json['num1'])
        num2 = int(request.json['num2'])
        if(operation=='add'):
            r=num1+num2
            result= 'the sum of '+str(num1)+' and '+str(num2) +' is '+str(r)
        if (operation == 'subtract'):
            r = num1 - num2
            result = 'the difference of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(r)
        if (operation == 'multiply'):
            r = num1 * num2
            result = 'the product of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(r)
        if (operation == 'divide'):
            r = num1 / num2
            result = 'the quotient when ' + str(num1) + ' is divided by ' + str(num2) + ' is ' + str(r)
        return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
