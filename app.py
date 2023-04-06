from flask import Flask, render_template, redirect
from settings import Telegram_bot_name

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/telegram_registration')
def telegram_registration():
    return redirect(f"https://t.me/{Telegram_bot_name}")


if __name__ == '__main__':
    app.run()