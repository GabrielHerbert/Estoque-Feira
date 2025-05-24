# Sistema de Controle de Estoque com Bot Telegram

Este sistema permite gerenciar o estoque de produtos em duas filiais (Lopes e Herbert) através de um bot do Telegram com funcionalidades completas de logs e rastreamento de movimentações.

## 🚀 Funcionalidades

### ✅ Gestão de Estoque
- **Visualização de estoque** por filial (Lopes/Herbert) ou combinado
- **Adição de produtos** ao estoque com quantidades
- **Retirada de produtos** do estoque com validação de disponibilidade
- **Modo contínuo** para operações em lote
- **Catálogo de produtos** com busca inteligente

### ✅ Sistema de Logs Completo
- **Registro automático** de todas as movimentações
- **Histórico detalhado** com data/hora, quantidades anteriores e novas
- **Filtros por filial** e período
- **Observações** para contexto adicional (ex: promoções)
- **Visualização formatada** no Telegram

### ✅ Processamento Inteligente de Texto
- **Reconhecimento automático** de produtos e quantidades
- **Suporte a variações** de nomes de produtos
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