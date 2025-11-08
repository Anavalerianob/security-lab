# 2.3 - Basic Reverse Shell

Este projeto é um "shell reverso" básico escrito em Python. Ele é composto por dois scripts:
1.  **`server.py`**: O "listener" (ouvinte), que é executado na máquina do atacante.
2.  **`client.py`**: O "payload", que é executado na máquina da vítima.

O shell reverso é uma técnica fundamental de pós-exploração onde a máquina da vítima *inicia* uma conexão de volta para o atacante, muitas vezes para contornar firewalls.

**AVISO: Este projeto é estritamente para fins educacionais. Nunca execute este código em qualquer sistema sem permissão explícita.**

## O que ele faz?

* **`server.py`**: Abre um socket em um IP e porta específicos e aguarda que uma conexão (do `client.py`) chegue.
* **`client.py`**: Conecta-se ao IP e porta do servidor e aguarda por comandos.
* O **Servidor** envia comandos (ex: `ls -la`, `whoami`).
* O **Cliente** recebe o comando, o executa no sistema operacional da vítima usando `subprocess`, e envia o resultado (a saída do terminal) de volta para o servidor.
* O `client.py` também tenta se reconectar automaticamente se a conexão cair.

## Como Usar

Você precisará de dois terminais. Idealmente, teste isso usando duas máquinas virtuais (VMs) em uma rede 'host-only' ou 'NAT' para simular um atacante e uma vítima.

**1. No Terminal do Atacante (Sua máquina):**

Inicie o servidor e diga a ele para escutar na porta `4444` (ou qualquer porta de sua escolha).

```bash
# O IP 0.0.0.0 significa "escutar em todos os IPs desta máquina"
python server.py -p 4444
