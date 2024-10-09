from flask import Flask, request, render_template
import spacy

# Charger le modèle de langue de votre choix
# Si vous avez besoin du français, utilisez 'fr_core_news_sm'
# Pour l'anglais, utilisez 'en_core_web_sm'
nlp = spacy.load("fr_core_news_sm")  # Modèle de langue française

app = Flask(__name__)

# Fonction de tokenisation utilisant spaCy
def tokenize_sentence(sentence):
    """
    Cette fonction prend une phrase en entrée, la passe à travers le pipeline de spaCy
    et extrait les mots et la ponctuation en tant que tokens séparés.
    
    Arguments :
    sentence -- une chaîne de caractères représentant une phrase à tokeniser
    
    Retour :
    Une liste de tokens (mots et ponctuation) extraits de la phrase.
    """
    doc = nlp(sentence)  # Passer la phrase à travers le pipeline de spaCy
    # Extraire les tokens comme des mots, y compris la ponctuation comme tokens séparés
    tokens = [token.text for token in doc]
    return tokens

# Route Flask pour gérer les requêtes
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Cette fonction gère la route principale de l'application.
    Elle traite les requêtes GET et POST :
    
    - Si c'est une requête POST (lorsque l'utilisateur soumet un texte), elle récupère
      le texte, le tokenise et prépare le résultat à afficher.
    - Si c'est une requête GET, elle affiche une page vide pour permettre à l'utilisateur
      d'entrer un texte.
    
    Retour :
    Le modèle 'index2.html' est rendu avec le résultat des tokens ou un message vide
    lors du chargement initial.
    """
    if request.method == "POST":
        input_text = request.form["text"]  # Récupérer le texte soumis par l'utilisateur via le formulaire
        
        if input_text.strip():  # Vérifier si le texte n'est pas vide
            words = tokenize_sentence(input_text)  # Tokeniser le texte d'entrée
            result = ", ".join(words)  # Joindre les tokens avec des virgules pour l'affichage
        else:
            result = "Veuillez entrer une phrase valide."  # Message de validation si le texte est vide
        
        return render_template("index2.html", result=result)  # Rendre le résultat sur la page HTML
    return render_template("index2.html", result="")  # Chargement initial de la page avec un résultat vide

# Exécuter l'application Flask
if __name__ == "__main__":
    app.run(debug=True)  # Lancer l'application en mode débogage pour afficher les erreurs éventuelles.


# Exemple :  L’analyse d’un texte écrit commence par un découpage de celui-ci en phrases et par un découpage de chaque phrase en mots. 