import json
from yondeokuApp import User, Word

class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {
                "id": obj.id,
                "username": obj.username,
                "threshold": obj.threshold,
                "known": obj.known,
                "blocks": obj.blocks
            }
        if isinstance(obj, Block):
            return {
                "id": obj.id
            }
        if isinstance(obj, Word):
            return {
                "language": obj.language,
                "word": obj.word
            }
        if isinstance(obj, set):
            return list(obj)
        return super(ModelEncoder, self).default(obj)
