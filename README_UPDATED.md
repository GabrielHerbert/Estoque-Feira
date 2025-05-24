# Sistema de Controle de Estoque com Bot Telegram

Este sistema permite gerenciar o estoque de produtos em duas filiais (Lopes e Herbert) atravu00e9s de um bot do Telegram com funcionalidades completas de logs e rastreamento de movimentau00e7u00f5es.

## ud83dude80 Funcionalidades

### u2705 Gestu00e3o de Estoque
- **Visualizau00e7u00e3o de estoque** por filial (Lopes/Herbert) ou combinado
- **Adiu00e7u00e3o de produtos** ao estoque com quantidades
- **Retirada de produtos** do estoque com validau00e7u00e3o de disponibilidade
- **Modo contu00ednuo** para operau00e7u00f5es em lote
- **Catu00e1logo de produtos** com busca inteligente

### u2705 Sistema de Logs Completo
- **Registro automu00e1tico** de todas as movimentau00e7u00f5es
- **Histu00f3rico detalhado** com data/hora, quantidades anteriores e novas
- **Filtros por filial** e peru00edodo
- **Observau00e7u00f5es** para contexto adicional (ex: promou00e7u00f5es)
- **Visualizau00e7u00e3o formatada** no Telegram

### u2705 Processamento Inteligente de Texto
- **Reconhecimento automu00e1tico** de produtos e quantidades
- **Suporte a variau00e7u00f5es** de nomes de produtos
- **Fuzzy matching** para nomes similares
- **Mu00faltiplos formatos** de entrada (kg, unidades, etc.)

### u2705 Armazenamento Preciso
- **Dados armazenados como inteiros** (gramas) para evitar erros de ponto flutuante
- **Conversu00e3o automu00e1tica** entre gramas (armazenamento) e kg (exibiu00e7u00e3o)
- **Formatau00e7u00e3o com 3 casas decimais** para exibiu00e7u00e3o precisa
- **Consistu00eancia garantida** mesmo apu00f3s mu00faltiplas operau00e7u00f5es

## ud83dudcbb Implantau00e7u00e3o no Servidor

Para implantar o sistema em um servidor, siga as instruu00e7u00f5es detalhadas no arquivo [INSTRUCOES_IMPLANTACAO.md](INSTRUCOES_IMPLANTACAO.md).

### Resumo do Processo de Implantau00e7u00e3o

1. **Preparar o Repositu00f3rio Git**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Backup do Banco de Dados Atual (se existir)**
   ```bash
   python3 backup_db.py
   ```

3. **Executar o Script de Implantau00e7u00e3o**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

4. **Iniciar o Bot**
   ```bash
   # Para manter o bot rodando em segundo plano
   nohup python3 telegram_bot.py > bot.log 2>&1 &
   ```

### Scripts de Manutenu00e7u00e3o

- `backup_db.py` - Cria um backup do banco de dados atual
- `restore_db.py` - Restaura um backup do banco de dados
- `migrate_db.py` - Migra o banco de dados, adicionando a tabela de logs se necessu00e1rio
- `verificar_sistema.py` - Verifica se o sistema estu00e1 configurado corretamente

## ud83dudcda Estrutura do Projeto

```
u251cu2500u2500 estoque.db                # Banco de dados SQLite
u251cu2500u2500 db_setup.py               # Configurau00e7u00e3o inicial do banco
u251cu2500u2500 estoque_core.py           # Mu00f3dulo principal de gestu00e3o de estoque
u251cu2500u2500 text_processor.py         # Processador inteligente de texto
u251cu2500u2500 telegram_bot.py           # Bot do Telegram
u251cu2500u2500 verificar_sistema.py      # Verificau00e7u00e3o do sistema
u251cu2500u2500 backup_db.py              # Backup do banco de dados
u251cu2500u2500 restore_db.py             # Restaurau00e7u00e3o de backups
u251cu2500u2500 migrate_db.py             # Migrau00e7u00e3o do banco de dados
u251cu2500u2500 deploy.sh                 # Script de implantau00e7u00e3o
u251cu2500u2500 requirements.txt          # Dependu00eancias Python
u251cu2500u2500 INSTRUCOES_IMPLANTACAO.md # Instruu00e7u00f5es detalhadas
u2514u2500u2500 README.md                 # Este arquivo
```

## ud83dudd27 Instalau00e7u00e3o e Configurau00e7u00e3o

### 1. Pru00e9-requisitos
```bash
pip install python-telegram-bot rapidfuzz
```

### 2. Configurau00e7u00e3o do Banco de Dados
```bash
# Criar o banco de dados inicial
python db_setup.py
```

### 3. Configurau00e7u00e3o do Bot Telegram
1. Crie um bot no Telegram atravu00e9s do @BotFather
2. Obtenha o token do bot
3. Edite o arquivo `telegram_bot.py` e substitua o TOKEN:
```python
TOKEN = "SEU_TOKEN_AQUI"
```

### 4. Verificau00e7u00e3o do Sistema
```bash
# Verificar se tudo estu00e1 configurado corretamente
python verificar_sistema.py
```

### 5. Iniciar o Bot
```bash
python telegram_bot.py
```

## ud83dudcf1 Como Usar o Bot

### Comandos Principais
- `/start` - Inicia o bot e mostra o menu principal
- `/estoque` - Mostra o estoque completo
- `/cancel` - Cancela a operau00e7u00e3o atual
- `/stop` - Encerra a conversa (sem parar o bot)

### Menu Principal
1. **Estoque Lopes** - Gerenciar estoque da filial Lopes
2. **Estoque Herbert** - Gerenciar estoque da filial Herbert  
3. **Estoque Conjunto** - Visualizar estoque combinado
4. **Ver Logs** - Histu00f3rico de movimentau00e7u00f5es
5. **Adicionar Novo Produto** - Cadastrar produto no catu00e1logo

### Operau00e7u00f5es por Filial
- **Adicionar Produtos** - Modo contu00ednuo para entrada de mercadorias
- **Retirar Produtos** - Modo contu00ednuo para sau00edda de mercadorias
- **Ver Logs desta Filial** - Histu00f3rico especu00edfico da filial

### Formato de Entrada de Produtos
```
2.5kg tilu00e1pia
3 camaru00e3o limpo g
1.2kg pescada amarela
4 camaru00e3o eviscerado xg
21.5kg c promou00e7u00e3o
```

## ud83duddc2ufe0f Estrutura do Banco de Dados

### Tabela: produtos
- `id` - ID u00fanico do produto
- `nome` - Nome do produto

### Tabela: estoque_lopes / estoque_herbert
- `id` - ID u00fanico do registro
- `produto_id` - Referu00eancia ao produto
- `quantidade` - Quantidade em estoque (em gramas, exibido como kg)

### Tabela: logs_movimentacao
- `id` - ID u00fanico do log
- `produto_id` - Referu00eancia ao produto
- `filial` - Nome da filial (lopes/herbert)
- `operacao` - Tipo de operau00e7u00e3o (adicionar/retirar)
- `quantidade` - Quantidade movimentada (em gramas)
- `quantidade_anterior` - Quantidade antes da operau00e7u00e3o (em gramas)
- `quantidade_nova` - Quantidade apu00f3s a operau00e7u00e3o (em gramas)
- `data_hora` - Timestamp da operau00e7u00e3o
- `observacao` - Observau00e7u00f5es adicionais

## ud83dudd27 Mu00f3dulos Principais

### estoque_core.py
Funu00e7u00f5es principais para gestu00e3o do estoque:
- `add_produto_catalogo()` - Adiciona produto ao catu00e1logo
- `add_to_stock()` - Adiciona quantidade ao estoque
- `remove_from_stock()` - Remove quantidade do estoque
- `get_stock()` - Obtu00e9m estoque por filial
- `get_stock_combined()` - Obtu00e9m estoque combinado
- `get_logs_movimentacao()` - Obtu00e9m logs de movimentau00e7u00e3o
- `format_stock_message()` - Formata mensagem de estoque
- `format_logs_message()` - Formata mensagem de logs

### text_processor.py
Processamento inteligente de texto:
- `TextProcessor` - Classe principal para processamento
- `process_text()` - Funu00e7u00e3o de conveniu00eancia para uso direto
- Suporte a variau00e7u00f5es de nomes de produtos
- Normalizau00e7u00e3o de quantidades e unidades
- Fuzzy matching para correspondu00eancia aproximada
- Conversu00e3o automu00e1tica de kg para gramas

### telegram_bot.py
Bot do Telegram com interface completa:
- Estados de conversau00e7u00e3o para navegau00e7u00e3o
- Menus interativos com botu00f5es
- Modo contu00ednuo para operau00e7u00f5es em lote
- Tratamento de erros e validau00e7u00f5es
- Formatau00e7u00e3o rica de mensagens
- Exibiu00e7u00e3o de quantidades em kg com 3 casas decimais

## ud83dudd0d Soluu00e7u00e3o de Problemas

### Erro: Tabela de logs nu00e3o encontrada
A tabela de logs u00e9 criada automaticamente pelo db_setup.py. Se estiver faltando, execute:
```bash
python criar_tabela_logs.py
```

### Erro: Banco de dados nu00e3o encontrado
```bash
python db_setup.py
```

### Erro: Mu00f3dulo nu00e3o encontrado
```bash
pip install python-telegram-bot rapidfuzz
```

### Bot nu00e3o responde
1. Verifique se o TOKEN estu00e1 correto
2. Verifique a conexu00e3o com a internet
3. Verifique se o bot estu00e1 rodando

### Problemas com o banco de dados
Se o banco de dados estiver corrompido ou com problemas, restaure um backup:
```bash
python restore_db.py
```

## ud83dudcca Exemplo de Uso

1. **Iniciar o bot**: `/start`
2. **Selecionar filial**: "Estoque Lopes"
3. **Adicionar produtos**: "Adicionar Produtos"
4. **Enviar lista**:
   ```
   2.5kg tilu00e1pia
   3 camaru00e3o limpo g
   1.2kg pescada amarela
   ```
5. **Ver resultado**: Confirmau00e7u00e3o com quantidades atualizadas
6. **Verificar logs**: "Ver Logs desta Filial"

## ud83cudfa8 Pru00f3ximas Melhorias

- [ ] Relatu00f3rios em PDF
- [ ] Interface web para administrau00e7u00e3o
- [ ] Notificau00e7u00f5es automu00e1ticas de estoque baixo
- [ ] Exportau00e7u00e3o de dados para Excel