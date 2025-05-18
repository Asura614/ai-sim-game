from flask import Flask, request, render_template, redirect, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

players = {}

class Player:
    def __init__(self, username):
        self.username = username
        self.money = 1000
        self.products = 0
        self.marketing = 0
        self.employees = 0
        self.premium = username.endswith("++")

    def take_action(self, action):
        if action == "produce" and self.money >= 50:
            self.products += 10
            self.money -= 50
        elif action == "market" and self.money >= 100:
            self.marketing += 1
            self.money -= 100
        elif action == "hire" and self.money >= 200:
            self.employees += 1
            self.money -= 200
        self.earn_income()

    def earn_income(self):
        income = (self.products * (1 + 0.1 * self.marketing)) * (1 + 0.05 * self.employees)
        if self.premium:
            income *= 1.2
        self.money += income
        self.products = 0

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["username"] = username
        if username not in players:
            players[username] = Player(username)
        return redirect("/home")
    return render_template("login.html")

@app.route("/home")
def home():
    username = session.get("username")
    if not username or username not in players:
        return redirect("/")
    player = players[username]
    return render_template("home.html", username=username, player=player)

@app.route("/action", methods=["POST"])
def action():
    username = session.get("username")
    if not username or username not in players:
        return redirect("/")
    action = request.form["action"]
    players[username].take_action(action)
    return redirect("/home")

if __name__ == "__main__":
    app.run(debug=True)
