# 📚 Blog project

Prosty projekt BLOG w oparciu o technologię Flask.

---

## 🛠 Wymagania

- Python 3.10+
- `pip`
- Wirtualne środowisko (rekomendowane)

## ⚙️ Instalacja

1. **Sklonuj repozytorium**

```bash
git clone https://github.com/likeahim/blog-project
cd blog

## ⚙️ Stwórz i aktywuj środowisko wirtualne

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

## ⚙️ Zainstaluj zależności

```bash
pip install -r requirements.txt

🧱 Inicjalizacja bazy danych

```bash
flask db init         # tylko za pierwszym razem
flask db migrate -m "Initial migration"
flask db upgrade

🚀 Uruchom aplikację

```bash
flask run

💬 Użycie w Flask Shell

```bash
flask shell

