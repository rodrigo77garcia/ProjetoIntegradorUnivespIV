import pytest
import os

def run():
    # Garante que a pasta de relatórios exista
    os.makedirs("reports", exist_ok=True)

    # Executa os testes com cobertura e gera relatórios
    pytest_args = [
        "tests",                         # pasta dos testes
        "--cov=app",                     # mede cobertura da pasta app
        "--cov-report=html:reports/cov_html",  # relatório de cobertura em HTML
        "--html=reports/test_report.html",     # relatório de testes em HTML
        "--self-contained-html",         # relatório HTML completo
        "-v"                             # verbose (opcional)
    ]
    
    pytest.main(pytest_args)

if __name__ == "__main__":
    run()
