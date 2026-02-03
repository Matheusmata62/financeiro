# 📱 Guia de Build para Android e iOS

## 📲 Opção 1: Desenvolvimento com Expo Go (Mais Fácil!)

### Requisitos
- Node.js 16+
- Expo CLI
- Expo Go app (baixe na Play Store ou App Store)

### Passos

```bash
cd mobile
npm install
npm start
```

Isso abrirá um QR code. Abra o **Expo Go** no seu celular e escaneie!

---

## 🔨 Opção 2: Build Profissional (Android APK/iOS IPA)

### Requisitos
- Conta Expo (gratuita em expo.dev)
- EAS CLI: `npm install -g eas-cli`

### Configurar EAS

```bash
cd mobile
eas login
eas build:configure
```

### Build Android

```bash
# Gerar APK (compatível com Play Store)
npm run build:android

# Ou IPA para iOS
npm run build:ios
```

Aguarde 10-15 minutos. Você receberá um link para baixar!

---

## 📲 Opção 3: Publicar na Play Store (Android)

### Pré-requisitos
1. Conta Google Play Developer ($25 uma vez)
2. Keystore assinado
3. App configurado no Play Console

### Passos

```bash
# 1. Gerar APK assinado
npm run build:android

# 2. Fazer upload no Play Console
# - Ve para https://play.google.com/console
# - Crie novo app
# - Faça upload do APK
# - Preencha informações
# - Envie para review
```

---

## 🍎 Opção 4: Publicar na App Store (iOS)

### Pré-requisitos
1. Conta Apple Developer ($99/ano)
2. Mac para fazer build final
3. Certificados e profiles

### Passos

```bash
# 1. Gerar IPA
npm run build:ios

# 2. Fazer upload no App Store Connect
# - Acesse https://appstoreconnect.apple.com
# - Crie novo app
# - Faça upload do IPA com Transporter
# - Preencha informações
# - Envie para review
```

---

## 🌐 Configurar URL da API

### Em desenvolvimento
API aponta para: `http://localhost:8000`

### Em produção
Edite `src/services/ApiService.js`:

```javascript
const API_BASE_URL = 'https://seu-dominio.vercel.app'
```

Ou use variável de ambiente:

```bash
REACT_APP_API_URL=https://seu-dominio.vercel.app npm start
```

---

## 🐛 Troubleshooting

### "Module not found"
```bash
npm install
npm install expo-modules
```

### "Port 8081 in use"
```bash
lsof -i :8081  # macOS/Linux
netstat -ano | findstr :8081  # Windows
kill -9 <PID>
```

### Expo Go não conecta
- Verifique se estão na mesma rede WiFi
- Verifique firewall
- Reinicie Expo: Ctrl+C e `npm start`

---

## 📦 Estrutura do Projeto

```
mobile/
├── App.js                  # App principal
├── app.json               # Configuração Expo
├── package.json           # Dependências
├── src/
│   ├── Navigation.js      # Navegação abas
│   ├── screens/           # Telas
│   │   ├── HomeScreen.js
│   │   └── NovoFinanciamentoScreen.js
│   └── services/
│       └── ApiService.js  # Conexão API
└── assets/                # Imagens e ícones
```

---

## ✅ Próximos Passos

1. **Desenvolver**: `npm start`
2. **Testar**: Exponyme Go no celular
3. **Build**: `npm run build:android` ou `npm run build:ios`
4. **Publicar**: Play Store ou App Store

---

**Status**: Pronto para desenvolvimento! 🚀

