from pydantic import BaseModel


class ApplicationCreate(BaseModel):

    linkedin: str
    email: str
