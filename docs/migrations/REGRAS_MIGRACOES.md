# 📋 REGRAS DE MIGRAÇÃO - SÓCRATES ONLINE

## 🚨 REGRAS OBRIGATÓRIAS PARA ALTERAÇÕES NO BANCO

### ❌ NUNCA FAZER:
- `flask db migrate` manualmente
- `flask db upgrade` manualmente  
- Alterar arquivos em `migrations/versions/` diretamente
- Deploy sem testar migrações localmente
- Ignorar erros de migração

### ✅ SEMPRE FAZER:

#### Para Novas Alterações no Banco:
1. **Alterar `models.py`** com as mudanças necessárias
2. **Executar `nova_migracao.bat`** (nunca comandos manuais)
3. **Testar localmente** se tudo funciona
4. **Fazer deploy:** `git add . && git commit -m "migration: descrição" && git push`
5. **Monitorar logs** no Railway Dashboard

#### Fluxo Automatizado:
```
models.py → nova_migracao.bat → git push → Railway aplica automaticamente
```

### 🔧 SCRIPTS DISPONÍVEIS:

- **`nova_migracao.bat`** - Para todas as futuras alterações no banco
- **`railway_auto_fix.py`** - Correção automática no Railway (já configurado)
- **`restore_railway.py`** - Restaurar configuração permanente (usar apenas uma vez)

### 🚂 CONFIGURAÇÃO RAILWAY:

O Railway está configurado para:
- Executar `flask db upgrade` automaticamente antes de iniciar o app
- Aplicar todas as migrações pendentes sem intervenção manual
- Reiniciar automaticamente em caso de falha

### 📊 MONITORAMENTO:

Sempre verificar após deploy:
1. **Logs do Railway Dashboard** - confirmar que migrações foram aplicadas
2. **Status da aplicação** - verificar se iniciou normalmente
3. **Funcionalidades afetadas** - testar as mudanças implementadas

### 🆘 EM CASO DE PROBLEMAS:

1. **Verificar logs detalhados** no Railway
2. **Consultar `INSTRUCOES_FINAIS.md`** para troubleshooting
3. **Nunca reverter manualmente** - usar os scripts apropriados
4. **Fazer backup** antes de correções complexas

### 🎯 LEMBRETE:

**O sistema está COMPLETAMENTE AUTOMATIZADO!** 
- Siga apenas o fluxo: `models.py` → `nova_migracao.bat` → `git push`
- Railway faz todo o resto automaticamente
- Nunca mais problemas de migração se seguir estas regras!
