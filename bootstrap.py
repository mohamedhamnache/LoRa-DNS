import uuid

id = uuid.uuid1()

id = id.hex[:8]
print(id)
