from flask import Flask, render_template
import pandas as pd
import numpy as np

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
station_display = stations[['STAID', 'STANAME                                 ']]

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", data=station_display.to_html())


@app.route("/api/<station>/<date>")
def details(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE'] == date]['    TG'].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": temperature}


@app.route("/api/<station>/")
def stat_det(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    info = df[['    DATE', '   TG']].to_html()
    return info


@app.route("/api/yearly/<station>/<year>")
def year_det(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(filename, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    info = df[df['    DATE'].str.startswith(str(year))]
    return info.to_html()


if __name__ == "__main__":
    app.run(debug=True)