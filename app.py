import pymongo
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://admin:admin@yam.3fsobk9.mongodb.net/?retryWrites=true&w=majority")
db = client["yam"]
registered_users = db["registered_users"]
token_received = db["token_received"]
authenticated = db["authenticated"]

global title
title = ""

global msgDisp
msgDisp = ""

@app.route("/", methods = ["GET", "POST"])
def index():
    global title
    title = ""

    global msgDisp
    msgDisp = ""

    try:
        if request.method == "POST":
            rollNo = request.form["rollNo"]

            rollNo = rollNo.replace(" ", "").upper()

            recordOld = token_received.find_one({'RollNo':rollNo})
            recordNew = authenticated.find_one({'RollNo':rollNo})

            if recordOld is not None and recordNew is None:
                if recordOld['Tokens'] == 1:
                    x = authenticated.insert_one({
                        "RollNo" : rollNo
                    })
                    title = "YES LUNCH | YAM"
                    msgDisp = "USER AUTHENTICATED SUCCESSFULLY !"
                    return redirect("/msgDisplay")
                else:
                    title = "NO LUNCH | YAM"
                    msgDisp = "USER HAS NOT OPTED FOR LUNCH !"
                    return redirect("/msgDisplay")
            elif recordNew is not None:
                title = "HAD LUNCH | YAM"
                msgDisp = "USER ALREADY HAD LUNCH !"
                return redirect("/msgDisplay")
            else:
                recordOld1 = registered_users.find_one({'RollNo':rollNo})
                if recordOld1 is not None and recordOld is None:
                    title = "QR NOT SCANNED | YAM"
                    msgDisp = "USER DID NOT SCAN QR CODE FOR LUNCH !"
                    return redirect("/msgDisplay")
                else:
                    title = "NOT REGISTERED | YAM"
                    msgDisp = "USER NOT REGISTERED FOR YAM !"
                    return redirect("/msgDisplay")
        else:
            return render_template("index.html")
    except:
        title = "404 ERROR | YAM"
        msgDisp = "404 ERROR. PAGE NOT FOUND !!!"
        return render_template("msgDisplay.html", title = title, msgDisp = msgDisp)

@app.route("/msgDisplay", methods = ["GET", "POST"])
def msgDisplay():
    global title
    global msgDisp

    try:
        if request.method == "POST":
            return redirect("/")
        else:
            return render_template("msgDisplay.html", title = title, msgDisp = msgDisp)
    except:
        title = "404 ERROR | YAM"
        msgDisp = "404 ERROR. PAGE NOT FOUND !!!"
        return render_template("msgDisplay.html", title = title, msgDisp = msgDisp)

@app.route('/<path>', methods = ["GET", "POST"])
def catchAll(path):
    try:
        if request.method == "POST":
            return redirect("/")
        else:
            return redirect("/")
    except:
        title = "404 ERROR | YAM"
        msgDisp = "404 ERROR. PAGE NOT FOUND !!!"
        return render_template("msgDisplay.html", title = title, msgDisp = msgDisp)

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        debug = False,
        port = 8080
    )