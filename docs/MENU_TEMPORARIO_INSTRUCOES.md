# Instruções para Reverter Ocultação Temporária do Menu

## O que foi feito

Foi implementada uma ocultação temporária dos seguintes itens de menu para usuários que não sejam `root@socratesonline.com`:

- **Dashboard**
- **Eventos** 
- **Gestão Financeira Empresa** (submenu completo)
- **Relatórios** (submenu completo)

**IMPORTANTE**: O usuário `root@socratesonline.com` tem acesso total e irrestrito a TODOS os menus, independente da categoria administrativa.

## Arquivos modificados

- `templates/base.html` - linhas 49-50 e demais seções comentadas
- `templates/marketing_dashboard.html` - botões de envio desativados temporariamente

## Como reverter (quando necessário)

### 1. Remover a variável temporária

No arquivo `templates/base.html`, **remover as linhas 49-50**:
```jinja2
{# TEMPORÁRIO: Ocultar menu para usuários não-root - REMOVER FUTURAMENTE #}
{% set is_root_user = session['email'] == 'root@socratesonline.com' %}
```

### 2. Reverter Dashboard (linhas 52-57)

**Substituir:**
```jinja2
{# Dashboard - oculto temporariamente para não-root #}
{% if is_root_user %}
<a class="nav-link {% if request.endpoint == 'dashboard' %}active{% endif %}" href="{{ url_for('dashboard') }}">
    <i class="bi bi-speedometer2"></i> Dashboard
</a>
{% endif %}
```

**Por:**
```jinja2
<a class="nav-link {% if request.endpoint == 'dashboard' %}active{% endif %}" href="{{ url_for('dashboard') }}">
    <i class="bi bi-speedometer2"></i> Dashboard
</a>
```

### 3. Reverter Eventos (linhas 59-64)

**Substituir:**
```jinja2
{# Eventos - oculto temporariamente para não-root #}
{% if is_root_user %}
<a class="nav-link {% if request.endpoint == 'listar_eventos' %}active{% endif %}" href="{{ url_for('listar_eventos') }}">
    <i class="bi bi-calendar-event"></i> Eventos
</a>
{% endif %}
```

**Por:**
```jinja2
<a class="nav-link {% if request.endpoint == 'listar_eventos' %}active{% endif %}" href="{{ url_for('listar_eventos') }}">
    <i class="bi bi-calendar-event"></i> Eventos
</a>
```

### 4. Reverter Cadastros (linha 67)

**Substituir:**
```jinja2
{% if categoria == 'administrativo' or is_root_user %}
```

**Por:**
```jinja2
{% if categoria == 'administrativo' %}
```

### 5. Reverter Gestão Financeira Empresa (linha 123)

**Substituir:**
```jinja2
{% if is_root_user %}
```

**Por:**
```jinja2
{% if session['categoria'] == 'administrativo' %}
```

### 6. Reverter Relatórios (linha 144)

**Substituir:**
```jinja2
{% if is_root_user %}
```

**Por:**
```jinja2
{% if session['categoria'] == 'administrativo' %}
```

### 7. Reverter Administrativo (linha 199)

**Substituir:**
```jinja2
{% if session['categoria'] == 'administrativo' or is_root_user %}
```

**Por:**
```jinja2
{% if session['categoria'] == 'administrativo' %}
```

### 8. Remover comentários temporários

Remover todos os comentários que começam com:
- `{# Dashboard - oculto temporariamente para não-root #}`
- `{# Eventos - oculto temporariamente para não-root #}`
- `{# Gestão Financeira Empresa - oculto temporariamente para não-root #}`
- `{# Relatórios - oculto temporariamente para não-root #}`

## Dashboard de Marketing - Botões desativados temporariamente

**Arquivo:** `templates/marketing_dashboard.html`

**Botões desativados:**
- Botão "Enviar E-mails Pendentes" (linhas 92-102)
- Botão "Enviar WhatsApp Pendentes" (linhas 125-135)

**Para reativar:**
- Remover o botão desativado e descomentar o código original que está comentado em cada seção.

## Menu Cadastros - Liberação parcial

**Modificação:** O menu Cadastros agora está liberado para usuários administrativos, mas apenas com:
- ✅ **Colaboradores** (liberado para todos administrativos)
- ✅ **Categorias Colaboradores** (liberado para todos administrativos)
- 🔒 **Demais cadastros** (apenas para root@socratesonline.com)

**Para liberar todos os cadastros para administrativos:**
- Remover a condição `{% if is_root_user %}` na linha 83 do `templates/base.html`
- Remover o `{% endif %}` correspondente na linha 117

## Status atual dos menus por tipo de usuário

### 👑 root@socratesonline.com (ACESSO TOTAL E IRRESTRITO)
- ✅ **Dashboard**
- ✅ **Eventos**
- ✅ **Cadastros** (completo)
- ✅ **Gestão Financeira Empresa** (completo)
- ✅ **Relatórios** (completo)
- ✅ **Marketing** (completo)
- ✅ **Administrativo**

### 👨‍💼 Usuário administrativo (não-root)
- ✅ **Marketing** (completo)
- ✅ **Cadastros** (apenas Colaboradores e Categorias)
- ✅ **Administrativo**
- 🔒 **Dashboard** (oculto temporariamente)
- 🔒 **Eventos** (oculto temporariamente)
- 🔒 **Gestão Financeira Empresa** (oculto temporariamente)
- 🔒 **Relatórios** (oculto temporariamente)

### 📈 Promotor de vendas
- ✅ **Marketing** (completo)
- 🔒 **Todos os demais menus** (ocultos)

## Resumo das mudanças

**IMPORTANTE**: O usuário `root@socratesonline.com` sempre terá acesso total, independente da categoria no sistema. Isso garante que o administrador principal sempre possa acessar todas as funcionalidades.

Todas as modificações estão claramente marcadas com comentários "TEMPORÁRIO", facilitando a identificação e reversão futura.

O sistema de permissões original permanece intacto, apenas foram adicionadas verificações adicionais temporárias baseadas no email do usuário root.