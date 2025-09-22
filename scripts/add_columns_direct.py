import psycopg2
import sys

def add_columns():
    try:
        # Conectar ao banco PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            database="socrates_online",
            user="postgres",
            password="postgres"
        )
        
        cursor = conn.cursor()
        
        # Adicionar colunas
        print("Adicionando coluna valor_pago_socrates na tabela despesas_evento...")
        cursor.execute("ALTER TABLE despesas_evento ADD COLUMN IF NOT EXISTS valor_pago_socrates FLOAT;")
        
        print("Adicionando coluna valor_pago_socrates na tabela despesas_empresa...")
        cursor.execute("ALTER TABLE despesas_empresa ADD COLUMN IF NOT EXISTS valor_pago_socrates FLOAT;")
        
        # Confirmar alterações
        conn.commit()
        
        print("✅ Colunas adicionadas com sucesso!")
        
        # Verificar se as colunas foram criadas
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'despesas_evento' 
            AND column_name = 'valor_pago_socrates';
        """)
        result1 = cursor.fetchone()
        
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'despesas_empresa' 
            AND column_name = 'valor_pago_socrates';
        """)
        result2 = cursor.fetchone()
        
        if result1 and result2:
            print("✅ Verificação: Ambas as colunas foram criadas corretamente!")
        else:
            print("⚠️ Aviso: Nem todas as colunas foram encontradas na verificação")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao adicionar colunas: {e}")
        sys.exit(1)

if __name__ == "__main__":
    add_columns()



