from enum import Enum

class ArtifactType(Enum):
    SCRIPT = 1
    AUDIO = 2
    VIDEO = 3
    
class Status(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    
class Guardrail(Enum):
    TYPE_GREETING = "greeting"
    TYPE_RELEVANCE = "relevance"
    