# 📋 ANÁLISE DE REQUISITOS - SISTEMA SÓCRATES ONLINE

## 📊 Visão Geral do Sistema

**Nome:** Sócrates Online  
**Versão:** 1.0  
**Tipo:** Sistema Web de Gestão de Eventos para Circos  
**Linguagem:** Python (Flask)  
**Banco de Dados:** PostgreSQL com SQLAlchemy  
**Frontend:** Bootstrap 5, JavaScript ES6, Jinja2  

### 🎯 Objetivo
Sistema integrado para gestão completa de eventos circenses, incluindo controle financeiro, recursos humanos, logística e relatórios gerenciais.

---

## 🏗️ ARQUITETURA DO SISTEMA

### **Tecnologias Utilizadas**
- **Backend:** Flask (Python)
- **Frontend:** Bootstrap 5.3.0, Bootstrap Icons, Font Awesome
- **Banco de Dados:** PostgreSQL + SQLAlchemy ORM
- **Autenticação:** Flask sessions
- **Validação:** WTForms + HTML5 validation
- **Gráficos:** Chart.js
- **Estilos:** CSS3 customizado + Google Fonts (Poppins)

### **Padrão Arquitetural**
- **MVC (Model-View-Controller)**
- **Templates Jinja2** para renderização
- **ORM SQLAlchemy** para persistência
- **Componentes reutilizáveis** (JavaScript classes)

---

## 👥 REQUISITOS DE USUÁRIO

### **Perfis de Acesso**
1. **Administrativo:** Acesso completo a todas as funcionalidades
2. **Operacional:** Acesso limitado (a ser definido)

### **Autenticação**
- Login com email/senha
- Sessões seguras
- Logout automático
- Controle de acesso por categoria

---

## 🎪 MÓDULOS E FUNCIONALIDADES

## 1. 📊 **DASHBOARD**

### **RF001 - Dashboard Principal**
- **Descrição:** Painel central com indicadores e acesso rápido
- **Funcionalidades:**
  - Contadores de eventos, receitas, despesas, colaboradores
  - Gráfico de lucro por período (7 dias, mês, customizado)
  - Lista de eventos do período com filtros
  - Menu de acesso rápido
  - Filtros de data personalizáveis

---

## 2. 🎭 **GESTÃO DE EVENTOS**

### **RF002 - Cadastro de Eventos**
- **Dados:** Nome, circo, datas, cidade/estado, endereço, status, produtor, observações
- **Status:** A realizar, Em andamento, Realizado
- **Validações:** Datas obrigatórias, relacionamentos

### **RF003 - Listagem de Eventos**
- **Visualização:** Cards responsivos com informações resumidas
- **Filtros:** Hoje, Ontem, 7 dias, Este mês, Período customizado
- **Ações:** Editar, Visualizar detalhes, Relatório de faturamento, Excluir
- **Status visual:** Badges coloridos por status

### **RF004 - Edição de Eventos**
- **Funcionalidades:** Mesmos campos do cadastro
- **Preservação:** Dados existentes mantidos
- **Validação:** Controle de integridade

### **RF005 - Gestão Financeira de Eventos**
- **Despesas Fixas:** Auto-cadastro na criação, edição inline via AJAX
- **Despesas Variáveis:** Adição/edição individual via AJAX
- **Receitas:** Vinculação ao evento
- **Salvamento:** Individual por linha sem recarregar página

---

## 3. 🏢 **CADASTROS PRINCIPAIS**

### **RF006 - Gestão de Circos**
- **Dados:** Nome, responsável, telefones, observações
- **Funcionalidades:** CRUD completo, busca, ordenação
- **Relacionamentos:** Vinculado a eventos

### **RF007 - Gestão de Colaboradores**
- **Dados:** Nome, múltiplas categorias
- **Categorias:** Seleção múltipla via checkboxes
- **Validação:** Nome obrigatório, pelo menos uma categoria
- **Exibição:** Badges coloridos para categorias

### **RF008 - Gestão de Elenco**
- **Dados:** Nome, CPF, endereço, cidade, estado, telefone, email, observações
- **Funcionalidades:** CRUD completo com validação

### **RF009 - Gestão de Veículos**
- **Dados:** Nome, categoria, marca, modelo, ano, placa, cor, combustível, capacidade
- **Categorização:** Por tipo de veículo
- **Combustível:** Gasolina, Álcool, Flex, Diesel, Elétrico

### **RF010 - Gestão de Fornecedores**
- **Dados:** Nome, telefone, categoria
- **Categorização:** Por tipo de fornecimento
- **Relacionamentos:** Vinculado a despesas

### **RF011 - Gestão de Receitas**
- **Dados:** Nome, categoria
- **Categorização:** Por tipo de receita
- **Relacionamentos:** Vinculado a eventos

### **RF012 - Gestão de Despesas**
- **Dados:** Nome, categoria, tipo, valor médio
- **Tipos:** 
  - Fixas - Evento
  - Variáveis - Evento  
  - Fixas - SócratesOnline
  - Variáveis - SócratesOnline
- **Validação:** Valor médio obrigatório para despesas fixas
- **Formato:** Suporte a vírgula decimal (100,50)

---

## 4. 🏷️ **GESTÃO DE CATEGORIAS**

### **RF013-017 - Categorias**
- **Categorias de Colaborador:** Classificação funcional
- **Categorias de Veículo:** Classificação por tipo
- **Categorias de Fornecedor:** Classificação por área
- **Categorias de Receita:** Classificação por origem
- **Categorias de Despesa:** Classificação por natureza

**Funcionalidades Comuns:**
- CRUD completo
- Nome único obrigatório
- Relacionamento com entidades principais
- Busca e ordenação

---

## 5. 📈 **RELATÓRIOS**

### **RF018 - Relatório de Lucratividade por Período**
- **Filtros:** Data início/fim
- **Dados:** Receitas, despesas, lucro por período
- **Visualização:** Gráficos interativos

### **RF019 - Relatório de Faturamento por Evento**
- **Listagem:** Eventos com indicadores financeiros
- **Gráficos:** Top 10 eventos mais lucrativos
- **Drill-down:** Relatório detalhado por evento específico

### **RF020 - Relatório Detalhado de Evento**
- **Dados:** Receitas, despesas, lucro específicos
- **Breakdown:** Detalhamento por categoria
- **Visualização:** Gráficos e tabelas

---

## 6. 🔍 **FUNCIONALIDADES TRANSVERSAIS**

### **RF021 - Sistema de Busca**
- **Implementação:** Busca em tempo real em todas as tabelas
- **Campos:** Busca em múltiplas colunas simultaneamente
- **Performance:** Filtro cliente-side instantâneo

### **RF022 - Sistema de Ordenação**
- **Implementação:** Ordenação clicável em cabeçalhos de tabela
- **Tipos de Dados:** 
  - Texto (alfabética case-insensitive)
  - Números (numérica)
  - Valores monetários (remove R$ e ordena numericamente)
  - Datas (DD/MM/YYYY e YYYY-MM-DD)
- **Interface:** Ícones visuais (↕️ ↑ ↓)
- **Comportamento:** Alternância crescente/decrescente

### **RF023 - Validação de Formulários**
- **Cliente:** HTML5 + JavaScript personalizado
- **Servidor:** WTForms validation
- **Feedback:** Mensagens de erro contextuais
- **UX:** Validação em tempo real

### **RF024 - Interface Responsiva**
- **Mobile:** Sidebar colapsável, navbar específica
- **Desktop:** Layout de 2 colunas
- **Breakpoints:** Bootstrap responsive design
- **Touch:** Compatibilidade com dispositivos touch

### **RF025 - Sistema de Notificações**
- **Flash Messages:** Sucesso, erro, warning, info
- **Auto-dismiss:** Fechamento automático
- **Posicionamento:** Topo da página

---

## 🎨 REQUISITOS DE INTERFACE

### **RNF001 - Design System**
- **Paleta:** Azul primário (#0ea5e9), verde sucesso, vermelho perigo
- **Tipografia:** Poppins (Google Fonts)
- **Ícones:** Bootstrap Icons + Font Awesome
- **Layout:** Cards, tabelas, formulários padronizados

### **RNF002 - Usabilidade**
- **Navegação:** Sidebar hierárquica com subminus
- **Breadcrumbs:** Implícito via estrutura de menu
- **Feedback:** Visual para todas as ações
- **Consistência:** Padrões mantidos em todo sistema

---

## 🔒 REQUISITOS NÃO FUNCIONAIS

### **RNF003 - Segurança**
- **Autenticação:** Session-based
- **Autorização:** Por categoria de usuário
- **Validação:** Cliente e servidor
- **CSRF:** Proteção via tokens

### **RNF004 - Performance**
- **Busca:** Filtro instantâneo cliente-side
- **Ordenação:** Processamento local sem requisições
- **Carregamento:** Assets otimizados via CDN
- **Animações:** Transições suaves (150ms)

### **RNF005 - Compatibilidade**
- **Navegadores:** Chrome, Firefox, Safari, Edge (versões recentes)
- **Dispositivos:** Desktop, tablet, mobile
- **Resolução:** 320px - 1920px+

### **RNF006 - Manutenibilidade**
- **Código:** Separação clara MVC
- **Componentes:** JavaScript reutilizável
- **CSS:** Classes utility + componentes
- **Documentação:** Comentários e estrutura clara

---

## 📋 CASOS DE USO PRINCIPAIS

### **UC001 - Criar Evento**
1. Usuário acessa "Novo Evento"
2. Preenche dados obrigatórios
3. Sistema valida e salva
4. Auto-cadastra despesas fixas
5. Redireciona para edição/gestão financeira

### **UC002 - Gerenciar Financeiro do Evento**
1. Usuário acessa evento em edição
2. Visualiza despesas fixas (azuis) e variáveis (verdes/brancas)
3. Edita valores inline
4. Salva individualmente via AJAX
5. Sistema atualiza totais em tempo real

### **UC003 - Gerar Relatório**
1. Usuário acessa relatórios
2. Define filtros (período, evento)
3. Sistema processa dados
4. Exibe gráficos interativos
5. Permite drill-down para detalhes

### **UC004 - Buscar e Ordenar Dados**
1. Usuário acessa qualquer listagem
2. Digita termo na busca (filtro instantâneo)
3. Clica em cabeçalho para ordenar
4. Sistema reorganiza dados localmente
5. Mantém busca + ordenação simultâneas

---

## 🗄️ MODELO DE DADOS

### **Entidades Principais**
- **Eventos:** Central do sistema
- **Circos:** Relacionado a eventos
- **Colaboradores:** N:N com categorias
- **Elenco:** Independente
- **Veículos:** Categorizados
- **Fornecedores:** Categorizados
- **Receitas:** Categorizadas, relacionadas a eventos
- **Despesas:** Categorizadas, tipificadas
- **DespesaEvento:** Relacionamento com valores específicos

### **Relacionamentos**
- Evento N:1 Circo
- Evento N:1 Colaborador (produtor)
- Colaborador N:N CategoriaColaborador
- Despesa 1:N DespesaEvento
- Evento 1:N DespesaEvento

---

## 🚀 ROADMAP DE EVOLUÇÃO

### **Fase 1 - Funcionalidades Básicas (✅ CONCLUÍDO)**
- ✅ Autenticação e autorização
- ✅ CRUD de todas as entidades
- ✅ Dashboard básico
- ✅ Relatórios essenciais
- ✅ Interface responsiva
- ✅ Sistema de busca e ordenação

### **Fase 2 - Melhorias de UX (SUGESTÕES)**
- 🔄 Notificações push
- 🔄 Exportação de dados (Excel/PDF)
- 🔄 Calendário de eventos
- 🔄 Upload de arquivos/imagens
- 🔄 Histórico de alterações

### **Fase 3 - Funcionalidades Avançadas (SUGESTÕES)**
- 🔄 API REST para integração
- 🔄 Relatórios personalizáveis
- 🔄 Dashboard customizável
- 🔄 Notificações por email
- 🔄 Backup automatizado

### **Fase 4 - Escalabilidade (SUGESTÕES)**
- 🔄 Migração para PostgreSQL
- 🔄 Cache Redis
- 🔄 Containerização Docker
- 🔄 Deploy automatizado
- 🔄 Monitoramento

---

## 📝 OBSERVAÇÕES TÉCNICAS

### **Pontos Fortes Atuais**
- ✅ Interface moderna e responsiva
- ✅ Navegação intuitiva
- ✅ Validação robusta
- ✅ Performance adequada
- ✅ Código bem estruturado
- ✅ Funcionalidades AJAX para UX fluida

### **Oportunidades de Melhoria**
- 🔧 Implementar testes automatizados
- 🔧 Adicionar logs estruturados
- 🔧 Melhorar tratamento de erros
- 🔧 Implementar cache estratégico
- 🔧 Adicionar métricas de uso

### **Considerações de Segurança**
- 🔒 Implementar rate limiting
- 🔒 Adicionar logs de auditoria
- 🔒 Criptografia de dados sensíveis
- 🔒 Backup e recovery
- 🔒 Testes de penetração

---

**📅 Última Atualização:** Janeiro 2024  
**👤 Responsável:** Equipe de Desenvolvimento  
**📧 Contato:** [contato@socratesonline.com]

---

*Este documento serve como base para futuras evoluções do sistema. Todas as funcionalidades listadas estão implementadas e operacionais na versão atual.* 