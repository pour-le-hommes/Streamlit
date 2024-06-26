from utils.database import init_db

class MyData(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance
    
    def __init__(self):
        self._dbskills = None
        self._localskills = None
        self._tasks = None

    def dbskills(self):
        return self._dbskills
    
    def localskills(self):
        return self._localskills
    
    def input_dbskills(self,skills):
        self._dbskills = skills
        return "Skills have been stored"
    
    def input_localskills(self,skills):
        self._localskills = skills
        return "Skills have been stored"
    
    def skills_retrieval():
        singletonInstance = MyData()

        skills = singletonInstance.localskills()
        if skills == None:
            db = init_db()
            response = db.table('LifeRPG_Skills').select("name","desc","level","exp","currentLevelExp","untilNextLevelExp").execute()
            singletonInstance.input_localskills(response.data)
            skills = response.data

        return skills