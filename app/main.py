from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import time
from sqlalchemy.exc import OperationalError

from app import database, models, schemas, redis_client

import warnings
warnings.filterwarnings('ignore') 


# MySQL bağlantısı hazır olana kadar bekle 
# bu bekleme olmadan fastapi ayağa kaldırılamıyor
for attempt in range(10):
    try:
        models.Base.metadata.create_all(bind=database.engine)
        print("MySQL bağlantısı başarılı.")
        break
    except OperationalError:
        print(f"MySQL henüz hazır değil, {attempt+1}. deneme...")
        time.sleep(2)
else:
    raise Exception("MySQL'e bağlanılamadı, uygulama sonlandırılıyor.")

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/insert")
def insert_data(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()

    redis_client.save_to_redis(person.id, {
        "id": person.id,
        "name": person.name,
        "surname": person.surname,
        "date": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    return {"status": "saved"}

@app.get("/user/{person_id}", response_model=schemas.SourceWrapper)
def get_user(person_id: int, db: Session = Depends(get_db)):
    # Önce Redis'te check
    cached = redis_client.get_from_redis(person_id)
    if cached:
        return {"source": "redis", "data": cached}

    # MySQL'den al
    user = db.query(models.Person).filter(models.Person.id == person_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

    # Redis'e yaz
    redis_client.save_to_redis(user.id, {
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "date": user.date.strftime("%Y-%m-%d %H:%M:%S"),
    })

    return {
        "source": "mysql",
        "data": {
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "date": user.date.strftime("%Y-%m-%d %H:%M:%S"),
        }
    }
