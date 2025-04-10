from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    contraseña = Column(String)

    # Relación inversa con las notas, un usuario puede tener varias notas
    notas = relationship("Nota", back_populates="propietario")
    # Relación con los comentarios, un usuario puede tener varios comentarios
    comentarios = relationship("Comentario", back_populates="usuario")


class Categoria(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)

    # Relación con las notas, una categoría puede tener varias notas
    notas = relationship("Nota", back_populates="categoria")


class Nota(Base):
    __tablename__ = 'notas'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    contenido = Column(Text)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    # Relación con el usuario, cada nota tiene un propietario (usuario)
    propietario = relationship("Usuario", back_populates="notas")
    # Relación con la categoría, cada nota pertenece a una categoría
    categoria = relationship("Categoria", back_populates="notas")
    # Relación con los comentarios, cada nota puede tener varios comentarios
    comentarios = relationship("Comentario", back_populates="nota")


class Comentario(Base):
    __tablename__ = 'comentarios'

    id = Column(Integer, primary_key=True, index=True)
    comentario = Column(Text)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    nota_id = Column(Integer, ForeignKey("notas.id"))

    # Relación con el usuario, cada comentario pertenece a un usuario
    usuario = relationship("Usuario", back_populates="comentarios")
    # Relación con la nota, cada comentario pertenece a una nota
    nota = relationship("Nota", back_populates="comentarios")
