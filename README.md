# Vodafone FastAPI Case

Bu proje, FastAPI, SQLAlchemy, MySQL ve Redis kullanılarak Docker ortamında çalışan bir REST API uygulamasıdır. 
Kullanıcı verileri hem MySQL veritabanına hem de Redis önbelleğine yazılır. 
Uygulama, test senaryoları dahil olmak üzere Docker Compose ile container içinde çalıştırılır.

---

## Kullanılan Teknolojiler ve Kütüphaneler

### Altyapı

- Docker Engine
- Docker Compose

> Docker Desktop, Windows/macOS kullanıcıları için önerilir.

### Backend

- Python 3.11
- FastAPI
- Uvicorn (ASGI server)
- SQLAlchemy (ORM)
- PyMySQL (MySQL bağlantısı)
- Redis (in-memory cache)
- Faker (rastgele veri üretimi)
- Cryptography (MySQL şifreleme desteği)
- Pytest (otomatik testler)
- httpx (TestClient için)

---

## Gereksinimler

Bu projeyi çalıştırmak için sisteminizde aşağıdaki yazılımların kurulu olması gerekir:

- Docker Engine
- Docker Compose
- Python 3.11+  (Docker dışında lokal test istenirse)

---

## Kurulum ve Çalıştırma

### 1. Projeyi klonlayın veya zip olarak indirin

```bash
git clone https://github.com/kullanici_adi/VODAFONE_CASE.git
cd VODAFONE_CASE
```

### 2. Docker servislerini başlatın

```bash
docker-compose up --build
```

### 3. API dokümantasyonuna erişim

Tarayıcınızdan aşağıdaki adrese gidin:

```
http://localhost:8000/docs
```

Bu sayfada Post ve Get endpoint’lerini Swagger UI üzerinden test edebilirsiniz.

---

## API Davranışı

- `POST /insert`: Gönderilen kullanıcıyı hem MySQL veritabanına hem Redis’e yazar
- `GET /user/{id}`: 
  - İlk olarak Redis’te arar
  - Yoksa MySQL’den alır ve Redis’e cache eder
  - JSON cevabında `"source": "redis"` veya `"source": "mysql"` bilgisi yer alır
  - Redis cache süresini geçerse (1 dakika olarak ayarlandı), o zaman source kısmında MySQL olarak görünür. 
---

## Otomatik Testlerin Çalıştırılması

Bu projede testler Docker container içinde `pytest` kullanılarak çalıştırılır.

### Windows Kullanıcıları:
Proje dizinindeki `run_tests.bat` dosyasını çift tıklayın.

### Terminal Üzerinden:

```bash
docker-compose run --rm test_runner
```

### Test Ne Yapar?

- Rastgele isimli kullanıcı ve ID üretir.
- Her kullanıcıyı `POST /insert` ile ekler MySQL ve Redis'e yazar.
- `GET /user/{id}` ile kullanıcıyı geri çağırır
- Verinin Redis’ten mi yoksa MySQL’den mi geldiğini kontrol eder.
- Test sonucu terminale yazılır.

---

### Test Otomasyon Nasıl çalıştırılır? (Windows için) - Swagger ile aynı şeyin CMD üzerinden otomatik uygulanması

- VodafoneFastAPI_TestOtomasyon.bat dosyasına çift tıklayın. 
- CMD ekranındaki yönergeleri takip edin. 
- Random birden fazla kullanıcıyı yaratır ve MySQL'de yaratılan birden fazla kullanıcıyı size getirir.
- Dilediğinizi seçerek Redis'ten mi MySQL'dan mı okunduğunu terminale yazar. 
- 60 sn bekleyerek redis Cache'inin silinmesinden sonra kullanıcıyı tekrar MySQL'dan getirildiğini gösterir. 
- Ve daha sonra 3. kez kullanıcıyı Redis'ten getirir. 


## Proje Klasör Yapısı

```
VODAFONE_CASE/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   └── redis_client.py
├── tests/
│   └── test_main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run_fast_api_project.bat 
├── run_tests.bat
├── test.http
├── VodafoneFastAPI_TestOtomasyon.bat


```

---

## Notlar

- Projede kullanılan MySQL ve Redis container olarak çalışır, dışarıdan kurulum gerektirmez.
- Testler doğrudan Docker içinde çalıştığı için sistem bağımsızdır.
- Proje mikroservis entegrasyonu yapısına sahiptir.

## Advanced Notlar

- MySQL hazır olana kadar FastAPI bekler.
- POST ile kullanıcı eklendiğinde Redis ve MySQL'e aynı anda yazılır.
- GET ile kullanıcı çekildiğinde önce Redis'e, yoksa MySQL'e bakılır.
- Redis Cache süresi 1 dakikadır. Bu süreyi bekledikten sonra tekrar GET ile aynı kullanıcı çekilirse MySQL'den kullanıcıyı getirir. 
- Swagger arayüzü otomatik olarak `/docs` adresinde oluşur. 
- Buradaki arayüzü tarayıcınızla kullanarak yeni kullanıcı ekle ve ID'si ile getir yapabilirsiniz.
- ID unique olduğundan aynı ID ile kullanıcı eklenmemelidir. 