import importlib
import os


def test_manual_crypto_settings_are_available(monkeypatch):
    monkeypatch.setenv('BOT_TOKEN', 'token123:abc')
    monkeypatch.setenv('ADMIN_TELEGRAM_ID', '6505578903')
    monkeypatch.setenv('PAYMENT_BTC_ADDRESS', '1EqgNKJMmnnWpGjYZJAapDEyyXruXxLCYj')
    monkeypatch.setenv('PAYMENT_USDT_TRC20_ADDRESS', 'TZADiUxhu9Y5bvJUMbMtBgFW43KqQ1hzaD')
    monkeypatch.setenv('PAYMENT_USDC_ADDRESS', '0xfe601096668c46d4bb0bd4e3c93751a3a8f4b3e5')
    monkeypatch.setenv('AUTO_CONFIRM', 'true')

    import config.settings as settings_module
    importlib.reload(settings_module)

    settings = settings_module.Settings()
    assert settings.PAYMENT_BTC_ADDRESS == '1EqgNKJMmnnWpGjYZJAapDEyyXruXxLCYj'
    assert settings.PAYMENT_USDT_TRC20_ADDRESS == 'TZADiUxhu9Y5bvJUMbMtBgFW43KqQ1hzaD'
    assert settings.PAYMENT_USDC_ADDRESS == '0xfe601096668c46d4bb0bd4e3c93751a3a8f4b3e5'
    assert settings.AUTO_CONFIRM is True


def test_manual_crypto_payment_method_exists():
    from database.models import PaymentMethod
    values = {item.value for item in PaymentMethod}
    assert 'manual_crypto' in values
