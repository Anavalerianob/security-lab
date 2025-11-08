# 3.1 - Scanner de Dados Sensíveis (LGPD/PII)

Este script é uma ferramenta de Data Loss Prevention (DLP) muito básica. Ele varre recursivamente um diretório em busca de arquivos de texto (`.txt`, `.csv`, `.json`, etc.) que possam conter Informações de Identificação Pessoal (PII).

O objetivo é demonstrar o uso de Expressões Regulares (Regex) para identificar e ajudar a proteger dados sensíveis, um pilar central da **LGPD** e de boas práticas de **Governança de Dados**.

## O que ele faz?

* Percorre recursivamente todas as subpastas a partir de um diretório inicial.
* Abre arquivos que correspondem a extensões de texto comuns (ex: `.log`, `.csv`).
* Lê cada linha do arquivo e aplica um conjunto de regras de Regex para encontrar:
    * CPFs (no formato `xxx.xxx.xxx-xx`)
    * Endereços de e-mail
    * Números de Cartão de Crédito
    * Números de Telefone
* Relata todos os arquivos, linhas e os dados exatos que foram encontrados.

## Como Usar

Execute o script a partir da linha de comando, passando o diretório que você deseja analisar como argumento.

**Sintaxe:**
```bash
python data_scanner.py <caminho_do_diretorio>
