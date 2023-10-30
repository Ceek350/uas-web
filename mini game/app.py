from flask import Flask, render_template
from flask import jsonify

app = Flask(__name__)

class Start:
    def __init__(self):
        self.playerName = "Player"
        self.botName = "Diibot"
        self.playerOption = None
        self.botOption = None
        self.winner = ""

    def getBotOption(self):
        return self.botOption

    def setBotOption(self, option):
        self.botOption = option

    def getPlayerOption(self):
        return self.playerOption

    def setPlayerOption(self, option):
        self.playerOption = option

    def botBrain(self):
        import random
        option = ["🖐", "✌", "✊"]
        bot = random.choice(option)
        return bot

    def winCalculation(self):
        if self.botOption == "🖐" and self.playerOption == "✌":
            self.winner = self.playerName
        elif self.botOption == "🖐" and self.playerOption == "✊":
            self.winner = self.botName
        elif self.botOption == "✌" and self.playerOption == "🖐":
            self.winner = self.botName
        elif self.botOption == "✌" and self.playerOption == "✊":
            self.winner = self.playerName
        elif self.botOption == "✊" and self.playerOption == "🖐":
            self.winner = self.playerName
        elif self.botOption == "✊" and self.playerOption == "✌":
            self.winner = self.botName
        else:
            self.winner = "SERI"


    def matchResult(self):
        if self.winner != "SERI":
            return f"{self.winner} MENANG!"
        else:
            return f"WAAA SAMA BROO 🤪"

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/pick_option/<option>')
def pick_option(option):
    start = Start()
    start.setPlayerOption(option)
    start.setBotOption(start.botBrain())
    start.winCalculation()

    inGame = f"{start.getPlayerOption()} VS {start.getBotOption()}"
    result = start.matchResult()

    return render_template('index.html', inGame=inGame, result=result)


if __name__ == '__main__':
    app.run(debug=True)
