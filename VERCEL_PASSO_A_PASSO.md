# 📖 Guia Completo: Deploy no Vercel Passo a Passo

## PASSO 1: Criar conta no Vercel

1. Abra [https://vercel.com](https://vercel.com)
2. Clique em **"Sign Up"** (canto superior direito)
3. Escolha **"Continue with GitHub"**
4. Será aberta janela para autorizar Vercel acessar GitHub
5. Clique em **"Authorize Vercel"**

✅ Pronto! Você está logado no Vercel

---

## PASSO 2: Importar seu repositório

1. Após login, clique em **"Add New..."** → **"Project"**
   (ou vá para https://vercel.com/new)

2. Você verá a tela: **"Select a Git Repository"**
   - Selecione **GitHub** como provedor
   - Procure por "**financeiro**"
   - Clique no repositório `Matheusmata62/financeiro`

✅ Repositório selecionado

---

## PASSO 3: Configurar o Projeto

Você verá a tela: **"Configure Project"**

### 📁 Project Name:
- **Nome**: `financeiro` (ou `financeiro-dashboard`)
- Deixa como está ✅

### 📁 Framework Preset:
- **Escolha**: `Other` (porque é Python/Streamlit)
- Deixa como está ✅

### 📁 Root Directory:
- **Deixa em branco** (padrão `.`)
- ✅ Pronto

---

## PASSO 4: Variáveis de Ambiente

Clique em **"Environment Variables"** e adicione:

### Variável 1:
```
Nome: PYTHONUNBUFFERED
Valor: 1
```
Clique em **"Add"**

### Variável 2:
```
Nome: STREAMLIT_SERVER_HEADLESS
Valor: true
```
Clique em **"Add"**

### Variável 3:
```
Nome: STREAMLIT_SERVER_ENABLE_CORS
Valor: false
```
Clique em **"Add"**

✅ 3 variáveis adicionadas

---

## PASSO 5: Deploy!

1. Clique em **"Deploy"** (botão grande azul)
2. Aguarde o deployment (2-5 minutos)
3. Você verá: **"Congratulations! Your project has been deployed"**

✅ Pronto! Seu app está online!

---

## PASSO 6: Acessar seu Dashboard

Após deploy, você receberá uma URL do tipo:
```
https://financeiro-XXXXXX.vercel.app
```

Copie essa URL e **abra no navegador** ou no seu **celular/iPhone**.

Se não encontrar a URL, procure por:
- Botão **"Visit"** na página de success
- Ou vá para [https://vercel.com/dashboard](https://vercel.com/dashboard) → `financeiro` → copia a URL

---

## 🔴 Se der erro...

### Erro: "Build Failed"
- Vercel pode ter dificuldade com Streamlit
- **Solução**: Use **Streamlit Cloud** em vez disso (mais fácil)

### Erro: "Port in use"
- Vercel já controla a porta automaticamente
- Arquivo `vercel.json` já está configurado ✅

### Erro: "Module not found"
- Verifique `requirements.txt` tem todas dependências:
  ```
  streamlit==1.53.1
  plotly==6.5.2
  pandas==2.3.3
  python-dateutil==2.8.2
  ```

### Dashboard carrega mas não mostra dados
- Verifique se `data/financiamentos.db` foi enviado
- Se não, crie um novo financiamento via interface

---

## 💡 Se não funcionar no Vercel...

**Use Streamlit Cloud em vez disso** (MAIS FÁCIL):

1. Vá para [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Clique em **"Sign in with GitHub"**
3. Clique em **"Deploy an app"**
4. **Repositório**: Matheusmata62/financeiro
5. **Branch**: main
6. **Main file path**: `src/dashboard.py`
7. Clique **"Deploy"**

✅ Seu app estará em: `https://financeiro.streamlit.app`

---

## ✅ Checklist Final

- [ ] Conta Vercel criada
- [ ] Repositório importado
- [ ] Variáveis de ambiente adicionadas
- [ ] Deploy realizado com sucesso
- [ ] URL recebida
- [ ] App acessível no navegador

**Pronto! Dashboard online! 🎉**

---

## 🆘 Precisa de Ajuda?

Se ficar preso em algum passo, me avisa qual é a dificuldade!
