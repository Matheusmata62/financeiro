#!/usr/bin/env python
# Teste rápido do dashboard

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    print("[Teste] Importando módulos...")
    
    import streamlit
    print(f"  ✓ Streamlit {streamlit.__version__}")
    
    import plotly
    print(f"  ✓ Plotly {plotly.__version__}")
    
    import pandas
    print(f"  ✓ Pandas {pandas.__version__}")
    
    from integracao import SistemaFinanciamento
    print(f"  ✓ SistemaFinanciamento")
    
    from amortizacao import CalculadoraAmortizacao
    print(f"  ✓ CalculadoraAmortizacao")
    
    print("\n✅ Dashboard pronto para executar!")
    print("\nExecute um dos comandos abaixo:")
    print("  1. python run_dashboard.py")
    print("  2. streamlit run src/dashboard.py")
    print("\nNo navegador: http://localhost:8501")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    sys.exit(1)
