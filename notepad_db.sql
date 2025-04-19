CREATE DATABASE notepad_db;

USE notepad_db;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);

CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    content TEXT,
    usuario_id INT,
    categoria_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nota_id INT,
    comment TEXT,
    usuario_id INT,
    FOREIGN KEY (nota_id) REFERENCES notas(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

INSERT INTO usuarios (name, email, password)
VALUES 
('Trinity', 'tri@gmail.com', '202020'),
('Patrick Marquillo', 'patrick3@gmail.com', '232041');

INSERT INTO categorias (name) VALUES ('Trabajo');
INSERT INTO categorias (name) VALUES ('Estudios');
INSERT INTO categorias (name) VALUES ('Personal');

SELECT * FROM users WHERE id = 1;

SELECT * FROM notas;
SELECT * FROM usuarios;
SELECT * FROM categorias;

es