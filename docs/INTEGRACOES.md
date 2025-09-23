# 🔗 Configuração de Integrações e Automações

## 🎯 Objetivo
Configurar integrações com outras plataformas e automatizar processos.

## 🔧 Integrações Disponíveis

### 1. **Notion (Já Configurado)**
- ✅ **5 bancos de dados** interconectados
- ✅ **Sistema de classificação** multidimensional
- ✅ **API** para automação
- ✅ **Templates** de conteúdo

#### Próximos Passos:
- [ ] **Configurar token** de integração
- [ ] **Testar** scripts de publicação
- [ ] **Personalizar** views e filtros
- [ ] **Configurar** notificações

### 2. **WordPress (Opcional)**
```python
# Configurar em config.json
{
  "integracao": {
    "wordpress": {
      "url": "https://seusite.com",
      "usuario": "admin",
      "senha": "sua_senha",
      "habilitado": true
    }
  }
}
```

#### Script de Publicação WordPress
```python
# publicar_wordpress.py
import requests
from wordpress_xmlrpc import Client, WordPressPost

def publicar_no_wordpress(conteudo, titulo):
    wp = Client('https://seusite.com/xmlrpc.php', 'usuario', 'senha')
    
    post = WordPressPost()
    post.title = titulo
    post.content = conteudo
    post.post_status = 'publish'
    
    wp.call(posts.NewPost(post))
```

### 3. **Medium (Opcional)**
```python
# publicar_medium.py
import requests

def publicar_no_medium(conteudo, titulo):
    headers = {
        'Authorization': f'Bearer {MEDIUM_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'title': titulo,
        'contentFormat': 'markdown',
        'content': conteudo,
        'publishStatus': 'public'
    }
    
    response = requests.post(
        'https://api.medium.com/v1/posts',
        headers=headers,
        json=data
    )
```

### 4. **LinkedIn (Opcional)**
```python
# publicar_linkedin.py
import requests

def publicar_no_linkedin(conteudo, titulo):
    headers = {
        'Authorization': f'Bearer {LINKEDIN_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'author': f'urn:li:person:{LINKEDIN_PERSON_ID}',
        'lifecycleState': 'PUBLISHED',
        'specificContent': {
            'com.linkedin.ugc.ShareContent': {
                'shareCommentary': {
                    'text': conteudo
                },
                'shareMediaCategory': 'NONE'
            }
        },
        'visibility': {
            'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
        }
    }
    
    response = requests.post(
        'https://api.linkedin.com/v2/ugcPosts',
        headers=headers,
        json=data
    )
```

## 🤖 Automações Avançadas

### 1. **Pipeline Automático**
```python
# pipeline_automatico.py
import schedule
import time
from datetime import datetime

def executar_pipeline():
    """Executa pipeline completo de publicação"""
    print(f"🚀 Iniciando pipeline: {datetime.now()}")
    
    # 1. Validar conteúdo pronto
    conteudo_pronto = validar_conteudo_pronto()
    
    # 2. Publicar em plataformas
    for conteudo in conteudo_pronto:
        publicar_notion(conteudo)
        publicar_wordpress(conteudo)
        publicar_medium(conteudo)
    
    # 3. Enviar notificações
    enviar_notificacoes()
    
    print("✅ Pipeline concluído")

# Agendar execução
schedule.every().day.at("09:00").do(executar_pipeline)
schedule.every().day.at("15:00").do(executar_pipeline)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 2. **Monitoramento de Conteúdo**
```python
# monitor_conteudo.py
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConteudoHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.md'):
            print(f"📝 Conteúdo modificado: {event.src_path}")
            validar_conteudo(event.src_path)
            notificar_mudanca(event.src_path)

def iniciar_monitoramento():
    event_handler = ConteudoHandler()
    observer = Observer()
    observer.schedule(event_handler, '2_conteudo/', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

### 3. **Geração de Relatórios**
```python
# gerar_relatorios.py
import json
from datetime import datetime, timedelta

def gerar_relatorio_semanal():
    """Gera relatório semanal de produção"""
    relatorio = {
        'periodo': 'semanal',
        'data': datetime.now().isoformat(),
        'metricas': {
            'conteudo_produzido': contar_conteudo_produzido(),
            'conteudo_publicado': contar_conteudo_publicado(),
            'tempo_medio_producao': calcular_tempo_medio(),
            'taxa_aprovacao': calcular_taxa_aprovacao()
        },
        'conteudo': {
            'novos_artigos': listar_novos_artigos(),
            'checklists_criados': listar_checklists(),
            'licoes_publicadas': listar_licoes()
        }
    }
    
    with open(f'relatorios/relatorio_{datetime.now().strftime("%Y%m%d")}.json', 'w') as f:
        json.dump(relatorio, f, indent=2)
    
    return relatorio
```

## 📊 Dashboard de Métricas

### 1. **Criar Dashboard Simples**
```html
<!-- dashboard.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - Modelo Projeto Conteúdo</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>📊 Dashboard de Produção</h1>
    
    <div class="metricas">
        <div class="metrica">
            <h3>Conteúdo Produzido</h3>
            <span id="total-conteudo">0</span>
        </div>
        <div class="metrica">
            <h3>Taxa de Aprovação</h3>
            <span id="taxa-aprovacao">0%</span>
        </div>
        <div class="metrica">
            <h3>Tempo Médio</h3>
            <span id="tempo-medio">0h</span>
        </div>
    </div>
    
    <canvas id="grafico-producao"></canvas>
    
    <script>
        // Carregar dados e atualizar dashboard
        fetch('/api/metricas')
            .then(response => response.json())
            .then(data => atualizarDashboard(data));
    </script>
</body>
</html>
```

### 2. **API de Métricas**
```python
# api_metricas.py
from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/api/metricas')
def obter_metricas():
    with open('relatorios/ultimo_relatorio.json', 'r') as f:
        return jsonify(json.load(f))

@app.route('/api/conteudo')
def obter_conteudo():
    return jsonify(listar_conteudo_disponivel())

if __name__ == '__main__':
    app.run(debug=True)
```

## 🔔 Notificações

### 1. **Discord Webhook**
```python
# notificacoes_discord.py
import requests
import json

def enviar_notificacao_discord(mensagem, tipo="info"):
    webhook_url = "SEU_WEBHOOK_DISCORD"
    
    cores = {
        "info": 0x3498db,
        "sucesso": 0x2ecc71,
        "erro": 0xe74c3c,
        "aviso": 0xf39c12
    }
    
    data = {
        "embeds": [{
            "title": f"📝 {tipo.upper()}",
            "description": mensagem,
            "color": cores.get(tipo, 0x3498db),
            "timestamp": datetime.now().isoformat()
        }]
    }
    
    requests.post(webhook_url, json=data)
```

### 2. **Slack Integration**
```python
# notificacoes_slack.py
import requests

def enviar_notificacao_slack(mensagem, canal="#conteudo"):
    webhook_url = "SEU_WEBHOOK_SLACK"
    
    data = {
        "channel": canal,
        "text": mensagem,
        "username": "Bot Conteúdo",
        "icon_emoji": ":robot_face:"
    }
    
    requests.post(webhook_url, json=data)
```

## 🚀 Próximos Passos

### 1. **Configurar Integrações Básicas**
- [ ] **Notion**: Configurar token e testar
- [ ] **WordPress**: Configurar se necessário
- [ ] **Notificações**: Configurar Discord/Slack

### 2. **Implementar Automações**
- [ ] **Pipeline automático**: Agendar execução
- [ ] **Monitoramento**: Configurar watch de arquivos
- [ ] **Relatórios**: Implementar geração automática

### 3. **Criar Dashboard**
- [ ] **Métricas básicas**: Contadores simples
- [ ] **Gráficos**: Visualização de dados
- [ ] **API**: Endpoints para dados

### 4. **Testar e Iterar**
- [ ] **Teste de integração**: Validar todas as conexões
- [ ] **Monitoramento**: Acompanhar performance
- [ ] **Ajustes**: Melhorar baseado no uso

---

**Dica**: Comece com integrações simples e expanda gradualmente!
