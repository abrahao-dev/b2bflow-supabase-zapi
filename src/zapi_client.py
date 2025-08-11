import logging
import re

import httpx

from settings import Settings
from util import retry

log = logging.getLogger("zapi")

def _normalize_phone(phone: str) -> str:
    # remove tudo que não é dígito
    digits = re.sub(r"\D", "", phone)
    # opcional: validar que começa com DDI (ex: 55)
    if not digits.startswith("55"):
        log.warning(f"Phone sem DDI 55? Enviando assim mesmo: {digits}")
    return digits

class ZapiClient:
    def __init__(self, st: Settings):
        self.st = st
        self._client = httpx.Client(timeout=20, headers={
            "Content-Type": "application/json",
            # se você ativou o Account security token, este header é obrigatório:
            "Client-Token": getattr(st, "zapi_client_token", "") or "",
        })

    def _endpoint(self) -> str:
        # Endpoint específico da instância b2bflow-teste
        return f"{self.st.zapi_base_url}/instances/{self.st.zapi_instance_id}/token/{self.st.zapi_token}/send-text"

    def _validate_phone(self, phone: str) -> bool:
        # Validação simples de formato E.164
        pattern = r'^\+[1-9]\d{1,14}$'
        return bool(re.match(pattern, phone))

    def _post(self, payload: dict):
        return retry(
            lambda: self._client.post(self._endpoint(), json=payload),
            (httpx.RequestError, httpx.HTTPStatusError),
            tries=3,
            base=0.5
        )()

    def send_message(self, nome: str, phone_e164: str) -> bool:
        if not self._validate_phone(phone_e164):
            log.error(f"Invalid phone format: {phone_e164}")
            return False

        text = f"Olá {nome}, tudo bem com você?"
        phone = _normalize_phone(phone_e164)
        payload = {
            "phone": phone,
            "message": text
        }

        if self.st.dry_run:
            log.info(f"[DRY_RUN] Would send to {phone}: {text}")
            return True

        try:
            resp = self._post(payload)
            if resp.status_code // 100 == 2:
                log.info(f"Sent to {phone}")
                return True
            log.error(f"Failed to send to {phone}: {resp.status_code} {resp.text}")
            return False
        except Exception as e:
            log.error(f"Error sending to {phone}: {e}")
            return False
