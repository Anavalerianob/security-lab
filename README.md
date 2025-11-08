# 🔬 Security Lab de Ana Luísa Valeriano

Olá! Este repositório é o meu laboratório pessoal de cibersegurança, onde aplico e documento meus estudos em projetos práticos.

Eu sou **Ana Luísa Valeriano Bomfim**, estudante de Ciência da Computação na UFJ e com grande interesse pela área de Segurança da Informação. Meu foco é o desenvolvimento de uma carreira em **Blue Team** e **testes de penetração**.

Este espaço serve como um portfólio técnico para demonstrar minhas habilidades em Python, análise de logs, reconhecimento de redes e governança.

---

## 📂 Projetos

Aqui estão os scripts e ferramentas que desenvolvi, organizados por área:

### 1. 🛡️ Blue Team (Defesa e Análise)

Projetos focados em detecção, monitoramento e resposta a incidentes.

* **[1.1 - Analisador de Logs `auth.log`](/1-blue-team/1.1-log-analyzer/)**
    * **Descrição:** Script em Python que analisa logs de autenticação do Linux (`/var/log/auth.log`) para identificar tentativas de login falhas, logins bem-sucedidos e potenciais ataques de força bruta.
    * **Habilidades:** `Python`, `Análise de Logs`, `Resposta a Incidentes`.

* **[1.2 - Verificador de Reputação de IP](/1-blue-team/1.2-ip-reputation-checker/)**
    * **Descrição:** Script que consome a API do AbuseIPDB (ou outra) para verificar se um endereço IP é conhecido por atividades maliciosas (Spam, C2, etc.).
    * **Habilidades:** `Python`, `Consumo de API`, `Threat Intelligence`.

### 2. 🔎 Pentest (Reconhecimento)

Ferramentas para automatizar a fase de reconhecimento (reconnaissance) em testes de penetração.

* **[2.1 - Simple Port Scanner](/2-pentest-recon/2.1-port-scanner/)**
    * **Descrição:** Um scanner de portas TCP simples, construído com sockets Python, para verificar portas abertas em um host alvo.
    * **Habilidades:** `Python`, `Redes (TCP/IP)`, `Scripting de Segurança`.

* **[2.2 - Enumerador de Subdomínios](/2-pentest-recon/2.2-subdomain-enumerator/)**
    * **Descrição:** Ferramenta que utiliza uma wordlist para fazer consultas DNS e descobrir subdomínios válidos de um domínio alvo.
    * **Habilidades:** `Python`, `Redes (DNS)`, `Pentest (Recon)`.

### 3. ⚖️ Governança e LGPD

Scripts focados em conformidade, gestão de riscos e proteção de dados.

* **[3.1 - Scanner de Dados Sensíveis (LGPD)](/3-governance-lgpd/3.1-sensitive-data-scanner/)**
    * **Descrição:** Script que varre arquivos (`.txt`, `.csv`) em um diretório local em busca de padrões que correspondam a dados sensíveis (ex: CPFs, e-mails), usando expressões regulares (Regex).
    * [cite_start]**Habilidades:** `Python`, `Regex`, `Governança (LGPD/DLP)`. [cite: 31]

---

## 🛠️ Tecnologias e Conceitos

As principais ferramentas e conceitos que estou aplicando neste laboratório incluem:

* **Linguagem:** Python
* [cite_start]**Conceitos de Segurança:** Análise de Incidentes (Blue Team), Testes de Penetração (Recon), Governança (LGPD, Gestão de Riscos), Análise de Logs. [cite: 31]
* [cite_start]**Redes e Sistemas:** Protocolos (TCP, DNS, HTTP), Administração Básica de Linux. [cite: 32]
* [cite_start]**Ferramentas:** Git/GitHub. [cite: 33]

---

## 📬 Contato

Vamos nos conectar!

* [cite_start]**LinkedIn:** [linkedin.com/in/analuisavaleriano](https://linkedin.com/in/analuisavaleriano) [cite: 4]
* [cite_start]**GitHub:** [github.com/Anavalerianob](https://github.com/Anavalerianob) [cite: 5]
