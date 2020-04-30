from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
# mongo = PyMongo(app)

# Or set inline
mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():

    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scraper():
    
    mars_data = mongo.db.mars_data
    # Run scrape function
    mars_new = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mars_data.update({}, mars_new, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)