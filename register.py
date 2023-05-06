from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Récupérer les données du formulaire d'inscription
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # TODO: valider les données d'inscription
        
        # TODO: ajouter le nouvel utilisateur à la base de données
        
        # Rediriger l'utilisateur vers la page de connexion
        return redirect('/login')
    
    # Afficher le formulaire d'inscription si la méthode de requête est GET
    return render_template('register.html')
