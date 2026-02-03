"""
Wrapper para rodar Streamlit no Vercel
"""
import subprocess
import sys
import os

# Configurar variáveis de ambiente
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
os.environ['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'false'

def main():
    # Rodar Streamlit
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run',
        'src/dashboard.py',
        '--server.port=3000',
        '--server.address=0.0.0.0',
        '--logger.level=error'
    ])

if __name__ == '__main__':
    main()
