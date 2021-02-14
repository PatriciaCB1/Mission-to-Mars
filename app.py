# Use Flask to render template, PyMongo to interact with MongoDB, use scraping code import from Jupyter notebook to Python

from flask import Flask, render_template
from flask_pymongo import PyMongo
import web_scraping

# Add to Flask set up
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the route to the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Add next route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = web_scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()