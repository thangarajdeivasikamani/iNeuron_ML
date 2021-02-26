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

# If we didn't give method will default GET
# If we try with POST - we will get 405 error
@app.route('/test1',methods=['POST'])
def test1():
    return"Hello word test1"

@app.route('/test1/test2',methods=['POST'])
def test2():
    return"Hello word test1test2"

# If we didn't give method will default GET
# If we try with POST - we will get 405 error

@app.route('/testgetmethod')
def testgetmethod():
    return"Hello word testgetmethod"

@app.route('/testgetmethod1',methods=['GET'])
def testgetmethod1():
    return"Hello word testgetmethod1"

if __name__ == '__main__':
    app.run(debug=True)