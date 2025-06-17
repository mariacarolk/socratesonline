# Sistema Sócrates Online

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