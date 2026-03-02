"""Check and report Django DB sessions that fail to decode.

Run from the `backend` folder where Django settings are available:

    python scripts/check_all_sessions.py

Or inside Docker:

    docker compose exec backend python scripts/check_all_sessions.py

The script will print a list of session keys that raised exceptions when decoding.
"""
import sys
from pathlib import Path

# Make project importable
BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore as DBSessionStore


def main(limit=None):
    qs = Session.objects.all().order_by('-expire_date')
    if limit:
        qs = qs[:limit]

    total = qs.count()
    print(f'Total sessions checked: {total}')

    failures = []
    for s in qs:
        key = s.session_key
        try:
            store = DBSessionStore(session_key=key)
            _ = store.load()
        except Exception as e:
            failures.append((key, repr(e)))

    if not failures:
        print('No session decode failures detected.')
        return 0

    print('\nFound sessions that failed to decode:')
    for k, err in failures:
        print(f'- {k}: {err}')

    print('\nYou can remove individual broken sessions with:')
    print("python manage.py shell -c \"from django.contrib.sessions.models import Session; Session.objects.filter(session_key='<KEY>').delete()\"")
    print('\nOr remove all sessions (will log out all users):')
    print('python manage.py shell -c "from django.contrib.sessions.models import Session; Session.objects.all().delete()"')

    return 1


if __name__ == '__main__':
    arg = None
    if len(sys.argv) > 1:
        try:
            arg = int(sys.argv[1])
        except Exception:
            arg = None
    sys.exit(main(limit=arg))
