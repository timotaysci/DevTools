from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth
import config

# Create the app
app = Flask(__name__)
app.secret_key = config.secret_key

oauth = OAuth(app)

#Google OAuth things - check README.md for what setting should be in the portal
google = oauth.remote_app(
    'google',
    consumer_key=config.your_google_client_id,
    consumer_secret=config.your_google_client_secret,
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


#define index route
@app.route('/')
def index():
    # Check if user is logged in
    if 'google_token' in session:
        #get user info
        me = google.get('userinfo')
        return 'Logged in as: {}'.format(me.data['email'])
    #if not send to login route
    return redirect(url_for('login'))


@app.route('/login')
def login():
    #redirect to OAuth
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    # Remove token from session on logout
    session.pop('google_token', None)
    return 'Logged out'



@app.route('/login/authorized')
def authorized():
    #check if authorized 
    resp = google.authorized_response()
    if resp is None:
        # If not, error this
        return 'Access denied: reason={}&error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    return redirect(url_for('index'))


# define tokengetter
@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

# Run app
if __name__ == '__main__':
    app.run(debug=True)
