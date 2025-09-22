import os 
import sys 
if not (os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT')): 
    sys.exit(0) 
if os.path.exists('/tmp/migration_fixed'): 
    sys.exit(0) 
try: 
    from app import app 
    from extensions import db 
    with app.app_context(): 
        try: 
            result = db.session.execute(db.text("DELETE FROM alembic_version")) 
            db.session.commit() 
            print(f"[RAILWAY] Removidos {result.rowcount} registros") 
            with open('/tmp/migration_fixed', 'w') as f: 
                f.write('done') 
        except Exception as e: 
            if "does not exist" in str(e): 
                with open('/tmp/migration_fixed', 'w') as f: 
                    f.write('done') 
            else: 
                sys.exit(1) 
except Exception as e: 
    sys.exit(1) 
