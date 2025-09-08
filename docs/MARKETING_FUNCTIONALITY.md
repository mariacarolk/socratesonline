# 📢 Funcionalidade de Marketing - Sistema Sócrates Online

## 📊 Visão Geral

A funcionalidade de Marketing foi completamente reestruturada para suportar **múltiplas visitas por escola** e oferecer um controle mais avançado sobre o relacionamento com instituições de ensino. O sistema agora separa claramente os dados básicos das escolas dos registros específicos de cada visita.

## 🎯 Objetivos

- **Modernizar** o processo de follow-up com escolas
- **Centralizar** informações de contato em uma base única
- **Permitir múltiplas visitas** à mesma escola ao longo do tempo
- **Automatizar** envios de material promocional
- **Gerar relatórios** e estatísticas de performance
- **Manter histórico completo** de todas as interações

---

## 🏗️ Arquitetura do Sistema

### **Separação de Responsabilidades**

**🏫 Escola (Cadastro Único)**
- Dados básicos da instituição
- Informações de contato principal
- Endereço e localização
- Uma escola = um registro permanente

**📅 Visita à Escola (Múltiplos Registros)**
- Data e hora específica da visita
- Promotor responsável
- Status da visita (agendada/realizada/cancelada)
- Controle de envios (email/WhatsApp)
- Observações específicas da visita

---

## ⚡ Funcionalidades Implementadas

## 1. 📊 **Dashboard de Marketing**
*Rota: `/marketing/dashboard`*

### **Estatísticas Principais**
- 🏫 **Total de Escolas Cadastradas**
- 📅 **Total de Visitas Realizadas**
- ⏰ **Visitas Agendadas**
- ✅ **Visitas Realizadas**
- ❌ **Visitas Canceladas**

### **Controle de Comunicação**
- 📧 **E-mails Pendentes de Envio**
- 📧 **E-mails Já Enviados**
- 📱 **WhatsApp Pendentes de Envio**
- 📱 **WhatsApp Já Enviados**

### **Funcionalidades Avançadas**
- 🎯 **Botões de Envio em Massa** para material pendente
- 📈 **Gráfico Visual** (pizza) do status das visitas
- 🏆 **Ranking** das escolas mais visitadas
- ⏰ **Lista** das últimas 5 visitas realizadas
- 🔗 **Links diretos** para histórico detalhado

---

## 2. 🏫 **Gerenciamento de Escolas**
*Rota: `/cadastros/escolas`*

### **Cadastro de Escola**
**Dados Básicos:**
- Nome da escola
- Endereço completo
- Cidade e Estado (com busca automática)
- E-mail institucional
- WhatsApp institucional

**Informações de Contato:**
- Nome da pessoa de contato
- Cargo da pessoa (opcional)
- Observações gerais da escola

### **Funcionalidades**
- ✅ **CRUD Completo** (Criar, Ler, Atualizar, Deletar)
- 🔍 **Listagem** com informações resumidas
- 📊 **Contador** de visitas por escola
- 🔗 **Link direto** para histórico de visitas
- 🛡️ **Proteção** contra exclusão (se houver visitas)

### **Busca Automática de Cidades**
- 🌍 **API Integrada** com cidades brasileiras
- 🔄 **Carregamento automático** ao selecionar estado
- ✨ **Autocompletar** com sugestões
- ✅ **Validação** de dados padronizados

---

## 3. 📅 **Gestão de Visitas**
*Rota: `/visitas/escolas`*

### **Agendamento de Visitas**
**Dados da Visita:**
- Escola (seleção da lista cadastrada)
- Data e hora da visita
- Status (agendada/realizada/cancelada)
- Observações específicas da visita
- Promotor (automático pelo usuário logado)

### **Controle de Comunicação**
**Por Visita Individual:**
- Flag de e-mail enviado
- Data/hora do envio do e-mail
- Flag de WhatsApp enviado
- Data/hora do envio do WhatsApp

### **Funcionalidades**
- 📋 **Listagem completa** de todas as visitas
- 🔍 **Filtros** por status, promotor, período
- 📊 **Estatísticas visuais** por status
- ✏️ **Edição** de visitas (com controle de permissão)
- 🗑️ **Exclusão** controlada por permissões

---

## 4. 📖 **Histórico Detalhado**
*Rota: `/escolas/<id>/historico`*

### **Timeline de Visitas**
- 📅 **Cronologia visual** de todas as visitas
- 👤 **Promotor responsável** por cada visita
- 📝 **Observações específicas** de cada visita
- 📧 **Status de comunicação** (e-mail/WhatsApp)
- 🎨 **Interface visual** com timeline

### **Informações da Escola**
- 📋 **Dados completos** da instituição
- 📊 **Estatísticas** de visitas
- 🔗 **Ações rápidas** (nova visita, editar escola)

---

## 🔐 Controle de Acesso

### **Permissões por Categoria**

**👑 Administrativo**
- ✅ Acesso total a todas as funcionalidades
- ✅ Pode editar/excluir qualquer visita
- ✅ Pode gerenciar todas as escolas
- ✅ Acesso a estatísticas globais

**🎯 Promotor de Vendas**
- ✅ Acesso ao dashboard de marketing
- ✅ Pode cadastrar escolas
- ✅ Pode agendar visitas
- ✅ Pode editar apenas suas próprias visitas
- ✅ Pode enviar material em massa

**❌ Outras Categorias**
- Acesso negado às funcionalidades de marketing

---

## 🚀 Automações Implementadas

### **Envio de Material Promocional**
*Endpoint: `/marketing/enviar-material`*

**Funcionalidade:**
- 🎯 **Envio em massa** para escolas pendentes
- 📧 **E-mail** - Envia para todas as escolas com e-mail não enviado
- 📱 **WhatsApp** - Envia para todas as escolas com WhatsApp não enviado
- ✅ **Marcação automática** após envio
- 📊 **Relatório** de quantos foram enviados

**Status Tracking:**
- Controle individual por visita
- Data/hora de cada envio
- Prevenção de envios duplicados
- Histórico completo de comunicações

---

## 🎨 Interface do Usuário

### **Design Responsivo**
- 📱 **Mobile-first** - Funciona em todos os dispositivos
- 🎨 **Bootstrap 5** - Interface moderna e consistente
- 📊 **Chart.js** - Gráficos interativos
- ⚡ **AJAX** - Operações sem recarregar página

### **Experiência do Usuário**
- 🔍 **Busca instantânea** de cidades
- ✨ **Feedback visual** para todas as ações
- 📊 **Indicadores visuais** de status
- 🎯 **Navegação intuitiva** entre funcionalidades

---

## 📊 Relatórios e Estatísticas

### **Métricas Disponíveis**
- 📈 **Total de escolas** cadastradas
- 📈 **Total de visitas** por período
- 📈 **Taxa de conversão** de visitas
- 📈 **Performance por promotor**
- 📈 **Efetividade** de comunicação

### **Visualizações**
- 🥧 **Gráfico de pizza** - Status das visitas
- 📊 **Ranking** - Escolas mais visitadas
- ⏰ **Timeline** - Últimas atividades
- 📋 **Listas** - Dados tabulares organizados

---

## 🔧 Aspectos Técnicos

### **Banco de Dados**
```sql
-- Estrutura Principal
escola (dados básicos da escola)
├── id_escola (PK)
├── nome, endereco, cidade, estado
├── email, whatsapp
├── nome_contato, cargo_contato
└── observacoes

visita_escola (registros de visitas)
├── id_visita (PK)
├── id_escola (FK)
├── id_promotor (FK)
├── data_visita, status_visita
├── email_enviado, data_email_enviado
├── whatsapp_enviado, data_whatsapp_enviado
└── observacoes_visita
```

### **APIs Integradas**
- 🌍 `/api/cidades/<estado>` - Busca de cidades por estado
- 📧 `/marketing/enviar-material` - Envio de material promocional

### **Segurança**
- 🔐 **Autenticação** obrigatória
- 🛡️ **Controle de permissões** por categoria
- ✅ **Validação** de dados no frontend e backend
- 🔒 **Proteção CSRF** em formulários

---

## 🎯 Fluxo de Trabalho

### **Para Promotores de Vendas**

1. **🏫 Cadastrar Escola**
   - Acessar "Marketing > Gerenciar Escolas"
   - Preencher dados básicos da escola
   - Sistema valida e salva informações

2. **📅 Agendar/Registrar Visita**
   - Acessar "Marketing > Visitas às Escolas"
   - Selecionar escola da lista
   - Definir data, hora e status
   - Adicionar observações específicas

3. **📊 Acompanhar Performance**
   - Acessar "Marketing > Dashboard Marketing"
   - Visualizar estatísticas atualizadas
   - Enviar material pendente em massa

4. **📖 Consultar Histórico**
   - Clicar em "Histórico" na lista de escolas
   - Ver timeline completa de visitas
   - Verificar comunicações realizadas

---

## 🚀 Benefícios da Nova Arquitetura

### **✅ Vantagens Implementadas**

**📊 Dados Organizados**
- Separação clara entre escola e visitas
- Histórico completo preservado
- Relatórios mais precisos

**🔄 Flexibilidade**
- Múltiplas visitas à mesma escola
- Diferentes promotores podem visitar
- Status independentes por visita

**⚡ Automação**
- Envios em massa eficientes
- Controle automático de duplicatas
- Estatísticas atualizadas em tempo real

**🎯 Controle**
- Permissões granulares
- Rastreamento completo de ações
- Proteção de dados importantes

**📱 Usabilidade**
- Interface responsiva
- Navegação intuitiva
- Feedback visual imediato

---

## 🔮 Próximas Evoluções Sugeridas

### **📧 Integração Real de E-mail**
- Configuração de SMTP
- Templates personalizáveis
- Tracking de abertura/cliques

### **📱 Integração WhatsApp Business**
- API oficial do WhatsApp
- Mensagens automáticas
- Confirmações de entrega

### **📊 Relatórios Avançados**
- Exportação para Excel/PDF
- Gráficos de tendência
- Comparativos por período

### **🔍 Filtros e Buscas**
- Busca avançada por múltiplos campos
- Filtros salvos
- Ordenação customizável

### **📅 Calendário Integrado**
- Visualização de visitas em calendário
- Lembretes automáticos
- Sincronização com Google Calendar

---

## 📞 Suporte Técnico

### **🛠️ Resolução de Problemas**

**Erro de Tabela Não Encontrada:**
```bash
# Execute o script de criação
python init_root_user.py
```

**Problemas de Permissão:**
- Verifique se o usuário tem categoria correta
- Administradores têm acesso total
- Promotores têm acesso limitado

**Cidades Não Carregam:**
- Verifique se JavaScript está habilitado
- Confirme se API `/api/cidades/<estado>` está funcionando

---

**Sistema Sócrates Online** - Marketing Inteligente para Eventos Circenses 🎪