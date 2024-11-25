import json
from github import Github

# Função para carregar configurações do arquivo config.json
def load_config():
    try:
        with open("../config.json", "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        return {}

# Função para salvar o token no arquivo config.json
def save_config(config):
    with open("../config.json", "w") as f:
        json.dump(config, f, indent=4)

# Carregar configurações do arquivo JSON
config = load_config()

# Obter o token do GitHub a partir do arquivo config.json ou solicitar ao usuário
github_token = config.get("GITHUB_TOKEN")

if not github_token:
    github_token = input("Por favor, insira o seu token do GitHub: ")
    config["GITHUB_TOKEN"] = github_token
    save_config(config)

# Conectar ao GitHub com o token
g = Github(github_token)

# Obter o limite de requisições da API
rate_limit = g.get_rate_limit()
print(f"Limite de requisições à API restante: {rate_limit.core.remaining}")
print(f"Reset em: {rate_limit.core.reset}")
