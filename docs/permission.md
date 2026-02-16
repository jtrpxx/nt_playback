# สรุปการเพิ่มระบบตรวจสิทธิ์ (Permissions)

เอกสารสั้น ๆ อธิบายการเปลี่ยนแปลงและแนวทางการใช้งานที่ผมได้เพิ่มไว้ในโปรเจค

## แนวคิดหลัก
- สิทธิ์ของผู้ใช้เก็บแบบ Role/Permission: ตารางต้นทาง `tb_userauth` -> `tb_user_permission_detail` (เฉพาะ `status = true` นับว่าอนุญาต)
- Backend: สร้าง helper เพื่อดึงรายการ `action` ที่ผู้ใช้มี และ decorator `require_action(action_name)` เพื่อป้องกัน view-level
- Frontend: ดึงรายการ permission หลังล็อกอินมาเก็บใน Pinia store (`auth`), ใช้ `hasPermission(name)` สำหรับ `v-if`/ป้องกัน UI และใช้ `meta.permission` + global router guard สำหรับการเข้าถึง route
 - หมายเหตุ: ระบบจะยกเว้นการตรวจสิทธิ์สำหรับผู้ใช้ที่มี `user.id == 1` (ถือเป็น root user)

---

## ไฟล์ที่เพิ่ม/แก้ไขสำคัญ
- Backend
  - `backend/apps/core/utils/permissions.py` :
    - `get_user_actions(user)` — คืน list/set ของ action ที่ผู้ใช้มี (จาก `UserAuth` → `UserPermissionDetail`)
    - `require_action(action_name)` — decorator สำหรับ view (คืน 401 ถ้ายังไม่ auth, 403 ถ้าไม่มีสิทธิ์)
  - `backend/apps/home/views.py` :
    - เพิ่ม `ApiGetMyPermissions` API: `/api/my-permissions/` — คืน JSON `{ status: 'success', permissions: [...] }`
    - เพิ่ม `@require_action('Play audio')` ให้ `ApiLogPlayAudio`
    - เพิ่ม `@require_action('Save file')` ให้ `ApiLogSaveFile`
  - `backend/apps/log_user/views.py` และ `backend/apps/core/log_user/views.py` : เพิ่มการเช็คสิทธิ์สำหรับการเรียกดู log ตาม `type` (เช่น `System Logs`, `Audit Logs`, `User Logs`) โดยเรียก `get_user_actions(request.user)` และคืน 403 เมื่อไม่มีสิทธิ์
  - ตัวอย่างอื่น ๆ (ตัวอย่าง): `backend/apps/user_management/views.py` ถูกตกแต่งด้วย `@require_action` ในหลาย endpoint (เช่น `Change Status`, `Delete User`, `Access Role & Permissions`, `Edit User`) — เพื่อป้องกันการสร้าง/แก้ไข/ลบ

- Frontend
  - `frontend/src/stores/auth.store.js` :
    - เก็บ `permissions` ใน state (persisted via localStorage)
    - `fetchPermissions()` เรียก `/api/my-permissions/` แล้วบันทึก
    - `hasPermission(name)` ตรวจการมี permission
  - `frontend/src/main.js` :
    - เมื่อเริ่มแอป ถ้ามี user ใน localStorage จะเรียก `auth.fetchPermissions()` เพื่อเตรียมการ
  - `frontend/src/router/index.js` :
    - ใช้ `meta.permission` ใน route (เมื่อกำหนด) และ global `beforeEach` เพื่อ redirect ไปหน้า `Denied` ถ้าไม่มีสิทธิ์
  - `frontend/src/views/Home.vue` :
    - ซ่อน/บล็อคเมนู Export ถ้าไม่มี `Export Recordings`
  - `frontend/src/views/UserLog.vue` :
    - ซ่อน/บล็อคการ Export/Filter ถ้าไม่มี `Export Logs` / `User Logs` ตาม `type`
  - `frontend/src/components/AudioPlayer.vue` :
    - ปุ่มดาวน์โหลดจะมี `v-if="canDownload"` ซึ่งมาจาก `authStore.hasPermission('Download Audio')`

---

## API ใหม่ / ที่สำคัญ
- `GET /api/my-permissions/` — คืน JSON แบบ `{ status: 'success', permissions: ['Play audio', 'Download Audio', ...] }`
  - ใช้โดย frontend หลังล็อกอิน หรือเมื่อเริ่มแอป เพื่อเก็บ permissions ลงใน `auth` store

## วิธีใช้งาน / แนวทางเพิ่มการป้องกันใหม่
- เพิ่ม permission ใหม่ในฐานข้อมูล (ข้อมูลปกติอยู่ใน `tb_user_permission_detail`) ให้ `action` ตรงกับ string ที่จะใช้ในโค้ด เช่น `Export Recordings` หรือ `Delete User` และให้ `status = true` สำหรับ role ที่ต้องการ
- ป้องกัน backend view (Django):
  - ถ้าเป็น view แบบฟังก์ชัน ให้เพิ่ม `@require_action('Action Name')` เหนือฟังก์ชัน เช่น:

```python
from apps.core.utils.permissions import require_action

@require_action('Delete User')
def ApiDeleteUser(request, user_id):
    ...
```

  - ถ้าเป็น class-based view ให้เรียกตรวจภายใน `dispatch` หรือ method ที่เกี่ยวข้อง โดยใช้ `get_user_actions(request.user)` เพื่อเช็ค
- ป้องกัน frontend:
  - ซ่อนปุ่ม/เมนูด้วย `v-if="authStore.hasPermission('Action Name')"`
  - สำหรับการเรียก API จากปุ่ม ให้เช็คก่อนเรียก เช่น `if (!authStore.hasPermission('Delete User')) { /* show denied */ return }`
  - ถ้าต้องการบล็อคการเข้าถึงทาง URL ให้ใส่ `meta.permission` ใน `router` และใช้ global guard (โปรเจคนี้มีตัวอย่างแล้ว)

## ตัวอย่างการเพิ่มการป้องกัน (เต็มสเต็ป)
1. ใน DB: เพิ่ม `action='Export Recordings'` กับ `status=true` ให้ role ที่ต้องการ
2. Backend: ถ้ามี endpoint สร้างไฟล์ export (เช่น `api/export/records/`) ให้เพิ่ม `@require_action('Export Recordings')`
3. Frontend: ใน `Home.vue` หรือตรงปุ่ม Export ให้ใช้ `v-if="authStore.hasPermission('Export Recordings')"` และเช็คในฟังก์ชันก่อนเรียก `exportTableToFormat()`

## การทดสอบแบบรวดเร็ว
- ล็อกอินด้วยผู้ใช้ที่มี/ไม่มี permission ต่างกัน
- ตรวจว่าเมนู/ปุ่มที่เกี่ยวข้องแสดง/ซ่อนตามคาด
- เรียก API ที่ถูกป้องกันโดยตรง (เช่น POST ไปยัง endpoint) โดยใช้ HTTP client เพื่อยืนยันว่า backend คืน 403 ถ้าไม่มีสิทธิ์

## ไฟล์ที่แก้ไข (สรุป path)
- backend/apps/core/utils/permissions.py
- backend/apps/home/views.py
- backend/apps/home/urls.py (route สำหรับ `/api/my-permissions/`)
- backend/apps/log_user/views.py
- backend/apps/core/log_user/views.py
- backend/apps/user_management/views.py (ตัวอย่างการใช้ decorator)
- frontend/src/stores/auth.store.js
- frontend/src/router/index.js
- frontend/src/views/Home.vue
- frontend/src/views/UserLog.vue
- frontend/src/components/AudioPlayer.vue
- frontend/src/main.js

## ข้อเสนอแนะเพิ่มเติม
- เก็บชื่อ `action` เป็น constants (ไฟล์เดียว) เพื่อป้องกัน typo
- พิจารณาเพิ่ม caching (Redis) สำหรับ `get_user_actions` เมื่อระบบมีผู้ใช้จำนวนมาก
- เพิ่ม unit/integration tests สำหรับ decorator และ router guard

---