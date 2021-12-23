from os.path import dirname, abspath, join
from os.path import isfile
from tinydb_base import DatabaseBase
from tinydb_base.getSet import GetSet

def projectRoot():
    return abspath(dirname('Pipfile'))

def dsfile():
    proot = abspath(dirname('Pipfile'))
    f = 'ds.json'
    if isfile(join(proot, '.dev')):
        f = 'ds.dev.json'
    return join(proot, f)


class BaseData(DatabaseBase):

    def __init__(self, table: str = 'BaseData', requiredKeys='title:str'):
        file = dsfile()
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)

    def readDoc_ids(self):

        doc_ids = []
        for row in self.readAll():
            doc_ids.append(str(row.doc_id))

        return doc_ids

class BaseGetSet(GetSet):

    def __init__(self, table: str = 'getSet'):
        file = dsfile()
        super().__init__(file=file, table=table)