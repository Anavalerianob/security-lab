#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
log_analyzer.py

Descrição:
Este script analisa logs de autenticação do Linux (ex: /var/log/auth.log)
para identificar tentativas de login falhas, logins bem-sucedidos e
potenciais ataques de força bruta.

Habilidades Demonstradas:
- Python (argparse, re, collections.Counter, file I/O)
- Análise de Logs
- Resposta a Incidentes (Identificação de Ameaças)

Autor: Ana Luísa Valeriano Bomfim
Data: 8 de Novembro de 2025
"""

import re
import argparse
from collections import Counter

# --- Constantes de Cores (para melhor visualização) ---
# Usamos códigos ANSI para colorir a saída no terminal
C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_BOLD = '\033[1m'
C_END = '\033[0m'

# --- Definições de Regex ---

# Regex para encontrar falhas de login (funciona para usuários válidos e inválidos)
# Ex: Nov  8 14:15:01 sshd[1234]: Failed password for invalid user admin from 1.2.3.4 port 12345
# Captura: (Timestamp), (Usuário), (IP)
FAILED_REGEX = re.compile(
    r"(\w+\s+\d+\s+\d{2}:\d{2}:\d{2}).*Failed password for (?:invalid user )?(.+?) from (.+?) port"
)

# Regex para encontrar logins bem-sucedidos
# Ex: Nov  8 14:16:02 sshd[1235]: Accepted password for analuisa from 1.2.3.5 port 54321
# Captura: (Timestamp), (Usuário), (IP)
ACCEPTED_REGEX = re.compile(
    r"(\w+\s+\d+\s+\d{2}:\d{2}:\d{2}).*Accepted password for (.+?) from (.+?) port"
)

def parse_logs(logfile_path):
    """
    Lê e analisa o arquivo de log linha por linha.
    Retorna tupla com (falhas_por_ip, falhas_por_usuario, sucessos)
    """
    # Counters são dicionários especiais para contar coisas
    failed_attempts_by_ip = Counter()
    failed_attempts_by_user = Counter()
    successful_logins = []

    try:
        # Abrimos o arquivo de log para leitura
        with open(logfile_path, 'r', encoding='utf-8') as f:
            for line in f:
                # 1. Checa por falhas
                failed_match = FAILED_REGEX.search(line)
                if failed_match:
                    # Se encontrar, extrai os grupos que definimos no regex
                    timestamp, user, ip = failed_match.groups()
                    failed_attempts_by_ip[ip] += 1
                    failed_attempts_by_user[user.strip()] += 1
                    continue  # Pula para a próxima linha, já encontramos o que queríamos

                # 2. Checa por sucessos (só se não for uma falha)
                accepted_match = ACCEPTED_REGEX.search(line)
                if accepted_match:
                    timestamp, user, ip = accepted_match.groups()
                    successful_logins.append({'timestamp': timestamp, 'user': user.strip(), 'ip': ip})

    except FileNotFoundError:
        print(f"{C_RED}[ERRO] Arquivo não encontrado: {logfile_path}{C_END}")
        exit(1)
    except PermissionError:
        print(f"{C_RED}[ERRO] Sem permissão para ler o arquivo: {logfile_path}{C_END}")
        print("Tente executar com 'sudo' se for um log de sistema protegido.")
        exit(1)
    except Exception as e:
        print(f"{C_RED}[ERRO] Ocorreu um erro inesperado: {e}{C_END}")
        exit(1)
            
    return failed_attempts_by_ip, failed_attempts_by_user, successful_logins

def generate_report(logfile, threshold, failed_by_ip, failed_by_user, successful_logins):
    """Imprime o relatório formatado no console."""
    
    print("="*70)
    print(f"🛡️  {C_BOLD}Relatório de Análise do Log: {logfile}{C_END} 🛡️")
    print("="*70)

    # --- Seção 1: Alertas de Brute Force ---
    print(f"\n{C_RED}{C_BOLD}[!] ALERTA: Possíveis Ataques de Força Bruta (Threshold: {threshold} falhas){C_END}")
    found_bruteforce = False
    # Itera sobre os IPs que tiveram falhas
    for ip, count in failed_by_ip.items():
        if count >= threshold:
            print(f"  -> IP: {C_YELLOW}{ip:<15}{C_END} | {C_RED}Tentativas: {count}{C_END}")
            found_bruteforce = True
    
    if not found_bruteforce:
        print(f"  {C_GREEN}Nenhuma atividade de força bruta detectada acima do threshold.{C_END}")

    # --- Seção 2: Resumo de Tentativas Falhas ---
    print(f"\n{C_YELLOW}{C_BOLD}[-] Resumo de Todas as Tentativas Falhas{C_END}")
    if not failed_by_ip:
        print(f"  {C_GREEN}Nenhuma tentativa de login falha encontrada.{C_END}")
    else:
        # most_common() é um método do Counter para ordenar do maior para o menor
        print(f"\n  {C_BOLD}Top 10 IPs com mais falhas:{C_END}")
        for ip, count in failed_by_ip.most_common(10):
            print(f"    - IP: {ip:<15} | Falhas: {count}")
            
        print(f"\n  {C_BOLD}Top 10 Usuários com mais falhas:{C_END}")
        for user, count in failed_by_user.most_common(10):
            print(f"    - Usuário: {user:<20} | Falhas: {count}")

    # --- Seção 3: Logins Bem-Sucedidos ---
    print(f"\n{C_GREEN}{C_BOLD}[+] Resumo de Logins Bem-Sucedidos{C_END}")
    if not successful_logins:
        print("  Nenhum login bem-sucedido encontrado.")
    else:
        # Imprime apenas os 10 últimos logins
        print(f"  (Mostrando os últimos {len(successful_logins[-10:])} logins bem-sucedidos)\n")
        for login in successful_logins[-10:]:
            print(f"  - {login['timestamp']} | Usuário: {login['user']:<15} | IP de Origem: {login['ip']}")

    print("\n" + "="*70)
    print("Análise Concluída.")

def main():
    """Função principal para executar o script."""
    
    # --- Configuração do argparse ---
    parser = argparse.ArgumentParser(
        description="Analisa logs de autenticação (auth.log) para detecção de anomalias.",
        formatter_class=argparse.RawTextHelpFormatter # Preserva a formatação no help
    )
    # Argumento obrigatório: o arquivo de log
    parser.add_argument(
        "logfile", 
        help="Caminho para o arquivo de log (ex: /var/log/auth.log)"
    )
    # Argumento opcional: -t ou --threshold
    parser.add_argument(
        "-t", "--threshold", 
        type=int, 
        default=10, 
        help="Limite de tentativas falhas de um mesmo IP para considerar 'Brute Force'.\n(Default: 10)"
    )
    
    args = parser.parse_args()

    # --- Execução ---
    failed_by_ip, failed_by_user, successful_logins = parse_logs(args.logfile)
    generate_report(args.logfile, args.threshold, failed_by_ip, failed_by_user, successful_logins)

# Garante que a função main() só será executada se o script for chamado diretamente
if __name__ == "__main__":
    main()
