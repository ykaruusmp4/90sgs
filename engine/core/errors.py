"""Exceções da engine."""


class EngineError(Exception):
    """Base para erros da engine."""


class ResourceError(EngineError):
    """Shader, fonte, textura ou outro recurso ausente/inválido."""


class SceneError(EngineError):
    """Cena não registrada, registro duplicado ou troca inválida."""
