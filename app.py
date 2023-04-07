from flask import Flask, render_template, redirect, request, abort, Response
from settings import Telegram_bot_name, SECRET_KEY, ALGORITHM
from database_connector import DatabaseConnector
import jwt

database = DatabaseConnector()

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def index_page():
    return render_template('index.html', telegram_bot_name=Telegram_bot_name)


@app.route('/auth')
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

    access_token = jwt.encode({'telegram_id': id}, SECRET_KEY, algorithm=ALGORITHM)
    response = redirect('/profile')
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@app.route('/profile')
def profile():
    access_token = request.cookies.get("access_token")
    telegram_id = None
    if access_token:
        try:
            telegram_id = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM]).get('telegram_id')
        except:
            abort(401)
    else:
        abort(401)
    user = database.users.find_one({'telegram_id': telegram_id})
    if not user:
        abort(401)

    return render_template('profile.html', user=user)


if __name__ == '__main__':
    app.run()
