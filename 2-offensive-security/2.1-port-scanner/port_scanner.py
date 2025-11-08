#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
port_scanner.py

Descrição:
Um scanner de portas TCP simples para identificar portas abertas em um host alvo.
Isso é usado na fase de Reconhecimento de um pentest.


Autor: Ana Luísa Valeriano Bomfim
Data: 8 de Novembro de 2025
"""

import socket
import sys
import argparse
from datetime import datetime

# --- Constantes de Cores ---
C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_CYAN = '\033[96m'
C_BOLD = '\033[1m'
C_END = '\033[0m'

def scan_port(host_ip, port):
    """
    Tenta se conectar a uma porta específica no host.
    Retorna True se a porta estiver aberta, False caso contrário.
    """
    try:
        # AF_INET = IPv4, SOCK_STREAM = TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Define um timeout curto (1 segundo) para a tentativa de conexão
        sock.settimeout(1.0)
        
        # connect_ex retorna 0 se a conexão for bem-sucedida (porta aberta)
        result = sock.connect_ex((host_ip, port))
        
        if result == 0:
            return True
        else:
            return False
    except socket.error as e:
        print(f"\n{C_RED}[ERRO] Erro de socket: {e}{C_END}")
        return False
    finally:
        # Garante que o socket seja sempre fechado
        sock.close()

def resolve_host(hostname):
    """
    Resolve um nome de host (ex: google.com) para um endereço IP.
    """
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror: # gaierror = get address info error
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Scanner de Portas TCP simples.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "host", 
        help="O host (IP ou domínio) a ser escaneado."
    )
    parser.add_argument(
        "-p", "--ports",
        dest="port_range",
        default="1-1024",
        help="O range de portas a escanear (ex: 1-1024, 80, 22,443).\n(Default: 1-1024)"
    )
    
    args = parser.parse_args()
    
    target_host = args.host
    port_range_str = args.port_range
    
    # --- Resolução do Host ---
    target_ip = resolve_host(target_host)
    if not target_ip:
        print(f"{C_RED}[ERRO] Não foi possível resolver o host: {target_host}{C_END}")
        sys.exit(1)

    # --- Análise do Range de Portas ---
    ports_to_scan = []
    try:
        # Se for um range (ex: 1-1024)
        if '-' in port_range_str:
            start, end = map(int, port_range_str.split('-'))
            ports_to_scan = list(range(start, end + 1))
        # Se for uma lista (ex: 22,80,443)
        elif ',' in port_range_str:
            ports_to_scan = list(map(int, port_range_str.split(',')))
        # Se for uma porta única
        else:
            ports_to_scan = [int(port_range_str)]
    except ValueError:
        print(f"{C_RED}[ERRO] Formato de porta inválido. Use '1-1024' ou '80,443'.{C_END}")
        sys.exit(1)

    # --- Execução do Scan ---
    print("="*50)
    print(f"Iniciando scan em {C_BOLD}{target_host}{C_END} ({C_CYAN}{target_ip}{C_END})")
    print(f"Scan de {len(ports_to_scan)} portas: {port_range_str}")
    print(f"Horário de início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)

    start_time = datetime.now()
    open_ports = []

    try:
        for port in ports_to_scan:
            # Imprime um status para o usuário não achar que travou
            print(f"  Testando porta {port}...", end='\r')
            if scan_port(target_ip, port):
                print(f"{C_GREEN}[+] Porta {port}/TCP está aberta!{C_END}{' '*20}") # ' '*20 limpa a linha
                open_ports.append(port)
                
    except KeyboardInterrupt:
        print(f"\n\n{C_YELLOW}[AVISO] Scan interrompido pelo usuário.{C_END}")
    
    end_time = datetime.now()
    total_time = end_time - start_time
    
    print("\n" + "="*50)
    print(f"{C_BOLD}Scan Concluído.{C_END}")
    print(f"Tempo total: {total_time}")
    
    if open_ports:
        print(f"\n{C_GREEN}Portas abertas encontradas:{C_END}")
        print(f"  {', '.join(map(str, open_ports))}")
    else:
        print(f"\n{C_YELLOW}Nenhuma porta aberta encontrada no range especificado.{C_END}")
    print("="*50)

if __name__ == "__main__":
    main()
