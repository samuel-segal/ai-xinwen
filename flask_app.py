

import os
from flask import Flask, redirect, session, url_for
from authlib.integrations.flask_client import OAuth


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
    print(user)
    if user:
        return f'Hello, {user['email']}. <a href="/logout">Logout</a>'
    else:
        return f'Welcome! Please <a href="/login">Login</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    print(redirect_uri)
    return oauth.oidc.authorize_redirect(redirect_uri)

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