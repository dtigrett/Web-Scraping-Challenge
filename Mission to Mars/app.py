#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo
import scrape_mars



app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Connect to a database. Will create one if not already available.
#db = client.team_db

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def index(): 

    # Find data
    mars_info = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrape functions
    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_image()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_hemispheres()
    mars_info.update({}, mars_data, upsert=True)


    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)






# In[ ]:





# In[ ]:




