def get_non_null_members_as_dict(obj: object):
    return {
        name: obj.__getattribute__(name)
        for name in obj.__annotations__
        if obj.__getattribute__(name) is not None
    }
