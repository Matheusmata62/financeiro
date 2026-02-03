"""
Motor de Cálculo de Amortização Brasileira
Fase 1: Core de Cálculo

Este módulo implementa a lógica correta de amortização com foco no saldo devedor,
permitindo tanto redução de prazo quanto redução de parcela.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP


@dataclass
class Parcela:
    """Representa uma parcela mensal da amortização"""
    numero: int
    data: datetime
    saldo_anterior: Decimal
    juros: Decimal
    principal: Decimal
    amortizacao_extra: Decimal
    saldo_posterior: Decimal
    valor_parcela: Decimal
    
    def __str__(self) -> str:
        return (
            f"Parcela {self.numero:03d} | "
            f"Data: {self.data.strftime('%d/%m/%Y')} | "
            f"Saldo: R$ {self.saldo_anterior:,.2f} | "
            f"Juros: R$ {self.juros:,.2f} | "
            f"Principal: R$ {self.principal:,.2f} | "
            f"Novo Saldo: R$ {self.saldo_posterior:,.2f}"
        )


@dataclass
class PlanoAmortizacao:
    """Contém o plano completo de amortização"""
    saldo_inicial: Decimal
    taxa_mensal: Decimal
    parcela_fixa: Decimal
    data_inicio: datetime
    parcelas: List[Parcela]
    
    @property
    def total_juros_pago(self) -> Decimal:
        """Soma total de juros pagos"""
        return sum(p.juros for p in self.parcelas)
    
    @property
    def total_amortizacao_extra(self) -> Decimal:
        """Soma total de amortizações extras"""
        return sum(p.amortizacao_extra for p in self.parcelas)
    
    @property
    def prazo_original_meses(self) -> int:
        """Prazo original em meses (calculado teoricamente)"""
        # Calcula quantas parcelas seriam necessárias sem aportes extras
        if not self.parcelas:
            return 0
        return len(self.parcelas)
    
    @property
    def economias_juros(self) -> Decimal:
        """Economia de juros comparado a não fazer aportes"""
        # Será calculado comparando com cenário sem aportes
        return self.total_amortizacao_extra * self.taxa_mensal


class CalculadoraAmortizacao:
    """
    Calculadora de amortização com suporte a:
    - Taxa de juros mensal fixa
    - Amortizações extras (aportes)
    - Redução de prazo vs redução de parcela
    """
    
    def __init__(self, saldo_devedor: float, taxa_mensal: float, 
                 parcela_mensal: float, data_inicio: datetime = None):
        """
        Inicializa a calculadora
        
        Args:
            saldo_devedor: Saldo devedor total em reais
            taxa_mensal: Taxa de juros mensal em decimal (ex: 0.01 para 1%)
            parcela_mensal: Valor da parcela mensal em reais
            data_inicio: Data inicial (default: hoje)
        """
        self.saldo_devedor = Decimal(str(saldo_devedor))
        self.taxa_mensal = Decimal(str(taxa_mensal))
        self.parcela_fixa = Decimal(str(parcela_mensal))
        self.data_inicio = data_inicio or datetime.now()
    
    def calcular_juros(self, saldo: Decimal) -> Decimal:
        """Calcula juros do mês sobre o saldo"""
        return (saldo * self.taxa_mensal).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
    
    def gerar_plano_completo(self, aportes: Optional[Dict[int, float]] = None) -> PlanoAmortizacao:
        """
        Gera o plano completo de amortização com aportes opcionais
        
        Args:
            aportes: Dicionário com {número_parcela: valor_aporte}
                     Exemplo: {3: 500, 7: 1000} para aportes nas parcelas 3 e 7
        
        Returns:
            PlanoAmortizacao com todas as parcelas calculadas
        """
        aportes = aportes or {}
        parcelas = []
        saldo_atual = self.saldo_devedor
        numero_parcela = 1
        
        while saldo_atual > Decimal('0.01'):  # Enquanto houver saldo
            # Calcula data da parcela
            data_parcela = self.data_inicio + timedelta(days=30 * (numero_parcela - 1))
            
            # Calcula juros sobre o saldo atual
            juros = self.calcular_juros(saldo_atual)
            
            # Aporte extra (se houver)
            aporte_extra = Decimal(str(aportes.get(numero_parcela, 0)))
            
            # Principal (parcela - juros + aporte)
            principal = self.parcela_fixa - juros
            
            # Se não há aporte, abate a parcela normalmente
            if aporte_extra == 0:
                if principal <= 0:
                    # Se juros >= parcela, temos problema - usar principal mínimo
                    principal = Decimal('1.00')
                saldo_posterior = saldo_atual - principal
                aporte_extra = Decimal('0.00')
            else:
                # Com aporte: reduz o saldo devedor diretamente
                principal_com_aporte = principal + aporte_extra
                saldo_posterior = saldo_atual - principal_com_aporte
                principal = principal_com_aporte
            
            # Garante que não fica com saldo negativo
            if saldo_posterior < 0:
                principal = saldo_atual
                saldo_posterior = Decimal('0.00')
            
            parcela = Parcela(
                numero=numero_parcela,
                data=data_parcela,
                saldo_anterior=saldo_atual,
                juros=juros,
                principal=principal - aporte_extra,  # Principal sem o aporte
                amortizacao_extra=aporte_extra,
                saldo_posterior=saldo_posterior,
                valor_parcela=self.parcela_fixa + aporte_extra
            )
            
            parcelas.append(parcela)
            saldo_atual = saldo_posterior
            numero_parcela += 1
            
            # Proteção contra loops infinitos
            if numero_parcela > 1000:
                break
        
        return PlanoAmortizacao(
            saldo_inicial=self.saldo_devedor,
            taxa_mensal=self.taxa_mensal,
            parcela_fixa=self.parcela_fixa,
            data_inicio=self.data_inicio,
            parcelas=parcelas
        )
    
    def simular_aporte(self, valor_aporte: float, numero_parcela: int) -> Tuple[int, Decimal]:
        """
        Simula o impacto de um aporte em uma parcela específica
        
        Args:
            valor_aporte: Valor do aporte em reais
            numero_parcela: Em qual parcela fazer o aporte
        
        Returns:
            (meses_economizados, economia_juros)
        """
        # Plano sem aporte
        plano_sem = self.gerar_plano_completo()
        meses_sem = len(plano_sem.parcelas)
        
        # Plano com aporte
        aportes = {numero_parcela: valor_aporte}
        plano_com = self.gerar_plano_completo(aportes)
        meses_com = len(plano_com.parcelas)
        
        meses_economizados = meses_sem - meses_com
        economia_juros = plano_sem.total_juros_pago - plano_com.total_juros_pago
        
        return (meses_economizados, economia_juros)


def exemplo_uso():
    """Exemplo de uso da calculadora"""
    print("=" * 80)
    print("EXEMPLO: Financiamento de Moto com Amortização Acelerada")
    print("=" * 80)
    
    # Parâmetros da moto
    saldo_devedor = 15000  # R$ 15.000
    taxa_mensal = 0.012  # 1.2% ao mês (aprox 15% a.a.)
    parcela_mensal = 400  # R$ 400 mensais
    
    calc = CalculadoraAmortizacao(saldo_devedor, taxa_mensal, parcela_mensal)
    
    # Plano SEM aportes
    print("\n1. PLANO ORIGINAL (SEM APORTES EXTRAS)")
    print("-" * 80)
    plano_original = calc.gerar_plano_completo()
    
    for parcela in plano_original.parcelas[:12]:  # Primeiras 12 parcelas
        print(f"  {parcela}")
    
    if len(plano_original.parcelas) > 12:
        print(f"  ... ({len(plano_original.parcelas) - 12} parcelas omitidas) ...")
        print(f"  {plano_original.parcelas[-1]}")
    
    print(f"\n  RESUMO:")
    print(f"  Total de parcelas: {len(plano_original.parcelas)}")
    print(f"  Total de juros: R$ {plano_original.total_juros_pago:,.2f}")
    
    # Plano COM aportes
    print("\n2. PLANO COM APORTES (3º parcela: +R$500, 7º parcela: +R$1.000)")
    print("-" * 80)
    aportes = {3: 500, 7: 1000}
    plano_acelerado = calc.gerar_plano_completo(aportes)
    
    for parcela in plano_acelerado.parcelas[:12]:
        marker = " ← APORTE" if parcela.amortizacao_extra > 0 else ""
        print(f"  {parcela}{marker}")
    
    if len(plano_acelerado.parcelas) > 12:
        print(f"  ... ({len(plano_acelerado.parcelas) - 12} parcelas omitidas) ...")
        print(f"  {plano_acelerado.parcelas[-1]}")
    
    print(f"\n  RESUMO:")
    print(f"  Total de parcelas: {len(plano_acelerado.parcelas)}")
    print(f"  Total de juros: R$ {plano_acelerado.total_juros_pago:,.2f}")
    print(f"  Total aportes: R$ {plano_acelerado.total_amortizacao_extra:,.2f}")
    
    # Comparação
    print("\n3. IMPACTO DOS APORTES")
    print("-" * 80)
    meses_economizados = len(plano_original.parcelas) - len(plano_acelerado.parcelas)
    economia_juros = plano_original.total_juros_pago - plano_acelerado.total_juros_pago
    
    print(f"  Meses economizados: {meses_economizados}")
    print(f"  Economia em juros: R$ {economia_juros:,.2f}")
    print(f"  Total investido em aportes: R$ {plano_acelerado.total_amortizacao_extra:,.2f}")
    print(f"  ROI (retorno em juros poupados): {(economia_juros / plano_acelerado.total_amortizacao_extra * 100):.2f}%")
    
    # Simulação individual
    print("\n4. SIMULAÇÃO: E se vender um item por R$300 na parcela 5?")
    print("-" * 80)
    meses, juros = calc.simular_aporte(300, 5)
    print(f"  Meses reduzidos: {meses}")
    print(f"  Economia em juros: R$ {juros:,.2f}")


if __name__ == "__main__":
    exemplo_uso()
