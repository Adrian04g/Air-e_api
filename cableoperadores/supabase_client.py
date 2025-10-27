# tu_app/supabase_client.py

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")

# ⚠️ Nota: El cliente de Supabase se inicializa una sola vez
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    raise EnvironmentError("Las variables SUPABASE_URL y SUPABASE_KEY no están configuradas.")