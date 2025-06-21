# 📚 KindIn – Meu Enviador de EPUBs para Kindle

> Feito com carinho por Ana Caroline Santos, criadora do Prosa Tech - Cybersec para Divas 💖  
> Um projeto pessoal para facilitar minha leitura no Kindle, baixando livros automaticamente e enviando por e-mail ✉️📲

## ✨ O que esse projeto faz

Este site simples permite:
1. Digitar o nome de um livro que já foi baixado (ex: do Telegram)
2. Buscar o arquivo `.epub` automaticamente na sua pasta
3. Enviar o livro direto para o seu Kindle, gratuitamente, via e-mail!


## ⚙️ Como rodar o o projeto no meu computador

### 🧱 1. Pré-requisitos

Você precisa ter:
- Python 3 instalado ✅
- Conta no Gmail com autenticação em dois fatores ativada
- Kindle configurado para receber e-mails ✅


### 🖥️ 2. Passo a passo simplificado:

#### 🪄 Clone o repositório:

```bash
git clone https://github.com/carolsnt/kindin.git
cd kindin

### Crie um ambiente virtual (pra manter tudo organizado):
python3 -m venv .venv
source .venv/bin/activate

# Instale as bibliotecas que o projeto precisa:
pip install -r requirements.txt
 
#Se quiser instalar manualmente:
pip install flask requests python-dotenv

Configure seu e-mail do Gmail
Vá em https://myaccount.google.com/apppasswords

Gere uma senha de app (tipo: "Kindle Sender")

Guarde essa senha com você!

Crie o arquivo .env
Crie um arquivo chamado .env na pasta principal com este conteúdo:

KINDLE_EMAIL=seuemail@kindle.com
GMAIL_EMAIL=seuemail@gmail.com
GMAIL_APP_PASSWORD=sua-senha-do-app
DOWNLOADS_FOLDER=/Users/seu-usuario/Downloads/epubs
🔁 Troque os valores pelos seus dados reais!

Rodando o servidor
Depois de tudo instalado:

python app.py
Abra seu navegador em http://127.0.0.1:5000
Digite o nome do livro (sem acento, igual ao nome do arquivo) e... pronto! 

Como atualizar o OpenSSL (se aparecer erro do LibreSSL)
bash
Copiar
Editar
brew install openssl@3
Se quiser usar o novo Python com OpenSSL:

bash
Copiar
Editar
brew install python@3.12
python3.12 -m venv .venv
source .venv/bin/activate
💡 Dicas
Use sempre nomes simples de arquivo (sem espaço nem acento).

Mantenha seus EPUBs na mesma pasta.

Deixe o navegador salvo com o site local http://127.0.0.1:5000 para facilitar.

Use o Obsidian pra registrar melhorias futuras ou ideias 💻✨

👩‍💻 Feito com amor
Projeto desenvolvido por Ana Caroline Santos –
👉 @carolsnt @prosa.tech | Fundadora da Prosa Tech – Cybersec para Divas