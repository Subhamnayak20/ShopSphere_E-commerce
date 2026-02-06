"""Lightweight in-memory model to use when Redis is unavailable.
This implements a minimal subset of redis_om.HashModel behavior used by the services:
- save()
- pk property
- classmethods: all_pks(), get(pk), all(), find_by(attr, value)
The find() API used by redis_om is approximated via find_by.
"""
from __future__ import annotations
from typing import Any, Dict, List, Type, Optional
import uuid

_registry: Dict[str, Dict[str, Dict[str, Any]]] = {}


class QueryResult:
    def __init__(self, items: List[Dict[str, Any]]):
        self._items = items

    def all(self):
        return [dict(item) for item in self._items]


class InMemoryModel:
    def __init__(self, **kwargs):
        self._data = dict(kwargs)
        self._pk: Optional[str] = None

    def save(self):
        name = self.__class__.__name__
        if name not in _registry:
            _registry[name] = {}
        if not self._pk:
            self._pk = uuid.uuid4().hex
        _registry[name][self._pk] = dict(self._data)
        _registry[name][self._pk]["pk"] = self._pk

    @property
    def pk(self) -> Optional[str]:
        return self._pk

    def dict(self):
        d = dict(self._data)
        if self._pk:
            d["pk"] = self._pk
        return d

    # Class methods
    @classmethod
    def all_pks(cls) -> List[str]:
        name = cls.__name__
        if name not in _registry:
            return []
        return list(_registry[name].keys())

    @classmethod
    def get(cls, pk: str):
        name = cls.__name__
        if name not in _registry or pk not in _registry[name]:
            return None
        data = dict(_registry[name][pk])
        obj = cls(**{k: v for k, v in data.items() if k != "pk"})
        obj._pk = pk
        return obj

    @classmethod
    def all(cls):
        return [cls.get(pk) for pk in cls.all_pks()]

    @classmethod
    def find_by(cls, attr: str, value: Any):
        name = cls.__name__
        if name not in _registry:
            return QueryResult([])
        matches = []
        for pk, data in _registry[name].items():
            if data.get(attr) == value:
                matches.append(dict(data))
        return QueryResult(matches)
