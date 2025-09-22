# 📋 MAPEAMENTO COMPLETO DO SISTEMA SÓCRATES ONLINE

> **Documento de Referência Técnica**  
> **Última Atualização:** 11/09/2025  
> **Versão:** 1.0  

---

## 📊 **VISÃO GERAL DO SISTEMA**

**Sistema:** Sócrates Online  
**Tipo:** Gestão de Eventos para Circos  
**Tecnologia:** Python Flask + PostgreSQL + Bootstrap 5  
**Total de Rotas:** 113 rotas principais  
**Total de Templates:** ~40 templates  
**Total de Funcionalidades:** ~220+ ações distintas  
**Sistema de Logs:** 20+ operações auditadas  

---

## 🎯 **CONTROLE DE ACESSO POR PERFIL**

### **🔴 ROOT** *(Acesso Total)*
- Dashboard completo
- Todos os eventos e gestão financeira
- Todos os cadastros
- Todos os relatórios
- Marketing (nível administrativo)
- Funcionalidades administrativas

### **🟡 ADMINISTRATIVO** *(Acesso Parcial)*
- Colaboradores e suas categorias
- Marketing (nível administrativo)
- Logs do sistema

### **🟢 PROMOTOR DE VENDAS** *(Acesso Limitado)*
- Marketing (funcionalidades básicas)
- Escolas e visitas

---

## 🏠 **MENU: DASHBOARD**
*Disponível apenas para usuários ROOT*

### **Tela Principal**
- **Rota:** `/` 
- **Função:** `dashboard()`
- **Template:** `dashboard.html`
- **Controlador:** Linha 185 em `app.py`

### **Funcionalidades:**
1. **Contadores Principais:**
   - Total de eventos
   - Total de receitas 
   - Total de despesas
   - Total de colaboradores

2. **Gráficos Interativos:**
   - Gráfico de lucro por período (7 dias, mês, customizado)
   - Filtros de data personalizáveis

3. **Lista de Eventos:**
   - Eventos do período com filtros
   - Menu de acesso rápido

---

## 🎭 **MENU: EVENTOS**
*Disponível apenas para usuários ROOT*

### **1. Listagem de Eventos**
- **Rota:** `/eventos`
- **Função:** `listar_eventos()` *(Linha 1919)*
- **Template:** `eventos.html`

**Ações disponíveis:**
- Visualizar eventos em cards responsivos
- Filtros: Hoje, Ontem, 7 dias, Este mês, Período customizado
- **Ações por evento:**
  - Adicionar Despesa (modal unificado)
  - Adicionar Receita (modal)
  - Editar evento
  - Visualizar detalhes completos
  - Relatório de faturamento
  - Excluir evento

### **2. Criar Novo Evento**
- **Rota:** `/eventos/novo`
- **Função:** `novo_evento()` *(Linha 2211)*
- **Template:** `novo_evento.html`

**Funcionalidades:**
- Formulário completo com dados do evento
- Seleção dinâmica de cidades por estado
- Auto-cadastro de despesas fixas ao criar

### **3. Editar Evento**
- **Rota:** `/eventos/editar/<int:id>`
- **Função:** `editar_evento()` *(Linha 2452)*
- **Template:** `novo_evento.html`

### **4. Excluir Evento**
- **Rota:** `/eventos/excluir/<int:id>`
- **Função:** `excluir_evento()` *(Linha 2891)*

### **5. Gestão Financeira do Evento**

#### **5.1 Despesas do Evento**
- **Rota:** `/eventos/<int:id_evento>/despesas`
- **Função:** `despesas_evento()` *(Linha 3674)*
- **Template:** `despesas_evento.html`
- **Funcionalidades:**
  - Listar despesas fixas (azuis) e variáveis (verdes/brancas)
  - Edição inline via AJAX
  - Salvamento individual por linha
  - Upload de comprovantes

#### **5.2 Ações AJAX para Despesas:**
- **Salvar despesa:** `/eventos/<int:id_evento>/salvar-despesa` *(Linha 3721)*
- **Excluir despesa:** `/eventos/<int:id_evento>/excluir-despesa/<int:despesa_evento_id>` *(Linha 4611)*
- **Editar despesa:** `/eventos/<int:id_evento>/editar-despesa/<int:despesa_evento_id>` *(Linha 4644)*
- **Atualizar cabeça:** `/eventos/<int:id_evento>/atualizar-despesa-cabeca/<int:despesa_evento_id>` *(Linha 4920)*
- **Excluir comprovante:** `/eventos/<int:id_evento>/excluir-comprovante/<int:despesa_evento_id>` *(Linha 4967)*

#### **5.3 Ações AJAX para Receitas:**
- **Salvar receita:** `/eventos/<int:id_evento>/salvar-receita` *(Linha 2138)*
- **Excluir receita:** `/eventos/<int:id_evento>/excluir-receita/<int:receita_evento_id>` *(Linha 4509)*
- **Atualizar receita:** `/eventos/<int:id_evento>/atualizar-receita/<int:receita_evento_id>` *(Linha 4542)*

### **6. Gestão de Recursos do Evento**

#### **6.1 Equipe do Evento**
- **Rota:** `/eventos/<int:id_evento>/equipe`
- **Função:** `equipe_evento()` *(Linha 3900)*
- **Template:** `equipe_evento.html`
- **Ações:** 
  - Adicionar: Incluído na função principal
  - Editar: `/eventos/<int:id_evento>/equipe/editar/<int:id>` *(Linha 3937)*
  - Excluir: `/eventos/<int:id_evento>/equipe/excluir/<int:id>` *(Linha 3966)*

#### **6.2 Veículos do Evento**
- **Rota:** `/eventos/<int:id_evento>/veiculos`
- **Função:** `veiculos_evento()` *(Linha 4174)*
- **Template:** `veiculos_evento.html`
- **Ações:**
  - Adicionar: Incluído na função principal
  - Editar: `/eventos/<int:id_evento>/veiculos/editar/<int:id>` *(Linha 4270)*
  - Excluir: `/eventos/<int:id_evento>/veiculos/excluir/<int:id>` *(Linha 4355)*

#### **6.3 Elenco do Evento**
- **Rota:** `/eventos/<int:id_evento>/elenco`
- **Função:** `elenco_evento()` *(Linha 4364)*
- **Template:** `elenco_evento.html`
- **Ações:**
  - Adicionar: Incluído na função principal
  - Editar: `/eventos/<int:id_evento>/elenco/editar/<int:id>` *(Linha 4400)*
  - Excluir: `/eventos/<int:id_evento>/elenco/excluir/<int:id>` *(Linha 4428)*

#### **6.4 Fornecedores do Evento**
- **Rota:** `/eventos/<int:id_evento>/fornecedores`
- **Função:** `fornecedores_evento()` *(Linha 4437)*
- **Template:** `fornecedor_evento.html`
- **Ações:**
  - Adicionar: Incluído na função principal
  - Editar: `/eventos/<int:id_evento>/fornecedores/editar/<int:id>` *(Linha 4473)*
  - Excluir: `/eventos/<int:id_evento>/fornecedores/excluir/<int:id>` *(Linha 4501)*

### **7. APIs de Suporte para Eventos**
- **Detalhes completos:** `/api/evento/<int:id_evento>/detalhes-completos` *(Linha 5032)*
- **Busca de fornecedores:** `/api/fornecedores-busca` *(Linha 4854)*
- **Despesas por categoria:** `/api/despesas-por-categoria/<int:categoria_id>` *(Linha 2015)*
- **Despesas empresa por categoria:** `/api/despesas-empresa-por-categoria/<int:categoria_id>` *(Linha 2047)*
- **Receitas por categoria:** `/api/receitas-por-categoria/<int:categoria_id>` *(Linha 2079)*
- **Detalhes de despesa:** `/api/despesa-detalhes/<int:despesa_id>` *(Linha 2095)*
- **Valor médio de despesas:** `/api/despesa-valor-medio/<int:despesa_id>` *(Linha 2115)*

---

## 📝 **MENU: CADASTROS**
*Parcialmente disponível para administrativos, completo para ROOT*

### **1. Colaboradores** *(Liberado para administrativos)*
- **Rota:** `/cadastros/colaboradores`
- **Função:** `cadastrar_colaborador()` *(Linha 692)*
- **Template:** `colaboradores.html`
- **Ações:** 
  - Listar/Criar: Função principal
  - Editar: `/cadastros/colaboradores/editar/<int:id>` *(Linha 807)*
  - Excluir: `/cadastros/colaboradores/excluir/<int:id>` *(Linha 907)*
  - **Gestão de usuários:**
    - Criar usuário: `/colaboradores/<int:id>/criar-usuario` *(Linha 940)*
    - Editar usuário: `/colaboradores/<int:id>/editar-usuario` *(Linha 994)*
    - Excluir usuário: `/colaboradores/<int:id>/excluir-usuario` *(Linha 1028)*

### **2. Categorias de Colaboradores** *(Liberado para administrativos)*
- **Rota:** `/cadastros/categorias-colaborador`
- **Função:** `cadastrar_categoria_colaborador()` *(Linha 680)*
- **Template:** `categorias_colaborador.html`
- **Ações:**
  - Listar/Criar: Função principal
  - Editar: `/cadastros/categorias-colaborador/editar/<int:id>` *(Linha 780)*
  - Excluir: `/cadastros/categorias-colaborador/excluir/<int:id>` *(Linha 792)*

### **3. Circos** *(Apenas ROOT)*
- **Rota:** `/cadastros/circos`
- **Função:** `cadastrar_circo()` *(Linha 633)*
- **Template:** `cadastrar_circo.html`
- **Ações:**
  - Listar/Criar: Função principal
  - Editar: `/cadastros/circos/editar/<int:id>` *(Linha 649)*
  - Excluir: `/cadastros/circos/excluir/<int:id>` *(Linha 664)*

### **4. Elencos** *(Apenas ROOT)*
- **Rota:** `/cadastros/elenco`
- **Função:** `cadastrar_elenco()` *(Linha 1060)*
- **Template:** `elenco.html`
- **Ações:**
  - Listar/Criar: Função principal
  - Editar: `/cadastros/elenco/editar/<int:id>` *(Linha 1080)*
  - Excluir: `/cadastros/elenco/excluir/<int:id>` *(Linha 1099)*

### **5. Veículos** *(Apenas ROOT)*
- **Rota:** `/cadastros/veiculos`
- **Função:** `cadastrar_veiculo()` *(Linha 3514)*
- **Template:** `veiculos.html`
- **Ações:**
  - Listar/Criar: Função principal
  - Editar: `/cadastros/veiculos/editar/<int:id>` *(Linha 3544)*
  - Excluir: `/cadastros/veiculos/excluir/<int:id>` *(Linha 3573)*

### **6. Categorias de Veículos** *(Apenas ROOT)*
- **Rota:** `/cadastros/categorias-veiculo`
- **Função:** `cadastrar_categoria_veiculo()` *(Linha 3475)*
- **Template:** `categorias_veiculo.html`
- **Ações:**
  - Listar/Criar: Função principal
  - Editar: `/cadastros/categorias-veiculo/editar/<int:id>` *(Linha 3486)*
  - Excluir: `/cadastros/categorias-veiculo/excluir/<int:id>` *(Linha 3498)*

### **7. Fornecedores** *(Apenas ROOT)*
- **Rota:** `/cadastros/fornecedores`
- **Função:** `cadastrar_fornecedor()` *(Linha 1120)*
- **Template:** `fornecedores.html`
- **Ações:**
  - Listar/Criar: Função principal
  - Editar: `/cadastros/fornecedores/editar/<int:id>` *(Linha 1171)*
  - Excluir: `/cadastros/fornecedores/excluir/<int:id>` *(Linha 1194)*

### **8. Categorias de Fornecedores** *(Apenas ROOT)*
- **Rota:** `/cadastros/categorias-fornecedor`
- **Função:** `cadastrar_categoria_fornecedor()` *(Linha 1108)*
- **Template:** `categorias_fornecedor.html`
- **Ações:**
  - Listar/Criar: Função principal
  - Editar: `/cadastros/categorias-fornecedor/editar/<int:id>` *(Linha 1144)*
  - Excluir: `/cadastros/categorias-fornecedor/excluir/<int:id>` *(Linha 1156)*

### **9. Receitas** *(Apenas ROOT)*
- **Rota:** `/cadastros/receitas`
- **Função:** `cadastrar_receita()` *(Linha 1205)*
- **Template:** `receitas.html`
- **Ações:**
  - Listar/Criar: Função principal
  - Editar: `/cadastros/receitas/editar/<int:id>` *(Linha 1223)*
  - Excluir: `/cadastros/receitas/excluir/<int:id>` *(Linha 1243)*

### **10. Categorias de Receitas** *(Apenas ROOT)*
- **Rota:** `/cadastros/categorias-receita`
- **Função:** `cadastrar_categoria_receita()` *(Linha 1259)*
- **Template:** `categorias_receita.html`
- **Ações:**
  - Listar/Criar: Função principal
  - Editar: `/cadastros/categorias-receita/editar/<int:id>` *(Linha 1270)*
  - Excluir: `/cadastros/categorias-receita/excluir/<int:id>` *(Linha 1282)*

### **11. Despesas** *(Apenas ROOT)*
- **Rota:** `/cadastros/despesas`
- **Função:** `cadastrar_despesa()` *(Linha 3584)*
- **Template:** `despesas.html`
- **Ações:**
  - Listar/Criar: Função principal
  - Editar: `/cadastros/despesas/editar/<int:id>` *(Linha 3620)*
  - Excluir: `/cadastros/despesas/excluir/<int:id>` *(Linha 3659)*

### **12. Categorias de Despesas** *(Apenas ROOT)*
- **Rota:** `/cadastros/categorias-despesa`
- **Função:** `cadastrar_categoria_despesa()` *(Linha 1298)*
- **Template:** `categorias_despesa.html`
- **Ações:**
  - Listar/Criar: Função principal
  - Editar: `/cadastros/categorias-despesa/editar/<int:id>` *(Linha 1309)*
  - Excluir: `/cadastros/categorias-despesa/excluir/<int:id>` *(Linha 1321)*

### **13. Parâmetros** *(Apenas ROOT)*
- **Rota:** `/cadastros/parametros`
- **Função:** `cadastrar_parametro()` *(Linha 1342)*
- **Template:** `parametros.html`
- **Ações:**
  - Listar/Criar: Função principal
  - Editar: `/cadastros/parametros/editar/<int:id>` *(Linha 1357)*
  - Excluir: `/cadastros/parametros/excluir/<int:id>` *(Linha 1371)*

---

## 🏦 **MENU: GESTÃO FINANCEIRA EMPRESA**
*Disponível apenas para usuários ROOT*

### **1. Informar Despesa da Empresa**
- **Rota:** `/empresa/despesas`
- **Função:** `despesas_empresa()` *(Linha 5827)*
- **Template:** `despesas_empresa.html`
- **Ações:** 
  - Listar/Criar: Função principal
  - Editar: `/empresa/despesas/editar/<int:id>` *(Linha 5937)*
  - Excluir: `/empresa/despesas/excluir/<int:id>` *(Linha 6046)*

### **2. Informar Receita da Empresa**
- **Rota:** `/empresa/receitas`
- **Função:** `receitas_empresa()` *(Linha 5895)*
- **Template:** `receitas_empresa.html`
- **Ações:**
  - Listar/Criar: Função principal
  - Editar: `/empresa/receitas/editar/<int:id>` *(Linha 6004)*
  - Excluir: `/empresa/receitas/excluir/<int:id>` *(Linha 6075)*

### **3. Financeiro Mês**
- **Rota:** `/empresa/financeiro-mes`
- **Função:** `financeiro_mes()` *(Linha 6100)*
- **Template:** `financeiro_mes.html`
- **Ações:**
  - Visualização do fechamento mensal
  - Adicionar despesas fixas em lote: `/empresa/adicionar-despesas-fixas` *(Linha 6374)*

---

## 📊 **MENU: RELATÓRIOS**
*Disponível apenas para usuários ROOT*

### **1. Lucratividade Mensal**
- **Rota:** `/relatorios/lucratividade-mensal`
- **Função:** `relatorios_lucratividade_mensal()` *(Linha 2988)*
- **Template:** `relatorios_lucratividade_mensal.html`
- **Funcionalidades:**
  - Filtros por período
  - Gráficos interativos
  - Breakdown de receitas/despesas

### **2. Faturamento por Evento**
- **Rota:** `/relatorios/faturamento-evento`
- **Função:** `relatorios_faturamento_evento()` *(Linha 3225)*
- **Template:** `relatorios_faturamento_evento.html`
- **Funcionalidades:**
  - Lista de eventos com indicadores
  - Top 10 eventos mais lucrativos
  - Drill-down: `/relatorios/faturamento-evento/<int:id_evento>` *(Linha 3317)*

### **3. Fechamento por Evento**
- **Rota:** `/relatorios/fechamento-evento`
- **Função:** `relatorios_fechamento_evento()` *(Linha 3364)*
- **Template:** `relatorios_fechamento_evento.html`
- **Funcionalidades:**
  - Lista de eventos para fechamento
  - Relatório detalhado: `/relatorios/fechamento-evento/<int:id_evento>` *(Linha 3412)*

### **4. Despesas Fixas**
- **Rota:** `/relatorios/despesas-fixas`
- **Função:** `relatorio_despesas_fixas()` *(Linha 5525)*
- **Template:** `relatorio_despesas_fixas.html`
- **Ações:**
  - Exportação: `/relatorios/despesas-fixas/exportar/<string:formato>` *(Linha 5584)*

### **5. Veículos e Eventos**
- **Rota:** `/relatorios/veiculos`
- **Função:** `relatorio_veiculos()` *(Linha 5630)*
- **Template:** `relatorio_veiculos.html`
- **Ações:**
  - Exportação: `/relatorios/veiculos/exportar/<string:formato>` *(Linha 5729)*

### **6. Veículos**
- **Rota:** `/relatorios/veiculos-servicos`
- **Função:** `relatorio_veiculos_servicos()` *(Linha 7420)*
- **Template:** `relatorio_veiculos_servicos.html`
- **Funcionalidades:**
  - Filtros por veículo e tipo de serviço
  - Gráficos de serviços por tipo (quantidade e valores)
  - Top 10 veículos por custo total
  - Detalhamento de multas, IPVA, licenciamento e manutenção
- **Ações:**
  - Exportação: `/relatorios/veiculos-servicos/exportar/<string:formato>` *(Linha 7582)*

### **7. Custo da Frota**
- **Rota:** `/relatorios/custo-frota`
- **Função:** `relatorio_custo_frota()` *(Linha 6412)*
- **Template:** `relatorio_custo_frota.html`
- **Ações:**
  - Exportação: `/relatorios/custo-frota/exportar/<string:formato>` *(Linha 6501)*

---

## 📢 **MENU: MARKETING**
*Disponível para Promotores, Administradores e ROOT*

### **1. Dashboard Escolas** *(Apenas para administradores e ROOT)*
- **Rota:** `/marketing/dashboard`
- **Função:** `marketing_dashboard()` *(Linha 1612)*
- **Template:** `marketing_dashboard.html`
- **Funcionalidades:**
  - Estatísticas completas de escolas e visitas
  - Controle de comunicação (email/WhatsApp)
  - Gráficos de performance
  - Ranking de escolas mais visitadas
  - Envio de material em massa: `/marketing/enviar-material` *(Linha 1820)*

### **2. Gerenciar Escolas**
- **Rota:** `/cadastros/escolas`
- **Função:** `cadastrar_escola()` *(Linha 1386)*
- **Template:** `escolas.html`
- **Ações:**
  - Listar/Criar: Função principal
  - Editar: `/cadastros/escolas/editar/<int:id>` *(Linha 1415)*
  - Excluir: `/cadastros/escolas/excluir/<int:id>` *(Linha 1445)*
  - Histórico de visitas: `/escolas/<int:id>/historico` *(Linha 1601)*

### **3. Visitas às Escolas**
- **Rota:** `/visitas/escolas`
- **Função:** `cadastrar_visita_escola()` *(Linha 1473)*
- **Template:** `visitas_escola.html`
- **Ações:**
  - Listar/Criar: Função principal
  - Editar: `/visitas/escolas/editar/<int:id>` *(Linha 1524)*
  - Excluir: `/visitas/escolas/excluir/<int:id>` *(Linha 1571)*

---

## ⚙️ **MENU: ADMINISTRATIVO**
*Disponível para administrativos e ROOT*

### **1. Logs do Sistema**
- **Rota:** `/administrativo/logs`
- **Função:** `listar_logs()` *(Linha 6584)*
- **Template:** `logs_sistema.html`
- **Funcionalidades:**
  - Visualização de logs do sistema
  - Controle de auditoria
  - Monitoramento de atividades

---

## 🔐 **FUNCIONALIDADES DE AUTENTICAÇÃO**

### **1. Login**
- **Rota:** `/login`
- **Função:** `login()` *(Linha 545)*
- **Template:** `login.html`

### **2. Auto-Cadastro**
- **Rota:** `/auto-cadastro`
- **Função:** `auto_cadastro()` *(Linha 582)*
- **Template:** `auto_cadastro.html`

### **3. Logout**
- **Rota:** `/logout`
- **Função:** `logout()` *(Linha 575)*

---

## 🔧 **APIs E FUNCIONALIDADES AUXILIARES**

### **1. APIs de Busca e Dados**
- **Cidades por estado:** `/api/cidades/<string:estado>` *(Linha 4795)*
- **Colaboradores por evento:** `/api/colaborador/<int:colaborador_id>/eventos` *(Linha 5342)*
- **Fornecedores por evento:** `/api/fornecedor/<int:fornecedor_id>/eventos` *(Linha 5383)*
- **Elenco por evento:** `/api/elenco/<int:elenco_id>/eventos` *(Linha 5440)*

### **2. Exportação Universal**
- **Rota:** `/exportar/<string:table_name>/<string:format>`
- **Função:** `exportar_dados()` *(Linha 5481)*
- **Formatos:** PDF, Excel
- **Disponível em:** Todos os cadastros principais

### **3. Upload de Arquivos**
- **Comprovantes:** `/uploads/comprovantes/<filename>` *(Linha 5022)*

### **4. Sistema de Logs de Auditoria**
- **Função:** `registrar_log()` *(Linha 302)*
- **Modelo:** `LogSistema` *(models.py - Linha 361)*
- **Visualização:** `/administrativo/logs` *(Linha 6584)*

**Operações que registram logs:**

#### **🔐 Autenticação:**
- **Login** - Registro de acesso ao sistema *(Linha 566)*
- **Logout** - Registro de saída do sistema *(Linha 585)*

#### **👥 Gestão de Usuários:**
- **Exclusão de Usuário** - Remoção de usuários do sistema *(Linha 1043)*

#### **🏫 Gestão de Escolas:**
- **Cadastrar Escola** - Nova escola adicionada *(Linha 1407)*
- **Editar Escola** - Dados de escola alterados *(Linha 1437)*
- **Excluir Escola** - Escola removida do sistema *(Linha 1467)*

#### **📅 Gestão de Visitas:**
- **Cadastrar Visita** - Nova visita agendada *(Linha 1515)*
- **Editar Visita** - Dados de visita alterados *(Linha 1563)*
- **Excluir Visita** - Visita cancelada/removida *(Linha 1596)*

#### **🎭 Gestão de Eventos:**
- **Criar Evento** - Novo evento criado *(Linha 2405)*
- **Editar Evento** - Dados de evento alterados *(Linha 2772)*
- **Excluir Evento** - Evento removido do sistema *(Linha 2999)*

#### **👤 Gestão de Colaboradores:**
- **Editar Colaborador** - Dados de colaborador alterados *(Linha 900)*
- **Excluir Colaborador** - Colaborador removido *(Linha 951)*

#### **💰 Gestão Financeira Empresa:**
- **Criar Despesa Empresa** - Nova despesa da empresa *(Linha 5912)*
- **Editar Despesa Empresa** - Despesa da empresa alterada *(Linha 6030)*
- **Excluir Despesa Empresa** - Despesa da empresa removida *(Linha 6108)*
- **Criar Receita Empresa** - Nova receita da empresa *(Linha 5960)*
- **Editar Receita Empresa** - Receita da empresa alterada *(Linha 6082)*
- **Excluir Receita Empresa** - Receita da empresa removida *(Linha 6141)*

#### **📢 Marketing e Comunicação:**
- **Envio WhatsApp** - Mensagens enviadas para escolas *(Linha 1893)*
- **Envio Email Marketing** - Emails de marketing enviados *(Linha 1794)*
- **Erro Envio Email** - Falhas no envio de emails *(Linha 1809)*

**Estrutura do Log:**
- **ID único** do registro
- **Ação** realizada
- **Descrição** detalhada
- **Usuário** que executou (ID, nome, email)
- **Data/hora** da operação
- **IP do usuário** (para operações de marketing)

---

## 📱 **RECURSOS TRANSVERSAIS**

### **Frontend/UX:**
- Navegação mobile com sidebar collapse
- Tables responsivas (`static/js/responsive-tables.js`)
- Masks para campos (`static/js/masks.js`)
- Filtros avançados (`static/js/advanced-filters.js`)
- Busca em tempo real
- Ordenação por colunas (`static/js/table-sort.js`)
- Gráficos interativos (`static/js/charts-modern.js`)

### **Validações e Segurança:**
- Controle de acesso baseado em sessão
- Validação de formulários (WTForms)
- Proteção CSRF
- Upload seguro de arquivos

### **Performance:**
- APIs AJAX para operações críticas
- Carregamento otimizado de assets
- Processamento local de ordenação/busca

---

## 📄 **ARQUIVOS DE CONFIGURAÇÃO E ESTRUTURA**

### **Principais Arquivos:**
- `app.py`: Aplicação principal (6.624 linhas)
- `models.py`: Modelos de dados
- `forms.py`: Formulários WTForms
- `config.py`: Configurações
- `extensions.py`: Extensões Flask

### **Templates Base:**
- `base.html`: Template principal com menu
- `auth_base.html`: Template para autenticação

### **Scripts JavaScript:**
- `table-sort.js`: Ordenação de tabelas
- `masks.js`: Máscaras de input
- `responsive-tables.js`: Responsividade
- `advanced-filters.js`: Filtros avançados
- `charts-modern.js`: Gráficos
- `cidades.js`: API dinâmica de cidades
- `despesa-modal.js`: Modal unificado de despesas
- `valor-medio-despesas.js`: Cálculo de valores médios

### **Estilos:**
- `style-modern.css`: Estilos principais modernos
- `style.css`: Estilos legados

---

## 📊 **ESTATÍSTICAS DE CÓDIGO**

### **Distribuição de Funcionalidades:**
1. **Eventos:** 46 ações
2. **Cadastros:** 39 ações
3. **Relatórios:** 12 ações
4. **Marketing:** 8 ações
5. **Gestão Financeira:** 6 ações
6. **Administrativo:** 2 ações
7. **Sistema de Logs:** 20+ operações auditadas

### **Métricas Técnicas:**
- **Rotas Flask:** 113
- **Funções Python:** 41+ principais
- **Templates Jinja2:** ~40
- **Scripts JS:** 8 especializados
- **Modelos de dados:** 15+ entidades
- **Formulários:** 20+ classes

---

## 🔄 **PROCESSO DE MANUTENÇÃO DESTE DOCUMENTO**

### **Quando Atualizar:**
- ✅ Nova rota criada
- ✅ Nova funcionalidade implementada
- ✅ Template adicionado/modificado
- ✅ API criada/alterada
- ✅ Mudança de permissões
- ✅ Alteração de estrutura de menu

### **Como Atualizar:**
1. Localizar a seção correspondente
2. Adicionar nova entrada com rota, função e linha de código
3. Atualizar estatísticas se necessário
4. Atualizar data de modificação no cabeçalho

### **Responsabilidade:**
- Desenvolvedores devem atualizar após cada alteração significativa
- Revisão quinzenal para garantir completude
- Versionamento alinhado com releases do sistema

---

**📝 Nota:** Este documento é vivo e deve ser atualizado sempre que houver modificações no sistema. Manter sempre sincronizado com o código atual.
