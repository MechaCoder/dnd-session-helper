from datetime import datetime
from random import randint, choice
# from tinydb_base import DatabaseBase
from .base import BaseData
from .exception import SlugFormat

def die(sides:int = 6):

    pool = []
    for rand in range(50):
        pool.append(
            randint(1, sides)
        )

    return choice(pool)

def roller(slug:str = '1D6'):
    
    if isinstance(slug, str) == False:
        raise TypeError('slug needs to be a string')

    sluglist = slug.lower().split('d')

    if len(sluglist) != 2:
        raise SlugFormat('slug format error')

    try:
        amount = int(sluglist[0])
        dieType = int(sluglist[1])
    except Exception:
        raise SlugFormat('there has benn a failer to covert')

    rolls = []
    total = 0

    if amount > 100:
        raise SlugFormat('you should not need to roll more 100 dice')

    for e in range(amount):

        rollValue = die(dieType)
        total += rollValue
        
        rolls.append(
            str(rollValue)
        )

    rollString = ','.join(rolls)
    DiceHistory().create(slug, rollString)

    return {
        'sum': total,
        'rolls': rollString
    }


class DiceHistory(BaseData):

    def __init__(self, table: str = 'dice_history', requiredKeys='slug,result,ts'):
        super().__init__(table=table, requiredKeys=requiredKeys)

    def create(self, slug:str, result:int) -> int:
        ts = datetime.now().timestamp()
        row = {
            'slug': slug,
            'result': str(result),
            'ts': str(ts)
        }
        return super().create(row)

    def readAll(self) -> list:
        
        formatTs = lambda ts: datetime.fromtimestamp(ts)
        
        data = super().readAll()
        for row in data:
            row['ts'] = formatTs(row['ts'])
        
        return data
