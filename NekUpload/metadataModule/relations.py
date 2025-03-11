from enum import Enum
from types import MappingProxyType
from typing import Dict

class RelationsSchemes(Enum):
    DOI = "doi"
    URL = "url"

RELATIONS_SCHEMES_REVERSE_MAP: MappingProxyType[str,RelationsSchemes] = MappingProxyType({
    "doi": RelationsSchemes.DOI,
    "url": RelationsSchemes.URL
})

class RelationType(Enum):
    CONTINUES = "continues"

RELATION_TYPE_TITLE: MappingProxyType[RelationType,Dict[str,str]] = MappingProxyType({
    RelationType.CONTINUES: {"en": "Continues"}
})

RELATIONS_TYPE_REVERSE_MAP: MappingProxyType[str,RelationType] = MappingProxyType({
    "continues": RelationType.CONTINUES
})

class ResourceType(Enum):
    DATASET = "dataset"
    PHYSICAL_OBJECT = "physicalobject"

RESOURCE_TYPE_TITLE: MappingProxyType[ResourceType,Dict[str,str]] = MappingProxyType({
    ResourceType.DATASET: {"en": "Dataset"},
    ResourceType.PHYSICAL_OBJECT: {"en": "Physical object"}
})

RESOURCE_TYPE_REVERSE_MAP: MappingProxyType[str,ResourceType] = MappingProxyType({
    "dataset": ResourceType.DATASET,
    "physical_object": ResourceType.PHYSICAL_OBJECT
})

class Relations:
    def __init__(self,
                id: str,
                scheme: RelationsSchemes,
                relation: RelationType,
                resource: ResourceType):
        self.id: str = id
        self.scheme: RelationsSchemes = scheme
        self.relation_type: RelationType = relation
        self.resource_type: ResourceType = resource

    def to_json(self):
        return {
            "identifier": self.id,
            "scheme": self.scheme.value,
            "relation_type": {
                "id": self.relation_type.value,
                "title": RELATION_TYPE_TITLE[self.relation_type]
            },
            "resource_type": {
                "id": self.resource_type.value,
                "title": RESOURCE_TYPE_TITLE[self.resource_type]
            }
        }
    
    @classmethod
    def from_json(cls,data) -> 'Relations':
        return Relations(data["identifier"],
                        RELATIONS_SCHEMES_REVERSE_MAP.get(data["scheme"]),
                        RELATIONS_TYPE_REVERSE_MAP.get(data["relation_type"]["id"]),
                        RESOURCE_TYPE_REVERSE_MAP.get(data["resource_type"]["id"]))