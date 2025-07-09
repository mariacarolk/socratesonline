from app import app, db
from models import Despesa

with app.app_context():
    # Deletar as despesas que foram criadas automaticamente
    despesas_criadas = Despesa.query.filter(
        Despesa.nome.like('Despesa Fixa -%') | 
        Despesa.nome.like('Despesa Variável -%')
    ).all()
    
    print(f'Encontradas {len(despesas_criadas)} despesas para deletar:')
    for despesa in despesas_criadas:
        print(f'- {despesa.nome}')
        db.session.delete(despesa)
    
    if despesas_criadas:
        db.session.commit()
        print('Despesas criadas automaticamente foram removidas.')
    else:
        print('Nenhuma despesa para remover.') 