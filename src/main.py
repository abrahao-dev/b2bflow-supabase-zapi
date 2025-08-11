import logging

from settings import get_settings
from supa_client import SupaClient
from util import setup_logging
from zapi_client import ZapiClient


def run() -> int:
    st = get_settings()
    setup_logging(st.log_level)
    log = logging.getLogger("app")
    log.info("Starting job…")

    supa = SupaClient(st)
    zapi = ZapiClient(st)

    contacts = supa.fetch_contacts(limit=st.max_messages)
    if not contacts:
        log.warning("No contacts found")
        return 0

    ok = 0
    failed = []
    sent = []

    for c in contacts:
        if zapi.send_message(c.nome, c.phone_e164):
            ok += 1
            sent.append(c.phone_e164)
        else:
            failed.append(c.phone_e164)

    log.info(f"Done: {ok}/{len(contacts)} sent.")
    if sent:
        log.info(f"Sent to: {', '.join(sent)}")
    if failed:
        log.warning(f"Failed to send to: {', '.join(failed)}")

    return 0

if __name__ == "__main__":
    raise SystemExit(run())
