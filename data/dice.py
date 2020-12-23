from datetime import datetime
from random import randint, choice
from tinydb_base import DatabaseBase
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

    slug = slug.lower().split('d')
    print(slug)
    # return ""

    if len(slug) != 2:
        raise SlugFormat('slug format error')

    try:
        amount = int(slug[0])
        dieType = int(slug[1])
    except Exception:
        raise SlugFormat

    rolls = []
    total = 0

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





class DiceHistory(DatabaseBase):

    def __init__(self, file: str = 'ds.json', table: str = 'dice_history', requiredKeys='slug,result,ts'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)

    def create(self, slug:str, result:int) -> int:
        ts = datetime.now().timestamp()
        row = {
            'slug': slug,
            'result': result,
            'ts': ts
        }
        return super().create(row)
