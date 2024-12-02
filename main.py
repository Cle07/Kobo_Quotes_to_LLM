import openai
import ell
import os

client = openai.Client(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
MODEL = "anthropic/claude-3.5-sonnet:beta"

@ell.simple(model=MODEL, client=client)
def synthetize(prompt):
    """Vous êtes une intelligence artificielle chargée de créer une synthèse approfondie, dense et informative à partir d'un ensemble de citations mises en évidence dans des livres lus. Votre synthèse doit être rédigée en français et se concentrer clairement sur les axes développés dans les citations fournies. Utilisez votre connaissance intrinsèque pour apporter un contexte pertinent lorsque vous êtes certain des informations, tout en vous basant principalement sur les citations fournies pour développer les thèses et arguments principaux du livre. La synthèse doit inclure les parties suivantes :

    Titre au format suivant : # Synthèse automatique du livre *[Titre du livre]*, par [Auteur], [Date]
    1. **Contexte** : Fournissez un bref contexte socio-historique du livre, de son auteur, du mouvement potentiel auquel il appartient, etc.
    2. **Thèse(s) et argument(s)** : Développez en profondeur les thèses principales et les arguments du livre, en vous basant essentiellement sur les citations fournies.
    3. **Point-clefs** : Présentez une liste de points clés sous forme de puces. Chaque point doit être extrêmement dense et très perspicace, permettant une rétention facile et rappelant l'ensemble du livre.

    Assurez-vous que la **Contexte** et **Thèse(s) et argument(s)** apparaissent en premier, suivis des **Point-clefs**. Utilisez un langage clair et concis, et formatez la synthèse en utilisant les fonctionnalités Markdown pour une meilleure lisibilité. Ne commencez jamais par les conclusions dans les exemples."""
    return prompt

def get_quotes(PATH):
    """
    Parameters :
    - PATH (str) : the path to the file containing the quotes
    Returns :
    - title (str) : the title of the book
    - prompt (str) : the prompt to send to LLM
    """
    file = open(PATH, "r", encoding="UTF-8")
    quotes = []
    lines = file.readlines()
    for line in lines:
        if line == "\n" or line == "":
            continue
        else:
            quotes.append(line)
    title = quotes[0]
    quotes.pop(0)
    file.close()
    prompt = f"""The book that you will study and analyze is {title}, here is a collection of quotes :\n"""
    for quote in quotes:
        prompt += f"{quote}\n"
    return (title, prompt)

def create_output(title, prompt, PATH):
    print("Waiting for answer...")
    response = synthetize(prompt)
    with open(f"note_folder/note_{PATH}.md", "w", encoding="UTF-8") as file:
        file.write(response) #type: ignore
    print(f"Done! You can check note_folder/note_{PATH}.md.")

if __name__ == "__main__":
    PATH = input("Enter the name of the file to synthetize\nShould be contained in the quotes_folder\n> ")
    try:
        file = open(f"quote_folder/{PATH}.txt", "r", encoding="UTF-8")
        file.close()
    except:
        print("The file does not exist")
        exit()
    if input(f"Current model is {MODEL}\nDo you want to change it? (y/n)\n> ") == "y":
        MODEL = input("Enter the model to use\n> ")
    title, prompt = get_quotes(f"quote_folder/{PATH}.txt")
    create_output(title, prompt, PATH)
