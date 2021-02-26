import sys
from flask import Flask, render_template, request, jsonify
print(sys.executable)
print(sys.version)
print(sys.version_info)
#Create the flask object
app = Flask("__name__")
# Give any url name & created simple route
@app.route('/thanga',methods=['POST'])
def test():
    return"Hello word"

# If we didn't give method will take default as GET method
# If we try with POST - we will get 405 error
@app.route('/test1',methods=['POST'])
def test1():
    return"Hello word test1"
# Creat the route with deep path
@app.route('/test1/test2',methods=['POST'])
def test2():
    return"Hello word test1test2"

# If we didn't give method will default GET
# If we try with POST - we will get 405 error

@app.route('/testgetmethod')
def testgetmethod():
    return"Hello word testgetmethod"
# Create the route with GET Method
@app.route('/testgetmethod1',methods=['GET'])
def testgetmethod1():
    return"Hello word testgetmethod1"
# alternate to Decorator. Bind the URL using app.add_url_rule with helo word method
def hello_world():
   return ‘hello world’
app.add_url_rule(‘/’, ‘hello’, hello_world)

if __name__ == '__main__':
    app.run(debug=True)
