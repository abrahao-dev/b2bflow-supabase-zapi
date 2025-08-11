from types import SimpleNamespace

from src.zapi_client import ZapiClient


def test_message_format():
    st = SimpleNamespace(
        zapi_base_url="http://test",
        zapi_instance_id="x",
        zapi_token="y",
        dry_run=True,
        log_level="INFO",
        max_messages=3
    )
    # só valida que a função não explode em DRY_RUN
    z = ZapiClient(st)
    assert z.send_message("Matheus", "+5511999999999") is True

def test_phone_validation():
    st = SimpleNamespace(
        zapi_base_url="http://test",
        zapi_instance_id="x",
        zapi_token="y",
        dry_run=True,
        log_level="INFO",
        max_messages=3
    )
    z = ZapiClient(st)

    # Teste telefones válidos
    assert z._validate_phone("+5511999999999") is True
    assert z._validate_phone("+1234567890") is True

    # Teste telefones inválidos
    assert z._validate_phone("5511999999999") is False  # sem +
    assert z._validate_phone("+551199999999") is False  # muito curto
    assert z._validate_phone("+05511999999999") is False  # começa com 0
    assert z._validate_phone("abc") is False  # não é número
