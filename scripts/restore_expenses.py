import os
import csv
from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker


def backup_table_to_csv(engine, table_name: str, out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)
    with engine.connect() as conn:
        rows = conn.execute(select(table)).mappings().all()
    if not rows:
        return
    out_path = os.path.join(out_dir, f"{table_name}.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    # Source (SQLite backup)
    sqlite_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance", "database.db")
    if not os.path.exists(sqlite_path):
        raise FileNotFoundError(f"Backup SQLite not found at {sqlite_path}")
    src_engine = create_engine(f"sqlite:///{sqlite_path}")

    # Target (current app DB)
    database_url = os.environ.get("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/socrates_online"
    dst_engine = create_engine(database_url)
    DstSession = sessionmaker(bind=dst_engine)
    dst_session = DstSession()

    # Reflect source tables
    src_meta = MetaData()
    categoria_src = Table("categoria_despesa", src_meta, autoload_with=src_engine)
    despesa_src = Table("despesa", src_meta, autoload_with=src_engine)

    # Reflect destination tables
    dst_meta = MetaData()
    categoria_dst = Table("categoria_despesa", dst_meta, autoload_with=dst_engine)
    despesa_dst = Table("despesa", dst_meta, autoload_with=dst_engine)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backups", f"pre_restore_{timestamp}")

    # Backup current destination data
    for table_name in ["categoria_despesa", "despesa"]:
        backup_table_to_csv(dst_engine, table_name, backup_dir)

    # Load existing destination name->id maps
    with dst_engine.connect() as conn:
        existing_cats = {
            row["nome"].strip().lower(): row["id_categoria_despesa"]
            for row in conn.execute(select(categoria_dst)).mappings()
        }
        existing_despesas = {
            (row["nome"].strip().lower(), row["id_categoria_despesa"]): row["id_despesa"]
            for row in conn.execute(select(despesa_dst)).mappings()
        }

    # Import categories (upsert by nome)
    cat_name_to_id = dict(existing_cats)
    with src_engine.connect() as src_conn, dst_engine.begin() as dst_conn:
        for src_row in src_conn.execute(select(categoria_src)).mappings():
            nome = (src_row["nome"] or "").strip()
            if not nome:
                continue
            key = nome.lower()
            if key in cat_name_to_id:
                continue  # already exists
            ins = categoria_dst.insert().values(nome=nome)
            res = dst_conn.execute(ins)
            # PostgreSQL returns nothing; fetch id
            new_id = dst_conn.execute(select(categoria_dst.c.id_categoria_despesa).where(categoria_dst.c.nome == nome)).scalar_one()
            cat_name_to_id[key] = new_id

    # Import despesas (upsert by (nome, categoria))
    with src_engine.connect() as src_conn, dst_engine.begin() as dst_conn:
        for src_row in src_conn.execute(select(despesa_src)).mappings():
            nome = (src_row["nome"] or "").strip()
            if not nome:
                continue
            src_cat_id = src_row.get("id_categoria_despesa")
            # Map category by name from source
            cat_nome = src_conn.execute(
                select(categoria_src.c.nome).where(categoria_src.c.id_categoria_despesa == src_cat_id)
            ).scalar_one_or_none()
            if not cat_nome:
                continue
            dst_cat_id = cat_name_to_id.get(cat_nome.strip().lower())
            if not dst_cat_id:
                # Should not happen; skip to be safe
                continue

            key = (nome.lower(), dst_cat_id)
            if key in existing_despesas:
                continue  # already exists

            ins = despesa_dst.insert().values(
                nome=nome,
                id_categoria_despesa=dst_cat_id,
                id_tipo_despesa=src_row.get("id_tipo_despesa", 1),
                valor_medio_despesa=src_row.get("valor_medio_despesa"),
                flag_alimentacao=src_row.get("flag_alimentacao", False),
                flag_combustivel=src_row.get("flag_combustivel", False),
            )
            dst_conn.execute(ins)

    dst_session.close()
    print("Restore completed successfully.")


if __name__ == "__main__":
    main()


