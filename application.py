# @app.after_request, @app.route("/", methods=["GET"]) and @app.route("/form", methods=["GET"]) were written by CS50
import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
# In case JS let something through, alerting user using this app
def post_form():
    # check validation of Name
    if not request.form.get("Name"):
        return render_template("error.html", message="You must provide your name!")
    # check validation of Prefix
    elif not request.form.get("Prefix"):
        return render_template("error.html", message="You must choose one of listed prefix!")
    # check validation of email
    elif not request.form.get("email"):
        return render_template("error.html", message="You must provide your email!")
    # check validation of education
    elif not request.form.get("education"):
        return render_template("error.html", message="You must provide your highest education grade!")
    # check validation of user's extra info
    elif not request.form.get("message"):
        return render_template("error.html", message="Please tell us briefly about yourself!")
    # if everything is fine, open and append the inputed and selected values in to the csv file
    file = open("survey.csv", "a")
    writer = csv.writer(file)
    writer.writerow((request.form.get("Name"), request.form.get("Prefix"), request.form.get("birth-date"),
                     request.form.get("email"), request.form.get("education"), request.form.get("message")))
    file.close()
    # redirect to the sheet.html
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
# render the inputed list from all users and add it into the table on the sheet.html
def get_sheet():
    # open and read the csv file
    file = open("survey.csv", "r")
    reader = csv.reader(file)
    inputed_survey = list(reader)
    file.close()
    return render_template("/sheet.html", inputed_survey=inputed_survey)
