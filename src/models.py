from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Usuario(db.Model):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)

    posteos: Mapped[List["Post"]] = relationship(back_populates="usuario")
    likes: Mapped[List["Likear"]] = relationship(back_populates="usuario")
    comentarios: Mapped[List["Comentar"]] = relationship(back_populates="usuario")

    seguidos: Mapped[List["Seguir"]] = relationship(foreign_keys="Seguir.seguidor_id", back_populates="seguidor")
    seguidores: Mapped[List["Seguir"]] = relationship(foreign_keys="Seguir.seguido_id", back_populates="seguido")
    


    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            # do not serialize the password, its a security breach
        }    

class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    descripcion: Mapped[str] = mapped_column(nullable=False)
    archivo_jpg: Mapped[str] = mapped_column(nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"),nullable=False)

    likes: Mapped[List["Likear"]] = relationship(back_populates="post")
    comentarios: Mapped[List["Comentar"]] = relationship(back_populates="post")

    usuario: Mapped["Usuario"] = relationship(back_populates="posteos")
    


    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, its a security breach
        }
    
class Likear(db.Model):
    __tablename__ = "likear"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"),nullable=False)
    le_gusta_usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"),nullable=False)
    
    usuario: Mapped["Usuario"] = relationship(back_populates="likes")
    post: Mapped["Post"] = relationship(back_populates="likes")

    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, its a security breach
        }   

class Seguir(db.Model):
    __tablename__ = "seguir"
    id: Mapped[int] = mapped_column(primary_key=True)
    seguido_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    seguidor_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)

    seguido: Mapped["Usuario"] = relationship(foreign_keys=[seguido_id], back_populates="seguidores")
    seguidor: Mapped["Usuario"] = relationship(foreign_keys=[seguidor_id], back_populates="seguidos")


    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, its a security breach
        }
    
class Comentar(db.Model):
    __tablename__ = "comentar"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"),nullable=False)
    comentario: Mapped[str] = mapped_column(nullable=False)
    id_post: Mapped[int] = mapped_column(ForeignKey("post.id"),nullable=False)
    
    usuario: Mapped["Usuario"] = relationship(back_populates="comentarios")
    post: Mapped["Post"] = relationship(back_populates="comentarios")

    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, its a security breach
        }
    
