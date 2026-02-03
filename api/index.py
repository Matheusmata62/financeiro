from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.integracao import SistemaFinanciamento
from src.amortizacao import CalculadoraAmortizacao

app = FastAPI(title="Financiando API", version="1.0.0")

# CORS para Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class NovoFinanciamento(BaseModel):
    nome: str
    saldo_inicial: float
    taxa_mensal: float
    parcela_fixa: float
    descricao: Optional[str] = None

class NovoAporte(BaseModel):
    financiamento_id: int
    valor: float
    numero_parcela: int
    descricao: Optional[str] = None

class VendaAporte(BaseModel):
    financiamento_id: int
    valor_venda: float
    descricao: Optional[str] = None

# Instância do sistema
sistema = SistemaFinanciamento()

# ==================== ENDPOINTS ====================

@app.get("/")
def root():
    return {"message": "Financiando API - v1.0", "status": "running"}

# ========== FINANCIAMENTOS ==========
@app.post("/api/financiamentos")
def criar_financiamento(fin: NovoFinanciamento):
    """Criar novo financiamento"""
    try:
        fin_id = sistema.criar_financiamento_completo(
            nome=fin.nome,
            saldo_inicial=fin.saldo_inicial,
            taxa_mensal=fin.taxa_mensal,
            parcela_fixa=fin.parcela_fixa,
            descricao=fin.descricao or ""
        )
        return {"success": True, "id": fin_id, "message": "Financiamento criado"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/financiamentos")
def listar_financiamentos():
    """Listar todos os financiamentos"""
    try:
        db = sistema.db
        cursor = db.conexao.cursor()
        cursor.execute("""
            SELECT id, nome, saldo_inicial, saldo_atual, taxa_mensal, 
                   parcela_fixa, data_criacao, descricao 
            FROM financiamentos
            ORDER BY data_criacao DESC
        """)
        colunas = [desc[0] for desc in cursor.description]
        financiamentos = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        return {"success": True, "data": financiamentos}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/financiamentos/{fin_id}")
def obter_financiamento(fin_id: int):
    """Obter detalhes de um financiamento"""
    try:
        dados = sistema.obter_dashboard_dados(fin_id)
        return {"success": True, "data": dados}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ========== APORTES ==========
@app.post("/api/aportes")
def registrar_aporte(aporte: NovoAporte):
    """Registrar novo aporte extra"""
    try:
        sistema.registrar_aporte(
            financiamento_id=aporte.financiamento_id,
            valor=aporte.valor,
            numero_parcela=aporte.numero_parcela,
            descricao=aporte.descricao or ""
        )
        return {"success": True, "message": "Aporte registrado"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/vendas")
def registrar_venda(venda: VendaAporte):
    """Registrar venda e criar aporte automaticamente"""
    try:
        sistema.registrar_venda_e_aporte(
            financiamento_id=venda.financiamento_id,
            valor_venda=venda.valor_venda,
            descricao=venda.descricao or "Venda registrada"
        )
        return {"success": True, "message": "Venda registrada"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ========== SIMULADOR ==========
@app.get("/api/simular/{fin_id}")
def simular_aporte(fin_id: int, valor: float, numero_parcela: int):
    """Simular impacto de um aporte"""
    try:
        db = sistema.db
        info = db.obter_info_financiamento(fin_id)
        calc = CalculadoraAmortizacao(
            saldo=info['saldo_atual'],
            taxa_mensal=info['taxa_mensal'],
            parcela_fixa=info['parcela_fixa']
        )
        
        meses_economizados, economia_juros = calc.simular_aporte(
            valor=valor,
            numero_parcela=numero_parcela
        )
        
        return {
            "success": True,
            "data": {
                "meses_economizados": meses_economizados,
                "economia_juros": float(economia_juros),
                "valor_aporte": valor
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# ========== HEALTH CHECK ==========
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": str(Path(__file__).stat().st_mtime)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
