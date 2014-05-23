
class Attributes(object):

    def __init__(self):
        """
        : attribute id : string
        : attribute value : string
        """
        self.id = None
        self.value = None


class BasicSubscription(object):

    def __init__(self):
        """
        : attribute id : string
        : attribute last_modified : string
        : attribute created : string
        : attribute allow_tags : bool
        : attribute attributes : array
        """
        self.id= None
        self.lastModified = None
        self.created = None
        self.allowTags = None
        self.attributes = Attributes()
       

def jdefault(o):
    if isinstance(o, BasicSubscription):
        return o.__dict__
    elif isinstance(o, Attributes):
        return o.__dict__


