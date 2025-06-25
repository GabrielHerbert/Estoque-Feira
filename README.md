# Sistema de Controle de Estoque com Bot Telegram

Sistema completo para gerenciamento de estoque de duas filiais (Lopes e Herbert) através de um bot do Telegram com funcionalidades avançadas de relatórios e logs.

## 🚀 Funcionalidades

### ✅ Gestão de Estoque
- **Visualização de estoque** por filial (Lopes/Herbert) ou combinado
- **Adição e retirada** de produtos com validação de disponibilidade
- **Modo contínuo** para operações em lote
- **Catálogo de produtos** com busca inteligente

### ✅ Sistema de Relatórios Avançado
- **Relatórios por filial** (Lopes ou Herbert)
- **Relatório conjunto** com detalhamento por filial
- **Exportação em arquivo .txt** para fácil compartilhamento
- **Preview no chat** do Telegram
- **Formatação otimizada** para leitura

### ✅ Sistema de Logs Completo
- **Registro automático** de todas as movimentações
- **Histórico detalhado** com data/hora e contexto completo
- **Filtros por filial** e período
- **Visualização formatada** no Telegram

### ✅ Gestão de Catálogo
- **Adicionar novos produtos** ao catálogo
- **Remover produtos** por ID com listagem completa
- **Listagem com quantidades** atuais por filial

### ✅ Processamento Inteligente de Texto
- **Reconhecimento automático** de produtos e quantidades
- **Suporte a variações** de nomes de produtos
- **Conversão automática** de unidades (kg, g)
- **Processamento em lote** de múltiplos produtos

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Token do bot Telegram (obtido via @BotFather)

## 🛠️ Instalação e Configuração

### 1. Clone ou baixe o projeto
```bash
git clone <seu-repositorio>
cd sistema-estoque-telegram
```

### 2. Execute o script de setup
```bash
python setup.py
```

O script irá:
- Instalar dependências automaticamente
- Criar o banco de dados com todas as tabelas
- Configurar o sistema
- Validar a instalação

### 3. Configure o token do bot
Edite o arquivo `telegram_bot.py` e substitua o token:
```python
TOKEN = "SEU_TOKEN_AQUI"
```

### 4. Inicie o bot
```bash
python telegram_bot.py
```

## 📱 Como Usar

### Comandos Principais
- `/start` - Inicia o bot e mostra o menu principal
- `/estoque` - Mostra estoque completo de todas as filiais
- `/relatorio` - Gera relatórios por filial ou conjunto
- `/cancel` - Cancela operação atual
- `/stop` - Para o bot

### Menu Principal
- **Estoque Lopes/Herbert** - Gerenciar estoque por filial
- **Estoque Conjunto** - Visualizar estoque combinado
- **Ver Logs** - Histórico de operações
- **📊 Relatório** - Gerar relatórios (Lopes/Herbert/Conjunto)
- **Adicionar Novo Produto** - Cadastrar produtos no catálogo
- **🗑️ Remover Produto** - Remover produtos por ID
- **Encerrar** - Finalizar sessão

### Operações de Estoque
1. Selecione a filial (Lopes ou Herbert)
2. Escolha "Adicionar" ou "Retirar"
3. Entre no modo contínuo
4. Envie mensagens com produtos (ex: "2.5kg tilápia")
5. Use os botões para parar ou ver estoque atual

### Geração de Relatórios
1. Clique em "📊 Relatório" ou use `/relatorio`
2. Selecione o tipo:
   - **Lopes**: Apenas produtos da filial Lopes
   - **Herbert**: Apenas produtos da filial Herbert
   - **Conjunto**: Produtos de ambas com detalhamento
3. Receba o arquivo .txt + preview no chat

### Remoção de Produtos
1. Clique em "🗑️ Remover Produto"
2. Veja a lista com IDs e quantidades
3. Digite o ID do produto a remover
4. Confirme a operação

## 📊 Exemplos de Uso

### Adicionando Produtos
```
2.5kg tilápia
3 camarão limpo g
1.2kg pescada amarela
500g salmão
```

### Relatório Conjunto
```
ESTOQUE CONJUNTO (19/12/2024)

5.5 tilápia (Lopes: 2.5, Herbert: 3.0)
3 camarão limpo g (apenas Herbert)
1.2 pescada amarela (apenas Lopes)
2 salmão (Lopes: 1.2, Herbert: 0.8)
```

## 🗄️ Estrutura do Banco de Dados

### Tabelas Principais
- `produtos` - Catálogo de produtos
- `estoque_lopes` - Estoque da filial Lopes
- `estoque_herbert` - Estoque da filial Herbert
- `operacoes` - Log de operações completas

### Tabela `operacoes`
```sql
CREATE TABLE operacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filial TEXT NOT NULL,
    operacao TEXT NOT NULL,
    mensagem TEXT NOT NULL,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observacao TEXT
);
```

## 📁 Estrutura do Projeto

```
sistema-estoque-telegram/
├── telegram_bot.py          # Bot principal
├── estoque_core.py          # Funções principais do sistema
├── estoque_db.py            # Funções de banco de dados
├── text_processor.py        # Processamento de texto
├── db_setup.py             # Configuração do banco
├── backup_db.py            # Backup do banco
├── setup.py                # Script de instalação
├── requirements.txt        # Dependências
├── README.md              # Este arquivo
├── CHANGELOG.md           # Histórico de mudanças
└── estoque.db            # Banco de dados (criado automaticamente)
```

## 🔧 Manutenção

### Backup do Banco de Dados
```bash
python backup_db.py
```

### Verificar Status do Sistema
O sistema inclui validações automáticas e tratamento de erros. Em caso de problemas, verifique:
1. Se o banco de dados existe (`estoque.db`)
2. Se todas as tabelas foram criadas
3. Se o token do bot está correto
4. Se as dependências estão instaladas

## 🆕 Novidades da Versão 2.1.0

### Relatório Conjunto
- Combina estoque de ambas as filiais
- Mostra distribuição por filial quando relevante
- Identifica produtos exclusivos de cada filial

### Remoção de Produtos
- Interface para remover produtos do catálogo
- Listagem com IDs e quantidades atuais
- Remoção segura de todos os estoques

### Melhorias Técnicas
- Sistema de logs aprimorado
- Criação automática de tabelas
- Validação de integridade
- Tratamento robusto de erros

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique se seguiu todos os passos de instalação
2. Execute `python setup.py` novamente se houver erros
3. Verifique o arquivo `CHANGELOG.md` para mudanças recentes

## 📄 Licença

Este projeto é de uso interno. Todos os direitos reservados.

---

**Sistema desenvolvido para controle de estoque de pescados - Versão 2.1.0**rodutos
- **Fuzzy matching** para nomes similares
- **Múltiplos formatos** de entrada (kg, unidades, etc.)

### ✅ Armazenamento Preciso
- **Dados armazenados como inteiros** (gramas) para evitar erros de ponto flutuante
- **Conversão automática** entre gramas (armazenamento) e kg (exibição)
- **Formatação com 3 casas decimais** para exibição precisa
- **Consistência garantida** mesmo após múltiplas operações

## 📁 Estrutura do Projeto

```
├── estoque.db                # Banco de dados SQLite
├── db_setup.py               # Configuração inicial do banco
├── estoque_core.py           # Módulo principal de gestão de estoque
├── estoque_db.py             # Funções de banco de dados
├── text_processor.py         # Processador inteligente de texto
├── telegram_bot.py           # Bot do Telegram
├── verificar_sistema.py      # Verificação do sistema
├── requirements.txt          # Dependências Python
└── README.md                 # Este arquivo
```

## 🛠️ Instalação e Configuração

### 1. Pré-requisitos
```bash
pip install python-telegram-bot rapidfuzz
```

### 2. Configuração do Banco de Dados
```bash
# Criar o banco de dados inicial
python db_setup.py
```

### 3. Configuração do Bot Telegram
1. Crie um bot no Telegram através do @BotFather
2. Obtenha o token do bot
3. Edite o arquivo `telegram_bot.py` e substitua o TOKEN:
```python
TOKEN = "SEU_TOKEN_AQUI"
```

### 4. Verificação do Sistema
```bash
# Verificar se tudo está configurado corretamente
python verificar_sistema.py
```

### 5. Iniciar o Bot
```bash
python telegram_bot.py
```

## 📱 Como Usar o Bot

### Comandos Principais
- `/start` - Inicia o bot e mostra o menu principal
- `/estoque` - Mostra o estoque completo
- `/cancel` - Cancela a operação atual
- `/stop` - Para o bot

### Menu Principal
1. **Estoque Lopes** - Gerenciar estoque da filial Lopes
2. **Estoque Herbert** - Gerenciar estoque da filial Herbert  
3. **Estoque Conjunto** - Visualizar estoque combinado
4. **Ver Logs** - Histórico de movimentações
5. **Adicionar Novo Produto** - Cadastrar produto no catálogo

### Operações por Filial
- **Adicionar Produtos** - Modo contínuo para entrada de mercadorias
- **Retirar Produtos** - Modo contínuo para saída de mercadorias
- **Ver Logs desta Filial** - Histórico específico da filial

### Formato de Entrada de Produtos
```
2.5kg tilápia
3 camarão limpo g
1.2kg pescada amarela
4 camarão eviscerado xg
21.5kg c promoção
```

## 🗄️ Estrutura do Banco de Dados

### Tabela: produtos
- `id` - ID único do produto
- `nome` - Nome do produto

### Tabela: estoque_lopes / estoque_herbert
- `id` - ID único do registro
- `produto_id` - Referência ao produto
- `quantidade` - Quantidade em estoque (em gramas, exibido como kg)

### Tabela: logs_movimentacao
- `id` - ID único do log
- `produto_id` - Referência ao produto
- `filial` - Nome da filial (lopes/herbert)
- `operacao` - Tipo de operação (adicionar/retirar)
- `quantidade` - Quantidade movimentada (em gramas)
- `quantidade_anterior` - Quantidade antes da operação (em gramas)
- `quantidade_nova` - Quantidade após a operação (em gramas)
- `data_hora` - Timestamp da operação
- `observacao` - Observações adicionais

## 🔧 Módulos Principais

### estoque_core.py
Funções principais para gestão do estoque:
- `add_produto_catalogo()` - Adiciona produto ao catálogo
- `add_to_stock()` - Adiciona quantidade ao estoque
- `remove_from_stock()` - Remove quantidade do estoque
- `get_stock()` - Obtém estoque por filial
- `get_stock_combined()` - Obtém estoque combinado
- `get_logs_movimentacao()` - Obtém logs de movimentação
- `format_stock_message()` - Formata mensagem de estoque
- `format_logs_message()` - Formata mensagem de logs

### text_processor.py
Processamento inteligente de texto:
- `TextProcessor` - Classe principal para processamento
- `process_text()` - Função de conveniência para uso direto
- Suporte a variações de nomes de produtos
- Normalização de quantidades e unidades
- Fuzzy matching para correspondência aproximada
- Conversão automática de kg para gramas

### telegram_bot.py
Bot do Telegram com interface completa:
- Estados de conversação para navegação
- Menus interativos com botões
- Modo contínuo para operações em lote
- Tratamento de erros e validações
- Formatação rica de mensagens
- Exibição de quantidades em kg com 3 casas decimais

## 🔍 Solução de Problemas

### Erro: Tabela de logs não encontrada
A tabela de logs é criada automaticamente pelo db_setup.py. Se estiver faltando, execute:
```bash
python db_setup.py
```

### Erro: Banco de dados não encontrado
```bash
python db_setup.py
```

### Erro: Módulo não encontrado
```bash
pip install python-telegram-bot rapidfuzz
```

### Bot não responde
1. Verifique se o TOKEN está correto
2. Verifique a conexão com a internet
3. Verifique se o bot está rodando

## 📊 Exemplo de Uso

1. **Iniciar o bot**: `/start`
2. **Selecionar filial**: "Estoque Lopes"
3. **Adicionar produtos**: "Adicionar Produtos"
4. **Enviar lista**:
   ```
   2.5kg tilápia
   3 camarão limpo g
   1.2kg pescada amarela
   ```
5. **Ver resultado**: Confirmação com quantidades atualizadas
6. **Verificar logs**: "Ver Logs desta Filial"

## 🎯 Próximas Melhorias

- [ ] Relatórios em PDF
- [ ] Backup automático
- [ ] Alertas de estoque baixo
- [ ] Integração com código de barras
- [ ] Dashboard web
- [ ] Múltiplos usuários com permissões

## 📞 Suporte

Para dúvidas ou problemas:
1. Execute `python verificar_sistema.py` para diagnóstico
2. Verifique os logs do bot no terminal
3. Consulte este README para instruções detalhadas

---

**Sistema desenvolvido para gestão eficiente de estoque com rastreamento completo de movimentações e precisão numérica.**