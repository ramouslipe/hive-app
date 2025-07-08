

-- Dropar as tabelas na ordem correta para evitar erros de chave estrangeira
DROP TABLE IF EXISTS Biblioteca_Jogo;
DROP TABLE IF EXISTS Avaliacao;
DROP TABLE IF EXISTS Item_compra;
DROP TABLE IF EXISTS Compra;
DROP TABLE IF EXISTS Biblioteca;
DROP TABLE IF EXISTS Jogo;
DROP TABLE IF EXISTS Desenvolvedora;
DROP TABLE IF EXISTS Usuario;

-- Criar tabela Usuario
CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    senha VARCHAR(100)
);

-- Criar tabela Desenvolvedora
CREATE TABLE Desenvolvedora (
    id_desenvolvedora SERIAL PRIMARY KEY,
    nome VARCHAR(100)
);

-- Criar tabela Jogo (com campo preco)
CREATE TABLE Jogo (
    id_jogo SERIAL PRIMARY KEY,
    titulo VARCHAR(100),
    preco NUMERIC(10,2),
    id_desenvolvedora INT,
    FOREIGN KEY (id_desenvolvedora) REFERENCES Desenvolvedora(id_desenvolvedora)
);

-- Criar tabela Biblioteca
CREATE TABLE Biblioteca (
    id_biblioteca SERIAL PRIMARY KEY,
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

-- Criar tabela Compra
CREATE TABLE Compra (
    id_compra SERIAL PRIMARY KEY,
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

-- Criar tabela Item_compra
CREATE TABLE Item_compra (
    id_item SERIAL PRIMARY KEY,
    id_compra INT,
    id_jogo INT,
    FOREIGN KEY (id_compra) REFERENCES Compra(id_compra),
    FOREIGN KEY (id_jogo) REFERENCES Jogo(id_jogo)
);

-- Criar tabela Avaliacao
CREATE TABLE Avaliacao (
    id_avaliacao SERIAL PRIMARY KEY,
    comentario TEXT,
    id_usuario INT,
    id_jogo INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_jogo) REFERENCES Jogo(id_jogo)
);

-- Criar tabela Biblioteca_Jogo (relacionamento N:N)
CREATE TABLE Biblioteca_Jogo (
    id_biblioteca INT,
    id_jogo INT,
    PRIMARY KEY (id_biblioteca, id_jogo),
    FOREIGN KEY (id_biblioteca) REFERENCES Biblioteca(id_biblioteca),
    FOREIGN KEY (id_jogo) REFERENCES Jogo(id_jogo)
);
