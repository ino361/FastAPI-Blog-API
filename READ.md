# FastAPI Blog Projesi 
*(TEASY BABAYA SELAM OLSUN)*

Bu proje; FastAPI ve SQLAlchemy kullanılarak geliştirilmiş, ilişkisel veritabanı (SQLite) barındıran, kullanıcı yetkilendirmeli (JWT) ve görsel yükleme/silme özelliklerine sahip gelişmiş bir Blog API projesidir.

---

## Özellikler 

* **Kullanıcı Sistemi:** Kayıt olma, giriş yapma ve JWT tabanlı yetkilendirme (OAuth2).
* **Blog Postları:** Görsel yükleme, post silindiğinde ilişkili görsellerin diskten otomatik temizlenmesi.
* **Yorum Sistemi:** Postlara yorum yapabilme ve yorum görsellerini yönetme.
* **Güvenli Altyapı:** `.env` ile çevre değişkenleri yönetimi ve Pydantic ile veri doğrulaması.

---

## Kurulum ve Çalıştırma 

### 1. Projeyi Klonlayın
```bash
git clone <github-depo-linkiniz>
cd <proje-klasör-adı>

2. Sanal Ortam Oluşturun ve Aktif Edin

python -m venv venv

Windows için: venv\Scripts\activate

Mac/Linux için: source venv/bin/activate

---

3. Gerekli Kütüphaneleri Kurun

pip install -r requirements.txt

---

4. Çevre Değişkenlerini Ayarlayın

SECRET_KEY="your-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
sqlalchemy_database_url="sqlite:///./blog.db"

---

5. Projeyi Başlatın

uvicorn main:app --reload

API dökümantasyonuna ulaşmak için tarayıcınızdan http://127.0.0.1:8000/docs adresine gidin.