# 🎭 Sócrates Online - Sistema de Gestão Circense

## 📋 Estrutura do Projeto

```
socrates_online/
├── app.py                 # Aplicação principal Flask
├── models.py              # Modelos do banco de dados
├── forms.py               # Formulários WTF
├── config.py              # Configurações
├── extensions.py          # Extensões Flask
├── requirements.txt       # Dependências Python
├── nova_migracao.bat     # Script para novas migrações
├── railway.json          # Configuração Railway
│
├── railway/              # Arquivos específicos do Railway
├── deployment/           # Documentação de deploy
├── temp_cleanup/         # Arquivos temporários/correções
├── docs/                # Documentação completa
│   └── migrations/      # Docs específicas de migração
├── scripts/             # Scripts utilitários
├── static/              # CSS, JS, imagens
├── templates/           # Templates HTML
├── migrations/          # Migrações do banco
├── uploads/             # Arquivos enviados
└── venv/               # Ambiente virtual Python
```

## 🚀 Como Usar

### Para Alterações no Banco de Dados:
1. Altere `models.py`
2. Execute `nova_migracao.bat`
3. Faça `git push origin main`
4. Railway aplica automaticamente!

### Para Deploy:
- Railway está configurado para aplicar migrações automaticamente
- Monitore logs no Railway Dashboard

## 📚 Documentação

- **Migrações:** `docs/migrations/REGRAS_MIGRACOES.md`
- **Deploy:** `deployment/INSTRUCOES_FINAIS.md`
- **Geral:** `docs/README.md`

## 🛠️ Tecnologias

- Python 3.12
- Flask 3.1.2
- PostgreSQL
- Railway (Deploy)
- Bootstrap (Frontend)
