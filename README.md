# Testes-PEN-Monitoramento
### Repositório utilizado para testes PEN e Monitoramento


# ✅ **ESCOPO DE TESTES (PENTEST E MONITORAMENTO)**
## **1) Objetivo Geral**

Avaliar a segurança, integridade e disponibilidade do ambiente de monitoramento, identificando vulnerabilidades e assegurando que o sistema detecte, registre e alerte sobre eventos de risco.

## **2) Escopo de Testes**
### **2.1 Infraestrutura Envolvida**

- Sistema operacional: Kali Linux

- Serviços instalados:

  - Prometheus

  - Grafana

- Rede local

- Possíveis integrações futuras:

- Script Python de monitoramento personalizado

- Banco de dados ou API coletando métricas

## **3) Testes de Pentest**
### **3.1 Testes de Reconhecimento**

- Coleta de informações públicas sobre o sistema

- Enumeração de portas e serviços

- Ferramentas:`nmap`, `masscan`, `netstat`

## **3.2 Testes de Segurança de Serviços Prometheus e Grafana**
### **3.2.1 Prometheus**

- Testar:

  - Exposição de porta sem autenticação

  - Acesso não autorizado ao `/metrics`

  - Falta de TLS/HTTPS

  - Configurações sensíveis expostas

- Ferramentas:

  - `curl`

  - `nikto`

  - `nmap`

### **3.2.2 Grafana**

- Testar:

  - Senhas fracas ou default

  - Enumeração de usuário

  - Tentativa de brute force

  - Falta de MFA

  - Plugins vulneráveis
- Ferramentas:

  - `hydra`

  - `wpscan` (adaptação para brute)

- **Mitigações Esperadas**

  - Autenticação habilitada

  - TLS configurado
  
  - Restringir acesso a portas via firewall

  - Uso de roles e permissões

## **3.3 Testes de Rede**

- Testes de firewall

- Testes de regras de NAT

- Análise de tráfego inseguro
- Ferramentas:

  - `wireshark`

  - `tcpdump`

  - `bettercap`

## **3.4 Testes de Hardening do Sistema Operacional**

- Verificação de falhas do Linux:

  - Serviços desnecessários rodando

  - Usuários não utilizados

  - Falta de controle de senhas

  - Falta de logs ativos

- Script de checklist:

  - `lynis`

  - `chkrootkit`

  - `clamav`

  - `systemctl list-units`

## **3.5 Testes de Escalação de Privilégio**

- Exploits locais

- Permissões mal configuradas

- SUID/SGID

- Ferramentas:

  - `linpeas.sh`

  - `linux-exploit-suggester`

## **4) Testes de Monitoramento**
## **4.1 O que deve ser monitorado**
### **4.1.1 Infraestrutura**

- CPU, memória, disco, rede

- Queda de serviços

- Consumo anormal

### **4.1.2 Segurança**

- Tentativas de login falhas

- Alterações de arquivos críticos

- Novos usuários criados

- Execução de processos suspeitos

### **4.1.3 Serviços Prometheus e Grafana**

- Disponibilidade (uptime)

- Latência de coleta

- Erros de API

- Uso de banco interno

## **4.2 Alertas Recomendados (Prometheus/Grafana)**


| Evento                     | Descrição                       | Ação recomendada          |
|---------------------------|----------------------------------|---------------------------|
| Alta carga de CPU         | CPU > 85% por 5 min              | Acionar alerta            |
| Múltiplas falhas de login | > 10 tentativas/5 min            | Registrar incidente       |
| Serviço parado            | Prometheus ou Grafana offline    | Notificar imediatamente   |
| Arquivo crítico alterado  | `/etc/passwd`, `/etc/shadow`         | Risco de intrusão         |


## **5) Futuro – Script de Monitoramento em Python**
## **5.1 Objetivo**

- Criar ferramenta própria para:

- Coletar métricas do sistema via Python

- Detectar eventos de segurança

 - Registrar logs

- Enviar alertas (Telegram, Slack, e-mail, API, etc.)

## **5.2 Tecnologias sugeridas**

`psutil` — métricas do sistema

`subprocess` — checagem de serviços

`argparse` — parâmetros de execução

`logging` — logs centralizados

`requests` — envio de alertas via API

`sqlite` ou `json` para armazenar histórico

## **5.3 Eventos a monitorar via Python**

- Alterações em arquivos críticos

- Novos processos suspeitos

- Falhas de login

- Reinício inesperado de serviços

- Checagem de integridade (hash de arquivos)

## **5.4 Possível ciclo de funcionamento**
```python
Coletar métricas → Detectar evento → Registrar log → Enviar alerta 
```
## **5.5 Integração com Prometheus**

- O Python pode expor métricas via:

`/metrics`


para o Prometheus coletar.

- Exemplo de biblioteca:

`prometheus_client`

## **6) Entregáveis do Projeto**
## **6.1 Relatórios**

- Relatório de vulnerabilidades com:

  - Risco

  - Evidência

  - Impacto

  - Recomendação

## **6.2 Dashboard no Grafana**

- Contendo:

   -Métricas de segurança

  - Disponibilidade

  - Alertas em tempo real

  - Indicadores de ataque

## **6.3 Documentação**

- Manual de resposta a incidentes

- Scripts utilizados

- Plano de hardening

## **7) Critérios de Sucesso**

- 90%+ das vulnerabilidades corrigidas

- Alertas funcionando em tempo real

- Auditoria e logs íntegros

- Visibilidade completa do ambiente

- Script Python funcional com alertas
