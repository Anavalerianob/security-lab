# 2.1 - Simple Port Scanner

Este é um scanner de portas TCP simples, construído em Python usando a biblioteca `socket`. Ele é projetado para identificar portas abertas em um host alvo, uma etapa fundamental na fase de reconhecimento (reconnaissance) de um teste de penetração.

## O que ele faz?

* Resolve um nome de domínio (ex: `google.com`) para seu endereço IP.
* Aceita um range de portas (ex: `1-1024`), uma lista de portas (ex: `80,443`) ou uma porta única.
* Tenta se conectar a cada porta especificada usando um socket TCP.
* Relata quais portas estão abertas (aceitando conexões).

## Como Usar

Execute o script a partir da linha de comando, passando o host como argumento obrigatório.

**Sintaxe:**
```bash
python port_scanner.py <host> [opções]
