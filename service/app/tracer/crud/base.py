from typing import Generic, List, Optional, Type, TypeVar

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4, BaseModel
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from tracer.db.base_class import Base
from tracer.exceptions import UniqueValueQueryException

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    From: https://github.com/tiangolo/full-stack-fastapi-postgresql
    """

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: UUID4) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()  # type: ignore

    def get_or_404(self, db: Session, id: UUID4) -> ModelType:
        try:
            return db.query(self.model).filter(self.model.id == id).one()  # type: ignore
        except UniqueValueQueryException:
            raise HTTPException(HTTP_404_NOT_FOUND, "resource not found")

    def get_multi(self, db: Session, *, skip=0, limit=100) -> List[ModelType]:
        query = db.query(self.model).offset(skip)
        if limit:
            query = query.limit(limit)
        return query.all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: UUID4) -> ModelType:
        obj = db.query(self.model).get(id)
        if not obj:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail=f"Object with id {id} not found",
            )
        db.delete(obj)
        db.commit()
        return obj
