import os # p acessar as variáveis de ambiente
import requests # p baixar o arquivo epub
import smtplib # p enviar o email com arquivo
from email.message import EmailMessage # Para montar o e-mail

def buscar_epub(nome_livro):
     # Formata o nome do livro (ex: "Dom Casmurro" → "dom_casmurro")
    nome_formatado = nome_livro.replace(" ", "_").lower()
    # Monta o link do arquivo no site que tem os epubs
    url = f"https://exemplo-de-site.com/livros/{nome_formatado}.epub"
    try:
         # Tenta baixar o arquivo
        response = requests.get(url)
        # Verifica se a requisição foi bem-sucedida
        # Se conseguiu (HTTP 200 = OK)
        if response.status_code == 200:
            file_path = f"{nome_formatado}.epub"
             # Salva o conteúdo em um arquivo no seu computador
            with open(file_path, "wb") as f:
                f.write(response.content)
            return file_path # Retorna o caminho do arquivo salvo
    except:
        return None # Se der erro, retorna None (não achou o livro)

def enviar_para_kindle(arquivo):  # Busca os dados secretos do .env
    EMAIL_KINDLE = os.getenv("EMAIL_KINDLE")
    EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
    SENHA = os.getenv("SENHA_EMAIL")
# Cria um e-mail simples
    msg = EmailMessage()
    msg["Subject"] = "" # Kindle ignora o assunto
    msg["From"] = EMAIL_REMETENTE # De quem está enviando
    msg["To"] = EMAIL_KINDLE # Para quem está enviando (seu Kindle)

    with open(arquivo, "rb") as f:  # Abre o arquivo EPUB e anexa ao e-mail
        msg.add_attachment(f.read(), maintype="application", subtype="epub", filename=os.path.basename(arquivo))

    try: # Conecta ao Gmail e envia
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False # Se der erro, retorna False
