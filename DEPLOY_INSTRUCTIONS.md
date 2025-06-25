# 🚀 Instruções de Deploy - Sistema de Estoque Telegram

## 📋 Pré-requisitos no Servidor

### Sistema Operacional
- Ubuntu 18.04+ / Debian 10+ / CentOS 7+
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- git (para versionamento)

### Instalação de Dependências do Sistema
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip git

# CentOS/RHEL
sudo yum install -y python3 python3-pip git
```

## 📦 Deploy do Sistema

### 1. Clonar/Copiar o Projeto
```bash
# Opção A: Via Git (recomendado)
git clone <seu-repositorio>
cd sistema-estoque-telegram

# Opção B: Upload manual
# Faça upload dos arquivos via FTP/SCP para o servidor
```

### 2. Executar Setup Automático
```bash
# Execute o script de setup que fará tudo automaticamente
python3 setup.py
```

O script de setup irá:
- ✅ Verificar versão do Python
- ✅ Instalar dependências automaticamente
- ✅ Criar banco de dados com todas as tabelas
- ✅ Inserir produtos de exemplo
- ✅ Testar todas as funcionalidades
- ✅ Validar a instalação

### 3. Configurar Token do Bot
```bash
# Edite o arquivo do bot
nano telegram_bot.py

# Localize e substitua:
TOKEN = "SEU_TOKEN_AQUI"
```

### 4. Testar o Sistema
```bash
# Teste rápido
python3 telegram_bot.py

# Se tudo estiver OK, pare com Ctrl+C
```

### 5. Executar em Produção
```bash
# Opção A: Execução simples (para testes)
python3 telegram_bot.py

# Opção B: Execução em background (produção)
nohup python3 telegram_bot.py > bot.log 2>&1 &

# Opção C: Com screen (recomendado)
screen -S estoque-bot
python3 telegram_bot.py
# Pressione Ctrl+A, depois D para desanexar
```

## 🔧 Gerenciamento do Bot

### Verificar Status
```bash
# Ver processos do bot
ps aux | grep telegram_bot

# Ver logs (se usando nohup)
tail -f bot.log

# Reconectar ao screen
screen -r estoque-bot
```

### Parar o Bot
```bash
# Se rodando em foreground: Ctrl+C

# Se rodando em background:
pkill -f telegram_bot.py

# Ou encontre o PID e mate o processo:
ps aux | grep telegram_bot
kill <PID>
```

### Reiniciar o Bot
```bash
# Pare o bot primeiro, depois:
python3 telegram_bot.py
# ou
nohup python3 telegram_bot.py > bot.log 2>&1 &
```

## 📊 Monitoramento

### Logs do Sistema
```bash
# Ver logs em tempo real
tail -f bot.log

# Ver últimas 50 linhas
tail -n 50 bot.log

# Buscar por erros
grep -i error bot.log
```

### Backup do Banco
```bash
# Backup manual
python3 backup_db.py

# Backup automático (adicionar ao crontab)
0 2 * * * cd /caminho/para/projeto && python3 backup_db.py
```

## 🛠️ Solução de Problemas

### Bot não inicia
```bash
# Verificar logs
cat bot.log

# Verificar dependências
python3 -c "import telegram; print('OK')"

# Verificar banco de dados
ls -la estoque.db
```

### Erro de permissões
```bash
# Dar permissões corretas
chmod 755 *.py
chmod 644 estoque.db
```

### Erro de token
```bash
# Verificar se o token está correto no arquivo
grep TOKEN telegram_bot.py

# Testar token manualmente
python3 -c "
import telegram
bot = telegram.Bot('SEU_TOKEN')
print(bot.get_me())
"
```

### Banco de dados corrompido
```bash
# Restaurar backup
python3 backup_db.py  # se houver backup
# ou recriar:
rm estoque.db
python3 setup.py
```

## 🔄 Atualizações

### Atualizar o Sistema
```bash
# Se usando Git
git pull

# Executar setup novamente (seguro)
python3 setup.py

# Reiniciar o bot
pkill -f telegram_bot.py
nohup python3 telegram_bot.py > bot.log 2>&1 &
```

## 📁 Estrutura de Arquivos Final

```
sistema-estoque-telegram/
├── telegram_bot.py          # Bot principal
├── estoque_core.py          # Funções do sistema
├── estoque_db.py            # Banco de dados
├── text_processor.py        # Processamento de texto
├── db_setup.py             # Setup do banco
├── backup_db.py            # Backup
├── setup.py                # Instalação automática
├── requirements.txt        # Dependências
├── README.md              # Documentação
├── CHANGELOG.md           # Histórico
├── .gitignore             # Git ignore
├── estoque.db            # Banco (criado automaticamente)
└── bot.log               # Logs (criado automaticamente)
```

## ✅ Checklist de Deploy

- [ ] Servidor com Python 3.8+
- [ ] Dependências do sistema instaladas
- [ ] Projeto copiado para o servidor
- [ ] `python3 setup.py` executado com sucesso
- [ ] Token do bot configurado
- [ ] Bot testado manualmente
- [ ] Bot executando em background
- [ ] Logs sendo gerados corretamente
- [ ] Backup configurado (opcional)

## 🎉 Sistema Pronto!

Após seguir todos os passos, seu sistema estará funcionando com:

- ✅ Bot Telegram operacional
- ✅ Banco de dados configurado
- ✅ Todas as funcionalidades ativas
- ✅ Sistema de logs funcionando
- ✅ Relatórios (individual e conjunto)
- ✅ Gestão completa de estoque
- ✅ Adição/remoção de produtos

**Para usar:** Inicie conversa com o bot no Telegram e use `/start`