from tinydb_base import DatabaseBase

class EncounterData(DatabaseBase): 
    
    def __init__(self, file: str = 'ds.json', table: str = 'encounter', requiredKeys='name,url,campaign'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)

    def create(self, name:str, url:str, campaign_id:int) -> int:
        row = {
            'name': name,
            'addr': url,
            'campaign': campaign_id
        }
        return super().create(row)
