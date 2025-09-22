from app import app
from models import *

with app.app_context():
    print("=== CATEGORIAS ===")
    categorias = CategoriaDespesa.query.all()[:5]
    for c in categorias:
        print(f"ID: {c.id_categoria_despesa}, Nome: {c.nome}")
    
    print("\n=== DESPESAS ===")
    despesas = Despesa.query.limit(10).all()
    for d in despesas:
        print(f"ID: {d.id_despesa}, Nome: {d.nome}, Categoria: {d.id_categoria_despesa}")
    
    print(f"\n=== TESTE API CATEGORIA 1 ===")
    if categorias:
        categoria_id = categorias[0].id_categoria_despesa
        despesas_categoria = Despesa.query.filter_by(id_categoria_despesa=categoria_id).filter(
            Despesa.id_tipo_despesa.in_([1, 2])
        ).all()
        print(f"Despesas da categoria {categoria_id}: {len(despesas_categoria)}")
        for d in despesas_categoria:
            print(f"  - {d.nome} (tipo: {d.id_tipo_despesa})")

