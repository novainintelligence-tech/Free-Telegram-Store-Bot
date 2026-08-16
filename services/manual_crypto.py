"""Manual crypto transaction verification helpers."""

from __future__ import annotations

import json
from typing import Dict, Iterable, Optional
from urllib import request, error

from config.settings import settings


class ManualCryptoService:
    """Verify submitted crypto transaction hashes against configured wallet addresses."""

    @staticmethod
    def _strip(value: Optional[str]) -> str:
        return (value or '').strip()

    @staticmethod
    def _normalize(value: Optional[str]) -> str:
        return ManualCryptoService._strip(value).lower()

    @staticmethod
    def _fetch_json(url: str) -> Optional[Dict]:
        try:
            req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with request.urlopen(req, timeout=15) as resp:
                payload = resp.read().decode('utf-8', 'replace')
                if not payload:
                    return None
                return json.loads(payload)
        except (error.URLError, ValueError, json.JSONDecodeError):
            return None

    @staticmethod
    def _btc_transaction_matches(tx_hash: str, address: str) -> bool:
        if not tx_hash or not address:
            return False
        data = ManualCryptoService._fetch_json(f'https://mempool.space/api/tx/{tx_hash}')
        if not isinstance(data, dict):
            return False
        for output in data.get('vout', []):
            script_address = output.get('scriptpubkey_address') or output.get('scriptpubkey')
            if script_address and ManualCryptoService._normalize(script_address) == ManualCryptoService._normalize(address):
                return True
        return False

    @staticmethod
    def _usdt_trc20_transaction_matches(tx_hash: str, address: str) -> bool:
        if not tx_hash or not address:
            return False
        url = f'https://api.trongrid.io/v1/transactions/{tx_hash}'
        headers = {'TRON-PRO-API-KEY': settings.TRONGRID_API_KEY} if settings.TRONGRID_API_KEY else {}
        try:
            req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0', **headers})
            with request.urlopen(req, timeout=15) as resp:
                payload = resp.read().decode('utf-8', 'replace')
                data = json.loads(payload)
            tx = (data or {}).get('data') or []
            if not tx:
                return False
            tx_info = tx[0] if isinstance(tx, list) else tx
            raw_data = tx_info.get('raw_data') or {}
            contract = ((raw_data.get('contract') or [])[:1] or [{}])[0]
            to_address = (contract.get('parameter') or {}).get('value', {}).get('to_address')
            if not to_address:
                return False
            return ManualCryptoService._normalize(to_address) == ManualCryptoService._normalize(address)
        except Exception:
            return False

    @staticmethod
    def _usdc_ethereum_transaction_matches(tx_hash: str, address: str) -> bool:
        if not tx_hash or not address:
            return False
        if not settings.INFURA_URL:
            return False
        payload = {
            'jsonrpc': '2.0',
            'method': 'eth_getTransactionReceipt',
            'params': [tx_hash],
            'id': 1,
        }
        try:
            req = request.Request(
                settings.INFURA_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
                method='POST'
            )
            with request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode('utf-8', 'replace'))
            result = (data or {}).get('result') or {}
            if not result or result.get('status') != '0x1':
                return False
            logs = result.get('logs') or []
            if not logs:
                return False
            normalized_address = ManualCryptoService._normalize(address)
            for log in logs:
                if ManualCryptoService._normalize(log.get('address')) == normalized_address:
                    return True
            return False
        except Exception:
            return False

    @classmethod
    def verify_transaction(cls, tx_hash: str, coin: str, amount: float = 0.0) -> bool:
        """Return True if the hash appears to be a valid payment to the configured wallet."""
        tx_hash = cls._strip(tx_hash)
        coin = (coin or '').strip().lower()
        if not tx_hash:
            return False

        if coin == 'btc':
            return cls._btc_transaction_matches(tx_hash, settings.PAYMENT_BTC_ADDRESS)
        if coin == 'usdt_trc20':
            return cls._usdt_trc20_transaction_matches(tx_hash, settings.PAYMENT_USDT_TRC20_ADDRESS)
        if coin in {'usdc', 'usdc_ethereum'}:
            return cls._usdc_ethereum_transaction_matches(tx_hash, settings.PAYMENT_USDC_ADDRESS)
        return False
