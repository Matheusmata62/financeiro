"""
Script para executar o Dashboard Streamlit

Uso: python run_dashboard.py
ou:  streamlit run src/dashboard.py
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Executa o dashboard Streamlit"""
    
    # Caminho para o dashboard
    dashboard_path = Path(__file__).parent / "src" / "dashboard.py"
    
    print("=" * 80)
    print("🚀 Iniciando Dashboard Streamlit")
    print("=" * 80)
    print()
    print("📱 Abra em seu navegador:")
    print("   http://localhost:8501")
    print()
    print("🏃 Para acessar no iPhone:")
    print("   1. Descubra o IP da sua máquina (ipconfig)")
    print("   2. No iPhone, acesse: http://SEU_IP:8501")
    print()
    print("💡 Pressione CTRL+C para parar o servidor")
    print()
    print("=" * 80)
    print()
    
    # Executar streamlit
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(dashboard_path)],
            check=False
        )
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard encerrado")
    except Exception as e:
        print(f"❌ Erro ao executar dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
