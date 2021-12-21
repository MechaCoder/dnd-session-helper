from os.path import join
from requests.api import request

from tinydb_base import DatabaseBase
from requests import get
from requests.exceptions import RequestException

from .base import projectRoot

def getProfile(monster_index):
    req = get(url=f'https://www.dnd5eapi.co/api/monsters/{monster_index}')
    if req.status_code != 200:
        raise Exception('unable to get monster ({})'.format(monster_index))

    return req.json()

class DbBase(DatabaseBase):

    def __init__(self, table: str = ..., requiredKeys='name:str'):
        file = join(projectRoot(), '5e.ds.json')
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)


    def _create(self, name:str, index:str, url:str):
    
        row = {
            'name': name,
            'index': index,
            'url': url
        }
        return super().create(row)

    def _build(self):

        req = get(self.path)
        if req.status_code != 200:
            return

        # req
        data = req.json()
        if 'results' in data.keys():
            
            for each in data['results']:
                self._create(
                    name=each['name'],
                    index=each['index'],
                    url=each['url']
                )

    def readDetail(self, doc_id:int):

        doc = self.readById(doc_id)
        u = doc['url']
        req = get(url=f'https://www.dnd5eapi.co{u}')
        data = req.json()
        req.close()

        return data

class MonstersIndex(DbBase):

    def __init__(self, table: str = 'MonstersIndex', requiredKeys='name:str,index:str,url:str'):
        super().__init__(table=table, requiredKeys=requiredKeys)
        self.path = 'https://www.dnd5eapi.co/api/monsters'
        if self.readAll() == []:
            self._build()

    def _create(self, name:str, index:str, url:str):

        row = {
            'name': name,
            'index': index,
            'url': url
        }
        return super().create(row)

    def _build(self):

        req = get(self.path)
        if req.status_code != 200:
            return

        # req
        data = req.json()
        if 'results' in data.keys():
            
            for each in data['results']:
                self._create(
                    name=each['name'],
                    index=each['index'],
                    url=each['url']
                )

    def readAllIndex(self):
        a = []

        for e in self.readAll():
            a.append(e['index'])

        return a

class EquipmentIndex(DbBase):

    def __init__(self, table: str = 'EquipmentIndex', requiredKeys='name:str,index:str,url:str'):
        super().__init__(table=table, requiredKeys=requiredKeys)
        self.path = 'https://www.dnd5eapi.co/api/Equipment'
        if self.readAll() == []:
            self._build()