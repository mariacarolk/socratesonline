# Sistema de Filtros Avançados e Exportação

## Funcionalidades Implementadas

### 1. Filtros Avançados por Campo
- **Botão "Filtros Avançados"**: Permite mostrar/ocultar os campos de filtro
- **Filtros individuais**: Cada coluna da tabela agora possui seu próprio campo de filtro
- **Filtro em tempo real**: Os resultados são filtrados conforme você digita
- **Botão "Limpar Filtros"**: Remove todos os filtros aplicados
- **Contador de registros**: Mostra quantos registros estão visíveis

### 2. Sistema de Exportação
- **Botão "Exportar"**: Abre modal com opções de exportação
- **Exportação para Excel (.xlsx)**: Arquivo formatado com cabeçalhos destacados
- **Exportação para PDF**: Documento com tabela organizada e título
- **Dados filtrados**: Exporta apenas os dados visíveis após aplicação dos filtros
- **Nome automático**: Arquivos nomeados com data atual

## Páginas Atualizadas

### Páginas Principais de Cadastros:
1. **Colaboradores** - Filtros: Nome, Categorias, Usuário
2. **Fornecedores** - Filtros: Nome, Telefone, Cidade, Estado, Categoria
3. **Veículos** - Filtros: Nome, Marca/Modelo, Ano, Placa, Categoria
4. **Despesas** - Filtros: Nome, Categoria, Tipo, Valor Médio
5. **Receitas** - Filtros: Nome, Categoria
6. **Elenco** - Filtros: Nome, CPF, Telefone, Cidade/Estado
7. **Circos** - Filtros: Nome, Responsável, Telefone Contato, Observações

### Páginas de Categorias:
1. **Categorias de Colaborador** - Filtros: Nome
2. **Categorias de Fornecedor** - Filtros: Nome
3. **Categorias de Receita** - Filtros: Nome
4. **Categorias de Despesa** - Filtros: Nome
5. **Categorias de Veículo** - Filtros: Nome

## Como Usar

### Filtros Avançados:
1. Acesse qualquer página de cadastro com listagem
2. Clique no botão "**Filtros Avançados**" para exibir os campos de filtro
3. Digite no campo correspondente à coluna que deseja filtrar
4. Os resultados são filtrados automaticamente conforme você digita
5. Use o botão "**Limpar Filtros**" para remover todos os filtros

### Exportação:
1. Aplique os filtros desejados (opcional)
2. Clique no botão "**Exportar**"
3. Escolha o formato desejado:
   - **Excel**: Para planilhas e análises
   - **PDF**: Para relatórios e impressão
4. O arquivo será baixado automaticamente

## Arquivos Modificados

### Dependências:
- `requirements.txt` - Adicionadas bibliotecas `openpyxl` e `reportlab`

### Backend:
- `app.py` - Adicionadas funções de exportação e rota `/exportar/<table>/<format>`

### Frontend:
- `static/js/advanced-filters.js` - Nova classe JavaScript para filtros avançados
- Todos os templates de cadastro - Atualizados com chamadas para o sistema de filtros

### Templates Atualizados:
- `templates/colaboradores.html`
- `templates/fornecedores.html`
- `templates/veiculos.html`
- `templates/despesas.html`
- `templates/receitas.html`
- `templates/elenco.html`
- `templates/cadastrar_circo.html`
- `templates/categorias_colaborador.html`
- `templates/categorias_fornecedor.html`
- `templates/categorias_receita.html`
- `templates/categorias_despesa.html`
- `templates/categorias_veiculo.html`

## Características Técnicas

### Filtros:
- **Busca case-insensitive**: Não diferencia maiúsculas/minúsculas
- **Busca por substring**: Encontra texto em qualquer parte do campo
- **Múltiplos filtros**: Todos os filtros são aplicados simultaneamente (AND lógico)
- **Performance otimizada**: Filtros aplicados no frontend para resposta rápida

### Exportação:
- **Server-side**: Processamento no backend para arquivos consistentes
- **Formatação automática**: Cabeçalhos destacados e colunas ajustadas
- **Segurança**: Validação de usuário logado antes da exportação
- **Tratamento de erros**: Mensagens de erro claras em caso de falha

## Melhorias Implementadas

1. **Design Responsivo**: Funciona em desktop e mobile
2. **Integração com Design Existente**: Mantém padrão visual do sistema
3. **Reutilização de Código**: Sistema único para todas as páginas
4. **Fácil Manutenção**: Código organizado e documentado
5. **Performance**: Filtros rápidos sem requisições ao servidor
6. **Usabilidade**: Interface intuitiva e familiar

## Testes Recomendados

1. **Teste os filtros** em cada página de cadastro
2. **Combine múltiplos filtros** para verificar funcionamento
3. **Teste exportação** com e sem filtros aplicados
4. **Verifique responsividade** em diferentes tamanhos de tela
5. **Teste com dados reais** para validar performance

---

**Desenvolvido respeitando as regras do projeto:**
- ✅ Design consistente com padrão existente
- ✅ Responsivo para desktop e mobile
- ✅ Código reutilizável (DRY)
- ✅ Funcionalidades não revertidas 