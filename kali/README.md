# Instruções e Instalação

### Instruções para instalação e uso dos Frameworks e utilização das VMs.

# ✅**Instalação**

## **1) Faça o download da ISO ou OVA Kali e o download do VirtualBox**

### Disponível no site oficial do Kali ou realizando cadastro/login no NetAcad e se dirigindo ao [hub de recursos e aplicações](https://www.netacad.com/resources/lab-downloads?courseLang=en-US)

### [VirtualBox](https://www.virtualbox.org/)

# ✅**Instruções**

## **2) Criação de uma nova VM no VirtualBox**

 - **Tipo:** Linux

 - **Versão:** Debian (64-bit)

 - **CPU:** 2 cores

 - **RAM:** 2-4 GB

 - **Disco:** 30-35 GB

 - **Rede:** Nat ou Bridged (Ambos funcionam)

### **2.1) Importe a ISO e dê boot**

### **2.2) No caso da OVA**

### Caso você baixou a OVA do NetAcad, basta ir em "importar appliance"

### **3) Importar os frameworks**

### **3.1) Crie pasta compartilhada**

 - VirtualBox  > Kali VM  > Configurações  > Pastas Compartilhadas

 - Caminho: Escolha o caminho de sua preferência

 - Ative: "Montagem Automática", "Permanente"

### **3.2) Dê boot na máquina**

 - A pasta aparece em:

	 `/media/sf _ <nomedapasta > `

### **3.3) Copie o arquivo Prometheus**

Exemplo:

 ` cp /media/sf _ <nomedapasta >/prometheus *.tar.gz  ~/Downloads/  `

Caso precise de permissões:

 `sudo usermod  -aG vboxsf $USER `

(reboot)

### **3.3.1) Implementação do `Prom` na Máquina**

### **3.3.2) Extraia o arquivo**

 ```bash
 cd  ~/Downloads

 tar xvf prometheus *.tar.gz

 cd prometheus- *
```

### **3.3.3) Rode o `Prom` manualmente**

 `./prometheus `

Prometheus agora está locado em:

 `http://localhost:9090 `

### **3.3.4) Adicione um .service (systemd)**

Crie um arquivo chamado  `prometheus.service `

 `sudo nano /etc/systemd/system/prometheus.service `

Cole no arquivo:

 ```bash
 [Unit ]

Description=Prometheus Monitoring

After=network.target

 [Service ]

User=root

ExecStart=/home/kali/Downloads/prometheus- */prometheus

Restart=always

 [Install ]

WantedBy=multi-user.target

```

Ative: 

	

 ```bash
 sudo systemctl daemon-reload

 sudo systemctl enable prometheus

 sudo systemctl start prometheus

 system status prometheus
```

### **3.4) Implementação do Grafana**

### **3.4.1) Adicione o repositório**

 ```bash
sudo apt install  -y apt-transport-https software-properties-common wget

wget  -q  -O  - https://packages.grafana.com/gpg.key | sudo apt-key add  -

echo "deb https://packages.grafana.com/oss/deb stable main" |   

sudo tee  -a /etc/apt/sources.list.d/grafana.list

sudo apt update
```

### **3.4.2) Instale o Grafana**

 `sudo apt install grafana  -y `

### **3.4.3) Utilize os comandos `enable` e `start`**

 ```bash
sudo systemctl enable grafana-server

sudo systemctl start grafana-server 
```

('Enable' server para ligar o servidor com o boot da máquina)

Servidor do grafana está locado em: 

 `http://localhost:3000 `

Login Default:

	 - user:  `admin `

	 - pw:  `admin `

### **4) Comece o monitoramento**

### **4.1) Instale o `node exporter` (revisar)**

 `sudo apt install prometheus-node-exporter  -y `

Servidor está locado em:

 `http://localhost:9100/metrics `

### **4.1.1) Adicione-o à config do `Prom`**

Edite o .yml

 `sudo nano /etc/prometheus/proetheus.yml `

Adicione:

 ```bash
	scrape _configs:

   - job _name: 'kali'

    static _configs:

      - targets:  ['localhost:9100' ]
```

Reinicie o  `Prom `

 `sudo systemctl restart prometheus `

Agora o sistema de  `metrics ` aparece no **Prometheus**e no **Grafana**

### **5) Adicione uma segunda VM (No meu caso estarei utilizando Debian 7)**

### **5.1)Adicione novamente as opções de pastas compartilhadas caso necessário (tópico 3.1)**

### **5.1.1) Atualize a VM caso necessário, se não, pule para o tópico "5.1.2".**

 ```bash
 sudo apt-get update

 sudo apt-get upgrade
```

### **5.1.2) Implemente o `node-exporter` ao Debian**

`cd /opt
 sudo wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz`

`sudo apt-get install prometheus-node-exporter -y`

`ip a`

Adicione a config do `Prom` ao Kali:

`- job_name: 'debian'
	static_configs:
		- targets: ['192.168.X.10']`

Reinicie:

`sudo systemctl restart prometheus`


### **Importe ou faça dashboards no grafana**

**Dashboards Recomendados**

|**Dashboard ID**|		**Purpose**                       |
|----------------|----------------------------------------|  
|      1860		 |	Full node exporter Linux monitoring   |
|      3662		 |	Process monitoring                    |
|      8919	   	 |	Host status overview                  |
|      13978	 |	Debian metrics                        |
|      11074	 |	System logs + performance             |


**Grafana → Dashboards → Import**

Coloque o ID do dashboard (e.g., `1860`) → Load → Selecione o `Prometheus` como data source → importar 

(Também deixarei um .json para ser importado, porém ainda protótipo)

### **Testes de Stress**

### **Gerenciador de Alertas (Alertmanager)**

### instalar

`cd /opt
sudo wget https://github.com/prometheus/alertmanager/releases/download/v0.27.0/alertmanager-0.27.0.linux-amd64.tar.gz
sudo tar -xvf alertmanager-0.27.0.linux-amd64.tar.gz`

###Mover e criar diretórios 

```bash
sudo cp /opt/alertmanager-0.27.0.linux-amd64/alertmanager /usr/local/bin/
sudo cp /opt/alertmanager-0.27.0.linux-amd64/amtool /usr/local/bin/
which alertmanager
alertmanager --version
sudo mkdir -p /etc/alertmanager
sudo mkdir -p /var/lib/alertmanager
sudo useradd --no-create-home --shell /bin/false alertmanager
sudo chown alertmanager:alertmanager /usr/local/bin/alertmanager
sudo chown alertmanager:alertmanager /usr/local/bin/amtool
sudo chown alertmanager:alertmanager /etc/alertmanager
sudo chown alertmanager:alertmanager /var/lib/alertmanager
sudo nano /etc/alertmanager/alertmanager.yml
```

### Dentro da config (`.yml`)

```bash
global:
  resolve_timeout: 5m

route:
  receiver: 'default'

receivers:
  - name: 'default'
```


### Crie um .service (`systemd`)

`sudo nano /etc/systemd/system/alertmanager.service`

### Dentro da config (`.service`)

```bash
[Unit]
Description=Prometheus Alertmanager
After=network.target

[Service]
User=alertmanager
Group=alertmanager
Type=simple
ExecStart=/usr/local/bin/alertmanager \
  --config.file=/etc/alertmanager/alertmanager.yml \
  --storage.path=/var/lib/alertmanager

Restart=always

[Install]
WantedBy=multi-user.target
```


### Enable, Start e Status

```bash
sudo systemctl daemon-reload
sudo systemctl enable alertmanager
sudo systemctl start alertmanager
sudo systemctl status alertmanager
```

### Dentro do navegador:

`http://localhost:9093`


### Conecte o Prometheus ao Alertmanager

`sudo nano /etc/prometheus/prometheus.yml`

### Dentro da config (`.yml`), adicione:


```bash
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - "localhost:9093"
```

`sudo systemctl restart prometheus`



### Test Alert

Na sua máquina principal: 

`sudo nano /etc/prometheus/alert.rules.yml`

Dentro da `.yml`:

```bash
groups:
- name: test
  rules:
  - alert: AlwaysFiringTest
    expr: vector(1)
    for: 10s
    labels:
      severity: warning
    annotations:
      summary: "Test alert"
      description: "This alert should always fire"
```


Conecte a regra dentro da `prometheus.yml`:

`sudo nano /etc/prometheus/prometheus.yml`

Adicione:

```bash
rule_files:
  - "alert.rules.yml"
```

```bash
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - "localhost:9093"
```

`sudo systemctl restart prometheus`

### Resultado

A cada 10-15 segundos abra:

`http://localhost:9093`

### Importante
Caso haja confirmação de que está rodando perfeitamente, delete a regra `AlwaysFiringTest` dentro da `alert.rules.yml`. Ou ficará rodando para sempre.


### Config `.json` Grafana 

Após habilitar o Grafana (`grafana-server`), deve-se importar o `prometheus` pela `datasource`

Connections > Data Sources > + Add new data source > Prometheus























### **Exportando o laboratório para outra máquina ´física**

### A Terceira máquina usada será um W11

Use `windows-exporter`

Porta HTTP padrão: **9182**

No powershell:

`msiexec /i C:\windows_exporter-0.31.3-amd64.msi ENABLED_COLLECTORS=cpu,cs,logical_disk,net,os,memory,process,service /qn`

Fine-tune process(Opcional):

`.\windows_exporter.exe --collectors.enabled "process,cs,logical_disk" --collector.process.include="firefox.+"`

Verificar o exporter no W11:

Browser:
`http://localhost:9182/metrics`

bash kali:
`curl https:/<WIN_IP>:9182/metrics`(substitua `<WIN_IP` pelo ip real)

Se o prometheus der get nas metricas --> sucesso, caso contrário verifique o Firewall ou se o serviço está up e rodando.

### **Caso contrário:**
`Get-Service windows_exporter`

Caso o `Status` esteja `Running`, OK.

Se não:

`cd "C:\Program Files\windows_exporter"`
`.\windows_exporter.exe --collectors.enabled="cpu,memory,os,net,logical_disk,process,service,system"`

'isso fará o exporter rodar' 

**Irei deixar um .json para exibir as métricas da maquina Win11**





### **No Kali (`prometheus.yml`), adicione um `job_name`: **

```bash
 scrape_configs:
  - job_name: 'real-windows-desktop'
    static_configs:
      - targets: ['192.168.1.55:9182']   # <-- replace with your Windows desktop IP
    params:
      # optional: to request only specific collectors from this scrape:
      # collect[]:
      #   - cpu
      #   - memory
```

Reinicie o prom e verifique `http://<PROM_HOST>:9090/targets` -- deve estar rodando (UP)








### **Este `markdown` será atualizado periodicamente, trazendo novas funções e implementações com o decorrer do tempo.**



