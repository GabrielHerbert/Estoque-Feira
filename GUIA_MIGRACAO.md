# Guia de Migrau00e7u00e3o para o Servidor

Este guia fornece instruu00e7u00f5es passo a passo para migrar o sistema de estoque para um servidor, mantendo o banco de dados atual.

## Passo 1: Preparar o Ambiente no Servidor

```bash
# Instalar dependu00eancias necessárias
sudo apt update
sudo apt install -y git python3 python3-pip
```

## Passo 2: Fazer Backup do Banco de Dados Atual

```bash
# Se você já tem o sistema rodando no servidor
cd /caminho/para/sistema-atual
python3 backup_db.py

# OU copie manualmente o arquivo estoque.db para um local seguro
cp estoque.db ~/estoque_backup_$(date +%Y%m%d).db
```

## Passo 3: Configurar o Repositório Git

```bash
# Criar um novo repositório no GitHub (se ainda não tiver)
# Em seguida, no servidor:

# Se estiver começando um novo diretório
mkdir -p ~/estoque-bot
cd ~/estoque-bot
git init

# OU se estiver usando o diretório atual
cd /caminho/para/sistema-atual
git init

# Adicionar o arquivo .gitignore
echo "*.db" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "backups/" >> .gitignore

# Configurar o repositório remoto
git remote add origin https://github.com/seu-usuario/seu-repositorio.git

# Adicionar todos os arquivos exceto os ignorados
git add .

# Fazer o primeiro commit
git commit -m "Versão inicial do sistema de estoque"

# Enviar para o GitHub
git push -u origin master
```

## Passo 4: Atualizar o Sistema em Outro Computador

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

# Copie os novos scripts para o repositório
# (backup_db.py, restore_db.py, migrate_db.py, deploy.sh, etc.)

# Adicione os novos arquivos ao Git
git add .
git commit -m "Adicionados scripts de migração e implantação"
git push
```

## Passo 5: Atualizar o Sistema no Servidor

```bash
# No servidor, atualize o repositório
cd ~/estoque-bot
git pull

# Dê permissão de execução ao script de implantação
chmod +x deploy.sh
```

## Passo 6: Restaurar o Banco de Dados

```bash
# Crie o diretório de backups se não existir
mkdir -p backups

# Copie o backup do banco de dados para o diretório de backups
cp ~/estoque_backup_*.db backups/

# Restaure o banco de dados
python3 restore_db.py
```

## Passo 7: Migrar o Banco de Dados

```bash
# Execute o script de migração para adicionar a tabela de logs se necessário
python3 migrate_db.py
```

## Passo 8: Verificar o Sistema

```bash
# Verifique se tudo está configurado corretamente
python3 verificar_sistema.py
```

## Passo 9: Iniciar o Bot

```bash
# Para executar o bot em segundo plano
nohup python3 telegram_bot.py > bot.log 2>&1 &

# Para verificar se o bot está rodando
ps aux | grep telegram_bot.py

# Para verificar os logs
tail -f bot.log
```

## Solução de Problemas

### O bot não inicia

Verifique os logs para identificar o problema:

```bash
cat bot.log
```

### Erro ao conectar ao banco de dados

Verifique se o arquivo do banco de dados existe e tem as permissões corretas:

```bash
ls -la estoque.db
chmod 644 estoque.db
```

### Erro na tabela de logs

Se a tabela de logs não foi criada corretamente:

```bash
python3 criar_tabela_logs.py
```

### Conflitos no Git

Se houver conflitos ao atualizar o repositório:

```bash
# Fazer backup dos arquivos modificados localmente
mkdir -p backup_files
cp -r * backup_files/

# Forçar a atualização do repositório
git fetch --all
git reset --hard origin/master
```