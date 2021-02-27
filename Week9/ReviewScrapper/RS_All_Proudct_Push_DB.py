from flask import Flask, render_template, request,jsonify
#from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import numpy as np
import time
import pandas as pd
import pymongo
# Intreact with two different hetrogenious system
app = Flask(__name__)  # initialising the flask app with the name 'app'

@app.route('/', methods=['POST','GET'])
def homepage():
    return render_template('index.html')

# base url + /
#http://localhost:8000 + /
# GET- URL (Every one can see)
# POST - BODY
@app.route('/scrap',methods=['POST']) # route with allowed methods as POST and GET
def index():
    if request.method == 'POST':
        # Request type multiple depends on me txt,json or Form ( web pages)
        # Home page typing content will be consider(e.g iphone)
        # If we enter space consider as null
        searchString = request.form['content'].replace(" ","") # obtaining the search string entered in the form
        try:
            # dbConn = pymongo.MongoClient("mongodb://localhost:27017/")  # opening a connection to Mongo
            # db = dbConn['Flipkart_review'] # connecting to the database called Flipkart_review
            # reviews = db[searchString].find({}) # searching the collection with the name same as the keyword
            # if reviews.count() > 0: # if there is a collection with searched keyword and it has records in it
            #     return render_template('results.html',reviews=reviews) # show the results to user
            # else:
                dbConn = pymongo.MongoClient("mongodb://localhost:27017/")  # opening a connection to Mongo
                db = dbConn['Flipkart_review']  # connecting to the database called Flipkart_review
                flipkart_url = "https://www.flipkart.com/search?q=" + searchString # preparing the URL to search the product on flipkart
                uClient = uReq(flipkart_url) # requesting the webpage from the internet
                flipkartPage = uClient.read() # reading the webpage
                uClient.close() # closing the connection to the web server
                flipkart_html = bs(flipkartPage, "html.parser") # parsing the webpage as HTML
                raw_bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"}) # seacrhing for appropriate tag to redirect to the product link
                bigboxes=raw_bigboxes[: len(raw_bigboxes)-5] # Delete last unwanted items
                del bigboxes[0:3] # the first 3 members of the list do not contain relevant information, hence deleting them.
                reviews =[]
                no_of_product_per_page=list(range(len(bigboxes)))
                #print('No_of_product_per_page',(len(bigboxes)))
                for i in no_of_product_per_page:
                    #print('Iterations:',i)
                    box = bigboxes[i] #  taking the first iteration (for demo)
                    productLink = "https://www.flipkart.com" + box.div.div.div.a['href'] # extracting the actual product link
                    prodRes = requests.get(productLink) # getting the product page from server
                    prod_html = bs(prodRes.text, "html.parser") # parsing the product page as HTML
                    commentboxes = prod_html.find_all('div', {'class': "_16PBlm"}) # finding the HTML section containing the customer comments
                    # Initially the dabase not avaliable, Here are we are searching, addinting into table
                    #filename = searchString+".csv" #  filename to save the details
                    #fw = open(filename, "w") # creating a local file to save the details
                    #headers = "Product, Customer Name, Rating, Heading, Comment \n" # providing the heading of the columns
                    #fw.write(headers) # writing first the headers to file
                    #  iterating over the comment section to get the details of customer and their comments
                    #print(reviews)
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
                        #fw.write(searchString+","+name.replace(",", ":")+","+rating + "," + commentHead.replace(",", ":") + "," + custComment.replace(",", ":") + "\n")
                        mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                                  "Comment": custComment} # saving that detail to a dictionary
                        reviews.append(mydict) #  appending the comments to the review list
                        time.sleep(1)
                    #print('Reviews length:',len(reviews))
                # columns =['Product','Name','Rating','CommentHead','Comment']
                # df =pd.DataFrame(reviews,columns)
                # print(df.size)
                #print(searchString)
                table = db[searchString]
                #print(db.list_collection_names())
                col_exists = searchString in db.list_collection_names()
                if col_exists == True:
                    table = db[searchString]
                    table.drop  # drop the existing collection
                table = db[searchString]  # creating a collection with the same name as search string. Tables and Collections are analogous.
                time.sleep(2)
                table.insert_many(reviews)  # insertig the dictionary containing the rview comments to the collection
                time.sleep(2)
                return render_template('results.html', reviews=reviews) # showing the review to the user

        except:
            return 'something is wrong'
            #return render_template('results.html')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(port=8000,debug=True) # running the app on the local machine on port 8000