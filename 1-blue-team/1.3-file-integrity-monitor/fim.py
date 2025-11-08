#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fim.py

Descrição:
Monitor de Integridade de Arquivos (FIM).
Este script cria uma 'baseline' de hashes SHA256 de arquivos
e verifica se esses arquivos foram alterados, adicionados ou removidos.


Autor: Ana Luísa Valeriano Bomfim
Data: 18 de Março de 2025
"""

import os
import sys
import json
import hashlib
import argparse

# --- Constantes de Cores ---
C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_CYAN = '\033[96m'
C_BOLD = '\033[1m'
C_END = '\033[0m'

# --- Constantes de Arquivos ---
BASELINE_FILE = 'file_baseline.json'
# Você deve criar este arquivo e listar os caminhos dos arquivos a monitorar
CONFIG_FILE = 'monitor_files.conf'

def calculate_sha256(filepath):
    """Calcula o hash SHA256 de um arquivo."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Lê o arquivo em blocos de 4KB para não sobrecarregar a memória
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except IOError as e:
        print(f"{C_RED}[ERRO] Não foi possível ler o arquivo: {filepath} ({e}){C_END}")
        return None

def get_files_to_monitor():
    """Lê o arquivo de configuração e retorna uma lista de arquivos."""
    if not os.path.exists(CONFIG_FILE):
        print(f"{C_YELLOW}[AVISO] Arquivo de configuração '{CONFIG_FILE}' não encontrado.{C_END}")
        print("Por favor, crie este arquivo e adicione os caminhos dos arquivos a monitorar, um por linha.")
        return []
        
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            # Lê as linhas, remove espaços em branco e ignora linhas vazias
            files = [line.strip() for line in f if line.strip()]
        return files
    except IOError as e:
        print(f"{C_RED}[ERRO] Não foi possível ler o '{CONFIG_FILE}': {e}{C_END}")
        sys.exit(1)

def create_baseline():
    """Cria a baseline de hashes dos arquivos monitorados."""
    print(f"{C_CYAN}[INFO] Criando baseline de integridade...{C_END}")
    files_to_monitor = get_files_to_monitor()
    
    if not files_to_monitor:
        print(f"{C_RED}[ERRO] Nenhum arquivo para monitorar. Verifique o '{CONFIG_FILE}'.{C_END}")
        return

    baseline_data = {}
    for filepath in files_to_monitor:
        if not os.path.exists(filepath):
            print(f"{C_YELLOW}[AVISO] Arquivo não encontrado (será monitorado para criação): {filepath}{C_END}")
            baseline_data[filepath] = None # Monitora arquivos que deveriam existir
            continue
            
        file_hash = calculate_sha256(filepath)
        if file_hash:
            print(f"  [+] Monitorando: {filepath}")
            baseline_data[filepath] = file_hash
            
    try:
        with open(BASELINE_FILE, 'w', encoding='utf-8') as f:
            json.dump(baseline_data, f, indent=4)
        print(f"\n{C_GREEN}[SUCESSO] Baseline salva em '{BASELINE_FILE}' com {len(baseline_data)} arquivos.{C_END}")
    except IOError as e:
        print(f"\n{C_RED}[ERRO] Não foi possível salvar a baseline em '{BASELINE_FILE}': {e}{C_END}")

def check_integrity():
    """Verifica a integridade dos arquivos contra a baseline."""
    print(f"{C_CYAN}[INFO] Verificando integridade dos arquivos...{C_END}")
    
    if not os.path.exists(BASELINE_FILE):
        print(f"{C_RED}[ERRO] Arquivo de baseline '{BASELINE_FILE}' não encontrado.{C_END}")
        print("Por favor, execute o script com o argumento '--baseline' primeiro.")
        sys.exit(1)

    try:
        with open(BASELINE_FILE, 'r', encoding='utf-8') as f:
            baseline_data = json.load(f)
    except IOError as e:
        print(f"{C_RED}[ERRO] Não foi possível ler a baseline: {e}{C_END}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{C_RED}[ERRO] O arquivo de baseline está corrompido (JSON inválido).{C_END}")
        sys.exit(1)

    print(f"  [+] Baseline carregada. Verificando {len(baseline_data)} arquivos...")
    
    issues_found = 0
    current_files_on_disk = get_files_to_monitor()
    
    # 1. Verifica arquivos da baseline (Alterados ou Removidos)
    for filepath, baseline_hash in baseline_data.items():
        if not os.path.exists(filepath):
            # O arquivo existia na baseline (tinha hash) mas não existe mais?
            if baseline_hash is not None:
                print(f"  {C_RED}{C_BOLD}[REMOVIDO] O arquivo foi removido: {filepath}{C_END}")
                issues_found += 1
            # O arquivo não existia e ainda não existe (OK)
            else:
                pass
        else:
            current_hash = calculate_sha256(filepath)
            
            # O arquivo não existia mas foi criado?
            if baseline_hash is None:
                print(f"  {C_GREEN}{C_BOLD}[ADICIONADO] Novo arquivo criado: {filepath}{C_END}")
                issues_found += 1 # Consideramos uma "issue" para reportar
            # O arquivo existia, vamos comparar os hashes
            elif baseline_hash != current_hash:
                print(f"  {C_RED}{C_BOLD}[ALTERADO] O arquivo foi modificado: {filepath}{C_END}")
                print(f"    - Baseline: {baseline_hash}")
                print(f"    - Atual:    {current_hash}")
                issues_found += 1
    
    # 2. Verifica se algum arquivo no .conf não estava na baseline (raro, mas bom checar)
    # (Este loop é mais complexo, podemos simplificar e checar apenas o get_files_to_monitor)
    current_files_set = set(current_files_on_disk)
    baseline_files_set = set(baseline_data.keys())
    
    new_files_not_in_baseline = current_files_set - baseline_files_set
    for new_file in new_files_not_in_baseline:
         if os.path.exists(new_file): # Garante que o arquivo existe
            print(f"  {C_YELLOW}{C_BOLD}[NÃO MONITORADO] Novo arquivo encontrado (não está na baseline): {new_file}{C_END}")
            issues_found += 1

    print("-" * 70)
    if issues_found == 0:
        print(f"{C_GREEN}{C_BOLD}Verificação concluída. Nenhuma alteração de integridade detectada.{C_END}")
    else:
        print(f"{C_YELLOW}{C_BOLD}Verificação concluída. {issues_found} problemas de integridade encontrados.{C_END}")

def main():
    """Função principal para executar o script."""
    parser = argparse.ArgumentParser(
        description="Monitor de Integridade de Arquivos (FIM) usando SHA256.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # Cria um grupo onde apenas um argumento pode ser usado de cada vez
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-b", "--baseline",
        action="store_true",
        help="Cria uma nova baseline de hashes dos arquivos em 'monitor_files.conf'."
    )
    group.add_argument(
        "-c", "--check",
        action="store_true",
        help="Verifica a integridade dos arquivos contra a baseline."
    )
    
    args = parser.parse_args()
    
    if args.baseline:
        create_baseline()
    elif args.check:
        check_integrity()

if __name__ == "__main__":
    main()
