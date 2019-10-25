import json
from bson import ObjectId
 
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if o.isJsonRegiteredType:
            return json.dumps(o.__dict__,sort_keys=True, indent=4)
        return json.JSONEncoder.default(self, o)



class JsonConvert(object):
    mappings = {}
     
    @classmethod
    def class_mapper(clsself, d):
        for keys, cls in clsself.mappings.items():
            mongo = False
            oid = None
            if len(d)>1 and '_id' in d.keys() and isinstance(d['_id'],ObjectId): 
                #This is necessary for an mongodb scenario
                oId = d['_id']
                del d['_id']
                mongo = True

            if keys.issuperset(d.keys()):   # are all required arguments present?
                if d=={} or d == None:
                    return d
                else:
                    c = cls()
                    for key in d:
                        setattr(c, key, d[key])

                    if mongo:
                        setattr(c, "_id", oId)

                    return c
            else:
                 if mongo:
                     d['_id'] = oId
        try:
            oid = d['$oid']
            id = ObjectId(oid)
            return id
        except:
            # Raise exception instead of silently returning None
            raise ValueError('Unable to find a matching class for object: {!s}'.format(d))
     
    @classmethod
    def complex_handler(clsself, Obj):
        if hasattr(Obj, '__dict__'):
            return Obj.__dict__
        else:
            raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj)))
 
    @classmethod
    def register(clsself, cls):
        try:
            clsself.mappings[frozenset(tuple([attr for attr,val in cls().__dict__.items()]))] = cls
            cls.isJsonRegiteredType = True
            return cls
        except Exception as e:
             raise TypeError('Object of type %s raised the following error while trying to register:  %s' % (cls, e))
 

    @classmethod
    def ToJSON(clsself, obj):
        if isinstance(obj,list):
            return JSONEncoder().encode(obj)
        else:
            return json.dumps(obj.__dict__, default=clsself.complex_handler, indent=4)
 
    @classmethod
    def FromJSON(clsself, json_str):
        return json.loads(json_str, object_hook=clsself.class_mapper)
     
    @classmethod
    def ToFile(clsself, obj, path):
        with open(path, 'w') as jfile:
            jfile.writelines([clsself.ToJSON(obj)])
        return path
 
    @classmethod
    def FromFile(clsself, filepath):
        result = None
        with open(filepath, 'r') as jfile:
            result = clsself.FromJSON(jfile.read())
        return result