#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
data_scanner.py

Descrição:
Varre recursivamente um diretório em busca de arquivos de texto (.txt, .csv,
.log, .json) que contenham dados sensíveis, como CPFs, e-mails ou
números de cartão de crédito, usando expressões regulares (Regex).


Autor: Ana Luísa Valeriano Bomfim
Data: 8 de Setembro de 2025
"""

import os
import re
import argparse
import sys

# --- Constantes de Cores ---
C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_CYAN = '\033[96m'
C_BOLD = '\033[1m'
C_END = '\033[0m'

# --- Definições de Regex ---
# Compilamos os regex para melhor performance
# Cada tupla contém: (Nome do Padrão, Padrão Regex Compilado)
REGEX_PATTERNS = [
    (
        "CPF",
        re.compile(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b')
    ),
    (
        "Email",
        re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
    ),
    (
        "Cartao de Credito (basico)",
        # Detecta 4 grupos de 4 dígitos, separados por espaço, - ou nada
        re.compile(r'\b(?:\d{4}[ -]?){3}\d{4}\b')
    ),
    (
        "Telefone BR (basico)",
        re.compile(r'\b(?:\(?\d{2}\)?\s?)?\d{4,5}[- ]?\d{4}\b')
    )
]

# Extensões de arquivo que vamos analisar
# Adicione outras se necessário (ex: .xml, .html)
TEXT_FILE_EXTENSIONS = {'.txt', '.csv', '.log', '.json', '.md', '.py', '.conf'}

def scan_file(filepath):
    """
    Lê um arquivo linha por linha e aplica todos os regex.
    Retorna uma lista de descobertas.
    """
    findings = []
    try:
        # Usamos 'utf-8' com 'errors=ignore' para evitar que o script
        # quebre em arquivos com codificação inválida.
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for pattern_name, regex in REGEX_PATTERNS:
                    # findall encontra todas as correspondências na linha
                    matches = regex.findall(line)
                    if matches:
                        for match in matches:
                            findings.append({
                                'line': line_num,
                                'pattern_name': pattern_name,
                                'match': match,
                                'line_content': line.strip()[:80] # Pega 80 chars da linha
                            })
    except IOError as e:
        print(f"  {C_YELLOW}[AVISO] Não foi possível ler o arquivo: {filepath} ({e}){C_END}")
    except Exception as e:
        print(f"  {C_YELLOW}[AVISO] Erro inesperado ao processar {filepath}: {e}{C_END}")
        
    return findings

def walk_directory(start_path):
    """
    Percorre recursivamente o diretório e inicia o scan
    nos arquivos com extensões válidas.
    """
    print("="*70)
    print(f"{C_BOLD}Iniciando varredura de dados sensíveis em: {start_path}{C_END}")
    print("Extensões alvo:", TEXT_FILE_EXTENSIONS)
    print("="*70)
    
    total_files_scanned = 0
    total_findings = 0
    
    # os.walk é um gerador que percorre a árvore de diretórios
    for root, dirs, files in os.walk(start_path):
        for filename in files:
            # Pega a extensão do arquivo (ex: '.txt')
            _, file_ext = os.path.splitext(filename)
            
            if file_ext.lower() in TEXT_FILE_EXTENSIONS:
                filepath = os.path.join(root, filename)
                total_files_scanned += 1
                
                print(f"\n{C_CYAN}[INFO] Analisando: {filepath}{C_END}")
                
                findings = scan_file(filepath)
                
                if findings:
                    total_findings += len(findings)
                    print(f"  {C_RED}{C_BOLD}[ALERTA] {len(findings)} dado(s) sensível(eis) encontrado(s) em {filepath}!{C_END}")
                    for find in findings:
                        print(f"  - {C_RED}Linha {find['line']}{C_END}: "
                              f"Tipo: {C_YELLOW}{find['pattern_name']}{C_END} | "
                              f"Dado: {C_BOLD}{find['match']}{C_END}")
                else:
                    # Imprime em modo "verbose" para mostrar que está funcionando
                    # print(f"  {C_GREEN}[OK] Nenhum dado sensível encontrado.{C_END}")
                    pass
                    
    print("\n" + "="*70)
    print(f"{C_BOLD}Varredura Concluída.{C_END}")
    print(f"  - Total de arquivos analisados: {total_files_scanned}")
    print(f"  - Total de dados sensíveis encontrados: {total_findings}")
    if total_findings > 0:
        print(f"{C_RED}{C_BOLD}RECOMENDAÇÃO: Revise os arquivos listados acima imediatamente.{C_END}")
    else:
        print(f"{C_GREEN}Nenhum dado sensível foi encontrado nos padrões definidos.{C_END}")
    print("="*70)

def main():
    parser = argparse.ArgumentParser(
        description="Varre um diretório em busca de dados sensíveis (PII) usando Regex.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "directory",
        help="O caminho do diretório para iniciar a varredura."
    )
    
    args = parser.parse_args()
    
    target_dir = args.directory
    
    if not os.path.isdir(target_dir):
        print(f"{C_RED}[ERRO] O caminho fornecido não é um diretório válido: {target_dir}{C_END}")
        sys.exit(1)
        
    try:
        walk_directory(target_dir)
    except KeyboardInterrupt:
        print(f"\n\n{C_YELLOW}[AVISO] Varredura interrompida pelo usuário.{C_END}")
        sys.exit(0)

if __name__ == "__main__":
    main()
