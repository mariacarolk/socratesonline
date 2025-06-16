import sqlite3

def fix_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Remover coluna documento da tabela receitas_evento
    try:
        cursor.execute('''
            CREATE TABLE receitas_evento_temp (
                id_receita_evento INTEGER PRIMARY KEY,
                id_evento INTEGER NOT NULL,
                id_receita INTEGER NOT NULL,
                data DATE NOT NULL,
                valor FLOAT NOT NULL,
                observacoes TEXT,
                FOREIGN KEY (id_evento) REFERENCES evento (id_evento),
                FOREIGN KEY (id_receita) REFERENCES receita (id_receita)
            )
        ''')
        
        cursor.execute('''
            INSERT INTO receitas_evento_temp 
            SELECT id_receita_evento, id_evento, id_receita, data, valor, observacoes 
            FROM receitas_evento
        ''')
        
        cursor.execute('DROP TABLE receitas_evento')
        cursor.execute('ALTER TABLE receitas_evento_temp RENAME TO receitas_evento')
        print("✅ Coluna 'documento' removida da tabela receitas_evento")
    except sqlite3.OperationalError as e:
        print(f"ℹ️ Tabela receitas_evento não existe ou já está correta: {e}")
    
    # Remover coluna documento da tabela despesas_evento
    try:
        cursor.execute('''
            CREATE TABLE despesas_evento_temp (
                id_despesa_evento INTEGER PRIMARY KEY,
                id_evento INTEGER NOT NULL,
                id_despesa INTEGER NOT NULL,
                data DATE NOT NULL,
                valor FLOAT NOT NULL,
                id_fornecedor INTEGER,
                status_pagamento VARCHAR(20) NOT NULL,
                forma_pagamento VARCHAR(20) NOT NULL,
                pago_por VARCHAR(100),
                observacoes TEXT,
                FOREIGN KEY (id_evento) REFERENCES evento (id_evento),
                FOREIGN KEY (id_despesa) REFERENCES despesa (id_despesa),
                FOREIGN KEY (id_fornecedor) REFERENCES fornecedor (id_fornecedor)
            )
        ''')
        
        cursor.execute('''
            INSERT INTO despesas_evento_temp 
            SELECT id_despesa_evento, id_evento, id_despesa, data, valor, id_fornecedor, 
                   status_pagamento, forma_pagamento, pago_por, observacoes 
            FROM despesas_evento
        ''')
        
        cursor.execute('DROP TABLE despesas_evento')
        cursor.execute('ALTER TABLE despesas_evento_temp RENAME TO despesas_evento')
        print("✅ Coluna 'documento' removida da tabela despesas_evento")
    except sqlite3.OperationalError as e:
        print(f"ℹ️ Tabela despesas_evento não existe ou já está correta: {e}")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    fix_database() 