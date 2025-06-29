

import os
from flask import Flask, redirect, session, url_for
from authlib.integrations.flask_client import OAuth

from article_format import get_unknown_words, reformat_article
from student_word_db import get_student_words
from user_integration import format_random_article, get_user_articles
from web_scrape import scrape_article


app = Flask(__name__)
app.secret_key = os.urandom(24)
oauth = OAuth(app)

oauth.register(
  name='oidc',
  authority='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_gvDkP1mei',
  client_id='757nogd3k0vs0cfpem0pqcoc7s',
  client_secret='189psgmpep4844tv81q2ffl6domja9r033pu1599bt17b86mc42p', #TODO Remove this
  server_metadata_url='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_gvDkP1mei/.well-known/openid-configuration',
  client_kwargs={'scope': 'phone openid email'}
)


@app.route('/')
def index():
    user = session.get('user')
    
    if user:
        return f'Hello, {user['sub']}<a href="/logout">Logout</a>'
    else:
        return f'Welcome! Please <a href="/login">Login</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    print('Redirect URI', redirect_uri)
    return oauth.oidc.authorize_redirect(redirect_uri)

@app.route('/articles')
def articles():
    with open('resources/article_page.html') as file:
        return file.read()

@app.route('/user_article_list')
def user_article_list():
    user = session.get('user')
    
    if user:
        user_id = user['sub']
        user_articles = get_user_articles(user_id, 10)
        return user_articles
        


    return '404'

@app.route('/paragraph')
def paragraph():
    user = session.get('user')
    
    if user:
        user_id = user['sub']
        known_words = get_student_words(user_id)
        article_url = 'https://news.qq.com/rain/a/20250622A05FZU00'
        article = scrape_article(article_url)
        reformatted_article = reformat_article(article, known_words)

        new_words = get_unknown_words(reformatted_article, known_words)
        return f'{reformatted_article}{'<br>'*3}{' '.join(new_words)}'

@app.route('/create', methods = ['POST'])
def create():
    user = session.get('user')
    print('Got here')
    if user:
        user_id = user['sub']
        print(user_id)
        format_random_article(user_id)
    return ':)'

@app.route('/authorize')
def authorize():
    print('Got here')
    token = oauth.oidc.authorize_access_token()
    user = token['userinfo']
    print('Authorized user:', user)
    session['user'] = user
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    print('Logout')
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)