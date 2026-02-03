"""
Testes para a calculadora de amortização
"""

import sys
from pathlib import Path
from decimal import Decimal
from datetime import datetime

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from amortizacao import CalculadoraAmortizacao, PlanoAmortizacao


def test_calculo_juros():
    """Testa cálculo básico de juros"""
    calc = CalculadoraAmortizacao(10000, 0.01, 300)
    juros = calc.calcular_juros(Decimal('10000'))
    assert juros == Decimal('100.00'), f"Esperado 100.00, obteve {juros}"
    print("✓ Teste de juros: PASSOU")


def test_saldo_devedor_zero():
    """Testa se o plano termina quando saldo fica zero"""
    calc = CalculadoraAmortizacao(1000, 0.01, 100)
    plano = calc.gerar_plano_completo()
    
    # Último saldo deve ser zero (ou muito próximo)
    ultimo_saldo = plano.parcelas[-1].saldo_posterior
    assert ultimo_saldo < Decimal('0.01'), f"Saldo final deve ser ~0, obteve {ultimo_saldo}"
    print(f"✓ Teste saldo zero: PASSOU ({len(plano.parcelas)} parcelas)")


def test_aportes_reduzem_prazo():
    """Testa se aportes realmente reduzem o prazo"""
    calc = CalculadoraAmortizacao(15000, 0.012, 400)
    
    plano_sem = calc.gerar_plano_completo()
    plano_com = calc.gerar_plano_completo({5: 1000, 10: 1000})
    
    meses_reduzidos = len(plano_sem.parcelas) - len(plano_com.parcelas)
    assert meses_reduzidos > 0, "Aportes devem reduzir prazo"
    print(f"✓ Teste aportes reduzem prazo: PASSOU (redução de {meses_reduzidos} meses)")


def test_aportes_reduzem_juros():
    """Testa se aportes reduzem os juros totais"""
    calc = CalculadoraAmortizacao(15000, 0.012, 400)
    
    plano_sem = calc.gerar_plano_completo()
    plano_com = calc.gerar_plano_completo({5: 1000, 10: 1000})
    
    economia = plano_sem.total_juros_pago - plano_com.total_juros_pago
    assert economia > 0, "Aportes devem reduzir juros"
    print(f"✓ Teste aportes reduzem juros: PASSOU (economia de R$ {economia:.2f})")


def test_simulacao_aporte():
    """Testa simulação de aporte individual"""
    calc = CalculadoraAmortizacao(15000, 0.012, 400)
    
    meses, economia = calc.simular_aporte(500, 3)
    assert meses >= 0, "Meses não pode ser negativo"
    assert economia > 0, "Deve haver economia"
    print(f"✓ Teste simulação aporte: PASSOU (economia de {meses} meses)")


if __name__ == "__main__":
    print("Executando testes da Fase 1...\n")
    
    test_calculo_juros()
    test_saldo_devedor_zero()
    test_aportes_reduzem_prazo()
    test_aportes_reduzem_juros()
    test_simulacao_aporte()
    
    print("\n✅ Todos os testes passaram!")
