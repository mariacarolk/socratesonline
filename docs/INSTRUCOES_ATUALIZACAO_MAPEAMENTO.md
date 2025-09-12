# 📋 INSTRUÇÕES PARA MANUTENÇÃO DO MAPEAMENTO DO SISTEMA

## 🎯 Objetivo
Manter o documento `MAPEAMENTO_COMPLETO_SISTEMA.md` sempre atualizado com todas as mudanças no sistema Sócrates Online.

---

## 🔄 QUANDO ATUALIZAR O MAPEAMENTO

### ✅ Situações que REQUEREM atualização:

1. **Nova Rota Criada**
   - Qualquer novo `@app.route` adicionado
   - Nova API endpoint
   - Nova funcionalidade acessível via URL

2. **Nova Funcionalidade**
   - Novo formulário ou tela
   - Nova ação (CRUD)
   - Novo relatório

3. **Alteração de Menu**
   - Item adicionado/removido do menu
   - Mudança de permissões de acesso
   - Reorganização da navegação

4. **Novo Template**
   - Arquivo `.html` criado
   - Template modificado significativamente

5. **Nova API ou Endpoint**
   - APIs de integração
   - Endpoints AJAX
   - Serviços internos

6. **Mudança de Permissões**
   - Alteração de controle de acesso
   - Nova categoria de usuário
   - Modificação de privilégios

---

## 🛠️ COMO ATUALIZAR

### **Método 1: Atualização Automática (Recomendado)**

```powershell
# Navegar para o diretório do projeto
cd "C:\Users\comer\Desktop\Python - Projects\socrates_online"

# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Executar script de atualização
python scripts/atualizar_mapeamento.py
```

**O script irá:**
- ✅ Atualizar automaticamente data e estatísticas
- ✅ Detectar inconsistências
- ✅ Sugerir ações corretivas

### **Método 2: Atualização Manual**

1. **Abrir o arquivo:** `docs/MAPEAMENTO_COMPLETO_SISTEMA.md`

2. **Localizar a seção apropriada** (Dashboard, Eventos, Cadastros, etc.)

3. **Adicionar nova entrada** seguindo o padrão:
   ```markdown
   ### **X. Nome da Nova Funcionalidade**
   - **Rota:** `/nova/rota`
   - **Função:** `nova_funcao()` *(Linha XXXX)*
   - **Template:** `novo_template.html`
   - **Ações:**
     - Listar/Criar: Função principal
     - Editar: `/nova/rota/editar/<int:id>` *(Linha YYYY)*
     - Excluir: `/nova/rota/excluir/<int:id>` *(Linha ZZZZ)*
   ```

4. **Atualizar estatísticas** no cabeçalho:
   - Data de última atualização
   - Total de rotas
   - Total de templates
   - Contadores por módulo

5. **Verificar links internos** e referências cruzadas

---

## 📝 PADRÃO DE DOCUMENTAÇÃO

### **Estrutura Padrão para Nova Funcionalidade:**

```markdown
### **N. Nome da Funcionalidade** *(Nível de acesso)*
- **Rota:** `/caminho/da/rota`
- **Função:** `nome_da_funcao()` *(Linha número)*
- **Template:** `nome_template.html`
- **Ações:**
  - Descrição da ação principal
  - Editar: rota *(linha)*
  - Excluir: rota *(linha)*
  - Outras ações específicas
```

### **Informações Obrigatórias:**
- ✅ Rota completa
- ✅ Nome da função Python
- ✅ Número da linha no `app.py`
- ✅ Template utilizado
- ✅ Nível de acesso (ROOT, Admin, etc.)

### **Informações Opcionais:**
- Descrição das funcionalidades
- APIs relacionadas
- Dependências
- Observações especiais

---

## 🔍 VERIFICAÇÃO DE QUALIDADE

### **Checklist antes de finalizar:**

- [ ] Data atualizada no cabeçalho
- [ ] Estatísticas corretas (rotas, templates, ações)
- [ ] Nova funcionalidade documentada completamente
- [ ] Padrão de formatação mantido
- [ ] Links e referências funcionando
- [ ] Nível de acesso especificado
- [ ] Linha de código conferida

### **Validação automática:**
Execute o script de atualização para detectar inconsistências:
```bash
python scripts/atualizar_mapeamento.py
```

---

## 🚨 REGRAS IMPORTANTES

### **❌ NÃO fazer:**
- Não remover funcionalidades existentes sem justificativa
- Não alterar a estrutura básica do documento
- Não documentar funcionalidades experimentais/temporárias
- Não esquecer de atualizar a data

### **✅ SEMPRE fazer:**
- Manter o padrão de formatação
- Incluir número da linha do código
- Especificar nível de acesso
- Testar links e referências
- Atualizar estatísticas

---

## 📅 CRONOGRAMA DE MANUTENÇÃO

### **Atualização Imediata:**
- Após implementar nova funcionalidade
- Antes de fazer commit no Git
- Antes de deploy em produção

### **Revisão Semanal:**
- Verificar consistência geral
- Validar todas as estatísticas
- Conferir se nada foi esquecido

### **Revisão Mensal:**
- Auditoria completa do documento
- Refatoração se necessário
- Versionamento alinhado com releases

---

## 🔧 FERRAMENTAS DE APOIO

### **Scripts Disponíveis:**
- `scripts/atualizar_mapeamento.py`: Atualização automática
- (Futuro) `scripts/validar_mapeamento.py`: Validação completa

### **Comandos Úteis:**
```bash
# Contar rotas no sistema
grep -c "@app.route" app.py

# Listar templates
ls templates/*.html | wc -l

# Buscar função específica
grep -n "def nome_funcao" app.py
```

---

## 📞 RESPONSABILIDADES

### **Desenvolvedor Principal:**
- Atualizar após cada implementação
- Manter qualidade da documentação
- Resolver inconsistências

### **Equipe de Desenvolvimento:**
- Reportar funcionalidades não documentadas
- Sugerir melhorias no processo
- Validar documentação de suas implementações

### **Revisão:**
- Semanal: Desenvolvedor principal
- Mensal: Equipe completa
- Release: Auditoria completa

---

## 📖 LINKS RELACIONADOS

- [Mapeamento Completo do Sistema](MAPEAMENTO_COMPLETO_SISTEMA.md)
- [Requisitos do Sistema](REQUISITOS_SISTEMA.md)
- [Guia de Deploy](DEPLOY_RAILWAY.md)
- [Documentação de Marketing](MARKETING_FUNCTIONALITY.md)

---

**💡 Lembre-se:** Um mapeamento atualizado é essencial para manutenção eficiente e onboarding de novos desenvolvedores!
