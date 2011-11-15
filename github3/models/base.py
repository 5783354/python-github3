"""
github3.models
~~~~~~~~~~~~~~

This package provides the Github3 object model.
"""

class BaseResource(object):
    """A BaseResource object."""

    def __init__(self, attrs=None):
        if attrs:
            for attr, value in attrs.items():
                setattr(self, attr, value)
        super(BaseResource, self).__init__()

    def __len__(self):
        return len(self.__dict__)

    @classmethod
    def idl(self):
        raise NotImplementedError('Each model need subcass that method')
