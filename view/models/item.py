
import json


class ItemView:
    id: int
    name: str
    description: str

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.description = kwargs['description']
        
    def __str__(self):
        return json.dumps(self.to_dict())
    
    def to_dict(self):
        return {field: getattr(self, field) for field in self.__annotations__}
