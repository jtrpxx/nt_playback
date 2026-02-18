import os
import sys
from pathlib import Path
import django
from django.db import connection

# Ensure `backend` directory is on sys.path so `config` package is importable
BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

with connection.cursor() as cur:
    print('Columns for django_migrations:')
    cur.execute("""
    SELECT column_name, column_default, is_nullable, data_type
    FROM information_schema.columns
    WHERE table_name = 'django_migrations'
    ORDER BY ordinal_position
    """)
    for row in cur.fetchall():
        print(row)

    print('\nSequence for django_migrations.id (pg_get_serial_sequence):')
    cur.execute("SELECT pg_get_serial_sequence('django_migrations','id')")
    seq = cur.fetchone()[0]
    print('sequence_name =', seq)

    if seq:
        cur.execute(f"SELECT last_value, is_called FROM {seq}")
        print('sequence state:', cur.fetchone())

    print('\nExample insert test (no commit): trying to insert to django_migrations with no id to see behavior')
    try:
        cur.execute("BEGIN")
        cur.execute("INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, now()) RETURNING id", ('licenses', '0001_initial'))
        res = cur.fetchone()
        print('insert returned id =', res)
    except Exception as e:
        print('insert error:', e)
    finally:
        cur.execute('ROLLBACK')
