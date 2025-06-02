import openai
import typer
import ell
import os


ell.init(store="./logdir", autocommit=True)
client = openai.Client(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1"
)


def create_synthetize_function(model: str):
    @ell.simple(client=client, model=model)
    def synthetize(prompt: str):
        """Vous êtes une intelligence artificielle chargée de créer une synthèse approfondie, dense et informative à partir d'un ensemble de citations mises en évidence dans des livres lus par un utilisateur. Votre synthèse doit être rédigée en français et se concentrer clairement sur les axes développés dans les citations fournies. Utilisez votre connaissance intrinsèque seulement pour apporter un contexte pertinent lorsque vous êtes absolument certains des informations, tout en vous basant principalement sur les citations fournies pour développer les thèses et arguments principaux du livre. La synthèse doit inclure les parties suivantes :

        Titre au format suivant : # Synthèse automatique du livre *[Titre du livre]*, par [Auteur], [Date]
        1. **Contexte** : Fournissez un bref contexte socio-historique du livre, de son auteur, du mouvement potentiel auquel il appartient, etc.
        2. **Thèse(s) et argument(s)** : Développez en profondeur les thèses principales et les arguments du livre, en vous basant essentiellement sur les citations fournies.
        3. **Point-clefs** : Présentez une liste de points clés sous forme de puces. Chaque point doit être extrêmement dense et très perspicace, permettant une rétention facile et rappelant l'ensemble du livre.

        Assurez-vous que la **Contexte** et **Thèse(s) et argument(s)** apparaissent en premier, suivis des **Point-clefs**. Utilisez un langage clair et concis, et formatez la synthèse en utilisant les fonctionnalités Markdown pour une meilleure lisibilité. Ne commencez jamais par les conclusions dans les exemples.

        Le texte que vous recevrez pour votre tâche contiendra des citations entourées de guillements qui proviennent du livre, mais possiblement aussi des annotations de l'utilisateur. Intégrez le dans un tout pour obtenir une fiche de synthèse réutilisable et qui garde tous les aspects essentiels. Densité, précision et atomicité sont les maîtres mots. Garde un ton neutre et efficace."""
        return prompt

    return synthetize


def synthetize(prompt: str, model: str):
    synthetize_func = create_synthetize_function(model)
    return synthetize_func(prompt)


def get_quotes(PATH: str):
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
    file.close()
    title = quotes[0]
    quotes.pop(0)
    prompt = f"""The book that you will study and analyze is {title}, here is a collection of quotes :\n\n"""
    for quote in quotes:
        prompt += f"{quote}\n"
    return (title, prompt)


def create_output(prompt: str, model: str, PATH: str):
    if PATH.endswith(".txt"):
        PATH = PATH[:-4]
    print("Waiting for answer...")
    response = synthetize(prompt, model=model)
    with open(f"note_folder/note_{PATH}.md", "w", encoding="UTF-8") as file:
        file.write(response)  # type: ignore


def main(
    all: bool = False,
    file_name: str = "",
    model: str = "anthropic/claude-3.5-sonnet:beta",
):
    """
    A CLI tool to process quotes from a file or all files in the quote_folder.

    Args:
        all (bool): Whether to process all files in the quote_folder.
    """
    if input(f"Current model is {model}\nDo you want to change it? (y/n)\n> ") == "y":
        model = input("Enter the model to use\n> ")
    if all:
        for file in os.listdir("quote_folder"):
            if file.endswith(".txt"):
                title, prompt = get_quotes(f"quote_folder/{file}")
                create_output(prompt, model, file)
                print(f"Done! You can check note_folder/note_{file[:-4]}.md")
    else:
        PATH = file_name
        try:
            file = open(f"quote_folder/{PATH}.txt", "r", encoding="UTF-8")
            file.close()
        except FileNotFoundError:
            print("The file does not exist")
            exit()
        title, prompt = get_quotes(f"quote_folder/{PATH}.txt")
        create_output(prompt, model, PATH)


if __name__ == "__main__":
    typer.run(main)
