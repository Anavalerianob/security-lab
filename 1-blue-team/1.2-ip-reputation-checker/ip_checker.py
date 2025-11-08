#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ip_checker.py

Descrição:
Verifica a reputação de um endereço IP usando a API do AbuseIPDB
para determinar se é malicioso (associado a spam, C2, etc.).


Autor: Ana Luísa Valeriano Bomfim
Data: 01 de fevereiro de 2025
"""

import requests
import argparse
import json
import os
import sys

# --- Constantes de Cores ---
C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_CYAN = '\033[96m'
C_BOLD = '\033[1m'
C_END = '\033[0m'

# --- Constantes da API ---
# URL base da API do AbuseIPDB (v2)
API_ENDPOINT = 'https://api.abuseipdb.com/api/v2/check'

def get_api_key():
    """
    Obtém a chave da API da variável de ambiente 'ABUSEIPDB_KEY'.
    """
    api_key = os.getenv('ABUSEIPDB_KEY')
    if not api_key:
        print(f"{C_RED}[ERRO] Variável de ambiente 'ABUSEIPDB_KEY' não definida.{C_END}")
        print("Por favor, defina a chave da API antes de executar o script:")
        print("  Linux/macOS: export ABUSEIPDB_KEY='sua_chave_aqui'")
        print("  Windows:     set ABUSEIPDB_KEY=sua_chave_aqui")
        sys.exit(1) # Termina o script se a chave não for encontrada
    return api_key

def check_ip_reputation(api_key, ip_address, max_age_days=90):
    """
    Consulta a API do AbuseIPDB e retorna a resposta JSON.
    """
    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }
    
    querystring = {
        'ipAddress': ip_address,
        'maxAgeInDays': max_age_days
    }
    
    try:
        response = requests.get(url=API_ENDPOINT, headers=headers, params=querystring, timeout=10)
        # Levanta um erro HTTP se a resposta for 4xx ou 5xx
        response.raise_for_status()
        
        # Converte a resposta de texto JSON para um dicionário Python
        return response.json()
        
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print(f"{C_RED}[ERRO 401] Não autorizado. Sua chave de API está correta?{C_END}")
        elif response.status_code == 402:
            print(f"{C_RED}[ERRO 402] Requisição falhou. Verifique seu plano de assinatura.{C_END}")
        elif response.status_code == 429:
            print(f"{C_RED}[ERRO 429] Muitas requisições. Você atingiu o limite da API.{C_END}")
        else:
            print(f"{C_RED}[ERRO HTTP] {http_err}{C_END}")
        sys.exit(1)
    except requests.exceptions.ConnectionError as conn_err:
        print(f"{C_RED}[ERRO] Erro de conexão: {conn_err}{C_END}")
        sys.exit(1)
    except requests.exceptions.Timeout as timeout_err:
        print(f"{C_RED}[ERRO] Timeout da requisição: {timeout_err}{C_END}")
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(f"{C_RED}[ERRO] Erro desconhecido na requisição: {err}{C_END}")
        sys.exit(1)

def print_report(data):
    """Imprime um relatório formatado a partir dos dados da API."""
    
    # Extrai o dicionário 'data' de dentro da resposta
    ip_data = data.get('data', {})
    
    if not ip_data:
        print(f"{C_RED}[ERRO] A resposta da API não contém os dados esperados.{C_END}")
        print("Resposta recebida:", data)
        return

    # --- Informações Principais ---
    ip = ip_data.get('ipAddress', 'N/A')
    score = ip_data.get('abuseConfidenceScore', 0)
    country = ip_data.get('countryCode', 'N/A')
    isp = ip_data.get('isp', 'N/A')
    domain = ip_data.get('domain', 'N/A')
    
    print("="*70)
    print(f"📊  {C_BOLD}Relatório de Reputação do IP: {ip}{C_END} 📊")
    print("="*70)

    # --- Score de Abuso (O mais importante) ---
    print(f"\n{C_BOLD}Score de Confiança de Abuso: {C_END}", end="")
    if score == 0:
        print(f"{C_GREEN}{score}% (Limpo){C_END}")
    elif 1 <= score <= 70:
        print(f"{C_YELLOW}{score}% (Suspeito){C_END}")
    else:
        print(f"{C_RED}{score}% (Malicioso!){C_END}")

    print(f"  - {C_CYAN}Este IP foi reportado {ip_data.get('totalReports', 0)} vezes.{C_END}")
    if ip_data.get('lastReportedAt'):
        print(f"  - {C_YELLOW}Última denúncia: {ip_data.get('lastReportedAt')}{C_END}")

    # --- Detalhes do IP ---
    print(f"\n{C_BOLD}Detalhes do IP:{C_END}")
    print(f"  - {C_BOLD}País:{C_END} {country}")
    print(f"  - {C_BOLD}Provedor (ISP):{C_END} {isp}")
    print(f"  - {C_BOLD}Domínio associado:{C_END} {domain}")
    print(f"  - {C_BOLD}IP é público?{C_END} {'Sim' if ip_data.get('isPublic') else 'Não (Privado)'}")
    print(f"  - {C_BOLD}IP é Whitelisted?{C_END} {'Sim (Confiável)' if ip_data.get('isWhitelisted') else 'Não'}")

    print("\n" + "="*70)
    print("Consulta Concluída.")

def main():
    """Função principal para executar o script."""
    
    parser = argparse.ArgumentParser(
        description="Verifica a reputação de um IP usando a API do AbuseIPDB.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-i", "--ip",
        dest="ip_address",
        required=True,
        help="O endereço IP a ser verificado."
    )
    parser.add_argument(
        "-d", "--days",
        type=int,
        default=90,
        help="Janela de tempo (em dias) para checar denúncias.\n(Default: 90 dias)"
    )
    
    args = parser.parse_args()
    
    api_key = get_api_key()
    report_data = check_ip_reputation(api_key, args.ip_address, args.days)
    print_report(report_data)

if __name__ == "__main__":
    main()
