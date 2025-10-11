# -*- coding: utf-8 -*-
import subprocess
import os
import re
import csv
import pandas as pd
import smtplib
from email.message import EmailMessage
from datetime import datetime
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Variáveis Globais (Ajuste para seu ambiente de teste)
SIMULATED_LOG_FILE = "server_error.log"
INVENTORY_FILE = "inventory_report.csv"
REPORT_DESTINATION = "automation_report.xlsx"

# --- 1. Automação de Senha e Usuário (Simulação de Ações de SO) ---

def reset_user_password(username):
    """
    Simula o reset de senha de um usuário, usando o módulo 'subprocess'
    para demonstrar interação com comandos de sistema operacional (Windows/Linux).
    """
    logging.info(f"Tentativa de reset de senha para usuário: {username}")
    
    # Simulação: Em um ambiente Windows, você usaria 'net user [username] [nova_senha]'
    # Em um ambiente de rede real, você usaria 'ldap3' para interagir com o Active Directory.
    try:
        # Comando simulado - usa 'echo' para simular a saída de um comando de sucesso
        comando_simulado = f'echo Senha de {username} resetada com sucesso na simulação.'
        
        # Executa o comando via shell
        resultado = subprocess.run(comando_simulado, shell=True, check=True, 
                                   capture_output=True, text=True)
        
        logging.info(f"Reset de Senha SUCESSO: {resultado.stdout.strip()}")
        return True
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Reset de Senha FALHA: Erro ao executar comando. {e.stderr.strip()}")
        return False

# --- 2. Análise de Logs Simples (Foco em Diagnóstico Rápido) ---

def analisar_logs_erros(log_file):
    """
    Analisa um arquivo de log em busca de padrões de erro críticos.
    Demonstra uso de Expressões Regulares (re) e Lógica de Suporte.
    """
    if not os.path.exists(log_file):
        logging.warning(f"Arquivo de log não encontrado: {log_file}. Criando log simulado...")
        with open(log_file, 'w') as f:
            f.write("[2025-10-10 08:30:00] INFO: Sistema Iniciado\n")
            f.write("[2025-10-10 09:15:22] ERROR: Falha na Conexão com DB: Timeout\n")
            f.write("[2025-10-10 10:45:01] INFO: Rotina de Backup OK\n")
            f.write("[2025-10-10 11:01:55] FATAL: Erro Crítico de Memória. Processo Terminado\n")
            
    logging.info(f"Iniciando análise de erros críticos em {log_file}...")
    
    erros_criticos = []
    # Expressão regular para buscar linhas com ERROR ou FATAL
    error_pattern = re.compile(r"\[.*?\] (ERROR|FATAL): (.*)")
    
    with open(log_file, 'r') as f:
        for linha in f:
            match = error_pattern.search(linha)
            if match:
                erros_criticos.append(f"{match.group(1)} - {match.group(2)}")
                
    if erros_criticos:
        logging.warning(f"*** {len(erros_criticos)} ERROS CRÍTICOS/FATAIS ENCONTRADOS ***")
        for erro in erros_criticos:
            print(f"  [ALERTA] {erro}")
    else:
        logging.info("Nenhum erro crítico ou fatal encontrado no log.")
        
    return erros_criticos

# --- 3. Geração de Relatório de Inventário (Análise de Dados) ---

def gerar_relatorio_inventario():
    """
    Lê dados de inventário (simulado em CSV) e gera um relatório consolidado em Excel.
    Demonstra manipulação de dados com pandas e geração de relatórios.
    """
    # Cria o CSV de inventário simulado se não existir
    if not os.path.exists(INVENTORY_FILE):
        logging.info(f"Criando arquivo de inventário simulado: {INVENTORY_FILE}")
        with open(INVENTORY_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Local', 'OS', 'Memoria_GB', 'CPU_Cores', 'Status'])
            writer.writerow([101, 'Financeiro', 'Win10', 8, 4, 'Online'])
            writer.writerow([102, 'Vendas', 'Win11', 16, 6, 'Offline'])
            writer.writerow([103, 'Desenvolvimento', 'Linux', 32, 8, 'Online'])
            
    try:
        df = pd.read_csv(INVENTORY_FILE)
        
        # Realiza uma análise simples com pandas (Lógica de Suporte)
        contagem_os = df['OS'].value_counts().to_frame(name='Total de Equipamentos')
        media_memoria = df.groupby('OS')['Memoria_GB'].mean().to_frame(name='Media Memória (GB)')
        
        # Salva o relatório consolidado em XLSX
        with pd.ExcelWriter(REPORT_DESTINATION, engine='xlsxwriter') as writer:
            contagem_os.to_excel(writer, sheet_name='Contagem por OS')
            media_memoria.to_excel(writer, sheet_name='Média de Memória')
            df.to_excel(writer, sheet_name='Dados Brutos', index=False)
            
        logging.info(f"Relatório de inventário consolidado salvo em: {REPORT_DESTINATION}")
        return True
    except Exception as e:
        logging.error(f"Falha ao gerar relatório de inventário: {e}")
        return False

# --- 4. Notificação de Erro Crítico (Integração) ---

def notificar_erro_critico(erros):
    """
    Envia um e-mail de alerta sobre os erros críticos encontrados.
    Demonstra Integração com sistemas externos (SMTP).
    """
    if not erros:
        logging.info("Nenhum erro crítico para notificar via e-mail.")
        return False
        
    # --- Configurações de SMTP (AJUSTAR PARA TESTE) ---
    SMTP_SERVER = 'smtp.gmail.com' # Use um servidor de teste ou real
    SMTP_PORT = 587
    SENDER_EMAIL = 'seu_email@dominio.com' 
    SENDER_PASSWORD = 'sua_senha_app' # Use senha de app se for Gmail
    RECIPIENT_EMAIL = 'gestor_ti@dominio.com'
    
    msg = EmailMessage()
    msg['Subject'] = f"ALERTA AUTOMÁTICO: {len(erros)} Erros Críticos Detectados ({datetime.now().strftime('%H:%M')})"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    
    corpo_email = "O HelpDesk-Automator detectou os seguintes erros críticos:\n\n"
    corpo_email += "\n".join([f"- {e}" for e in erros])
    corpo_email += "\n\nPor favor, investigue o arquivo de log para mais detalhes."
    msg.set_content(corpo_email)

    logging.info(f"Tentando enviar alerta para {RECIPIENT_EMAIL}...")
    
    # Simulação da conexão e envio:
    try:
        # Comente as linhas abaixo para SIMULAR APENAS
        # with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        #     server.starttls()
        #     server.login(SENDER_EMAIL, SENDER_PASSWORD)
        #     server.send_message(msg)
            
        logging.info("Notificação por e-mail ENVIADA com sucesso (Simulado).")
        return True
    except Exception as e:
        logging.error(f"Falha no envio do e-mail (Verifique configurações SMTP): {e}")
        logging.warning("Prosseguindo com a simulação. Alerta foi logado.")
        return False

# --- Menu Principal ---

def main():
    """
    Menu de console para orquestrar as rotinas de automação.
    """
    while True:
        print("\n" + "="*50)
        print("    HelpDesk-Automator (Automação de Suporte L1/L2)")
        print("="*50)
        print("1. Resetar Senha de Usuário (Simulação AD/OS)")
        print("2. Analisar Logs e Notificar Erros Críticos")
        print("3. Gerar Relatório Consolidado de Inventário (XLSX)")
        print("4. Executar Todas as Rotinas (Diário)")
        print("5. Sair")
        print("="*50)
        
        escolha = input("Selecione uma opção: ")
        
        if escolha == '1':
            user = input("Nome de usuário para resetar: ")
            reset_user_password(user)
        
        elif escolha == '2':
            erros = analisar_logs_erros(SIMULATED_LOG_FILE)
            notificar_erro_critico(erros)
            
        elif escolha == '3':
            gerar_relatorio_inventario()
            
        elif escolha == '4':
            logging.info("Executando Rotina Diária Completa...")
            reset_user_password("usuario_teste_rotina") # Simulação de reset
            erros = analisar_logs_erros(SIMULATED_LOG_FILE)
            notificar_erro_critico(erros)
            gerar_relatorio_inventario()
            logging.info("Rotina Diária Completa: FIM.")
            
        elif escolha == '5':
            print("Encerrando o HelpDesk-Automator. Até logo!")
            break
            
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()