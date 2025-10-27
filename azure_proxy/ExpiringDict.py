import asyncio
import time
from typing import Any, Iterator, Optional, MutableMapping
from collections.abc import MutableMapping as _MutableMapping

class ExpiringDict(_MutableMapping[str, Any]):
    """
    Dict-like úložiště s TTL pro každou položku.
    - Přímé přiřazení přes obj[key] = value nastaví TTL = default_ttl_sec.
    - Pro individuální TTL použij set(key, value, ttl_sec=...).
    - Čtení expirovaných klíčů se chová jako „KeyError“ / „není v dictu“.
    - Lze spustit background „sweeper“ (periodicky uklízí expirované položky).
    """
    def __init__(
        self,
        default_ttl_sec: int = 3600,
        sweep_interval_sec: int = 60,
        auto_start: bool = True,
        refresh_on_get = False
    ) -> None:
        self._data: dict[str, tuple[Any, float]] = {}  # key -> (value, expires_at)
        self._default_ttl = max(1, int(default_ttl_sec))
        self._sweep_interval = max(1, int(sweep_interval_sec))
        self._task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()
        self._refresh_on_get = refresh_on_get
        if auto_start:
            self.start()

    # ------- dict-like API (MutableMapping) -------

    def __contains__(self, key: object) -> bool:  # type: ignore[override]
        if not isinstance(key, str):
            return False
        item = self._data.get(key)
        if not item:
            return False
        _, exp = item
        if time.time() >= exp:
            # len()/iter() by měly působit, že položka neexistuje
            self._data.pop(key, None)
            return False
        return True

    def __getitem__(self, key: str) -> Any:
        item = self._data.get(key)
        if not item:
            raise KeyError(key)
        value, exp = item
        if time.time() >= exp:
            self._data.pop(key, None)
            raise KeyError(key)
        if self._refresh_on_get:
            # obnovíme TTL
            exp = time.time() + self._default_ttl
            self._data[key] = (value, exp)
        return value

    def __setitem__(self, key: str, value: Any) -> None:
        exp = time.time() + self._default_ttl
        self._data[key] = (value, exp)

    def __delitem__(self, key: str) -> None:
        if key not in self:
            raise KeyError(key)
        self._data.pop(key, None)

    def __iter__(self) -> Iterator[str]:
        # iterujeme jen neexpirované klíče
        now = time.time()
        expired = [k for k, (_, exp) in self._data.items() if exp <= now]
        for k in expired:
            self._data.pop(k, None)
        return iter(self._data.keys())

    def __len__(self) -> int:
        # spočítáme pouze neexpirované
        now = time.time()
        expired = [k for k, (_, exp) in self._data.items() if exp <= now]
        for k in expired:
            self._data.pop(k, None)
        return len(self._data)

    # ------- rozšíření pro TTL -------

    def set(self, key: str, value: Any, ttl_sec: Optional[int] = None) -> None:
        """Explicitní nastavení TTL pro daný klíč."""
        ttl = self._default_ttl if ttl_sec is None else max(1, int(ttl_sec))
        self._data[key] = (value, time.time() + ttl)

    def get(self, key: str, default: Any = None) -> Any:  # type: ignore[override]
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: str, default: Any = ...):  # type: ignore[override]
        try:
            val = self[key]
            self._data.pop(key, None)
            return val
        except KeyError:
            if default is ...:
                raise
            return default

    def setdefault(self, key: str, default: Any = None, ttl_sec: Optional[int] = None) -> Any:
        if key in self:
            return self[key]
        self.set(key, default, ttl_sec=ttl_sec)
        return default

    def clear(self) -> None:  # type: ignore[override]
        self._data.clear()

    def update(self, *args, ttl_sec: Optional[int] = None, **kwargs) -> None:  # type: ignore[override]
        # zachováme chování dict.update, ale s možností TTL pro všechny položky
        if args:
            other = dict(args[0])
            for k, v in other.items():
                self.set(k, v, ttl_sec=ttl_sec)
        for k, v in kwargs.items():
            self.set(k, v, ttl_sec=ttl_sec)

    # ------- async „sweeper“ -------

    async def _sweeper(self) -> None:
        try:
            while True:
                await asyncio.sleep(self._sweep_interval)
                now = time.time()
                # zamykáme, pokud někde používáš store z více requestů zároveň
                async with self._lock:
                    expired = [k for k, (_, exp) in self._data.items() if exp <= now]
                    for k in expired:
                        self._data.pop(k, None)
        except asyncio.CancelledError:
            pass

    def start(self) -> None:
        if self._task is None:
            loop = asyncio.get_running_loop()
            self._task = loop.create_task(self._sweeper())

    def stop(self) -> None:
        if self._task:
            self._task.cancel()
            self._task = None
