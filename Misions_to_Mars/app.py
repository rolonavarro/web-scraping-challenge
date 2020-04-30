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
    
    # Run scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # redirect back to homepage
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)