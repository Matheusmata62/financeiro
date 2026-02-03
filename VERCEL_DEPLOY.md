# 🚀 Deploy no Vercel (SEM CARTÃO)

## Opção 1: Deploy direto (Recomendado)

### Passo 1: Preparar repositório
Já está feito! Seu código está em:
```
https://github.com/Matheusmata62/financeiro
```

### Passo 2: Conectar ao Vercel
1. Vá para [vercel.com](https://vercel.com)
2. Clique em **"Sign Up"** → Escolha **"Continue with GitHub"**
3. Autorize Vercel acessar seus repositórios
4. Clique em **"Import Project"**
5. Procure por `financeiro` e clique em **"Import"**

### Passo 3: Configurar variáveis
1. Na aba **"Environment Variables"**, adicione:
   ```
   STREAMLIT_SERVER_HEADLESS = true
   STREAMLIT_SERVER_ENABLE_CORS = false
   PYTHONUNBUFFERED = 1
   ```

### Passo 4: Deploy
1. Clique em **"Deploy"**
2. Aguarde ~2-3 minutos
3. Seu app estará em: `https://financeiro.vercel.app`

---

## Opção 2: Deploy com Streamlit Cloud (MELHOR - Gratuito e sem configuração)

Se o Vercel não funcionar, use **Streamlit Cloud**:

1. Vá para [streamlit.io/cloud](https://streamlit.io/cloud)
2. Clique em **"Deploy an app"**
3. Conecte seu GitHub
4. Selecione repositório `financeiro`
5. Selecione arquivo: `src/dashboard.py`
6. Clique em **"Deploy"**

Seu app estará em: `https://financeiro.streamlit.app`

---

## Troubleshooting

### Erro: "Python version not found"
- Altere em `vercel.json`: `"runtime": "python3.11"`

### Erro: "Module not found"
- Verifique se `requirements.txt` tem todas as dependências
- Faça `git add .` e `git push` novamente

### Porta recusada
- Vercel usa porta 3000 automaticamente
- Já está configurado em `.streamlit/config.toml`

---

**Dica**: Streamlit Cloud é a forma mais simples para Streamlit no Vercel!
