from flask import Flask, request, render_template
import re  # Importation du module re pour la manipulation des expressions régulières

app = Flask(__name__)

def generate_sentence(word_list):
    """
    Cette fonction génère une phrase à partir d'une liste de mots en appliquant des règles de grammaire,
    des contractions et des corrections typographiques.
    
    Arguments :
    word_list -- une liste de mots à assembler en une phrase
    
    Retour :
    Une phrase corrigée et formatée.
    """
    # Joindre les mots en une seule chaîne
    sentence = " ".join(word_list)
    
    # Gestion des contractions et des apostrophes
    contractions = {
        "Le homme": "L'homme",
        "le à": "à l'",
        "de le": "du",
        "à le": "au",
        "de les": "des",
        "à les": "aux",
        "ce est": "c'est",
        "que il": "qu'il",
        "que elle": "qu'elle",
        "si il": "s'il",
        "si elle": "s'elle",
        "je ai": "j'ai",
        "de elle": "d'elle",
        "c est": "c'est",
        "ne il": "n'il",
        "ne elle": "n'elle",
        "ne est" : "n'est",
        "ne a"   : "n'a",
        "de à": "d'à",
        "de eux": "d'eux",
        "de elles": "d'elles",
        # Ajout d'autres cas
        "à le": "au",
        "à l": "à l'", 
        "l à": "l'à",
        "l avec": "l'avec",
        "l en": "l'en",
        "l ou": "l'où",
        "que ça": "qu'sa",
        "que vous": "qu'vous",
        "et elle": "et elle",  # Ajout d'autres cas
        "et il": "et il", 
    }
    
    # Remplacer les contractions dans la phrase
    for contraction, replacement in contractions.items():
        sentence = re.sub(r'\b' + re.escape(contraction) + r'\b', replacement, sentence)

    # Gestion des tirets pour les questions inversées
    sentence = re.sub(r"(\w+)\s+([tT])\s+il", r"\1-\2-il", sentence)

    # Correction des espaces autour de la ponctuation
    sentence = re.sub(r"\s+([,!?;])", r"\1", sentence)  # Supprimer les espaces avant la ponctuation
    sentence = re.sub(r"\s*\.\s*", ". ", sentence)  # Assurer un espace après un point
    sentence = re.sub(r"\s+\.", ".", sentence)  # Supprimer les espaces avant un point

    # Mettre une majuscule au début de la phrase
    if sentence:
        sentence = sentence[0].upper() + sentence[1:]  # Mettre la première lettre en majuscule

    return sentence.strip()  # Supprimer les espaces supplémentaires au début et à la fin

# Route principale pour l'interface
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Cette fonction gère la route principale de l'application.
    Elle traite les requêtes GET et POST :
    
    - Si c'est une requête POST (lorsque l'utilisateur soumet un texte), elle récupère
      le texte, le sépare en mots et génère une phrase.
    - Si c'est une requête GET, elle affiche une page vide pour permettre à l'utilisateur
      d'entrer un texte.
    
    Retour :
    Le modèle 'index3.html' est rendu avec la phrase générée ou un message vide
    lors du chargement initial.
    """
    if request.method == "POST":
        input_text = request.form["text"]  # Récupérer le texte soumis par l'utilisateur via le formulaire
        
        # Séparer les mots par des espaces
        word_list = input_text.split()  
        
        # Générer la phrase à partir de la liste de mots
        result = generate_sentence(word_list)
        
        return render_template("index3.html", result=result)  # Rendre la phrase générée sur la page HTML
    return render_template("index3.html", result="")  # Chargement initial de la page avec un résultat vide

# Exécuter l'application Flask
if __name__ == "__main__":
    app.run(debug=True)  # Lancer l'application en mode débogage pour afficher les erreurs éventuelles.


# Exemple : Le homme à le chapeau que nous avons rencontré à la  forêt sera t il invité aujourd'hui ? 