# Security Lab de Ana Luísa Valeriano

Olá! Decidi criar este repositório com alguns scripts que desenvolvi durante meus estudos, se tornado meu laboratório pessoal de cibersegurança, aqui estão documentados alguns desses projetos práticos.

Eu sou Ana Luísa Valeriano Bomfim, estudante de Ciência da Computação na UFJ e extremamente interessada pela área de Segurança da Informação. Meu foco é o desenvolvimento de uma carreira em Blue Team e testes de penetração.

Este espaço serve como um portfólio técnico para demonstrar minhas habilidades em Python, análise de logs, reconhecimento de redes e governança.

---

## Projetos

Aqui estão os scripts e ferramentas que desenvolvi, organizados por área:

### 1. Blue Team (Defesa e Análise)

Projetos focados em detecção, monitoramento e resposta a incidentes.

* **[1.1 - Analisador de Logs `auth.log`](/1-blue-team/1.1-log-analyzer/)**
    * **Descrição:** Script em Python que analisa logs de autenticação do Linux (`/var/log/auth.log`) para identificar tentativas de login falhas, logins bem-sucedidos e potenciais ataques de força bruta.
    * **Habilidades:** `Python`, `Análise de Logs`, `Resposta a Incidentes`.

* **[1.2 - Verificador de Reputação de IP](/1-blue-team/1.2-ip-reputation-checker/)**
    * **Descrição:** Script que consome a API do AbuseIPDB para verificar se um endereço IP é conhecido por atividades maliciosas (Spam, C2, etc.).
    * **Habilidades:** `Python`, `Consumo de API`, `Threat Intelligence`.

* **[1.3 - Monitor de Integridade de Arquivos (FIM)](/1-blue-team/1.3-file-integrity-monitor/)**
    * **Descrição:** Script que usa hashes SHA256 para criar uma baseline de arquivos e detectar alterações, adições ou remoções não autorizadas.
    * **Habilidades:** `Python (hashlib)`, `Hashing`, `Monitoramento de Sistemas`.

### 2. Offensive Security (Red Team & Pentest)

Ferramentas e scripts que simulam as fases de um ataque, desde o reconhecimento até a pós-exploração.

* **[2.1 - Simple Port Scanner](/2-offensive-security/2.1-port-scanner/)**
    * **Descrição:** Scanner de portas TCP para identificar serviços abertos em um alvo (Fase: Reconhecimento).
    * **Habilidades:** `Python`, `Redes (TCP/IP)`.

* **[2.2 - Enumerador de Subdomínios](/2-offensive-security/2.2-subdomain-enumerator/)**
    * **Descrição:** Ferramenta para descobrir subdomínios válidos de um alvo (Fase: Reconhecimento).
    * **Habilidades:** `Python`, `Redes (DNS)`.

* **[2.3 - Basic Reverse Shell](/2-offensive-security/2.3-simple-reverse-shell/)**
    * **Descrição:** Par de scripts (servidor/cliente) para estabelecer um shell reverso básico (Fase: Exploração/C2).
    * **Habilidades:** `Python (Sockets)`, `Pós-Exploração`.

### 3. Governança e LGPD

Scripts focados em conformidade, gestão de riscos e proteção de dados.

* **[3.1 - Scanner de Dados Sensíveis (LGPD)](/3-governance-lgpd/3.1-sensitive-data-scanner/)**
    * **Descrição:** (Em desenvolvimento) Script que varre arquivos locais em busca de padrões de dados sensíveis (CPFs, etc.) usando Regex.
    * **Habilidades:** `Python`, `Regex`, `Governança (LGPD/DLP)`.

---

## Tecnologias e Conceitos

As principais ferramentas e conceitos que estou aplicando neste laboratório incluem:

* **Linguagem:** Python
* **Conceitos de Segurança:** Análise de Incidentes (Blue Team), Testes de Penetração (Red Team), Governança (LGPD, Gestão de Riscos), Análise de Logs, Threat Intelligence.
* **Redes e Sistemas:** Protocolos (TCP, DNS, HTTP), Administração Básica de Linux, Hashing Criptográfico.
* **Ferramentas:** Git/GitHub, APIs REST.

---

## Contato

Vamos nos conectar!

* **LinkedIn:** [linkedin.com/in/analuisavaleriano](https://linkedin.com/in/analuisavaleriano)
* **GitHub:** [github.com/Anavalerianob](https://github.com/Anavalerianob)
