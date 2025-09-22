#!/usr/bin/env python
# Script executado antes do app no Railway
import os
import subprocess
import sys

print("=" * 60)
print(" RAILWAY DEPLOYMENT - MIGRATIONS CHECK")
print("=" * 60)

# Configurar ambiente
os.environ['FLASK_APP'] = 'app.py'

# Verificar migração atual
try:
    result = subprocess.run(['flask', 'db', 'current'], capture_output=True, text=True)
    print("Current migration:", result.stdout)
except Exception as e:
    print(f"Error checking current migration: {e}")

# Aplicar migrações
print("\nApplying migrations...")
try:
    result = subprocess.run(['flask', 'db', 'upgrade'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Migrations applied successfully")
        print(result.stdout)
    else:
        print("❌ Migration failed:")
        print(result.stderr)
        sys.exit(1)
except Exception as e:
    print(f"Error applying migrations: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print(" MIGRATIONS COMPLETE - STARTING APP")
print("=" * 60)
