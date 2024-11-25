import re
import csv
import json
from PyPDF2 import PdfReader
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

# Função para extrair texto do PDF a partir de uma palavra-chave
def extract_user_stories_from_pdf(pdf_path, start_keyword):
    reader = PdfReader(pdf_path)
    text = ""
    
    # Combina todo o texto das páginas
    for page in reader.pages:
        text += page.extract_text()
    
    # Localiza o início do Sprint 3
    start_index = text.find(start_keyword)
    if start_index == -1:
        print(f"Palavra-chave '{start_keyword}' não encontrada no PDF.")
        return []
    
    # Cortar o texto a partir da palavra-chave
    sprint_text = text[start_index:]
    
    # Regex para capturar as User Stories no formato 7.x.x com a descrição
    us_pattern = re.compile(r"(\d+\.\d+\.\d+)\s+(.+?)(?=\d+\.\d+\.\d+|$)", re.DOTALL)
    matches = us_pattern.findall(sprint_text)
    print(f"{len(matches)} User Stories encontradas.")
    
    user_stories = []
    
    for match in matches:
        us_id, description = match
        
        # Verificar se existe Acceptance Criteria para esta User Story
        acceptance_criteria = ""
        if "Acceptance Criteria" in description:
            # Regex para capturar os Acceptance Criteria
            ac_pattern = re.compile(r"Acceptance Criteria:(.*?)(?=\d+\.\d+\.\d+|$)", re.DOTALL)
            ac_match = ac_pattern.search(description)
            
            if ac_match:
                acceptance_criteria = ac_match.group(1).strip()

                # Remover os Acceptance Criteria da descrição principal
                description = description.split("Acceptance Criteria:")[0].strip()
        
        user_stories.append({
            "ID": us_id.strip(),
            "Title": description.strip(),
            "Acceptance Criteria": acceptance_criteria
        })
    
    return user_stories

# Exportar as User Stories para CSV
def export_to_csv(user_stories, output_file):
    fields = ["ID", "Title", "Acceptance Criteria"]
    
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for us in user_stories:
            writer.writerow(us)

# Carregar configurações do arquivo JSON
config = load_config()
pdf_path = config.get("RFP_DOCUMENT_PDF_PATH")

# Caso o caminho do PDF não esteja configurado, pedir ao usuário e salvar no JSON
if not pdf_path:
    pdf_path = input("Por favor, insira o caminho do PDF do documento RFP: ")
    config["RFP_DOCUMENT_PDF_PATH"] = pdf_path
    save_config(config)

# Pedir a palavra-chave ao usuário (com valor padrão)
start_keyword = input("Digite a palavra-chave para procurar as User Stories (Enter para padrão: 'Sprint 3'): ") or "Sprint 3"

# Caminho para o arquivo CSV de saída
csv_output = "user_stories.csv"

# Executar extração e exportação
user_stories = extract_user_stories_from_pdf(pdf_path, start_keyword)

if user_stories:
    export_to_csv(user_stories, csv_output)
    print(f"User stories exportadas para '{csv_output}' com sucesso!")
else:
    print("Nenhuma User Story encontrada.")
