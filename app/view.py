from app.app import app
from flask import render_template, redirect, url_for, Markup, request
from app.mage import Mage
from const import Const
import os
from essense.user import User


@app.route('/')
def index():
    return render_template('index.html', name='index', sockets=True)


@app.route('/register')
def register(error={}):
    return render_template('register.html', name='register', no_header=True, error=error)


@app.route('/login')
def login():
    if Mage().action_user():
        return redirect(url_for('index'))
    
    return render_template('login.html', name='login', no_header=True)


@app.route('/message', methods=['POST', 'GET'])
def message():
    type_message = request.args.get('type')
    user_data = User().get_user_info()

    if not type_message:
        return redirect(url_for('index'))

    mes = ''

    if type_message == 'registration':
        if not Mage().action_user():
            return redirect(url_for('index'))

        mes = {
            "title": "Спасибо за регистрацию!",
            "body": Markup('''
                <p class="message__text message__text_center">Мы рады видеть нового пользователя нашего приложения!</p>
                <p class="message__text message__text_center message__text_middle-margin">Данные по адресам ниже 
                ни в коем случае нельзя терять, они будут необходимы для дальнейщего входа в систему. 
                При их потере вы не сможете получить доступ к аккаунту и восстановить его.</p>
                <p class="message__text">Ваш адрес в сети лежит в файле: <span class="message__undertext">{0}</span></p>
                <p class="message__text">Ваши ключи находятся в директории: <span class="message__undertext">{1}</span></p>
                '''.format(Const.PATH_TO_ADDRESS,
                           Const.PATH_TO_KEYS
                           ))
        }

    if not mes:
        return redirect(url_for('index'))

    return render_template('message.html', name='message', message=mes)


@app.route('/admin')
def admin():
    if not Mage().action_user():
        return redirect(url_for('login'))

    return render_template('admin.html', name='admin')


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('index'))

