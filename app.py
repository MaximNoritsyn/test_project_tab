from flask import Flask, render_template, redirect, request, abort
from settings import Telegram_bot_name
from database_connector import DatabaseConnector

database = DatabaseConnector()

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def index_page():
    return render_template('index.html', telegram_bot_name=Telegram_bot_name)


@app.route('/auth', methods=['GET'])
def auth():
    id = request.args.get('id')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    username = request.args.get('username')
    photo_url = request.args.get('photo_url')
    auth_date = request.args.get('auth_date')
    hash = request.args.get('hash')

    if not id:
        abort(400)

    user = database.users.find_one({'telegram_id': id})

    if not user:
        user = {
            'telegram_id': id,
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'photo_url': photo_url,
            'auth_date': auth_date,
            'hash': hash
        }
        database.users.insert_one(user)

    return render_template('profile.html', user=user)


if __name__ == '__main__':
    app.run()
