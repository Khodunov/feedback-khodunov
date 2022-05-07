from flask import Flask, render_template
from telegram import Bot

app = Flask(__name__)

bot = Bot(token="5262077049:AAHD770jn0dnml4HWRG25i3pjAM2a00Tpzc")
admin_id = 289940489


@app.route('/feedback')
def feedback():
    return render_template("main.html")


@app.route('/success')
def success():
    return render_template("success.html")


@app.route('/submit', method=['POST'])
def submit(alias, subject, message):
    bot.send_message(chat_id=admin_id, text=message)
    print(message)


if __name__ == '__main__':
    app.run(debug=True)
