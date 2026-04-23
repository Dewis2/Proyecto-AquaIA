from enum import Enum


class UserRole(str, Enum):
    operador = "operador"
    analista = "analista"
    administrador = "administrador"


class ZoneType(str, Enum):
    urbana = "urbana"
    periurbana = "periurbana"
    rural = "rural"


class SensorType(str, Enum):
    flujo = "flujo"
    presion = "presion"
    calidad = "calidad"


class SensorStatus(str, Enum):
    activo = "activo"
    mantenimiento = "mantenimiento"
    inactivo = "inactivo"


class AlertLevel(str, Enum):
    critica = "critica"
    alta = "alta"
    media = "media"
    baja = "baja"


class AlertState(str, Enum):
    activa = "activa"
    resuelta = "resuelta"
