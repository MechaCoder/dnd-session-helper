from .base import BaseGetSet

from tinydb_base.factory import Factory

class Links(BaseGetSet):

    def __init__(self, table: str = 'links'):
        super().__init__(table)

        # set the default links.
        self.defaultRows({
            'roll20 Virtual Table Top': 'https://app.roll20.net/login',
            'roll20 Markplace': 'https://marketplace.roll20.net/',
            'Tableplop Virtual Table Top': 'https://new.tableplop.com/',
            'Asciiflow - ascii drawing tool': 'https://asciiflow.com/#/',
            'dnd beyond': 'https://www.dndbeyond.com/',
            'donjon genrators': 'https://donjon.bin.sh/',
            'world writeing': 'https://www.worldanvil.com/',
            'Arcane eye - DMs tools ': 'https://arcaneeye.com/dm-tools-5e/',
            'Adventurers Codex': 'https://adventurerscodex.com/',
            'Drive Thru RPG': 'https://www.drivethrurpg.com/index.php',
        })

    def readAll(self):

        data = []
        factory = Factory(self.fileName, self.tableName)
        data = factory.tbl.all()
        factory.close()

        return data


