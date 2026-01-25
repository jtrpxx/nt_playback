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

**Using flatpickr in frontend (directive)**

- We provide a reusable Vue directive `v-flatpickr` (registered in `main.js`) to attach Flatpickr to inputs without repeating lifecycle code.
- Supported binding patterns:
	- Object form (recommended):
		- `<input v-flatpickr="{ target: filters, key: 'from', options: { minDate: '2025-01-01' } }" />`
		- Directive will set `filters.from = '<date string>'` when user picks a date.
	- Arg form (concise):
		- `<input v-flatpickr:from="filters" />` — shorthand for object form where `key` is the argument (`from`) and `target` is the bound object (`filters`).
	- Function form (callback):
		- `<input v-flatpickr="(dates, str) => filters.from = str" />` — pass a function to receive change events directly.

- Options: pass flatpickr options via `options` in object form. The directive defaults include `enableTime: true`, `dateFormat: 'Y-m-d H:i'`, `time_24hr: true`, and default hour/minute set to `00:00`.

- Cleanup: the directive destroys the flatpickr instance automatically when the element unmounts.

Examples (Home.vue):

```vue
<script setup>
import { reactive, ref } from 'vue'
const filters = reactive({ from: '', to: '' })
</script>

<template>
	<input v-flatpickr:from="filters" />
	<input v-flatpickr:to="filters" />
</template>
```

If you prefer `v-model`-like syntax (`v-flatpickr="filters.from"`) note that template expressions are evaluated and the directive receives the value (not the path), so the directive cannot write back to that path. Use the `arg` form (`v-flatpickr:from="filters"`) or pass a setter function instead.

---

คู่มือภาษาไทย (สรุปการใช้ `v-flatpickr`)

- เรามี directive `v-flatpickr` ที่ลงทะเบียนใน `main.js` เพื่อผูก Flatpickr เข้ากับ input โดยไม่ต้องเขียน lifecycle init/cleanup ซ้ำในทุก component
- รูปแบบการใช้งานที่รองรับ:
	- Object form (แนะนำ):
		- `<input v-flatpickr="{ target: filters, key: 'from', options: { minDate: '2025-01-01' } }" />`
		- เมื่่อผู้ใช้เลือกวันที่ directive จะตั้ง `filters.from = '<date string>'`
	- Arg form (สั้น):
		- `<input v-flatpickr:from="filters" />` — เป็น shorthand ที่ `key` มาจาก argument (`from`) และ `target` คือ object ที่ bind (`filters`)
	- Function form (callback):
		- `<input v-flatpickr="(dates, str) => filters.from = str" />` — ส่งฟังก์ชันเพื่อรับ event เมื่อวันที่เปลี่ยน

- ค่าเริ่มต้น: directive ตั้งค่า default เป็น `enableTime: true`, `dateFormat: 'Y-m-d H:i'`, `time_24hr: true`, และ `defaultHour/defaultMinute` เป็น `00:00` เพื่อให้เวลาเริ่มต้นเป็น `00:00`
- Cleanup: directive จะทำการ `destroy()` instance ให้อัตโนมัติเมื่อ element ถูก unmount

ข้อสังเกต:
- ถ้าต้องการเขียนค่าเข้า object reactive ให้ใช้ `v-flatpickr:from="filters"` หรือ object form
- การใช้ `v-flatpickr="filters.from"` แบบ v-model ไม่สามารถเขียนกลับได้ (เพราะ template ส่งค่า ไม่ใช่ path)

ตัวอย่าง (Home.vue):

```vue
<script setup>
import { reactive } from 'vue'
const filters = reactive({ from: '', to: '' })
</script>

<template>
	<input v-flatpickr:from="filters" />
	<input v-flatpickr:to="filters" />
</template>
```

