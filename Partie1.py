from flask import Flask, request, render_template
import spacy

# Charger le modèle de langue française de spaCy
nlp = spacy.load("fr_core_news_sm")

app = Flask(__name__)

# Fonction pour segmenter le texte en phrases et les numéroter
def segmenter_en_phrases(texte):
    """
    Cette fonction prend un texte en entrée, le segmente en phrases à l'aide de spaCy et ajoute une numérotation à chaque phrase.
    Elle renvoie ensuite les phrases séparées par des sauts de ligne.
    
    Arguments :
    texte -- une chaîne de caractères contenant le texte à segmenter
    
    Retour :
    Une chaîne de caractères avec chaque phrase numérotée, séparée par des retours à la ligne.
    """
    doc = nlp(texte)  # Le texte est traité par le modèle spaCy pour le découper en phrases.
    
    # On crée une liste de phrases numérotées. On utilise enumerate pour avoir un index (i+1) et sent.text.strip() pour retirer les espaces inutiles.
    phrases = [f"Phrase {i+1}: {sent.text.strip()}" for i, sent in enumerate(doc.sents)]
    
    # On retourne les phrases jointes par des sauts de ligne '\n' pour bien séparer chaque phrase.
    return '\n'.join(phrases)

# Route principale pour l'interface
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Cette fonction gère la route principale de l'application.
    Elle traite les requêtes GET et POST :
    
    - Si c'est une requête GET (par défaut), elle affiche un formulaire vide.
    - Si c'est une requête POST (quand l'utilisateur soumet un texte), elle segmente le texte en phrases, les numérote, puis affiche le résultat.
    
    Retour :
    - Le modèle 'index1.html' est rendu avec soit un texte segmenté soit un résultat vide.
    """
    if request.method == "POST":
        input_text = request.form["text"]  # Récupérer le texte soumis par l'utilisateur via le formulaire
        
        if input_text:  # Si le texte n'est pas vide
            phrases = segmenter_en_phrases(input_text)  # On segmente le texte en phrases
            return render_template("index1.html", result=phrases)  # On renvoie le modèle HTML avec le texte segmenté
    return render_template("index1.html", result="")  # En cas de requête GET ou texte vide, on renvoie une page vide

if __name__ == "__main__":
    app.run(debug=True)  # On lance l'application en mode débogage pour afficher les erreurs éventuelles.



# Exemple : L’analyse d’un texte écrit commence par un découpage de celui-ci en phrases et par un découpage de chaque phrase en mots. 
# On suppose qu’on commence par un découpage en phrases. Le signe de ponctuation qui pose problème est le point car il peut être utilisé à d’autres effets,
# notamment pour marquer des abréviations M. salma (, etc., cf., fig.. .) et des acronymes exemples : (O.N.U., S.P.A.). Par ailleurs, 
# les points de suspension ne marquent pas toujours la fin d’une phrase.Ceci est une phrase supplémentaire pour tester le script !