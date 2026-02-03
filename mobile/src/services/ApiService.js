import axios from 'axios'

// Configurar URL da API
// Em desenvolvimento: http://localhost:8000
// Em produção: https://seu-dominio.vercel.app

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

export const ApiService = {
  // Financiamentos
  getFinanciamentos: () => api.get('/api/financiamentos'),
  getFinanciamento: (id) => api.get(`/api/financiamentos/${id}`),
  criarFinanciamento: (data) => api.post('/api/financiamentos', data),
  
  // Aportes
  registrarAporte: (data) => api.post('/api/aportes', data),
  registrarVenda: (data) => api.post('/api/vendas', data),
  
  // Simulador
  simularAporte: (finId, valor, numero_parcela) =>
    api.get(`/api/simular/${finId}?valor=${valor}&numero_parcela=${numero_parcela}`),
  
  // Health check
  health: () => api.get('/api/health'),
}

export default api
