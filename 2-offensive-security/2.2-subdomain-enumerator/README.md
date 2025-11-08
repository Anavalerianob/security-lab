# 2.2 - Enumerador de Subdomínios

Este script realiza uma enumeração de subdomínios baseada em dicionário. Ele usa uma lista de palavras (wordlist) para "adivinhar" subdomínios e tenta resolvê-los via consultas DNS para ver se eles existem.

## O que ele faz?

* Lê um domínio alvo (ex: `google.com`) e uma wordlist.
* Para cada palavra na wordlist (ex: `www`), ele forma um subdomínio (ex: `www.google.com`).
* Tenta resolver o registro DNS 'A' (IPv4) para esse subdomínio.
* Se a resolução for bem-sucedida, o subdomínio é considerado "encontrado" e é relatado ao usuário.

## Pré-requisitos

Este script depende da biblioteca `dnspython`. Você deve instalá-la antes de usar:

```bash
pip install dnspython
