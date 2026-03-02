import sys
from pathlib import Path

# Make sure backend package is importable
BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
from django.conf import settings

django.setup()

from django.contrib.sessions.backends.db import SessionStore as DBSessionStore
from django.contrib.sessions.models import Session


def decode_db_session(session_key: str):
    try:
        # Try to load via SessionStore
        store = DBSessionStore(session_key=session_key)
        data = store.load()
        print('Decoded session data (via SessionStore):')
        print(data)
        return
    except Exception as e:
        print('SessionStore.load() failed with:', repr(e))

    try:
        # Fallback: read raw session_data from DB and show it
        s = Session.objects.get(session_key=session_key)
        print('\nRaw session record:')
        print('expire_date =', s.expire_date)
        print('session_data (raw) =', s.session_data[:200] + ('...' if len(s.session_data) > 200 else ''))
    except Session.DoesNotExist:
        print('No session found with key', session_key)
    except Exception as e:
        print('Reading raw session failed with:', repr(e))


def usage():
    print('Usage: python decode_session.py <session_key>')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(2)

    session_key = sys.argv[1]
    print('Django settings: SESSION_ENGINE=%r, SESSION_SERIALIZER=%r' % (
        settings.SESSION_ENGINE, getattr(settings, 'SESSION_SERIALIZER', None)
    ))
    decode_db_session(session_key)
