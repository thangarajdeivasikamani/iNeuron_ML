# doing necessary imports
# For bulk lib installtion use pip install -r requirements.txt
# If permission issue use pip install --user -r requirements.txt
# Steps
"""
Steps
1. website
2. search
3. result
4. info (Selected) Ratings and reviews
5. Scraping
6. Done

"""
from flask import Flask, render_template, request,jsonify
#from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
# Intreact with two different hetrogenious system
app = Flask(__name__)  # initialising the flask app with the name 'app'

@app.route('/', methods=['POST','GET'])
def homepage():
    return render_template('index.html')

# base url + /
#http://localhost:8000 + /
# GET- URL
# POST - BODY
@app.route('/scrap',methods=['POST']) # route with allowed methods as POST and GET
def index():
    if request.method == 'POST':
        # Request type multiple depends on me txt,json or Form ( web pages)
        # Home page typing content will be consider(e.g iphone)
        # If we enter space consider as null
        searchString = request.form['content'].replace(" ","") # obtaining the search string entered in the form
        try:
            # User typed string we are concate with flipkart URL
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString # preparing the URL to search the product on flipkart
            # Using U request pass the URL previously prepared
            uClient = uReq(flipkart_url) # requesting the webpage from the internet
            flipkartPage = uClient.read() # reading the webpage
            uClient.close() # closing the connection to the web server
            # BeautifulSoup will create the beatiful structure
            flipkart_html = bs(flipkartPage, "html.parser") # parsing the webpage as HTML
            # Go to particular class using inspect & find all product
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"}) # seacrhing for appropriate tag to redirect to the product link
            # From that may be we have multiple class - del uncessary
            del bigboxes[0:3] # the first 3 members of the list do not contain relevant information, hence deleting them.
            box = bigboxes[0] #  taking the first iteration (for demo)
            # Go each product we need to hit create the link
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href'] # extracting the actual product link
            # next pass the URL & beautify.
            prodRes = requests.get(productLink) # getting the product page from server
            prod_html = bs(prodRes.text, "html.parser") # parsing the product page as HTML
            # Again we have multiple section,we need to filter review comments
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"}) # finding the HTML section containing the customer comments

            # table = db[searchString] # creating a collection with the same name as search string. Tables and Collections are analogous.
            #filename = searchString+".csv" #  filename to save the details
            #fw = open(filename, "w") # creating a local file to save the details
            #headers = "Product, Customer Name, Rating, Heading, Comment \n" # providing the heading of the columns
            #fw.write(headers) # writing first the headers to file
            reviews = [] # initializing an empty list for reviews
            #  iterating over the comment section to get the details of customer and their comments
            for commentbox in commentboxes:
                # If it's writen review in paragraph take
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
                # From the result we are creating the own dict
                #fw.write(searchString+","+name.replace(",", ":")+","+rating + "," + commentHead.replace(",", ":") + "," + custComment.replace(",", ":") + "\n")
                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment} # saving that detail to a dictionary
                # Insert the data into tabel database
                # If we more than 1000 record how to insert check
                # While display we can use limit
                # x = table.insert_one(mydict) #insertig the dictionary containing the rview comments to the collection
                reviews.append(mydict) #  appending the comments to the review list
            # Disply the result using result html template
            return render_template('results.html', reviews=reviews) # showing the review to the user
        except:
            return 'something is wrong'

# Initial point to start executing
if __name__ == "__main__":
    app.run(port=8000,debug=True) # running the app on the local machine on port 8000