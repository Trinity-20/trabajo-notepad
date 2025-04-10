CREATE DATABASE notepad_db;

USE notepad_db;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    contraseña VARCHAR(100)
);

CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100),
    contenido TEXT,
    usuario_id INT,
    categoria_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nota_id INT,
    comentario TEXT,
    usuario_id INT,
    FOREIGN KEY (nota_id) REFERENCES notas(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);


INSERT INTO usuarios (nombre, email, contraseña)
VALUES 
('Trinity', 'tri@gmail.com', '202020'),
('Patrick Marquillo', 'patrick3@gmail.com', '232041');


INSERT INTO categorias (nombre) VALUES ('Trabajo');
INSERT INTO categorias (nombre) VALUES ('Estudios');
INSERT INTO categorias (nombre) VALUES ('Personal');


SELECT * FROM usuarios WHERE id = 1;

SELECT * FROM notas;
SELECT * FROM usuarios;
SELECT * FROM categorias;

SELECT * FROM usuarios WHERE nombre = 'Juan Pérez';

DELETE FROM usuarios WHERE nombre = 'Juan Pérez';


DELETE FROM notas WHERE usuario_id = (SELECT id FROM usuarios WHERE nombre = 'Juan Pérez');
DELETE FROM usuarios WHERE nombre = 'Juan Pérez';