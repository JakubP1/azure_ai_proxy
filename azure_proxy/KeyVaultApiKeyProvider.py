# kv_provider.py
import os, time, asyncio
from typing import Optional, Tuple
from azure.identity.aio import DefaultAzureCredential
from azure.keyvault.secrets.aio import SecretClient

class KeyVaultApiKeyProvider:
    def __init__(self, *, vault_url: str, secret_name: str, ttl_seconds: int = 300):
        self.vault_url = vault_url
        self.secret_name = secret_name
        self.ttl = ttl_seconds
        self._lock = asyncio.Lock()
        self._cached: Tuple[Optional[str], float] = (None, 0.0)
        self._cred: Optional[DefaultAzureCredential] = None
        self._client: Optional[SecretClient] = None

    async def start(self):
        if self._cred is None:
            self._cred = DefaultAzureCredential()
            self._client = SecretClient(self.vault_url, self._cred)

    async def close(self):
        if self._client: await self._client.close()
        if self._cred: await self._cred.close()

    async def _fetch_now(self) -> str:
        assert self._client is not None
        secret = await self._client.get_secret(self.secret_name)  # bere nejnovější verzi
        return secret.value

    async def get(self, *, force_refresh: bool = False) -> str:
        now = time.time()
        val, exp = self._cached
        if (not val) or force_refresh or now >= exp:
            async with self._lock:
                val2, exp2 = self._cached
                if (not val2) or force_refresh or now >= exp2:
                    fresh = await self._fetch_now()
                    self._cached = (fresh, now + self.ttl)
                    return fresh
                return val2
        return val

    async def invalidate(self):
        async with self._lock:
            self._cached = (None, 0.0)
