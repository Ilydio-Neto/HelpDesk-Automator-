#HelpDesk-Automator - Automação e Otimização de Suporte de TI

## Visão Geral do Projeto

O `HelpDesk-Automator` é um sistema modular que demonstra minha capacidade de aplicar Python para **automatizar rotinas de Suporte Nível 1 (L1) e Nível 2 (L2)**, liberando técnicos para tarefas que exigem intervenção humana especializada.

Este projeto foca em **redução de tempo operacional**, transformando tarefas manuais (como análise de logs, resets de senha e consolidação de relatórios) em processos instantâneos e repetíveis.

**Valor para o Negócio:** Demonstra uma mentalidade de DevOps/SRE aplicada ao Suporte, garantindo consistência, reduzindo erros humanos e aumentando a eficiência da equipe de TI.

## Habilidades Demonstradas

* **Automação de Tarefas Críticas:** Uso do `subprocess` para executar e validar comandos de Sistema Operacional (simulação de reset de conta).
* **Análise de Dados e Diagnóstico:** Uso de Expressões Regulares (`re`) para análise rápida de logs e `pandas` para consolidar dados brutos em relatórios gerenciais (inventário).
* **Integração:** Simulação de envio de notificações via `smtplib` e `email.message`, provando a capacidade de integrar a automação com sistemas de alerta (e-mail, Slack, etc.).
* **Lógica de Suporte:** A estrutura de menu e as rotinas mapeiam diretamente processos comuns de um Help Desk.

## Como Testar e Rodar o Script

### Pré-requisitos

Certifique-se de ter o Python 3.x instalado.

### 1. Configurar o Ambiente

Crie e ative o ambiente virtual e instale as dependências.

```bash
# Crie o ambiente virtual
python -m venv venv
# Ative o ambiente virtual (Linux/macOS)
source venv/bin/activate
# Ative o ambiente virtual (Windows)
.\venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
