from flask import Flask, jsonify, request
import psycopg2
import os
import json
from datetime import datetime

app = Flask(__name__)

# variaveis de ambiente do docker
# 'db' é o nome do serviço PostgreSQL no docker-compose
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
                CO.codigo_concurso,
                CO.lista_vagas::text
            FROM
                Candidatos C
            JOIN
                Concursos CO ON TRUE
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

        results = []
        for concurso in concursos:
            try:
                lista_vagas_tratada = json.loads(concurso[3]) if concurso[3] else []
            except json.JSONDecodeError:
                lista_vagas_tratada = []
            results.append({
                "orgao": concurso[0],
                "edital": concurso[1],
                "codigo_concurso": concurso[2],
                "lista_vagas": lista_vagas_tratada
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
    Lista o nome, data de nascimento, CPF e as profissões dos candidatos que se encaixam
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

        query = """
            SELECT
                C.nome,
                C.data_nascimento,
                C.cpf,
                C.profissoes::text
            FROM
                Concursos CO
            JOIN
                Candidatos C ON TRUE
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

        results = []
        for candidato in candidatos:
            try:
                profissoes_tratadas = json.loads(candidato[3]) if candidato[3] else []
            except json.JSONDecodeError:
                profissoes_tratadas = []
            results.append({
                "nome": candidato[0],
                "data_nascimento": candidato[1].strftime('%d/%m/%Y') if candidato[1] else None,
                "cpf": candidato[2],
                "profissoes": profissoes_tratadas
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

@app.route('/concursos', methods=['GET'])
def get_concursos():
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Não foi possível conectar ao banco de dados."}), 500
        
        cur = conn.cursor()

        query = """
            SELECT
                orgao,
                edital,
                codigo_concurso,
                lista_vagas::text
            FROM
                Concursos
            ORDER BY
                edital DESC;
        """

        cur.execute(query)
        concursos = cur.fetchall()

        results = []
        for concurso in concursos:
            try:
                lista_vagas_tratada = json.loads(concurso[3]) if concurso[3] else [] # corrigido o índice para 4
            except json.JSONDecodeError:
                lista_vagas_tratada = []
            results.append({
                "orgao": concurso[0],
                "edital": concurso[1],
                "codigo_concurso": concurso[2],
                "lista_vagas": lista_vagas_tratada
            })

        cur.close()
        return jsonify(results), 200

    except psycopg2.Error as e:
        print(f"Erro no banco de dados ao buscar todos concursos disponíveis: {e}")
        return jsonify({"error": "Erro interno do servidor ao processar a requisição.", "details": str(e)}), 500
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return jsonify({"error": "Erro inesperado do servidor.", "details": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/concursos/<string:codigo_concurso>', methods=['GET'])
def get_concurso_by_codigo(codigo_concurso):
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Não foi possível conectar ao banco de dados."}), 500
        
        cur = conn.cursor()
        query = """
            SELECT
                orgao,
                edital,
                codigo_concurso,
                lista_vagas::text
            FROM
                Concursos
            WHERE
                codigo_concurso = %s;
        """
        cur.execute(query, (codigo_concurso,))
        concurso = cur.fetchone() # fetchone() para obter apenas um resultado

        if not concurso:
            return jsonify({"error": "Concurso não encontrado."}), 404

        try:
            lista_vagas_tratada = json.loads(concurso[3]) if concurso[3] else []
        except json.JSONDecodeError:
            lista_vagas_tratada = []

        result = {
            "orgao": concurso[0],
            "edital": concurso[1],
            "codigo_concurso": concurso[2],
            "lista_vagas": lista_vagas_tratada
        }

        cur.close()
        return jsonify(result), 200

    except psycopg2.Error as e:
        print(f"Erro no banco de dados ao buscar concurso por código: {e}")
        return jsonify({"error": "Erro interno do servidor ao buscar concurso.", "details": str(e)}), 500
    except Exception as e:
        print(f"Erro inesperado ao buscar concurso por código: {e}")
        return jsonify({"error": "Erro inesperado do servidor.", "details": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/vagas', methods=['GET'])
def get_all_vagas():
    """Endpoint para listar todas as vagas únicas."""
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Não foi possível conectar ao banco de dados."}), 500
        
        cur = conn.cursor()
        query = """
            SELECT DISTINCT vaga_unica
            FROM Concursos, jsonb_array_elements_text(lista_vagas) AS vaga_unica
            ORDER BY vaga_unica;
        """
        cur.execute(query)
        vagas = cur.fetchall()

        results = [vaga[0] for vaga in vagas]

        cur.close()
        return jsonify(results), 200

    except psycopg2.Error as e:
        print(f"Erro no banco de dados ao buscar todas as vagas: {e}")
        return jsonify({"error": "Erro interno do servidor ao buscar vagas.", "details": str(e)}), 500
    except Exception as e:
        print(f"Erro inesperado ao buscar todas as vagas: {e}")
        return jsonify({"error": "Erro inesperado do servidor.", "details": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/candidatos', methods=['GET'])
def get_candidatos():
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Não foi possível conectar ao banco de dados."}), 500
        
        cur = conn.cursor()

        query = """
            SELECT
                nome,
                data_nascimento,
                cpf,
                profissoes::text
            FROM
                Candidatos
            ORDER BY
                nome DESC;
        """

        cur.execute(query)
        candidatos = cur.fetchall()

        results = []
        for candidato in candidatos:
            try:
                lista_profissoes_tratada = json.loads(candidato[3]) if candidato[3] else []
            except json.JSONDecodeError:
                lista_profissoes_tratada = []
            results.append({
                "nome": candidato[0],
                "data_nascimento": candidato[1],
                "cpf": candidato[2],
                "profissoes": lista_profissoes_tratada
            })

        cur.close()
        return jsonify(results), 200

    except psycopg2.Error as e:
        print(f"Erro no banco de dados ao buscar todos concursos disponíveis: {e}")
        return jsonify({"error": "Erro interno do servidor ao processar a requisição.", "details": str(e)}), 500
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return jsonify({"error": "Erro inesperado do servidor.", "details": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/candidatos/<string:cpf_candidato>', methods=['GET'])
def get_candidato_by_cpf(cpf_candidato):
    """Obter um único candidato por CPF."""
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Não foi possível conectar ao banco de dados."}), 500
        
        cur = conn.cursor()
        cpf_limpo = cpf_candidato.replace('.', '').replace('-', '')

        query = """
            SELECT
                cpf,
                nome,
                data_nascimento,
                profissoes::text
            FROM
                Candidatos
            WHERE
                cpf = %s;
        """
        cur.execute(query, (cpf_limpo,))
        candidato = cur.fetchone()

        if not candidato:
            return jsonify({"error": "Candidato não encontrado."}), 404

        try:
            profissoes_tratadas = json.loads(candidato[3]) if candidato[3] else []
        except json.JSONDecodeError:
            profissoes_tratadas = []

        result = {
            "cpf": candidato[0],
            "nome": candidato[1],
            "data_nascimento": candidato[2].strftime('%d/%m/%Y') if candidato[2] else None,
            "profissoes": profissoes_tratadas
        }

        cur.close()
        return jsonify(result), 200

    except psycopg2.Error as e:
        print(f"Erro no banco de dados ao buscar candidato por CPF: {e}")
        return jsonify({"error": "Erro interno do servidor ao buscar candidato.", "details": str(e)}), 500
    except Exception as e:
        print(f"Erro inesperado ao buscar candidato por CPF: {e}")
        return jsonify({"error": "Erro inesperado do servidor.", "details": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/candidatos', methods=['POST'])
def add_candidato():
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Não foi possível conectar ao banco de dados."}), 500
        
        data = request.get_json()
        nome = data.get('nome')
        data_nascimento_str = data.get('data_nascimento')
        cpf = data.get('cpf')
        profissoes = data.get('profissoes', []) # Espera uma lista de strings

        if not all([nome, data_nascimento_str, cpf]):
            return jsonify({"error": "Nome, data de nascimento e CPF são obrigatórios."}), 400

        cpf_limpo = cpf.replace('.', '').replace('-', '')
        
        try:
            data_nascimento = datetime.strptime(data_nascimento_str, '%d/%m/%Y').date()
        except ValueError:
            return jsonify({"error": "Formato de data de nascimento inválido. Use DD/MM/YY."}), 400

        profissoes_json = json.dumps(profissoes)

        cur = conn.cursor()
        query = """
            INSERT INTO Candidatos (nome, data_nascimento, cpf, profissoes)
            VALUES (%s, %s, %s, %s)
            RETURNING cpf;
        """
        cur.execute(query, (nome, data_nascimento, cpf_limpo, profissoes_json))
        inserted_cpf = cur.fetchone()[0]
        conn.commit()

        cur.close()
        return jsonify({"message": "Candidato adicionado com sucesso!", "cpf": inserted_cpf}), 201

    except psycopg2.IntegrityError as e:
        conn.rollback()
        if "duplicate key value violates unique constraint" in str(e):
            return jsonify({"error": "CPF já cadastrado."}), 409
        return jsonify({"error": "Erro de integridade do banco de dados.", "details": str(e)}), 500
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro no banco de dados ao adicionar candidato: {e}")
        return jsonify({"error": "Erro interno do servidor ao adicionar candidato.", "details": str(e)}), 500
    except Exception as e:
        conn.rollback()
        print(f"Erro inesperado ao adicionar candidato: {e}")
        return jsonify({"error": "Erro inesperado do servidor.", "details": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/candidatos/<string:cpf>', methods=['PUT'])
def update_candidato(cpf):
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Não foi possível conectar ao banco de dados."}), 500
        
        data = request.get_json()
        cpf_limpo = cpf.replace('.', '').replace('-', '')

        updates = []
        params = []

        if 'nome' in data:
            updates.append("nome = %s")
            params.append(data['nome'])
        if 'data_nascimento' in data:
            try:
                data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
                updates.append("data_nascimento = %s")
                params.append(data_nascimento)
            except ValueError:
                return jsonify({"error": "Formato de data de nascimento inválido. Use YYYY-MM-DD."}), 400
        if 'profissoes' in data:
            updates.append("profissoes = %s")
            params.append(json.dumps(data['profissoes']))

        if not updates:
            return jsonify({"message": "Nenhum dado para atualizar."}), 200

        query = f"UPDATE Candidatos SET {', '.join(updates)} WHERE cpf = %s RETURNING cpf;"
        params.append(cpf_limpo)

        cur = conn.cursor()
        cur.execute(query, tuple(params))
        updated_cpf = cur.fetchone()
        conn.commit()

        cur.close()
        if updated_cpf:
            return jsonify({"message": "Candidato atualizado com sucesso!", "cpf": updated_cpf[0]}), 200
        else:
            return jsonify({"error": "Candidato não encontrado."}), 404

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro no banco de dados ao atualizar candidato: {e}")
        return jsonify({"error": "Erro interno do servidor ao atualizar candidato.", "details": str(e)}), 500
    except Exception as e:
        conn.rollback()
        print(f"Erro inesperado ao atualizar candidato: {e}")
        return jsonify({"error": "Erro inesperado do servidor.", "details": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/candidatos/<string:cpf>', methods=['DELETE'])
def delete_candidato(cpf):
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Não foi possível conectar ao banco de dados."}), 500
        
        cpf_limpo = cpf.replace('.', '').replace('-', '')

        cur = conn.cursor()
        query = "DELETE FROM Candidatos WHERE cpf = %s RETURNING cpf;"
        cur.execute(query, (cpf_limpo,))
        deleted_cpf = cur.fetchone()
        conn.commit()

        cur.close()
        if deleted_cpf:
            return jsonify({"message": "Candidato deletado com sucesso!", "cpf": deleted_cpf[0]}), 200
        else:
            return jsonify({"error": "Candidato não encontrado."}), 404

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro no banco de dados ao deletar candidato: {e}")
        return jsonify({"error": "Erro interno do servidor ao deletar candidato.", "details": str(e)}), 500
    except Exception as e:
        conn.rollback()
        print(f"Erro inesperado ao deletar candidato: {e}")
        return jsonify({"error": "Erro inesperado do servidor.", "details": str(e)}), 500
    finally:
        if conn:
            conn.close()

# endpoints de edição para concursos

@app.route('/concursos', methods=['POST'])
def add_concurso():
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Não foi possível conectar ao banco de dados."}), 500
        
        data = request.get_json()
        orgao = data.get('orgao')
        edital = data.get('edital')
        codigo_concurso = data.get('codigo_concurso')
        lista_vagas = data.get('lista_vagas', []) # Espera uma lista de strings

        if not all([orgao, edital, codigo_concurso]):
            return jsonify({"error": "Órgão, edital e código do concurso são obrigatórios."}), 400

        lista_vagas_json = json.dumps(lista_vagas)

        cur = conn.cursor()
        query = """
            INSERT INTO Concursos (orgao, edital, codigo_concurso, lista_vagas)
            VALUES (%s, %s, %s, %s)
            RETURNING codigo_concurso;
        """
        cur.execute(query, (orgao, edital, codigo_concurso, lista_vagas_json))
        inserted_codigo_concurso = cur.fetchone()[0]
        conn.commit()

        cur.close()
        return jsonify({"message": "Concurso adicionado com sucesso!", "Código do concurso": inserted_codigo_concurso}), 201

    except psycopg2.IntegrityError as e:
        conn.rollback()
        if "duplicate key value violates unique constraint" in str(e):
            return jsonify({"error": "Código do concurso já cadastrado."}), 409
        return jsonify({"error": "Erro de integridade do banco de dados.", "details": str(e)}), 500
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro no banco de dados ao adicionar concurso: {e}")
        return jsonify({"error": "Erro interno do servidor ao adicionar concurso.", "details": str(e)}), 500
    except Exception as e:
        conn.rollback()
        print(f"Erro inesperado ao adicionar concurso: {e}")
        return jsonify({"error": "Erro inesperado do servidor.", "details": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/concursos/<string:codigo_concurso>', methods=['PUT'])
def update_concurso(codigo_concurso):
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Não foi possível conectar ao banco de dados."}), 500
        
        data = request.get_json()

        updates = []
        params = []

        if 'orgao' in data:
            updates.append("orgao = %s")
            params.append(data['orgao'])
        if 'edital' in data:
            updates.append("edital = %s")
            params.append(data['edital'])
        if 'lista_vagas' in data:
            updates.append("lista_vagas = %s")
            params.append(json.dumps(data['lista_vagas']))

        if not updates:
            return jsonify({"message": "Nenhum dado para atualizar."}), 200

        query = f"UPDATE Concursos SET {', '.join(updates)} WHERE codigo_concurso = %s RETURNING codigo_concurso;"
        params.append(codigo_concurso)

        cur = conn.cursor()
        cur.execute(query, tuple(params))
        updated_codigo_concurso = cur.fetchone()
        conn.commit()

        cur.close()
        if updated_codigo_concurso:
            return jsonify({"message": "Concurso atualizado com sucesso!", "codigo_concurso": updated_codigo_concurso[0]}), 200
        else:
            return jsonify({"error": "Concurso não encontrado."}), 404

    except psycopg2.IntegrityError as e: # Caso tente atualizar para um código de concurso já existente
        conn.rollback()
        if "duplicate key value violates unique constraint" in str(e):
            return jsonify({"error": "Novo código do concurso já está em uso."}), 409
        return jsonify({"error": "Erro de integridade do banco de dados.", "details": str(e)}), 500
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro no banco de dados ao atualizar concurso: {e}")
        return jsonify({"error": "Erro interno do servidor ao atualizar concurso.", "details": str(e)}), 500
    except Exception as e:
        conn.rollback()
        print(f"Erro inesperado ao atualizar concurso: {e}")
        return jsonify({"error": "Erro inesperado do servidor.", "details": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/concursos/<string:codigo_concurso>', methods=['DELETE'])
def delete_concurso(codigo_concurso):
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Não foi possível conectar ao banco de dados."}), 500
        
        cur = conn.cursor()
        query = "DELETE FROM Concursos WHERE codigo_concurso = %s RETURNING codigo_concurso;"
        cur.execute(query, (codigo_concurso,))
        # print(type(codigo_concurso), codigo_concurso)
        deleted_codigo_concurso = cur.fetchone()
        conn.commit()

        cur.close()
        if deleted_codigo_concurso:
            return jsonify({"message": "Concurso deletado com sucesso!", "codigo_concurso": deleted_codigo_concurso[0]}), 200
        else:
            return jsonify({"error": "Concurso não encontrado."}), 404

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro no banco de dados ao deletar concurso: {e}")
        return jsonify({"error": "Erro interno do servidor ao deletar concurso.", "details": str(e)}), 500
    except Exception as e:
        conn.rollback()
        print(f"Erro inesperado ao deletar concurso: {e}")
        return jsonify({"error": "Erro inesperado do servidor.", "details": str(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)