from extensions import db
from models import *
from app import app

with app.app_context():
    print("=== CATEGORIAS DE DESPESA ===")
    cats = CategoriaDespesa.query.all()
    for c in cats:
        print(f"  {c.id_categoria_despesa}: {c.nome}")
    print(f"\nTotal de categorias: {len(cats)}")
    
    print("\n=== TODAS AS DESPESAS ===")
    despesas = Despesa.query.all()
    for d in despesas:
        categoria_nome = d.categoria.nome if d.categoria else "Sem categoria"
        print(f"  {d.id_despesa}: {d.nome} - Categoria: {categoria_nome} - Tipo: {d.tipo_nome}")
    
    print("\n=== DESPESAS DA EMPRESA (TIPOS 3 E 4) ===")
    despesas_empresa = Despesa.query.filter(Despesa.id_tipo_despesa.in_([3, 4])).all()
    for d in despesas_empresa:
        categoria_nome = d.categoria.nome if d.categoria else "Sem categoria"
        print(f"  {d.id_despesa}: {d.nome} - Categoria: {categoria_nome} - Tipo: {d.tipo_nome}")
    print(f"\nTotal de despesas empresa: {len(despesas_empresa)}")
    
    print("\n=== QUERY USADA NO CÓDIGO ===")
    # Esta é a query usada no código da função despesas_empresa
    categorias_com_despesas_empresa = db.session.query(CategoriaDespesa).join(Despesa).filter(
        Despesa.id_tipo_despesa.in_([3, 4])
    ).distinct().all()
    
    print(f"Categorias encontradas pela query: {len(categorias_com_despesas_empresa)}")
    for c in categorias_com_despesas_empresa:
        print(f"  {c.id_categoria_despesa}: {c.nome}") 