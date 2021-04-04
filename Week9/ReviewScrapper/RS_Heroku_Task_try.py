#Add logging part
#Add plotly & some graph

from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import itertools
import time
import pandas as pd
import json
import pymongo


app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ","")
        try:
            USR = "thangaraj"
            PWD = "Test#12345"
            # Connection URL
            #CONNECTION_URL = f"mongodb+srv://{USR}:{PWD}@cluster0.zvs9q.mongodb.net/{DB_NAME}?retryWrites=true&w=majority"
            CONNECTION_URL = "mongodb://localhost:27017/"  # opening a connection to Mongo  # opening a connection to Mongo
            try:
            # Establish a connection with mongoDB
                dbConn = pymongo.MongoClient(CONNECTION_URL)
                print("Connected successfully!!!")
            except:
                print("Could not connect to MongoDB")
            # Enter into collection Name
            dataBase = dbConn["Web_Scraping_Project"]  # Specifiy a Database Name
            collection = dataBase[searchString].find({})
            # check collection count
            if collection.count() > 500: # if there is a collection with searched keyword and it has records in it
                  return render_template('results1.html',reviews=collection) # show the results to user

            else:
                flipkart_url = "https://www.flipkart.com/search?q=" + searchString
                uClient = uReq(flipkart_url)
                flipkartPage = uClient.read()
                uClient.close()
                # Create a Collection Name
                collection = dataBase[searchString]
                review_soup = bs(flipkartPage, 'html.parser')
                pagesize_content = review_soup.find("div", {"class": "_2MImiq"})
                pagesize_content.prettify()
                pagesize_info = pagesize_content.span.contents[0]
                res = [int(i) for i in pagesize_info.split() if i.isdigit()]
                page_size = res[-1]
                page_size = 1
                print(page_size)
                for n in list(range(page_size)):
                    print("Entering into page:", n + 1)
                    product_scrap_data = [] # Create the list to store the final result
                    print("Pagesize****************:",n)
                    #Navigate the required page
                    page_url = "https://www.flipkart.com/search?q="+searchString+"+&amp%3Bas=on&amp%3Bas-show=on&amp%3Botracker=AS_Query_HistoryAutoSuggest_1_2_na_na_na&amp%3Botracker1=AS_Query_HistoryAutoSuggest_1_2_na_na_na&amp%3Bas-pos=1&amp%3Bas-type=HISTORY&amp%3BsuggestionId=samsung+&amp%3BrequestId=3deaa522-51bf-4a70-a7fc-d86c0a81128d&amp%3Bpage=4&page="+str(n)
                    eachpage = requests.get(page_url)
                    eachpages = bs(eachpage.content,'html.parser')
                    #Extratc the product size from the page
                    container = eachpages.find('span',attrs={"class":'_10Ermr'})
                    page_product_start_count=(int(container.text.split(' ')[1]))-1
                    page_product_end_count = (int(container.text.split(' ')[3]))
                    products_per_page = page_product_end_count-page_product_start_count
                    print("products_per_page:",products_per_page)

                    #Extratc the product list from that page
                    pre_product_name_list = ['None'] * products_per_page
                    product_name_list = []
                    try:
                        for container in  eachpages.findAll('a',href=True,attrs={"class":'_1fQZEK'}):
                            product_name_list.append(container.get('href').split('/')[1])
                    except:
                        product_name_list.append("Product name is not available")
                    pre_product_name_list[:len(product_name_list)] =               product_name_list[:min(len(pre_product_name_list),len(product_name_list))]
                    #print("product_name_list",len(pre_product_name_list))
                    product_name = pre_product_name_list
                    #print(product_name)

                    #Extarct the product rating
                    pre_product_rating_list = ['None'] * products_per_page
                    product_rating_list = []
                    try:
                        for container in eachpages.findAll('div',attrs={"class":'_3LWZlK'}):
                            product_rating_list.append(container.text)
                    except:
                        product_rating_list.append("Product rating is not available")
                    #Consider only poduct rating from the main list
                    pre_product_rating_list[:len(product_rating_list)] = product_rating_list[:min(len(pre_product_rating_list),len(product_rating_list))]
                    product_rating= pre_product_rating_list
                    #print("product_rating",len(product_rating))
                    #print(product_rating)

                    #Extarct the rating count & review count
                    pre_rating_counts_list = ['None'] * products_per_page
                    pre_review_counts_list = ['None'] * products_per_page
                    rating_counts_list = []
                    review_counts_list = []
                    try:
                        for container in eachpages.findAll('span',attrs={"class":'_2_R_DZ'}):
                            rating_counts_list.append((container.text.replace('\xa0','').split('&'))[0])
                            review_counts_list.append((container.text.replace('\xa0','').split('&'))[1])
                    except:
                        review_counts_list.append("Product review count is not available")
                        rating_counts_list.append("Product rating count is not available")
                    pre_rating_counts_list[:len(rating_counts_list)] = rating_counts_list[:min(len(pre_rating_counts_list),len(rating_counts_list))]
                    pre_review_counts_list[:len(review_counts_list)] = review_counts_list[:min(len(pre_review_counts_list),len(review_counts_list))]
                    #print("rating_counts_list",len(pre_rating_counts_list))
                    #print("review_counts_list",len(pre_review_counts_list))
                    rating_counts = pre_rating_counts_list
                    review_counts = pre_rating_counts_list
                    #print(rating_counts)
                    #print(review_counts)


                    #Extarct the product description
                    pre_product_description_list = ['None'] * products_per_page
                    product_description_list = []
                    try:
                        for container in eachpages.findAll('ul',attrs={"class":'_1xgFaf'}):
                            product_description_list.append(container.text)
                    except:
                        product_description_list.append("Product description is not available")
                    pre_product_description_list[:len(product_description_list)] = product_description_list[:min(len(pre_product_description_list),len(product_description_list))]
                    #print(len(pre_product_description_list))
                    product_description = pre_product_description_list
                    #print(product_description)

                    #Extarct the offer price
                    pre_offer_price_list = ['None'] * products_per_page
                    offer_price_list =[]
                    try:
                        for container in eachpages.findAll('div',attrs={"class":'_30jeq3 _1_WHN1'}):
                            offer_price_list.append(container.text)
                    except:
                        offer_price_list.appned("Product offer_price is not available")
                    pre_offer_price_list[:len(offer_price_list)] = offer_price_list[:min(len(pre_offer_price_list),len(offer_price_list))]
                    #print(len(pre_offer_price_list))
                    offer_price = pre_offer_price_list
                    #print(offer_price)

                    #Extarct the actual price
                    pre_actual_price_list = ['None'] * products_per_page
                    actual_price_list = []
                    try:
                        for container in eachpages.findAll('div',attrs={"class":'_3I9_wc _27UcVY'}):
                            actual_price_list.append(container.text)
                        actual_price_list = actual_price_list[0:page_product_count[0]]
                    except:
                        actual_price_list.append("Product actual_price is not available")
                    pre_actual_price_list[:len(actual_price_list)] = actual_price_list[:min(len(pre_actual_price_list),len(actual_price_list))]
                    #print("length of price list",len(pre_actual_price_list))
                    #print(actual_price_list)
                    actual_price = pre_actual_price_list
                    #print(actual_price)

                    #Extarct the offer percentage
                    pre_offer_percentage_list = ['None'] * products_per_page
                    offer_percentage_list = []
                    try:
                        for container in eachpages.findAll('div',attrs={"class":'_3Ay6Sb'}):
                            offer_percentage_list.append(container.text)
                        offer_percentage_list = offer_percentage_list[0:page_product_count[0]]
                    except:
                        offer_percentage_list.append("Product offer_percentage is not available")
                    pre_offer_percentage_list[:len(offer_percentage_list)] = offer_percentage_list[:min(len(pre_offer_percentage_list),len(offer_percentage_list))]
                    #print(len(pre_offer_percentage_list)
                    offer_percentage = pre_offer_percentage_list
                    #print(offer_percentage)

                    # Extarct the top level class content
                    container = eachpages.findAll("div", {"class": "_1YokD2 _3Mn1Gg"})
                    # print(len(raw_bigboxes))
                    # Navigate to product list section
                    raw_bigboxes = container[1].findAll("div", {"class": "_1AtVbE col-12-12"})
                    # print(len(bigboxes))
                    # Eliminate the last two uncessary product info link
                    bigboxes = raw_bigboxes[: len(raw_bigboxes) - 2]
                    # print(len(bigboxes))
                    review_list = []
                    for i in list(range(products_per_page)):
                        print("Entering into product", i + 1)
                        box = bigboxes[i]
                        productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
                        prodlink_info = requests.get(productLink)
                        prod_detail_info_html = bs(prodlink_info.content,'html.parser')

                        # Function to extarct the product info
                        def product_info_finder(tag_name, class_name, required_info):
                            try:
                                for container in prod_detail_info_html.find(tag_name, attrs={"class": class_name}):
                                    return container.text
                            except:
                                return required_info + " data is not available"

                                # Extarct the offer difference

                        offer_difference = (product_info_finder('div', '_1V_ZGU', 'offer_difference'))
                        # print(offer_difference)

                        # Extarct the avaliable offer
                        avaliable_offer = (product_info_finder('div', '_3TT44I', 'avaliable_offer'))

                        # Extarct the warrenty info
                        warranty_info = (product_info_finder('div', 'XcYV4g', 'warranty_info'))
                        # print(warranty_info)

                        # Extarct the highlights_info
                        highlights_info = (product_info_finder('div', '_2418kt', 'highlights_info'))
                        # print(highlights_info)

                        # Extarct the easy payment info
                        easy_payment_info = (product_info_finder('div', '_250Jnj', 'easy_payment_info'))
                        # print(easy_payment_info)

                        # Extarct the seller info
                        seller_info = (product_info_finder('div', '_1RLviY', 'seller_info'))
                        # print(seller_info)

                        # Extarct the description_info
                        description_info = (product_info_finder('div', '_2o-xpa', 'description_info'))
                        # print(description_info)

                        # Extarct the product specification
                        product_spec = []
                        try:
                            for containers in prod_detail_info_html.findAll('div', attrs={"class": '_3k-BhJ'}):
                                summary = containers.findAll('table', attrs={"class": '_14cfVK'})
                                for items in summary:
                                    rows = items.findAll('tr')
                                    product_spec.append(
                                        [':'.join([td.findNext(text=True) for td in tr.findAll("td")]) for tr in rows])
                        except:
                            product_spec.append("product_specification is not available")
                        product_spec_jointed = itertools.chain(*product_spec)
                        # Join the list item into single string
                        product_specification = (' '.join(product_spec_jointed))

                        # print(product_specification)

                        # function to extract the review details
                        def review_info_finder(tag_name, class_name, required_info):
                            try:
                                commentbox = prod_detail_info_html.find('div', {'class': "_16PBlm"})
                                tag_result = commentbox.find(tag_name, attrs={"class": class_name})
                                return tag_result.text
                            except:
                                return required_info + " data is not available"

                                # Extarct the Reviewer name

                        reviewer_name = (review_info_finder('p', '_2sc7ZR _2V5EHH', 'reviewer_name'))
                        # print(reviewer_name)

                        # Extarct the reviewer_rating
                        reviewer_rating = (review_info_finder('div', '_3LWZlK _1BLPMq', 'reviewer_rating'))
                        # print(reviewer_rating)

                        # Extract the comment_heading
                        comment_heading = (review_info_finder('p', '_2-N8zT', 'comment_heading'))
                        # print(comment_heading)

                        # Extarct the review_comments
                        review_comments = (review_info_finder('div', 't-ZTKy', 'review_comments'))
                        # print(review_comments)

                        # Extract the thumps up
                        try:
                            commentbox = prod_detail_info_html.find('div', {'class': "_16PBlm"})
                            thumsup = (commentbox.div.div.find_all('span', {'_3c3Px5'})[0].text)
                        except:
                            thumsup = 'Thumsup data is not avaliable'
                        # print(thumsup)

                        # Extarct the thumpsdown
                        try:
                            commentbox = prod_detail_info_html.find('div', {'class': "_16PBlm"})
                            thumsdown = (commentbox.div.div.find_all('span', {'_3c3Px5'})[1].text)
                        except:
                            thumsdown = 'Thumsdown data is not avaliable'
                        # print(thumsdown)
                        mydict = {"Product_Name": product_name[n], "Product_Rating": product_rating[n],
                                  "Rating_Counts": rating_counts[n],
                                  "Review_Counts": review_counts[n],
                                  "Product_Description": product_description[n],
                                  "Offer_Price": offer_price[n],
                                  "Actual_Price": actual_price[n], "Offer_Percentage": offer_percentage[n],
                                  "Offer_Difference": offer_difference,
                                  "Avaliable_Offer": avaliable_offer, "Warranty_Info": warranty_info,
                                  "Highlights_Info": highlights_info,
                                  "Easy_Payment_Info": easy_payment_info, "Seller_Info": seller_info,
                                  "Description_Info": description_info,
                                  "Product_Specification": product_specification, "Reviewer_Name": reviewer_name,
                                  "Reviewer_Rating": reviewer_rating, "Comment_Heading": comment_heading,
                                  "Review_Comments": review_comments, "Thums-Up": thumsup, "Thums_Down": thumsdown}

                        review_list.append(mydict)
                    table = dataBase[searchString]
                    # print(db.list_collection_names())
                    col_exists = searchString in dataBase.list_collection_names()
                    if col_exists == True:
                        table = dataBase[searchString]
                        table.drop  # drop the existing collection
                    table = dataBase[searchString]  # creating a collection with the same name as search string. Tables and Collections are analogous.
                    time.sleep(1)
                    table.insert_many(review_list)  # insertig the dictionary containing the rview comments to the collection
                    time.sleep(1)
                    return render_template('results1.html', reviews=review_list)
        except:
                return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)
