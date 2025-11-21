#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Monitoramento básico de sistema e serviços
Rodar em Kali Linux

Requisitos:
pip install psutil
"""

import psutil
import datetime
import subprocess
import logging
import os

# Caminho para o log
LOG_FILE = "/var/log/monitoramento.log"

# Configuração do log
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def registrar_evento(msg):
    print(msg)
    logging.info(msg)

def check_cpu():
    uso_cpu = psutil.cpu_percent(interval=1)
    if uso_cpu > 85:
        registrar_evento(f"⚠️ Uso alto de CPU: {uso_cpu}%")
    return uso_cpu

def check_memoria():
    mem = psutil.virtual_memory()
    uso_mem = mem.percent
    if uso_mem > 85:
        registrar_evento(f"⚠️ Uso alto de memória: {uso_mem}%")
    return uso_mem

def check_disco():
    disco = psutil.disk_usage('/')
    uso = disco.percent
    if uso > 90:
        registrar_evento(f"⚠️ Disco quase cheio: {uso}%")
    return uso

def check_servico(nome_servico):
    try:
        resultado = subprocess.getoutput(f"systemctl is-active {nome_servico}")
        if "active" not in resultado:
            registrar_evento(f"❌ Serviço parado: {nome_servico}")
            return False
        return True
    except Exception as e:
        registrar_evento(f"Erro ao checar serviço {nome_servico}: {str(e)}")
        return False

def check_processos_suspeitos():
    blacklist = ["nc", "ncat", "hydra", "nikto", "msfconsole", "powershell"]
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            comando = " ".join(proc.info['cmdline']) if proc.info['cmdline'] else ""
            for item in blacklist:
                if item in comando:
                    registrar_evento(f"⚠️ Processo suspeito detectado: PID {proc.info['pid']} - {comando}")
        except:
            pass

def main():
    registrar_evento("=== Iniciando monitoramento ===")

    cpu = check_cpu()
    mem = check_memoria()
    disco = check_disco()

    servicos = ["prometheus", "grafana-server"]

    for serv in servicos:
        check_servico(serv)

    check_processos_suspeitos()

    registrar_evento(
        f"Métricas atuais | CPU: {cpu}% | RAM: {mem}% | Disco: {disco}%"
    )

    registrar_evento("=== Monitoramento finalizado ===\n")

if __name__ == "__main__":
    main()
