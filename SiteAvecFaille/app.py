from flask import Flask, render_template, request, redirect, session
from user import save_user_to_xml
from user import verify_credentials
from user import userExist
from user import userExistEmail
from user import getUser
import user as User
app = Flask(__name__)
app.secret_key = b'f\x95P"\xb4\xebp9r\xe9`\xb5rt\x97h\xd3lQ\x95\x19\xac4\x8e'

@app.route('/', methods=['GET', 'POST'])
def index():
    AllUsersFiltered = None
    if request.method == 'POST':
        if "SearchUsername" in request.form:
            UserFilter = request.form["SearchUsername"]
            AllUsersFiltered = User.GetUsersBy(UserFilter)
        if "Deconnexion" in request.form:
            session.pop("logged_in", None)
            session.pop("username", None)
            return render_template('index.html', username=None, email=None, password=None, role=None, AllUsersFiltered=None)

    username = None
    email = None
    password = None
    role = None
    if session.get("logged_in") == True:
        usernameSessions = session.get('username')
        account = getUser(usernameSessions)
        if account is not None:
            username = account.find("username").text
            email = account.find("email").text
            password = account.find("password").text
            role = account.find("role").text
    return render_template('index.html', username=username, email=email, password=password, role=role, AllUsersFiltered=AllUsersFiltered)



@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        # Récupérer les informations de l'utilisateur à partir du formulaire
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if (userExist(username) or userExistEmail(email)):
            error = "User already exist !"
            return render_template('register.html',error=error)
        else:
            # Enregistrer les informations de l'utilisateur dans un fichier XML
            save_user_to_xml(username,email,password)
            # Rediriger l'utilisateur vers la page d'accueil
            return redirect('/')
    else:
        return render_template('register.html',error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        goodcredential = verify_credentials(username, password)

        if type(goodcredential) is not bool:
            error = goodcredential
        elif goodcredential:
            session['logged_in'] = True
            session['username'] = username
            return redirect('/')
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=False)
