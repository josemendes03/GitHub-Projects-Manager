import json
import csv
from github import Github
from datetime import datetime, timezone
import os

# Função para carregar configurações do arquivo config.json
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

# Função para converter string para datetime
def str_to_datetime(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        print("Formato de data inválido. A data deve ser no formato 'YYYY-MM-DD'.")
        return None

# Carregar configurações do arquivo JSON
config = load_config()

# Verificar se as variáveis necessárias estão presentes, caso contrário, solicitar ao usuário
github_token = config.get("GITHUB_TOKEN")
repo_name = config.get("GITHUB_REPO")

# Se não estiverem no arquivo config.json, pedir ao usuário para inserir
if not github_token:
    github_token = input("Por favor, insira o seu token do GitHub: ")

if not repo_name:
    repo_name = input("Por favor, insira o nome do repositório (exemplo: 'utilizador/repositorio'): ")

# Salvar as configurações no arquivo config.json, se necessário
if not config.get("GITHUB_TOKEN"):
    config["GITHUB_TOKEN"] = github_token
if not config.get("GITHUB_REPO"):
    config["GITHUB_REPO"] = repo_name

save_config(config)

# Conectar ao GitHub com o token
g = Github(github_token)
repo = g.get_repo(repo_name)

# Solicitar as datas de início e fim do sprint
start_date_str = input("Por favor, insira a data de início do sprint (formato: YYYY-MM-DD): ")
end_date_str = input("Por favor, insira a data de fim do sprint (formato: YYYY-MM-DD): ")

# Converter as strings em objetos datetime
start_date = str_to_datetime(start_date_str)
end_date = str_to_datetime(end_date_str)

# Verificar se as datas são válidas
if not start_date or not end_date:
    print("Datas inválidas. O processo será interrompido.")
    exit()

# Lista todas as issues do repositório
issues = repo.get_issues(state="all")

# Preparar uma lista para armazenar os dados
issues_data = []

for issue in issues:
    # Filtrar apenas issues criadas dentro do intervalo de datas especificado
    if start_date <= issue.created_at <= end_date:
        issue_data = {
            "issue_id": issue.number,
            "title": issue.title,
            "status": issue.state,
            "created_at": issue.created_at,
            "closed_at": issue.closed_at if issue.state == "closed" else None
        }
        issues_data.append(issue_data)

# Salvar os dados em um arquivo CSV
with open('issues_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["issue_id", "title", "status", "created_at", "closed_at"])
    writer.writeheader()
    for issue in issues_data:
        writer.writerow(issue)

print("Data saved to 'issues_data.csv'")
