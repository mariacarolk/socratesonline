# Sistema de Gestão de Eventos - Sócrates Online

Sistema web para gestão de eventos de circo, desenvolvido em Flask.

## Funcionalidades Principais

- Gestão de eventos, colaboradores, elenco e fornecedores
- Controle financeiro (receitas e despesas)
- Relatórios de faturamento e fechamento
- Sistema de usuários com diferentes níveis de acesso

## Cálculo de Lucro Unificado

O sistema utiliza uma função unificada (`calcular_lucro_evento`) para garantir consistência nos cálculos de lucro entre diferentes relatórios:

### Fórmula de Cálculo:
1. **Total Receitas** - **Despesas de Cabeça** = **Total Líquido**
2. **Total Líquido** ÷ 2 = **50% Show**
3. **Reembolso Mídias** = despesas de cabeça excluindo categoria "PAGAS PELO CIRCO"
4. **Repasse Total** = **50% Show** + **Reembolso Mídias**
5. **Total Despesas Sócrates** = todas as despesas excluindo categoria "PAGAS PELO CIRCO"
6. **Resultado do Show (Lucro Real)** = **Repasse Total** - **Total Despesas Sócrates**

### Funções Disponíveis:
- `calcular_lucro_evento(id_evento)`: Retorna todos os valores detalhados do cálculo
- `calcular_lucro_simples(id_evento)`: Retorna apenas o lucro final

### Relatórios que Utilizam:
- **Top 10 Eventos Mais Lucrativos**: Usa o cálculo unificado para ranking
- **Relatório de Fechamento Individual**: Usa o cálculo unificado para consistência

## Tecnologias Utilizadas

- **Backend**: Python Flask
- **Banco de Dados**: SQLite com SQLAlchemy
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Gráficos**: Chart.js

## Como Executar

```bash
python app.py
```

O sistema estará disponível em `http://127.0.0.1:5000`

## Funcionalidade Cidades/Estados Dinâmicas

### O que foi implementado:

1. **API de Cidades por Estado** (`/api/cidades/<estado>`)
   - Endpoint que retorna as cidades de um estado específico
   - Utiliza dados completos dos 26 estados + DF
   - Retorna resposta JSON com lista de cidades

2. **JavaScript Dinâmico** (`static/js/cidades.js`)
   - Carregamento automático de cidades baseado no estado selecionado
   - Suporte a múltiplos formulários na mesma página
   - Autocompletar com datalist HTML5
   - Validação opcional de cidades

3. **Formulários Atualizados:**
   - **Fornecedores**: Estado primeiro, depois cidade com autocompletar
   - **Elenco**: Estado primeiro, depois cidade com autocompletar  
   - **Eventos**: Estado primeiro, depois cidade com autocompletar
   - **Forms.py**: ElencoForm atualizado para usar SelectField no estado

### Como usar:

1. **Selecione o Estado**: Primeiro campo obrigatório
2. **Campo Cidade**: Fica habilitado após selecionar estado
3. **Autocompletar**: Digite para buscar cidades ou selecione da lista
4. **Validação**: Sistema valida se cidade existe no estado

### Formulários que usam a funcionalidade:

- ✅ Cadastro/Edição de Fornecedores
- ✅ Cadastro/Edição de Elenco  
- ✅ Cadastro/Edição de Eventos
- 🔄 Outros formulários podem ser facilmente adaptados

### Estrutura técnica:

```
/api/cidades/SP → Retorna cidades de São Paulo
/api/cidades/RJ → Retorna cidades do Rio de Janeiro
```

### Benefícios:

- ✅ Padronização de dados de localização
- ✅ Redução de erros de digitação
- ✅ Interface mais intuitiva
- ✅ Busca/filtros mais eficientes
- ✅ Priorização de fornecedores locais

### Próximos passos sugeridos:

1. Aplicar em demais formulários que usem cidade/estado
2. Implementar cache da API para melhor performance
3. Adicionar coordenadas geográficas para funcionalidades avançadas 