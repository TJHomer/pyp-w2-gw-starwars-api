from starwars_api.client import SWAPIClient
from starwars_api.exceptions import SWAPIClientError


api_client = SWAPIClient()


class BaseModel(object):

    def __init__(self, json_data):
        for key, value in json_data.items():
            setattr(self,key,value)

    @classmethod
    def get(cls, resource_id):
        get_func = getattr(
        api_client,
        'get_{}'.format(cls.RESOURCE_NAME)
        )

        json_data = get_func(resource_id)

        # return a new instance created based on the json_data
        return cls(json_data)


    @classmethod
    def all(cls):
        get_func = getattr(
        api_client,
        'get_{}'.format(cls.RESOURCE_NAME)
        )

        json_data = get_func()

        query = '{}QuerySet'.format(cls.RESOURCE_NAME.title())
        return eval(query)(json_data)


class People(BaseModel):
    """Representing a single person"""
    RESOURCE_NAME = 'people'

    def __init__(self, json_data):
        super(People, self).__init__(json_data)

    def __repr__(self):
        return 'Person: {0}'.format(self.name)


class Films(BaseModel):
    RESOURCE_NAME = 'films'

    def __init__(self):
        super(Films, self).__init__(json_data)

    def __repr__(self):
        return 'Film: {0}'.format(self.title)


class BaseQuerySet(object):

    def __init__(self):
        get_func = getattr(
        api_client,
        'get_{}'.format(self.RESOURCE_NAME)
        )

        self.page = [1, 2]
        self.objects = []
        for page in self.page:
            json_data = get_func(page=page)
            for result in json_data['results']:
                p = eval(self.RESOURCE_NAME.title())(result)
                self.objects.append(p)
        self.objects = iter(self.objects)
        
        __next__ = next
        
    
    def __iter__(self):
        return (self.objects)


    def next(self):
        next_object = next(self.objects)
        return next_object
        
    def count(self):
        numb = 0
        for object in self.objects:
            numb += 1
        return numb

class PeopleQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'people'

    def __init__(self, model):
        super(PeopleQuerySet, self).__init__()

    def __repr__(self):
        return 'PeopleQuerySet: {0} objects'.format(str(len(self.objects)))


class FilmsQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'films'

    def __init__(self):
        super(FilmsQuerySet, self).__init__()

    def __repr__(self):
        return 'FilmsQuerySet: {0} objects'.format(str(len(self.objects)))
        
        