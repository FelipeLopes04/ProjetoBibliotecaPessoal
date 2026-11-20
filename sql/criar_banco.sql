IF DB_ID('BibliotecaPessoal') IS NULL
    CREATE DATABASE BibliotecaPessoal;
GO

USE BibliotecaPessoal;
GO

IF OBJECT_ID('dbo.categoria') IS NULL
CREATE TABLE categoria (
    id   INT IDENTITY(1,1) PRIMARY KEY,
    nome NVARCHAR(100) NOT NULL UNIQUE
);
GO

IF OBJECT_ID('dbo.livro') IS NULL
CREATE TABLE livro (
    id           INT IDENTITY(1,1) PRIMARY KEY,
    titulo       NVARCHAR(200) NOT NULL,
    autor        NVARCHAR(150) NOT NULL,
    ano          INT NULL,
    status       NVARCHAR(20)  NOT NULL DEFAULT N'Quero ler'
                 CHECK (status IN (N'Quero ler', N'Lendo', N'Lido')),
    categoria_id INT NOT NULL,
    CONSTRAINT FK_livro_categoria FOREIGN KEY (categoria_id) REFERENCES categoria (id)
);
GO

IF NOT EXISTS (SELECT 1 FROM categoria)
BEGIN
    INSERT INTO categoria (nome) VALUES (N'Romance'), (N'Fantasia'), (N'Tecnologia');

    INSERT INTO livro (titulo, autor, ano, status, categoria_id) VALUES
        (N'Dom Casmurro',  N'Machado de Assis', 1899, N'Lido',      1),
        (N'O Hobbit',      N'J. R. R. Tolkien', 1937, N'Lendo',     2),
        (N'Código Limpo',  N'Robert C. Martin', 2008, N'Quero ler', 3);
END
GO

SELECT * FROM categoria;
SELECT * FROM livro;
