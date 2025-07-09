# 🎯 GUIA SIMPLIFICADO PARA O CLIENTE - SOCRATES ONLINE

## 📋 O QUE VOCÊ PRECISA PARA COLOCAR NA WEB

### **PASSO 1: CONTRATAR SERVIDOR**
Recomendações de provedores:
- **DigitalOcean**: Droplet de $20/mês (4GB RAM, 2 vCPUs)
- **AWS**: EC2 t3.medium (similar)
- **Vultr**: VPS de $20/mês
- **Linode**: Nanode de $20/mês

**Especificações mínimas:**
- Ubuntu 20.04 LTS
- 4GB RAM
- 2 vCPUs  
- 80GB SSD
- IP fixo

### **PASSO 2: REGISTRAR DOMÍNIO**
- Registre um domínio (.com.br, .com, etc.)
- Configure DNS para apontar para o IP do servidor
- Registros necessários:
  - `A` para `seudominio.com.br` → IP do servidor
  - `A` para `www.seudominio.com.br` → IP do servidor

### **PASSO 3: EXECUTAR DEPLOY AUTOMÁTICO**

1. **Conectar no servidor:**
```bash
ssh root@SEU_IP_SERVIDOR
```

2. **Criar usuário para aplicação:**
```bash
adduser socrates
usermod -aG sudo socrates
su - socrates
```

3. **Fazer download do projeto:**
```bash
git clone https://github.com/SEU_USUARIO/socrates_online.git
cd socrates_online
```

4. **Editar configurações no script:**
```bash
nano deploy/complete-deploy-script.sh
```
Altere estas linhas no início do arquivo:
```bash
DOMAIN="seudominio.com.br"          # SEU DOMÍNIO AQUI
DB_PASSWORD="sua_senha_123"         # SUA SENHA DO BANCO
ADMIN_EMAIL="admin@seudominio.com.br" # SEU EMAIL
```

5. **Executar deploy automático:**
```bash
chmod +x deploy/complete-deploy-script.sh
bash deploy/complete-deploy-script.sh
```

6. **Aguardar conclusão (15-30 minutos)**

### **PASSO 4: VERIFICAR SE FUNCIONOU**

Acesse: `https://seudominio.com.br`

Se funcionar, você verá a tela de login do Socrates Online!

## 💰 CUSTOS ESTIMADOS (MENSAL)

| Item | Custo |
|------|-------|
| Servidor VPS | R$ 100-200 |
| Domínio .com.br | R$ 8-15 (anual) |
| SSL Certificate | Gratuito (Let's Encrypt) |
| **TOTAL** | **~R$ 110-220/mês** |

## 🛠️ MANUTENÇÃO BÁSICA

### **Comandos Essenciais:**

**Ver se a aplicação está funcionando:**
```bash
sudo supervisorctl status socrates
```

**Reiniciar aplicação:**
```bash
sudo supervisorctl restart socrates
```

**Ver logs de erro:**
```bash
sudo tail -f /home/socrates/socrates_online/logs/supervisor.log
```

**Verificar espaço em disco:**
```bash
df -h
```

**Backup manual:**
```bash
/home/socrates/socrates_online/backup.sh
```

### **Atualizações do Sistema:**
Execute mensalmente:
```bash
sudo apt update && sudo apt upgrade -y
sudo reboot
```

## 🚨 PROBLEMAS COMUNS E SOLUÇÕES

### **Aplicação não carrega:**
```bash
# Verificar status
sudo supervisorctl status socrates
sudo systemctl status nginx

# Reiniciar tudo
sudo supervisorctl restart socrates
sudo systemctl restart nginx
```

### **Erro 502 Bad Gateway:**
```bash
# Verificar logs
sudo tail -f /var/log/nginx/socrates_error.log
sudo tail -f /home/socrates/socrates_online/logs/supervisor.log

# Reiniciar aplicação
sudo supervisorctl restart socrates
```

### **Disco cheio:**
```bash
# Verificar espaço
df -h

# Limpar logs antigos
sudo find /var/log -name "*.log" -type f -mtime +30 -delete

# Limpar backups antigos
find /home/socrates/backups -type f -mtime +30 -delete
```

### **Site lento:**
```bash
# Verificar uso de recursos
htop

# Reiniciar aplicação
sudo supervisorctl restart socrates
```

## 📞 SUPORTE TÉCNICO

Se algo der errado:

1. **Anote a mensagem de erro completa**
2. **Verifique os logs:**
   ```bash
   sudo tail -100 /home/socrates/socrates_online/logs/supervisor.log
   ```
3. **Entre em contato com suporte técnico**

## ✅ CHECKLIST DE VERIFICAÇÃO

- [ ] Servidor contratado e configurado
- [ ] Domínio registrado e DNS configurado
- [ ] Deploy executado com sucesso
- [ ] Site acessível via HTTPS
- [ ] Login funcionando
- [ ] Upload de arquivos funcionando
- [ ] Backup automático configurado
- [ ] Firewall ativo
- [ ] SSL válido

## 🎉 PRONTO!

Sua aplicação Socrates Online está no ar e funcionando!

**Próximos passos:**
1. Criar primeiro usuário administrativo
2. Configurar categorias básicas
3. Treinar usuários
4. Configurar backup externo (opcional)

---

💡 **Dica:** Mantenha este documento salvo para consultas futuras! 