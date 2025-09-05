import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


def import_from_sqlite_to_postgres(sqlite_path: str = 'backups/database.db', pg_url_env: str = 'DATABASE_URL') -> None:
    """Importa dados de categoria_despesa e despesa do backup SQLite para o PostgreSQL.

    Regras:
    - Mantém os IDs originais
    - Upsert por ID: se existir no Postgres, atualiza; se não existir, insere
    - Insere categorias antes das despesas (respeita FK)
    - Não remove dados no destino
    - Tenta ajustar sequences após inserção (se existirem)
    """

    if not os.path.exists(sqlite_path):
        raise FileNotFoundError(f"Backup SQLite não encontrado em {sqlite_path}")

    pg_url = os.getenv(pg_url_env)
    if not pg_url:
        raise RuntimeError("DATABASE_URL não configurada. Defina a variável de ambiente com a URL do Postgres.")

    sqlite_engine = create_engine(
        f'sqlite:///{sqlite_path}',
        connect_args={'check_same_thread': False, 'timeout': 30}
    )
    pg_engine = create_engine(pg_url)

    SQLiteSession = sessionmaker(bind=sqlite_engine)
    PGSession = sessionmaker(bind=pg_engine)

    sqlite_session = SQLiteSession()
    pg_session = PGSession()

    try:
        # --- Categorias de Despesa ---
        categorias = sqlite_session.execute(
            text("SELECT id_categoria_despesa, nome FROM categoria_despesa")
        ).fetchall()

        for id_cat, nome in categorias:
            existente = pg_session.execute(
                text("SELECT 1 FROM categoria_despesa WHERE id_categoria_despesa = :id"),
                {"id": id_cat}
            ).scalar()

            if existente is None:
                pg_session.execute(
                    text("INSERT INTO categoria_despesa (id_categoria_despesa, nome) VALUES (:id, :nome)"),
                    {"id": id_cat, "nome": nome}
                )
            else:
                pg_session.execute(
                    text("UPDATE categoria_despesa SET nome = :nome WHERE id_categoria_despesa = :id"),
                    {"id": id_cat, "nome": nome}
                )

        # --- Despesas ---
        despesas = sqlite_session.execute(text(
            """
            SELECT id_despesa, nome, id_categoria_despesa, id_tipo_despesa,
                   valor_medio_despesa, flag_alimentacao, flag_combustivel
            FROM despesa
            """
        )).fetchall()

        for (
            id_despesa, nome, id_categoria_despesa, id_tipo_despesa,
            valor_medio_despesa, flag_alimentacao, flag_combustivel
        ) in despesas:

            existente = pg_session.execute(
                text("SELECT 1 FROM despesa WHERE id_despesa = :id"),
                {"id": id_despesa}
            ).scalar()

            params = {
                "id": id_despesa,
                "nome": nome,
                "id_categoria_despesa": id_categoria_despesa,
                "id_tipo_despesa": id_tipo_despesa,
                "valor_medio_despesa": valor_medio_despesa,
                "flag_alimentacao": bool(flag_alimentacao) if flag_alimentacao is not None else False,
                "flag_combustivel": bool(flag_combustivel) if flag_combustivel is not None else False,
            }

            if existente is None:
                pg_session.execute(text(
                    """
                    INSERT INTO despesa (
                        id_despesa, nome, id_categoria_despesa, id_tipo_despesa,
                        valor_medio_despesa, flag_alimentacao, flag_combustivel
                    ) VALUES (
                        :id, :nome, :id_categoria_despesa, :id_tipo_despesa,
                        :valor_medio_despesa, :flag_alimentacao, :flag_combustivel
                    )
                    """
                ), params)
            else:
                pg_session.execute(text(
                    """
                    UPDATE despesa SET
                        nome = :nome,
                        id_categoria_despesa = :id_categoria_despesa,
                        id_tipo_despesa = :id_tipo_despesa,
                        valor_medio_despesa = :valor_medio_despesa,
                        flag_alimentacao = :flag_alimentacao,
                        flag_combustivel = :flag_combustivel
                    WHERE id_despesa = :id
                    """
                ), params)

        pg_session.commit()

        # --- Ajuste de sequences (PostgreSQL) ---
        try:
            pg_session.execute(text(
                """
                SELECT setval(
                    pg_get_serial_sequence('categoria_despesa','id_categoria_despesa'),
                    COALESCE((SELECT MAX(id_categoria_despesa) FROM categoria_despesa), 1),
                    true
                );
                """
            ))
            pg_session.execute(text(
                """
                SELECT setval(
                    pg_get_serial_sequence('despesa','id_despesa'),
                    COALESCE((SELECT MAX(id_despesa) FROM despesa), 1),
                    true
                );
                """
            ))
            pg_session.commit()
        except Exception:
            # Se não houver sequences (por ex. PKs não são serial/identity), apenas ignora
            pg_session.rollback()

        # --- Relatório simples ---
        cat_count_pg = pg_session.execute(text("SELECT COUNT(1) FROM categoria_despesa")).scalar() or 0
        desp_count_pg = pg_session.execute(text("SELECT COUNT(1) FROM despesa")).scalar() or 0
        print(f"Importação concluída. Categorias: {cat_count_pg}, Despesas: {desp_count_pg}")

    finally:
        sqlite_session.close()
        pg_session.close()


if __name__ == '__main__':
    import_from_sqlite_to_postgres()


