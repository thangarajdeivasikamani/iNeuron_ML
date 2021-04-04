from flask import Flask, render_template, request,jsonify
#from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)  

@app.route('/', methods=['POST','GET'])
def homepage():
    return render_template('index.html')

@app.route('/scrap',methods=['POST']) 
def index():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ","")
        try:
            
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString             
            uClient = uReq(flipkart_url) 
            flipkartPage = uClient.read() 
            uClient.close() 
            flipkart_html = bs(flipkartPage, "html.parser") 
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"}) 
            del bigboxes[0:3] 
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink) 
            prod_html = bs(prodRes.text, "html.parser") 
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"}) 
            reviews = [] 
            for commentbox in commentboxes:
                try:
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text

                except:
                    name = 'No Name'

                try:
                    rating = commentbox.div.div.div.div.text

                except:
                    rating = 'No Rating'

                try:
                    commentHead = commentbox.div.div.div.p.text
                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    custComment = comtag[0].div.text
                except:
                    custComment = 'No Customer Comment'

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment} # saving that detail to a dictionary
                reviews.append(mydict) #  appending the comments to the review list
            # Disply the result using result html template
            return render_template('results.html', reviews=reviews) # showing the review to the user
        except:
            return 'something is wrong'

# Initial point to start executing
if __name__ == "__main__":
    app.run(port=8000,debug=True) # running the app on the local machine on port 8000
