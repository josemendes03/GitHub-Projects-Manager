import csv
from github import Github
import json
import os

# Função para ler as configurações do arquivo config.json
def load_config():
    try:
        with open("../config.json", "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        return {}

# Função para salvar as configurações no arquivo config.json
def save_config(config):
    with open("../config.json", "w") as f:
        json.dump(config, f, indent=4)

# Obter configurações do arquivo JSON
config = load_config()
github_token = config.get("GITHUB_TOKEN")
repo_name = config.get("GITHUB_REPO")
csv_path = config.get("OBTAINED_ISSUES_CSV_PATH")

# Caso as variáveis não estejam no JSON, pedir ao usuário
if not github_token:
    github_token = input("Por favor, insira o seu token do GitHub: ")

if not repo_name:
    repo_name = input("Por favor, insira o nome do repositório (exemplo: 'usuario/repositorio'): ")

# Pedir o caminho do CSV se não estiver no config
if not csv_path:
    csv_path = input("Por favor, insira o caminho do arquivo CSV com as User Stories: ")

    # Salvar o novo CSV_PATH no arquivo config.json
    config["OBTAINED_ISSUES_CSV_PATH"] = csv_path
    save_config(config)

# Conectar ao GitHub com o token
g = Github(github_token)
repo = g.get_repo(repo_name)

# Função para ler o CSV com as User Stories
def read_user_stories_from_csv(csv_path):
    user_stories = []
    # Verifica se o arquivo existe
    if not os.path.exists(csv_path):
        print(f"Erro: O arquivo '{csv_path}' não foi encontrado.")
        return []

    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_stories.append({
                "ID": row["ID"],
                "Title": row["Title"],
                "Acceptance Criteria": row["Acceptance Criteria"] if "Acceptance Criteria" in row else ""
            })
    return user_stories

# Ler as User Stories do CSV
user_stories = read_user_stories_from_csv(csv_path)

# Se o arquivo não existir ou não houver User Stories, encerrar o script
if not user_stories:
    print("Não foi possível ler as User Stories. O script será encerrado.")
else:
    # Obter todas as issues existentes
    existing_issues = repo.get_issues(state="all")
    existing_titles = [issue.title for issue in existing_issues]

    # Itera sobre as User Stories e cria uma issue para cada uma se ainda não existir
    for us in user_stories:
        issue_title = f"{us['ID']} - {us['Title']}"
        issue_body = f"**Acceptance Criteria**:\n{us['Acceptance Criteria']}" if us['Acceptance Criteria'] else "Não há Acceptance Criteria especificado."
        
        # Verifica se a issue já existe pelo título
        if issue_title in existing_titles:
            print(f"Issue já existe: {issue_title}")
        else:
            # Criar a issue com o rótulo "Todo"
            issue = repo.create_issue(
                title=issue_title,
                body=issue_body,
                labels=["Todo"]  # Adiciona ao "Todo"
            )
            print(f"Issue criada: {issue.title} (#{issue.number})")
    
    print("Todas as issues não duplicadas foram criadas!")
