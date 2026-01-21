โปรเจคนี้เป็นตัวอย่างสแต็กแบบแยกระหว่าง API (Django) และ frontend (Vue 3) ที่ใช้ PostgreSQL และรันด้วย Docker

โครงสร้างหลักของโปรเจค

project-root/
│ 
├── backend/ # Django (API only)
│ ├── Dockerfile
├── manage.py
├── requirements.txt
│
│ ├── config/ # Django project config
│ ├── **init**.py
│ ├── asgi.py
│ ├── wsgi.py
│ ├── urls.py # main router
│ └── settings.py # โหลดค่า env (python-dotenv)
|
│ ├── apps/ # Django apps
│ │ ├── core/ # shared logic
│ │ │ ├── **init**.py
│ │ ├── services.py # business logic
│ │ ├── utils.py # helper functions
│ │ └── permissions.py # shared permissions
│
│ └── tests/ # backend tests
│ ├── **init**.py
│
├── frontend/ # Vue 3
│ ├── Dockerfile
├── index.html
├── package.json
├── vite.config.js
│
│ └── src/
│ ├── main.js
├── App.vue
│
│ ├── api/ # call Django API
│ ├── axios.js
│ ├── auth.api.js
│ └── users.api.js
│
│ ├── router/
│ └── index.js
│
│ ├── stores/ # Pinia
│ └── auth.store.js
│
│ ├── views/ # pages
│ ├── Login.vue
│ ├── Dashboard.vue
│ └── Users.vue
│
│ ├── components/ # reusable UI
│ ├── BaseButton.vue
│ ├── BaseModal.vue
│ └── Navbar.vue
│
│ ├── assets/
│ ├── css/
│ │ ├── base.css # reset / typography
│ │ ├── components.css # buttons / forms
│ │
│ └── images/
│
│ └── utils/
└── storage.js # localStorage helpers
│
├── .env (ไม่ควร commit)
├── docker-compose.yml
└── README.md

**Quick start (development)**

- คัดลอก `.env.example` เป็น `.env` แล้วแก้ค่า (เช่น `SECRET_KEY`, `POSTGRES_*`)

```bash
cp .env.example .env
```

- รันด้วย Docker Compose (จะ build image และรัน container):

```bash
docker compose up --build
```

- Backend: ถ้าต้องการรัน migration / สร้าง superuser:

```bash
docker compose run --rm backend python manage.py migrate
docker compose run --rm backend python manage.py createsuperuser
```

- Frontend (ถ้าไม่ใช้ container):

```bash
cd frontend
npm install
npm run dev
```

**สังเกต / คำแนะนำสำคัญ**

- ค่า configuration ใน `backend/config/settings.py` ถูกอ่านจาก environment variables (และจะโหลด `.env` ผ่าน `python-dotenv` ถ้ามี) — อย่าฝัง `SECRET_KEY` จริงใน repo
- ใน `docker-compose.yml` service `db` ใช้ PostgreSQL; service `backend` ขึ้นกับ `db`
- สำหรับ production: ตั้ง `DEBUG=False`, ตั้งค่า `ALLOWED_HOSTS` และใช้ secret manager / env injection แทนไฟล์ `.env` ที่เก็บใน repo

**ไฟล์สำคัญ**

- `backend/config/settings.py`: การตั้งค่า Django
- `backend/requirements.txt`: รายการ Python deps (รวม `python-dotenv` และ `psycopg2-binary`)
- `frontend/package.json`: สคริปต์ `dev` / `build`
- `docker-compose.yml`: orchestration ของ `db`, `backend`, `frontend`

