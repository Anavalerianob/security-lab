> **Nota:** Este script requer a biblioteca `dnspython`. Instale-a primeiro:
> `pip install dnspython`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
sub_enum.py

Descrição:
Um enumerador de subdomínios simples que usa uma wordlist para
tentar resolver subdomínios de um domínio alvo via consultas DNS.


Autor: Ana Luísa Valeriano Bomfim
Data: 3 de Abril de 2025
"""

import argparse
import sys

try:
    import dns.resolver
except ImportError:
    print("Erro: A biblioteca 'dnspython' não está instalada.")
    print("Por favor, instale com: pip install dnspython")
    sys.exit(1)

# --- Constantes de Cores ---
C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_BOLD = '\033[1m'
C_END = '\033[0m'

def enumerate_subdomains(target_domain, wordlist_path):
    """
    Lê a wordlist e tenta resolver cada subdomínio.
    """
    found_subdomains = []
    
    try:
        with open(wordlist_path, 'r') as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{C_RED}[ERRO] Wordlist não encontrada em: {wordlist_path}{C_END}")
        sys.exit(1)
    except IOError as e:
        print(f"{C_RED}[ERRO] Não foi possível ler a wordlist: {e}{C_END}")
        sys.exit(1)
        
    print(f"Iniciando enumeração em {C_BOLD}{target_domain}{C_END} com {len(words)} palavras...")
    
    # Configura o resolvedor DNS
    resolver = dns.resolver.Resolver()
    # Tenta usar um resolver público comum
    resolver.nameservers = ['8.8.8.8', '1.1.1.1'] 
    
    for word in words:
        subdomain = f"{word}.{target_domain}"
        
        try:
            # Tenta resolver o registro 'A' (Endereço IPv4)
            resolver.resolve(subdomain, 'A')
            # Se a linha acima não falhar, o subdomínio existe
            print(f"{C_GREEN}[+] Encontrado: {subdomain}{C_END}")
            found_subdomains.append(subdomain)
            
        except dns.resolver.NXDOMAIN:
            # NXDOMAIN = Não existe (Normal)
            pass
        except dns.resolver.NoAnswer:
            # O domínio existe, mas não tem registro 'A' (ex: um CNAME)
            # Você poderia adicionar uma checagem de CNAME aqui
            pass
        except dns.resolver.Timeout:
            print(f"{C_YELLOW}[AVISO] Timeout ao checar: {subdomain}{C_END}")
        except KeyboardInterrupt:
            print(f"\n\n{C_YELLOW}[AVISO] Enumeração interrompida pelo usuário.{C_END}")
            return found_subdomains
        except Exception as e:
            # Captura outros erros de DNS
            pass
            
    return found_subdomains

def main():
    parser = argparse.ArgumentParser(
        description="Enumerador de subdomínios via DNS.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-d", "--domain",
        dest="target_domain",
        required=True,
        help="O domínio alvo (ex: google.com)."
    )
    parser.add_argument(
        "-w", "--wordlist",
        dest="wordlist_path",
        required=True,
        help="Caminho para a wordlist (lista de subdomínios)."
    )
    
    args = parser.parse_args()
    
    print("="*50)
    print("Iniciando Enumerador de Subdomínios")
    print("="*50)

    start_time = datetime.now()
    
    found = enumerate_subdomains(args.target_domain, args.wordlist_path)
    
    end_time = datetime.now()
    total_time = end_time - start_time
    
    print("\n" + "="*50)
    print(f"{C_BOLD}Enumeração Concluída.{C_END}")
    print(f"Tempo total: {total_time}")
    
    if found:
        print(f"\n{C_GREEN}{len(found)} Subdomínios encontrados:{C_END}")
        for sub in found:
            print(f"  - {sub}")
    else:
        print(f"\n{C_YELLOW}Nenhum subdomínio encontrado com esta wordlist.{C_END}")
    print("="*50)

# Importamos datetime aqui para não quebrar se o dnspython não estiver instalado
from datetime import datetime

if __name__ == "__main__":
    main()
O README.md (para 2.2-subdomain-enumerator)
Crie este arquivo em: 2-offensive-security/2.2-subdomain-enumerator/README.md

Markdown

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
