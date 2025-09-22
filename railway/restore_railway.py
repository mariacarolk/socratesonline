import json 
import os 
config = { 
    "$schema": "https://railway.app/railway.schema.json", 
    "build": {"builder": "NIXPACKS"}, 
    "deploy": { 
        "startCommand": "flask db upgrade && python app.py", 
        "restartPolicyType": "ON_FAILURE", 
        "restartPolicyMaxRetries": 10, 
        "healthcheckPath": "/", 
        "healthcheckTimeout": 300 
    } 
} 
with open('railway.json', 'w') as f: 
    json.dump(config, f, indent=2) 
print("Railway.json restaurado!") 
for f in ['railway_auto_fix.py', 'railway_backup.json']: 
    if os.path.exists(f): 
        os.remove(f) 
