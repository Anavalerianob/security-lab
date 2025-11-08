# 1.3 - Monitor de Integridade de Arquivos (FIM)

Este script Python é um Monitor de Integridade de Arquivos (FIM) simples. Ele é usado para detectar alterações, adições ou remoções não autorizadas em arquivos críticos do sistema.

## O que ele faz?

Ele usa **hashes SHA256** para criar uma "impressão digital" (baseline) de um conjunto de arquivos. Em seguida, ele pode comparar o estado atual desses arquivos com a baseline salva para identificar qualquer adulteração.

**Funcionalidades:**
* **Modo Baseline (`--baseline`):** Cria um arquivo `file_baseline.json` que armazena os hashes SHA256 de todos os arquivos listados em `monitor_files.conf`.
* **Modo Verificação (`--check`):** Compara os hashes atuais dos arquivos com os hashes salvos na baseline e relata:
    * **[ALTERADO]**: Se o hash de um arquivo mudou.
    * **[REMOVIDO]**: Se um arquivo monitorado foi deletado.
    * **[ADICIONADO]**: Se um arquivo que não existia na baseline foi criado.
      
##  Como Usar

Este script requer um arquivo de configuração para saber quais arquivos monitorar.

1.  **Criar `monitor_files.conf`**:
    Na mesma pasta do script (`1.3-file-integrity-monitor/`), crie um arquivo chamado `monitor_files.conf`. Adicione os caminhos dos arquivos que você deseja monitorar, um por linha.

    *Exemplo de `monitor_files.conf`:*
    ```
    /etc/passwd
    /etc/shadow
    /etc/hosts
    /var/www/html/index.html
    /home/ana/meu_script_importante.py
    ```
    *(Se estiver no Windows, use caminhos do Windows, ex: `C:\Windows\System32\drivers\etc\hosts`)*

2.  **Criar a Baseline Inicial**:
    Execute o script com a flag `--baseline`.
    ```bash
    python fim.py --baseline
    ```
    Isso criará o `file_baseline.json`.

3.  **Verificar a Integridade**:
    Para checar se algo mudou, execute o script com a flag `--check`.
    ```bash
    python fim.py --check
    ```

4.  **(Teste)**:
    Tente modificar um dos arquivos que você está monitorando (ex: adicione um comentário no `hosts`). Rode `--check` novamente para ver o alerta **[ALTERADO]**!

##  Habilidades Demonstradas

* **Python:** `argparse`, `hashlib`, `json`, `os`, `sys`.
* **Criptografia:** Geração e comparação de hashes SHA256.
* **Blue Team:** Monitoramento de Sistemas (Host-based), Detecção de Adulteração (Tampering), Controles de Segurança.
