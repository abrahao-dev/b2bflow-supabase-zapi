import logging
from dataclasses import dataclass

from supabase import Client, create_client

from settings import Settings

log = logging.getLogger("supa")

@dataclass
class Contact:
    nome: str
    phone_e164: str

class SupaClient:
    def __init__(self, st: Settings):
        self.client: Client = create_client(st.supabase_url, st.supabase_key)

    def fetch_contacts(self, limit: int = 3) -> list[Contact]:
        res = (
            self.client.table("contacts")
            .select("nome, phone_e164")
            .eq("is_active", True)
            .limit(limit)
            .execute()
        )
        rows = res.data or []
        contacts = [Contact(nome=r["nome"], phone_e164=r["phone_e164"]) for r in rows]
        log.info(f"Fetched {len(contacts)} contact(s) from Supabase")
        return contacts
