from tinydb_base import DatabaseBase

class BaseData(DatabaseBase):

    def readDoc_ids(self):

        doc_ids = []
        for row in self.readAll():
            doc_ids.append(str(row.doc_id))

        return doc_ids