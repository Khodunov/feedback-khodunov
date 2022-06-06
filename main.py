from flask import Flask, render_template, request
from telegram import Bot
from datetime import datetime

from lib.database import DatabaseDict, DatabaseJSON, DatabaseDatastore

# Flask application
app = Flask(__name__)

# Telegram bot
bot = Bot(token="5262077049:AAHD770jn0dnml4HWRG25i3pjAM2a00Tpzc")
admin_id = 289940489

# Database
database = DatabaseDatastore()


@app.route('/feedback')
def feedback():
    return render_template("main.html")


@app.route('/success', methods=['POST'])
def success():
    name = request.form['alias']
    subject = request.form['subject']
    message = request.form['message']
    database.add_note({
        'Имя отправителя': name,
        'Предмет': subject,
        'Сообщение': message,
        'Время': str(datetime.now())
    })

    bot.send_message(chat_id=admin_id, text=f"Новый фидбек, предмет: {subject}")
    return render_template("success.html")

@app.route('/send_updates_in_feedback')
def send_feedback():
    # достать из базы все отзывы
    all_feedback = database.get_feedback()

    # оставить сегодняшние
    today_feedback = []
    for feedback in all_feedback:
        if 'Время' in feedback:
            feedback_date = datetime.fromisoformat(feedback['Время']).date()
            if feedback_date == datetime.now().date():
                today_feedback.append(feedback)

    # отправить отзывы через бота
    if len(today_feedback) > 0:
        message = "Ежедневная сводка отзывов:"
        for j in range(len(today_feedback)):
            feedback = today_feedback[j]
            feedback_time = datetime.fromisoformat(feedback['Время']).strftime("%H:%M:%S")
            translations = {
                'python': "питон",
                'algebra': "алгебру",
                'analysis': "матан",
            }
            subject = translations[feedback['Предмет']]
            message = message + f"\n\n{j+1}). {feedback_time}\n" \
                                f"{feedback['Имя отправителя']} написал про " \
                                f"{subject}:\n" \
                                f"{feedback['Сообщение']}"
    else:
        message = "Сегодня новых отзывов не было :("

    bot.send_message(chat_id=admin_id, text=message)
    return "success"



if __name__ == '__main__':
    app.run(debug=True)
