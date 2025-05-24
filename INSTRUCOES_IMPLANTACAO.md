# Instruu00e7u00f5es de Implantau00e7u00e3o

Este documento contu00e9m instruu00e7u00f5es detalhadas para implantar o sistema de estoque em um novo servidor ou atualizar uma instalau00e7u00e3o existente.

## Pru00e9-requisitos

- Git
- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)
- Acesso ao servidor via SSH ou terminal

## Implantau00e7u00e3o em um Novo Servidor

### 1. Clonar o Repositu00f3rio

```bash
# Navegue atu00e9 o diretu00f3rio onde deseja instalar o sistema
cd /caminho/para/diretorio

# Clone o repositu00f3rio
git clone https://github.com/seu-usuario/seu-repositorio.git

# Entre no diretu00f3rio do projeto
cd seu-repositorio
```

### 2. Configurar o Ambiente

```bash
# Instalar dependu00eancias
pip3 install -r requirements.txt

# Dar permissu00e3o de execuu00e7u00e3o ao script de implantau00e7u00e3o
chmod +x deploy.sh
```

### 3. Inicializar o Banco de Dados

Se vocu00ea estu00e1 comeu00e7ando do zero:

```bash
python3 db_setup.py
```

Se vocu00ea tem um backup do banco de dados:

```bash
# Copie o arquivo de backup para a pasta 'backups'
mkdir -p backups
cp /caminho/para/seu/backup.db backups/

# Restaure o backup
python3 restore_db.py
```

### 4. Migrar o Banco de Dados

```bash
python3 migrate_db.py
```

### 5. Verificar o Sistema

```bash
python3 verificar_sistema.py
```

### 6. Iniciar o Bot

```bash
python3 telegram_bot.py
```

Para manter o bot rodando mesmo apu00f3s fechar o terminal, vocu00ea pode usar o `nohup` ou o `screen`:

```bash
# Usando nohup
nohup python3 telegram_bot.py > bot.log 2>&1 &

# OU usando screen
screen -S bot
python3 telegram_bot.py
# Pressione Ctrl+A, D para desanexar a sessu00e3o
```

## Atualizau00e7u00e3o de uma Instalau00e7u00e3o Existente

### 1. Fazer Backup do Banco de Dados

```bash
python3 backup_db.py
```

### 2. Atualizar o Cu00f3digo

```bash
# Certifique-se de estar no diretu00f3rio do projeto
cd /caminho/para/seu-repositorio

# Obter as u00faltimas alterau00e7u00f5es
git pull
```

### 3. Executar o Script de Implantau00e7u00e3o

```bash
./deploy.sh
```

### 4. Reiniciar o Bot

Se vocu00ea estu00e1 usando `screen`:

```bash
# Listar sessu00f5es screen
screen -ls

# Reconectar u00e0 sessu00e3o do bot
screen -r bot

# Encerrar o bot (Ctrl+C) e reiniciu00e1-lo
python3 telegram_bot.py
```

Se vocu00ea estu00e1 usando `nohup`:

```bash
# Encontrar o processo do bot
ps aux | grep telegram_bot.py

# Encerrar o processo
kill <PID>

# Reiniciar o bot
nohup python3 telegram_bot.py > bot.log 2>&1 &
```

## Soluu00e7u00e3o de Problemas

### Erro ao Conectar ao Banco de Dados

Verifique se o arquivo `estoque.db` existe e tem permissu00f5es corretas:

```bash
ls -la estoque.db
chmod 644 estoque.db
```

### Bot Nu00e3o Responde

Verifique se o token do bot estu00e1 configurado corretamente em `telegram_bot.py`.

### Erro na Tabela de Logs

Se houver problemas com a tabela de logs, vocu00ea pode recriu00e1-la:

```bash
python3 criar_tabela_logs.py
```

### Restaurar Backup

Se precisar restaurar um backup anterior:

```bash
python3 restore_db.py
```

## Manutenu00e7u00e3o

### Backups Regulares

Configure um cron job para fazer backups regulares:

```bash
# Editar crontab
crontab -e

# Adicionar linha para backup diu00e1rio u00e0s 3 da manhu00e3
0 3 * * * cd /caminho/para/seu-repositorio && python3 backup_db.py
```

### Monitoramento

Verifique regularmente os logs do bot:

```bash
tail -f bot.log
```