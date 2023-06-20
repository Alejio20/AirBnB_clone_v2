"""Base model for all other classes"""

import uuid
from datetime import datetime
import models


class BaseModel():
    """BaseModel class definition"""

    def __init__(self, *args, **kwargs):
        """Initialize the BaseModel class"""

        if kwargs is not None and kwargs != {}:
            time_format = "%Y-%m-%dT%H:%M:%S.%f"

            for key, val in kwargs.items():
                if key == "created_at":
                    self.__dict__[key] = datetime.strptime(val, time_format)
                elif key == "updated_at":
                    self.__dict__[key] = datetime.strptime(val, time_format)
                else:
                    self.__dict__[key] = val
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """print() & str() representation of BaseModel"""

        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """updates the public instance attribute
        updated_at with the current datetime"""

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values
        of __dict__ of the instance"""

        base_dict = self.__dict__.copy()
        base_dict["__class__"] = type(self).__name__
        base_dict["created_at"] = base_dict["created_at"].isoformat()
        base_dict["updated_at"] = base_dict["updated_at"].isoformat()
        return base_dict
