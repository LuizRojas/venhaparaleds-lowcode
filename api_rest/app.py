# api_rest/app.py

from flask import Flask, jsonify, request
import psycopg2
import os
import json

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('POSTGRES_DB', 'processo_seletivo_app')
DB_USER = os.getenv('POSTGRES_USER', 'admin')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'Anyplace5-Augmented3-Crop3')
DB_PORT = os.getenv('DB_PORT', '5432')

def get_db_connection():
    """Estabelece e retorna uma conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

@app.route('/')
def home():
    """Endpoint de teste simples para verificar se a API está funcionando."""
    return jsonify({"message": "API de Concursos e Candidatos está online!"})

@app.route('/concursos/by_cpf/<string:cpf>', methods=['GET'])
def get_concursos_by_cpf(cpf):
    """
    Lista os órgãos, códigos e editais dos concursos públicos que se encaixam
    no perfil do candidato, tomando como base o seu CPF.
    O "encaixe no perfil" é definido pela correspondência entre as profissões
    do candidato e as vagas do concurso.
    """
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Não foi possível conectar ao banco de dados."}), 500

        cur = conn.cursor()
        cpf_limpo = cpf.replace('.', '').replace('-', '')

        query = """
            SELECT
                CO.orgao,
                CO.edital,
                CO.codigo_concurso
            FROM
                Candidatos C
            JOIN
                Concursos CO ON TRUE -- JOIN inicial para permitir a comparação posterior
            WHERE
                C.cpf = %s
                AND EXISTS (
                    SELECT 1
                    FROM jsonb_array_elements_text(C.profissoes) AS p_candidato
                    JOIN jsonb_array_elements_text(CO.lista_vagas) AS v_concurso
                    ON p_candidato = v_concurso
                )
            ORDER BY
                CO.edital DESC;
        """
        cur.execute(query, (cpf_limpo,))
        concursos = cur.fetchall()

       # json
        results = []
        for concurso in concursos:
            results.append({
                "orgao": concurso[0],
                "edital": concurso[1],
                "codigo_concurso": concurso[2]
            })

        cur.close()
        return jsonify(results), 200

    except psycopg2.Error as e:
        print(f"Erro no banco de dados ao buscar concursos por CPF: {e}")
        return jsonify({"error": "Erro interno do servidor ao processar a requisição.", "details": str(e)}), 500
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return jsonify({"error": "Erro inesperado do servidor.", "details": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/candidatos/by_codigo_concurso/<string:codigo_concurso>', methods=['GET'])
def get_candidatos_by_codigo_concurso(codigo_concurso):
    """
    Lista o nome, data de nascimento e o CPF dos candidatos que se encaixam
    no perfil do concurso, tomando como base o Código do Concurso.
    O "encaixe no perfil" é definido pela correspondência entre as vagas
    do concurso e as profissões do candidato.
    """
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Não foi possível conectar ao banco de dados."}), 500

        cur = conn.cursor()

        # buscar candidatos por código de concurso com logica de encaixe no perfil (mesma do appsmith)
        query = """
            SELECT
                C.nome,
                C.data_nascimento,
                C.cpf
            FROM
                Concursos CO
            JOIN
                Candidatos C ON TRUE -- JOIN inicial
            WHERE
                CO.codigo_concurso = %s
                AND EXISTS (
                    SELECT 1
                    FROM jsonb_array_elements_text(CO.lista_vagas) AS v_concurso
                    JOIN jsonb_array_elements_text(C.profissoes) AS p_candidato
                    ON v_concurso = p_candidato
                )
            ORDER BY
                C.nome ASC;
        """
        cur.execute(query, (codigo_concurso,))
        candidatos = cur.fetchall()

        # Formata os resultados para JSON
        results = []
        for candidato in candidatos:
            results.append({
                "nome": candidato[0],
                "data_nascimento": candidato[1].strftime('%d/%m/%Y') if candidato[1] else None, # Formata a data
                "cpf": candidato[2]
            })

        cur.close()
        return jsonify(results), 200

    except psycopg2.Error as e:
        print(f"Erro no banco de dados ao buscar candidatos por código de concurso: {e}")
        return jsonify({"error": "Erro interno do servidor ao processar a requisição.", "details": str(e)}), 500
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return jsonify({"error": "Erro inesperado do servidor.", "details": str(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # rodando via Gunicorn no Docker, este bloco não será executado.
    # somente testes locais fora do Docker.
    app.run(host='0.0.0.0', port=5000, debug=True)
