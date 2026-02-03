# ??? Financiando - Sistema de Aceleração de Empréstimos

Sistema web completo para gerenciar e acelerar pagamento de empréstimos de motos através de aportes estratégicos.

## ??? Arquitetura

Next.js (Frontend) + FastAPI (Backend) + SQLite (Dados)

## ?? Deploy no Vercel

1. Vá para vercel.com
2. Clique em "Add New..." ? "Project"
3. Selecione repositório financeiro
4. Configure e Deploy!

## ?? Funcionalidades

- Dashboard responsivo
- Gerenciamento de financiamentos
- Simulador de aportes
- Cálculos de amortização Brasil
- Histórico de transações

## ?? API Endpoints

POST /api/financiamentos - Criar
GET /api/financiamentos - Listar
GET /api/financiamentos/{id} - Detalhes
POST /api/aportes - Registrar aporte
POST /api/vendas - Registrar venda
GET /api/simular/{id} - Simular impacto

## ?? Desenvolvimento Local

### Backend
`
pip install fastapi uvicorn
python -m uvicorn api.index:app --reload
`

### Frontend
`
npm install
npm run dev
`

Acesso: http://localhost:3000

## ? Versão: 2.0.0 (Next.js + FastAPI)

