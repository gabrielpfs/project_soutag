-- Criação da tabela inicial bruta do dataset Netflix from Kaggle
-- Fonte: https://www.kaggle.com/datasets/shivamb/netflix-shows

-- src/sql/create_tables.sql

CREATE TABLE netflix_raw (
    show_id VARCHAR(10) PRIMARY KEY,
    type VARCHAR(20),
    title VARCHAR(255),
    director VARCHAR(255),
    cast TEXT,
    country TEXT,
    date_added DATE,
    release_year INT,
    rating VARCHAR(10),
    duration VARCHAR(50),
    listed_in TEXT,
    description TEXT
);

-- Fim do arquivo create_tables.sql
-- Data de criação: 2024-06-10
-- Autor: Gabriel Santos
-- Última modificação: 2024-06-10
-- Modificador: Gabriel Santos
-- Descrição: Criação da tabela inicial bruta do dataset Netflix from Kaggle
-- Fonte: https://www.kaggle.com/datasets/shivamb/netflix-shows
-- Versão: 1.0
-- Histórico de modificações:
-- 2024-06-10: Criação do arquivo e definição da estrutura inicial da
-- tabela netflix_raw.
-- 2024-06-10: Adição de comentários e metadados ao arquivo.
-- 2024-06-10: Revisão final e validação da estrutura da tabela.
-- Observações:
-- A tabela netflix_raw é a estrutura inicial para armazenar os dados
-- brutos do dataset Netflix from Kaggle. Ela pode ser expandida ou
-- modificada conforme necessário para atender aos requisitos do projeto.
-- Certifique-se de que os tipos de dados e tamanhos das colunas sejam
-- adequados para os dados que serão inseridos.
-- Recomenda-se a criação de índices adicionais para otimizar consultas
-- frequentes, dependendo dos padrões de uso.
-- Fim do arquivo create_tables.sql
