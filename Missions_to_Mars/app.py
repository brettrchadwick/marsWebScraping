from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app=Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")



@app.route("/")
def index():
    
    all_mars_info=mongo.db.all_mars_info.find_one()

    return render_template("index.html", all_mars_info=all_mars_info)


@app.route('/scrape')
def scrape():

    all_mars_info=mongo.db.all_mars_info
    new_data=scrape_mars.scrape_news()
    new_data=scrape_mars.scrape_image()
    new_data=scrape_mars.scrape_facts()
    new_data=scrape_mars.scrape_hemispheres()
    new_data=scrape_mars.scrape_weather()

    all_mars_info.update({}, new_data, upsert=True)

    return redirect("/", code=302)


if __name__=="__main__":
    app.run(debug=True)