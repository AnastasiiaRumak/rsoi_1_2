from flask import Flask, request, jsonify
from src.Tokenizer import Tokenizer
from src.Database import Database

app = Flask(__name__)

@app.route('/authorize', methods=['GET'])
def authorize():
    db = Database()
    if db.is_set(request.args):
        tokenizer = Tokenizer()
        profile = request.args.get('profile')
        email = request.args.get('email')
        isAdmin = db.is_admin(email)
        token = tokenizer.generate_token({"profile": profile, "email": email, "isAdmin": isAdmin})
        return token
    else:
        return jsonify({"message": "Access Denied"})

@app.route('/callback', methods=['GET'])
def callback():
    tokenizer = Tokenizer()
    try:
        jwt = request.args.get('jwt')
        return tokenizer.check_token(jwt)
    except Exception as e:
        return jsonify({"message": "Access Denied"})

@app.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    with open(".well-known/jwks.json", "r") as jwks_file:
        jwks_data = jwks_file.read()
    return jwks_data

@app.route('/registration', methods=['POST'])
def registration():
    tokenizer = Tokenizer()
    params = request.get_json()
    token = request.headers.get('token', "")
    user = tokenizer.check_token(token)
    db = Database()
    if db.is_admin(user['email']):
        if not db.is_set(params):
            message = db.save(params)
            if message:
                return jsonify({"message": message}), 201
            else:
                return jsonify({"message": "data isnt validate. fields 'email' and 'profile' is required, 'email' is unique"}), 206
        else:
            return jsonify({"message": "data isnt validate. fields 'email' and 'profile' is required, 'email' is unique"}), 206
    else:
        return jsonify({"message": "403 Forbidden"}), 403

@app.route('/manage/health', methods=['GET'])
def health():
    # Implement health check logic here
    return "Health Check Passed"

if __name__ == '__main__':
    app.run()