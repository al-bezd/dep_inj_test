
import json
from pydantic import BaseModel

class ItemView(BaseModel):
    id: int
    name: str
    description: str

        
    def __str__(self):
        return json.dumps(self.to_dict())
    
    def to_dict(self):
        return {field: getattr(self, field) for field in self.__annotations__}
