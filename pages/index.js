import React, { useState, useEffect } from 'react'
import axios from 'axios'
import styles from '@/styles/Home.module.css'

export default function Home() {
  const [financiamentos, setFinanciamentos] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedId, setSelectedId] = useState(null)
  const [dados, setDados] = useState(null)

  useEffect(() => {
    carregarFinanciamentos()
  }, [])

  const carregarFinanciamentos = async () => {
    try {
      const response = await axios.get('/api/financiamentos')
      if (response.data.success) {
        setFinanciamentos(response.data.data)
      }
    } catch (error) {
      console.error('Erro ao carregar financiamentos:', error)
    } finally {
      setLoading(false)
    }
  }

  const carregarDados = async (id) => {
    try {
      const response = await axios.get(`/api/financiamentos/${id}`)
      if (response.data.success) {
        setDados(response.data.data)
        setSelectedId(id)
      }
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
    }
  }

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>🏍️ Financiando</h1>
        <p>Acelerador de Empréstimos de Motos</p>
      </header>

      <main className={styles.main}>
        <div className={styles.grid}>
          <section className={styles.card}>
            <h2>Meus Financiamentos</h2>
            {loading ? (
              <p>Carregando...</p>
            ) : financiamentos.length === 0 ? (
              <p>Nenhum financiamento ainda</p>
            ) : (
              <ul className={styles.list}>
                {financiamentos.map((fin) => (
                  <li key={fin.id} className={styles.item}>
                    <button
                      onClick={() => carregarDados(fin.id)}
                      className={selectedId === fin.id ? styles.active : ''}
                    >
                      <strong>{fin.nome}</strong>
                      <span>R$ {parseFloat(fin.saldo_atual).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</span>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </section>

          {dados && (
            <section className={styles.card}>
              <h2>📊 Dashboard</h2>
              <div className={styles.metrics}>
                <div className={styles.metric}>
                  <label>Saldo Atual</label>
                  <strong>R$ {parseFloat(dados.saldo_atual).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</strong>
                </div>
                <div className={styles.metric}>
                  <label>Meses Economizados</label>
                  <strong>{dados.meses_economizados}</strong>
                </div>
                <div className={styles.metric}>
                  <label>Economia em Juros</label>
                  <strong>R$ {parseFloat(dados.economia_juros).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</strong>
                </div>
                <div className={styles.metric}>
                  <label>Total de Aportes</label>
                  <strong>R$ {parseFloat(dados.total_aportes).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</strong>
                </div>
              </div>
            </section>
          )}
        </div>
      </main>

      <style jsx>{`
        @media (max-width: 768px) {
          .grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  )
}
