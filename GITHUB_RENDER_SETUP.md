# 🚀 Hospedar no GitHub + Render

## Passo 1: Criar repositório no GitHub

1. Acesse [github.com/new](https://github.com/new)
2. Preencha os dados:
   - **Repository name**: `financiando`
   - **Description**: "Sistema de aceleração de empréstimos com dashboard Streamlit"
   - **Public** (gratuito)
3. Clique em "Create repository"
4. **NÃO INICIALIZE com README** (já temos)

## Passo 2: Conectar repositório local ao GitHub

Execute esses comandos (substitua `SEU_USUARIO` pelo seu usuário GitHub):

```powershell
cd c:\Users\mathe\Desktop\financiando

git remote add origin https://github.com/SEU_USUARIO/financiando.git
git branch -M main
git push -u origin main
```

## Passo 3: Hospedar no Render

1. Acesse [render.com](https://render.com) e faça login com GitHub
2. Clique em **"New +"** → **"Web Service"**
3. Selecione seu repositório `financiando`
4. Preencha:
   - **Name**: `financiando-dashboard`
   - **Runtime**: `Python 3.11`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run src/dashboard.py --server.port=$PORT --server.address=0.0.0.0`
5. Adicione variáveis de ambiente:
   - `PYTHONUNBUFFERED` = `true`
   - `STREAMLIT_SERVER_HEADLESS` = `true`
6. Clique em **"Deploy"**

## Passo 4: Acessar seu dashboard

Após deploy (3-5 minutos):
```
https://financiando-dashboard.onrender.com
```

## Troubleshooting

Se der erro de porta ou timeout:
- Render usa variável `$PORT` automaticamente
- Streamlit já está configurado em `.streamlit/config.toml`

Pronto! Seu dashboard estará online! ✅

