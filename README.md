# Desafio LEDS - Sistema de Gerenciamento de Concursos e Candidatos

## [_Clique para acessar Aplicação_](https://desafio-leds-luizrojas.appsmith.com/app/desafio-back-end-lowcode-leds/home-686eec1a4c97004f2122aea6?branch=main)

## 1. Contextualização e Objetivo

Este projeto foi desenvolvido como parte do **Desafio Low/No Code - LEDS**.  
O objetivo principal é criar um sistema capaz de realizar buscas e gerenciar dados de concursos públicos e candidatos, atendendo aos seguintes requisitos:

- **Listar os órgãos, códigos e editais** dos concursos públicos que se encaixam no perfil do candidato, com base no CPF informado.
- **Listar o nome, data de nascimento e CPF** dos candidatos que se encaixam no perfil de um concurso, com base no código do concurso.
- Disponibilizar operações completas de **CRUD** (Create, Read, Update, Delete) para candidatos e concursos.

---

## 2. Tecnologias Utilizadas

| Camada | Tecnologia |
| ------ | ---------- |
| Frontend / Plataforma Low‑Code | **Appsmith** |
| Backend / API REST | **Python (Flask)** |
| Banco de Dados | **PostgreSQL** (local via Docker) <br> **Neon DB** (nuvem) |
| Conteinerização | **Docker** & **Docker Compose** |

---

## 3. Arquitetura da Solução

A solução foi pensada em microsserviços conteinerizados, separados em duas abordagens complementares:

1. **Execução local (Docker Compose)**  
   - **Appsmith**: Interface do usuário, comunicando‑se com a API.  
   - **API REST (Flask)**: Implementa a lógica de negócio e expõe endpoints RESTful.  
   - **PostgreSQL**: Banco de dados rodando em contêiner.  

2. **Execução em nuvem (Appsmith Cloud + Neon DB)**  
   - **Appsmith Online** se conecta **diretamente** ao **Neon DB**, dispensando API própria quando desejado.  
   - O código‑fonte da API permanece disponível para evoluções futuras ou execução on‑premises.

Um diagrama simplificado:

```text
┌──────────┐        REST        ┌────────────┐
│ Appsmith │ ───────────────▶  │   API      │
│ Frontend │ ◀───────────────  │  Flask     │
└──────────┘     JSON          └────┬───────┘
                                     │ SQL
                              ┌──────▼──────┐
                              │ PostgreSQL  │
                              └─────────────┘
```

---

## 4. Como Executar a Solução Localmente

### 4.1 Pré‑requisitos

- **Docker Desktop** (inclui Docker Compose).  
- **Python 3.9+**

### 4.2 Clonar o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <nome_do_seu_repositorio>
```

### 4.3 Configurar o PostgreSQL

Crie a pasta **postgres_config/** na raiz do projeto contendo:

**postgresql.conf**

```ini
listen_addresses = '*'
```

**pg_hba.conf**

```
host    processo_seletivo_app    admin    0.0.0.0/0    md5
```

### 4.4 Subir o Ambiente

```bash
docker compose up --build -d
```

Isso irá:

1. Construir a imagem da API;
2. Criar contêineres para **Appsmith**, **PostgreSQL** e **API**;
3. Executá‑los em *detached mode*.

### 4.5 Acessar

- **Appsmith**: <http://localhost>  
- **API REST** (endpoint de rest): <http://localhost:5000/>


Via `psql` dentro do contêiner:

```bash
docker exec -it <nome_do_container_postgres> psql -U admin -d processo_seletivo_app
```

---

## 5. Uso do Appsmith + Neon DB (Abordagem Cloud)

- **Appsmith Online**: Interface acessível via navegador, conectada ao Neon DB.  
- **Neon DB**: PostgreSQL serverless e escalável, com credenciais configuradas diretamente no Appsmith.  

Esta abordagem demonstra a flexibilidade do projeto, possibilitando desenvolvimento local e implantação rápida na nuvem.

---

## 6. Estrutura da API REST

A API **não** está incluída neste arquivo para facilitar a leitura.  
Abaixo você encontra um **resumo dos endpoints** disponíveis (todos respondem em JSON):

| Método | Rota | Descrição |
| ------ | ---- | --------- |
| `GET` | `/` | Teste de rest da API |
| `GET` | `/concursos` | Lista todos os concursos |
| `GET` | `/concursos/<codigo>` | Detalhes de um concurso |
| `GET` | `/concursos/by_cpf/<cpf>` | Concursos compatíveis com o candidato |
| `POST` | `/concursos` | Cria novo concurso |
| `PUT` | `/concursos/<codigo>` | Atualiza concurso |
| `DELETE` | `/concursos/<codigo>` | Remove concurso |
| `GET` | `/candidatos` | Lista todos os candidatos |
| `GET` | `/candidatos/<cpf>` | Detalhes de um candidato |
| `GET` | `/candidatos/by_codigo_concurso/<codigo>` | Candidatos compatíveis com o concurso |
| `POST` | `/candidatos` | Cria novo candidato |
| `PUT` | `/candidatos/<cpf>` | Atualiza candidato |
| `DELETE` | `/candidatos/<cpf>` | Remove candidato |
| `GET` | `/vagas` | Lista de vagas únicas cadastradas |

---

## 7. Critérios de Avaliação

### 7.1 Legibilidade

- Nomes descritivos para variáveis, funções e endpoints.  
- Projeto modular.

### 7.2 Documentação

- Docstrings nos endpoints Flask.  
- Comentários explicativos em JS Objects do Appsmith.  
- **Dockerfile** e **docker‑compose.yml** comentados.

### 7.3 Tratamento de Erros

- Respostas JSON padronizadas (`400`, `404`, `409`, `500`).  
- `try‑except` na API e `showAlert()` no Appsmith.

---

## 8. Diferenciais Implementados

- **API RESTful** separada, seguindo Clean Code.  
- **PostgreSQL** local + **Neon DB** na nuvem.  
- **Docker** para portabilidade total.  
- Abordagem **Low‑Code** com Appsmith acelerando o desenvolvimento.

---

> **Licença**: Este projeto é distribuído sob a licença MIT. Sinta‑se à vontade para usar e contribuir!
