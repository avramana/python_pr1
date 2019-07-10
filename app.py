from flask import Flask, render_template , request
import sqlite3
from send_email import sendmail

app = Flask(__name__)

class Database:
    def __init__(self,filename):
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS HEIGHT_DATA (id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL, height INTEGER NOT NULL)")
        self.conn.commit()

    def insert(self,email,height):
        print("insert email : ",email)
        self.cur.execute("INSERT INTO HEIGHT_DATA VALUES(NULL,?,?)",(email,height))
        self.conn.commit()

    def retrive(self):
#        self.cur.execute("DELETE FROM HEIGHT_DATA WHERE id = 5")
#        self.conn.commit()
        rows=self.cur.execute("SELECT * FROM HEIGHT_DATA")
        for item in rows.fetchall():
            print(item)

    def avgData(self):
        print("average Data")
        rows = self.cur.execute("SELECT COUNT(height), AVG(height) FROM HEIGHT_DATA")
        return rows.fetchall()

    def __del__(self):
        self.conn.close()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method == "POST":
        email=request.form["email_name"]
        height=request.form["height_name"]
        print(request.form)
        print("Email : ",email)
        print("Height : ", height)
        db = Database("height_collector.db")
        try:
            db.insert(email,height)
            avgdt=db.avgData()
            sendmail(email,height,avgdt[0][0],avgdt[0][1])
#            db.retrive()
            return render_template("success.html")
        except:
            return render_template("index.html",text="seems to be Duplicate mailid!")
    return render_template("index.html")

if __name__ == "__main__":
    app.debug=True
    app.run()