# Instruções para Aplicar a Migração dos Campos de Quantidade

## Execução da Migração

Para aplicar as alterações nos campos `qtd_dias` e `qtd_pessoas` nas tabelas de despesas, execute os seguintes comandos:

### 1. Primeiro, atualize o arquivo de migração
Edite o arquivo `migrations/versions/adicionar_qtd_dias_pessoas_despesas.py` e substitua:
- `down_revision = None` pela última migração existente no seu banco

### 2. Execute a migração
```bash
# No terminal, navegue até o diretório do projeto
cd /c/Users/comer/Desktop/Python - Projects/socrates_online

# Execute a migração
flask db upgrade
```

### 3. Verifique se a migração foi aplicada
Verifique se os campos `qtd_dias` e `qtd_pessoas` foram adicionados nas tabelas:
- `despesas_evento`
- `despesas_empresa`

## Funcionalidades Implementadas

### 1. Campos Adicionados
- `qtd_dias`: Quantidade de dias (Integer, opcional)
- `qtd_pessoas`: Quantidade de pessoas (Integer, opcional)

### 2. Funcionalidade JavaScript
- **Despesas de Evento**: Campos aparecem quando o checkbox "Despesa de Alimentação" está marcado
- **Despesas de Empresa**: Campos aparecem automaticamente quando uma despesa com flag_alimentacao=True é selecionada

### 3. Validação
- Campos se tornam obrigatórios quando visíveis
- Valores devem ser números inteiros positivos
- Campos são limpos automaticamente quando ocultados

### 4. API Adicionada
- `GET /api/despesa-detalhes/<int:despesa_id>`: Retorna detalhes da despesa incluindo flag_alimentacao

## Uso

1. **Cadastro de Despesas de Eventos**: Marque o checkbox "Despesa de Alimentação" e os campos de quantidade aparecerão
2. **Cadastro de Despesas da Empresa**: Selecione uma despesa que tenha flag_alimentacao=True e os campos aparecerão automaticamente
3. **Edição**: Os campos funcionam da mesma forma na edição, mantendo os valores salvos

## Observações

- Os campos são opcionais para despesas que não são de alimentação
- A funcionalidade é totalmente compatível com despesas existentes
- O sistema verifica automaticamente se uma despesa é de alimentação através da flag_alimentacao 