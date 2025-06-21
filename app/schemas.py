from pydantic import BaseModel

import warnings
warnings.filterwarnings('ignore') 


class PersonCreate(BaseModel):
    id: int
    name: str
    surname: str

class PersonOut(BaseModel):
    id: int
    name: str
    surname: str
    date: str

    class Config:
        from_attributes = True

# Swagger IU si için : 
class SourceWrapper(BaseModel):
    source: str
    data: PersonOut
