# 📖 Guia Completo: Deploy no Vercel (Next.js + FastAPI)

## PASSO 1: Acessar Vercel

1. Abra [https://vercel.com](https://vercel.com)
2. Faça login (se não tiver conta, crie uma com GitHub)
3. Clique em **"Add New..."** (canto superior esquerdo)
4. Selecione **"Project"**

---

## PASSO 2: Selecionar Repositório

Você verá a tela: **"Create a new project"**

```
┌─────────────────────────────────────────┐
│ Where would you like to import from?   │
├─────────────────────────────────────────┤
│ GitHub    GitLab    Bitbucket         │
└─────────────────────────────────────────┘
```

1. Clique em **"GitHub"**
2. Autorize Vercel (se pedido)
3. Procure por **"financeiro"** na lista
4. Clique em **"Import"** ao lado do repositório

✅ Repositório selecionado

---

## PASSO 3: Configure Project Details

Você verá a tela: **"Import project"**

### ⚙️ Project Name
```
Project Name: financeiro
```
✅ Deixe como está

### ⚙️ Framework Preset
```
┌─────────────────────────┐
│ Next.js ✓              │
│ (com logo do Next)      │
└─────────────────────────┘
```

**Ele detecta automaticamente!** Vercel vê `next.config.js` e escolhe Next.js

✅ Já está selecionado (não precisa mexer)

### ⚙️ Root Directory
```
Root Directory: .
(ou deixe em branco - significa raiz do projeto)
```

Você verá um campo que diz:
```
┌──────────────────────┐
│  .  (ou vazio)      │
└──────────────────────┘
```

✅ **Deixe em branco ou com ponto** - significa a raiz da pasta `c:\Users\mathe\Desktop\financiando`

---

## PASSO 4: Environment Variables

Clique em **"Environment Variables"** (aba ou seção abaixo)

### Adicionar Variável 1:

```
Nome (left):   PYTHONUNBUFFERED
Valor (right): 1
```

Clique em **"Add"**

✅ Variável adicionada (você verá na lista)

---

## PASSO 5: Build Settings

Você verá (geralmente auto-preenchido):

```
Build Command:  npm run build
Output Directory: .next
Install Command: npm ci (ou npm install)
```

✅ Deixe como está! (Vercel detecta automaticamente)

---

## PASSO 6: Deploy!

1. Role até o final da página
2. Clique no botão grande **"Deploy"**
3. Aguarde... você verá:

```
Building...
```

Isso pode levar **2-5 minutos**. Você verá progresso:

```
✓ Created deployment
✓ Analyzing source code
✓ Installing dependencies
✓ Building application
✓ Optimizing build
✓ Uploading build outputs
✓ Deployment complete!
```

---

## PASSO 7: Acessar Seu App!

Após deploy, você verá uma tela como esta:

```
┌────────────────────────────────────────┐
│ 🎉 Congratulations!                   │
│ Your project has been deployed!       │
├────────────────────────────────────────┤
│ Visit: financeiro.vercel.app           │
│        [Botão azul "Visit"]            │
└────────────────────────────────────────┘
```

Clique em **"Visit"** ou copie a URL:
```
https://financeiro.vercel.app
```

✅ **Seu app está online!**

---

## 🔴 Se der erro...

### Erro: "Build Failed"

Significa que algo deu errado durante a compilação. Clique em **"Deployments"** e veja os logs:

```
1. Vá para seu projeto Vercel
2. Clique em aba "Deployments"
3. Clique no deployment que falhou (vermelho)
4. Scroll down para ver os erros
5. Procure por linhas com "ERROR"
```

**Causas comuns**:
- Falta o `next.config.js`
- Falta `package.json`
- Falta arquivo em `pages/`

**Solução**: Verifique se todos esses arquivos existem:
```
✓ package.json
✓ next.config.js
✓ pages/index.js
✓ pages/_app.js
✓ api/index.py
✓ vercel.json
```

### Erro: "Python Build Failed"

Se a API (FastAPI) falhar:

Adicione variável de ambiente:
```
PYTHONUNBUFFERED = 1
```

### App carrega mas não mostra dados

- Backend pode não estar rodando
- Verifique se API está respondendo em `/api/health`

---

## ✅ Checklist Final

- [ ] GitHub conta conectada ao Vercel
- [ ] Repositório `financeiro` importado
- [ ] Framework: Next.js (auto detectado)
- [ ] Root Directory: `.` (vazio ou ponto)
- [ ] Variável PYTHONUNBUFFERED = 1 adicionada
- [ ] Deploy clicado
- [ ] Aguardou 2-5 minutos
- [ ] App aberto em https://financeiro.vercel.app
- [ ] Dashboard carregou com sucesso ✨

---

## 🆘 Stuck em algum passo?

Se não conseguir:

1. **Screenshot** onde você está travado
2. **Me avisa qual é o passo** (1 a 7)
3. **Descreva o erro** que aparece na tela

Eu ajudo! 👍
