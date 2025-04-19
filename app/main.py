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
    notas = crud.get_notas(db)
    categorias = db.query(models.Categoria).all()
    usuarios = db.query(models.Usuario).all()
    return templates.TemplateResponse("index.html", {"request": request, "notas": notas, "categorias": categorias, "usuarios": usuarios})

@app.post("/notas/", response_class=HTMLResponse)
async def create_nota(
    request: Request,
    titulo: str = Form(...),
    contenido: str = Form(...),
    categoria: str = Form(...),
    usuario_id: int = Form(...),
    db: Session = Depends(get_db)
):
    # Buscar o crear categoría
    categoria_obj = db.query(models.Categoria).filter(models.Categoria.nombre == categoria).first()
    if not categoria_obj:
        categoria_obj = models.Categoria(nombre=categoria)
        db.add(categoria_obj)
        db.commit()
        db.refresh(categoria_obj)

    # Crear nota
    nueva_nota = models.Nota(
        titulo=titulo,
        contenido=contenido,
        categoria_id=categoria_obj.id,
        usuario_id=usuario_id
    )
    db.add(nueva_nota)
    db.commit()
    db.refresh(nueva_nota)

    return RedirectResponse(url="/", status_code=303)

@app.post("/notas/{nota_id}", response_class=HTMLResponse)
async def delete_nota(nota_id: int, request: Request, db: Session = Depends(get_db)):
    deleted_nota = crud.delete_nota(db=db, nota_id=nota_id)
    if deleted_nota is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return RedirectResponse(url="/", status_code=303)

@app.get("/notas/{nota_id}/editar", response_class=HTMLResponse)
async def edit_nota(request: Request, nota_id: int, db: Session = Depends(get_db)):
    nota = db.query(models.Nota).filter(models.Nota.id == nota_id).first()
    if nota is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    usuarios = db.query(models.Usuario).all()
    return templates.TemplateResponse("edit_nota.html", {"request": request, "nota": nota, "usuarios": usuarios})

@app.post("/notas/{nota_id}/editar", response_class=HTMLResponse)
async def update_nota(
    request: Request,
    nota_id: int,
    titulo: str = Form(...),
    contenido: str = Form(...),
    categoria: str = Form(...),
    usuario_id: int = Form(...),
    db: Session = Depends(get_db)
):
    nota = db.query(models.Nota).filter(models.Nota.id == nota_id).first()
    if nota is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    # Buscar o crear categoría
    categoria_obj = db.query(models.Categoria).filter(models.Categoria.nombre == categoria).first()
    if not categoria_obj:
        categoria_obj = models.Categoria(nombre=categoria)
        db.add(categoria_obj)
        db.commit()
        db.refresh(categoria_obj)

    # Actualizar nota
    nota.titulo = titulo
    nota.contenido = contenido
    nota.categoria_id = categoria_obj.id
    nota.usuario_id = usuario_id

    db.commit()
    db.refresh(nota)

    return RedirectResponse(url="/", status_code=303)
