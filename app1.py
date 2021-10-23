import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def weather_dashboard():
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']

    api_key = get_api_key()
    data = get_weather_results(zip_code, api_key)
    temp = data["main"]["temp"]
    temp="{0:.2f}".format((temp-32)*5/9)
    feels_like = data["main"]["feels_like"]
    feels_like= "{0:.2f}".format((feels_like-32)*5/9)
    weather = data["weather"][0]["main"]
    location = data["name"]
    country= data["sys"]["country"]
    return render_template('results.html',
                           location=location, temp=temp,
                           feels_like=feels_like, weather=weather, country=country)
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results(zip_code, api_key):
    api_url = "http://api.openweathermap.org/" \
              "data/2.5/weather?q={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


if __name__ == '__main__':
    app.run()
