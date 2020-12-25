from tinydb_base.getSet import GetSet, Factory, Query

class SettingsData(GetSet):
    
    def __init__(self, file: str = 'ds.json', table: str = 'settings'):
        super().__init__(file=file, table=table)
        # self.defaultRows({
        #     'Active Campain', 1
        # })

    def exist(self, tag:str):
        db = Factory(self.fileName, self.tableName)
        exists = db.tbl.contains(Query().tag == tag)
        db.close()

        return exists

    def rmTag(self, tag:str):
        db = Factory(self.fileName, self.tableName)
        db.tbl.remove(Query().tag == tag)
        db.close()
        return True
