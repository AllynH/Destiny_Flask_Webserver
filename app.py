from flask import Flask, abort, request, redirect, url_for, render_template, session
from datetime import datetime, timedelta
import pickle
import requests
import requests.auth
import json
from OpenSSL  import SSL
import time
from flask_bootstrap import Bootstrap
from Inventory_Management import *
import urllib

# initialise the app:
app = Flask(__name__)
app.secret_key = 'Put-your-key-here'
bootstrap = Bootstrap(app)

oauth_session = requests.Session()

# Add you API-KEY-HERE!
API_KEY = YOUR-API-KEY
HEADERS = {"X-API-Key": API_KEY }

REDIRECT_URI		=	'https://localhost:5000/callback/playstation'
AUTH_URL			= 	'https://www.bungie.net/en/Application/Authorize/11487?'
access_token_url 	=	'https://www.bungie.net/Platform/App/GetAccessTokensFromCode/'
refresh_token_url	=	'https://www.bungie.net/Platform/App/GetAccessTokensFromRefreshToken/'

# Open Manifest:
print "Opening Manifest..."
with open('manifest.pickle', 'rb') as data:
	all_data = pickle.load(data)
print "Finished!"

@app.route('/')
@app.route('/index')
def index():
	state =  make_authorization_url()
	state_params = {'state': state}
	url = AUTH_URL + urllib.urlencode(state_params)
	print url
	return render_template('index.html', url=url)

@app.route('/vault')
def vault():
	account = getAccount(oauth_session)
	userSummary = GetCurrentBungieAccount(oauth_session)
	charSummary = GetCharacterSummary(oauth_session)
	return render_template('vault.html', 
							character=userSummary.json()['Response']['user']['displayName'], 
							lightLevel = charSummary.json()['Response']['data']['characterBase']['stats']['STAT_LIGHT']['value'],
							emblemImage = account.json()['Response']['data']['characters'][0]['emblemPath'],
							backgroundImage = account.json()['Response']['data']['characters'][0]['backgroundPath'],
							) 

def make_authorization_url():
	# Generate a random string for the state parameter
	# Save it for use later to prevent xsrf attacks
	from uuid import uuid4
	state = str(uuid4())
	save_created_state(state)
	return state

@app.route('/callback/bungie')
def bungie_callback():
	error = request.args.get('error', '')
	if error:
		return "Error: " + error
	state = session.get('state_token')
	if not is_valid_state(state):
		## Uh-oh, this request wasn't started by us!
		print "Uh-oh, this request wasn't started by us!"
		abort(403)
	session.pop('state_token', None)
	code = request.args.get('code')
	authorisation_code = code
	token = get_token(code)
	return redirect(url_for('index'))
	
def get_token(code):
	post_data = {'code': code}
	response = requests.post(access_token_url, json=post_data, headers=HEADERS)
	token_json = response.json()['Response']['accessToken']['value']
	refresh_json = response.json()['Response']['refreshToken']['value']
	refresh_ready = datetime.now() + timedelta(seconds=int(response.json()['Response']['refreshToken']['readyin']))
	refresh_expired = datetime.now() + timedelta(seconds=int(response.json()['Response']['refreshToken']['expires']))
	save_session(token_json)
	return token_json
	
# Update Session:
def save_session(token_json):
	print "Updating session"
	oauth_session.headers["X-API-Key"] = API_KEY
	oauth_session.headers["Authorization"] = 'Bearer ' + str(token_json)
	access_token = "Bearer " + str(token_json)


# Save state parameter used in CSRF protection:	
def save_created_state(state):
	session['state_token'] = state
	pass

def is_valid_state(state):
	saved_state = session['state_token']
	if state == saved_state:
		print "States match, you are who you say you are!"
		return True
	else:
		return False

# Main program - call app:	
if __name__ == '__main__':
	# User needs to add these:
	context = ('host-2.cert', 'host-2.key')
	app.run(debug=True, port=5000, ssl_context=context)

