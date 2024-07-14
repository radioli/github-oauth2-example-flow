import requests
from urllib.parse import urlencode
from flask import Flask, redirect, request


github_client_id = ''
github_client_secret = ''

# This is the URL we'll send the user to first to get their authorization
authorize_url = 'https://github.com/login/oauth/authorize'

# This is the endpoint our server will request an access token from
token_url = 'https://github.com/login/oauth/access_token'

# This is the Github base URL we can use to make authenticated API requests
api_url_base = 'https://api.github.com/'

# The URL for this script, used as the redirect URL

redirect_url = 'http://127.0.0.1:8080/redirect'

# The code returned by github from #GET /login/oauth/authorize

payload = {"response_type": "code", 'client_id': github_client_id,
           'redirect_uri': redirect_url, 'scope': 'repo'}


def provide_token_payload(code):
    return {'grant_type': 'authorization_code', 'client_id': github_client_id,
            'client_secret': github_client_secret, 'redirect_uri': redirect_url, 'code': code}


app = Flask(__name__)


@app.route("/")
def index():
    auth_req = authorize_url+'?'+urlencode(payload)
    return redirect(auth_req)


@app.route("/redirect")
def redirect_github_url():
    code = request.args['code']
    print(code)
    print(provide_token_payload(code))
    resp = requests.post(token_url, provide_token_payload(code)).text
    return resp


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
