from sqlalchemy.orm import Session
from .models import Nota
from .schemas import NotaCreate

# Función para crear una nueva nota
def create_nota(db: Session, nota: NotaCreate, usuario_id: int):
    db_nota = Nota(titulo=nota.titulo, contenido=nota.contenido, usuario_id=usuario_id, categoria_id=nota.categoria_id)
    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)
    return db_nota

# Función para obtener todas las notas
def get_notas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Nota).offset(skip).limit(limit).all()

# Función para eliminar una nota por su ID
def delete_nota(db: Session, nota_id: int):
    # Buscar la nota en la base de datos
    db_nota = db.query(Nota).filter(Nota.id == nota_id).first()
    
    # Si la nota no existe, devolver None
    if db_nota:
        db.delete(db_nota)  # Eliminar la nota
        db.commit()  # Confirmar los cambios
        return db_nota
    return None  # Si no se encuentra la nota, devolver None
