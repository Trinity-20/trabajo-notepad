from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from . import models
from . import crud
from . import schemas
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de Jinja2
templates = Jinja2Templates(directory="templates")

# Configuración de archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_notas(request: Request, db: Session = Depends(get_db)):
    # Obtener las notas de la base de datos
    notas = crud.get_notas(db)
    
    # Obtener las categorías de la base de datos
    categorias = db.query(models.Categoria).all()
    
    # Obtener los usuarios
    usuarios = db.query(models.Usuario).all()
    
    # Renderizar la plantilla y pasar las notas, categorías y usuarios
    return templates.TemplateResponse("index.html", {"request": request, "notas": notas, "categorias": categorias, "usuarios": usuarios})

@app.post("/notas/", response_model=schemas.Nota)
async def create_nota(
    titulo: str = Form(...),  # Recibiendo el título como un formulario
    contenido: str = Form(...),  # Recibiendo el contenido como un formulario
    categoria_id: int = Form(...),  # Recibiendo la categoría seleccionada como un formulario
    usuario_id: int = Form(...),  # Recibiendo el usuario seleccionado como un formulario
    db: Session = Depends(get_db)
):
    # Verificar si la categoría existe
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=400, detail="Categoría no encontrada")
    
    # Verificar si el usuario existe
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    
    # Crear una nueva nota usando los datos del formulario
    crud.create_nota(db=db, nota=schemas.NotaCreate(titulo=titulo, contenido=contenido, categoria_id=categoria_id), usuario_id=usuario_id)
    
    # Redirigir de nuevo a la página principal con las notas actualizadas
    return RedirectResponse(url="/", status_code=303)

@app.post("/notas/{nota_id}", response_class=HTMLResponse)
async def delete_nota(nota_id: int, request: Request, db: Session = Depends(get_db)):
    # Llamar a la función para eliminar la nota
    deleted_nota = crud.delete_nota(db=db, nota_id=nota_id)
    if deleted_nota is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    
    # Redirigir de nuevo a la página principal con las notas actualizadas
    return RedirectResponse(url="/", status_code=303)

# Ruta para mostrar el formulario de edición
@app.get("/notas/{nota_id}/editar", response_class=HTMLResponse)
async def edit_nota(request: Request, nota_id: int, db: Session = Depends(get_db)):
    # Obtener la nota a editar
    nota = db.query(models.Nota).filter(models.Nota.id == nota_id).first()
    if nota is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    
    # Obtener todas las categorías
    categorias = db.query(models.Categoria).all()
    
    # Obtener todos los usuarios
    usuarios = db.query(models.Usuario).all()
    
    # Renderizar la plantilla de edición con los datos actuales de la nota, categorías y usuarios
    return templates.TemplateResponse("edit_nota.html", {"request": request, "nota": nota, "categorias": categorias, "usuarios": usuarios})

# Ruta para actualizar la nota
@app.post("/notas/{nota_id}/editar", response_class=HTMLResponse)
async def update_nota(nota_id: int, titulo: str = Form(...), contenido: str = Form(...), categoria_id: int = Form(...), usuario_id: int = Form(...), db: Session = Depends(get_db)):
    # Obtener la nota para actualizar
    nota = db.query(models.Nota).filter(models.Nota.id == nota_id).first()
    if nota is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    
    # Verificar si la categoría existe
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=400, detail="Categoría no encontrada")
    
    # Verificar si el usuario existe
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    
    # Actualizar los campos de la nota
    nota.titulo = titulo
    nota.contenido = contenido
    nota.categoria_id = categoria_id  # Actualizar la categoría
    nota.usuario_id = usuario_id  # Actualizar el usuario
    db.commit()
    db.refresh(nota)
    
    # Redirigir de nuevo a la página principal con las notas actualizadas
    return RedirectResponse(url="/", status_code=303)
