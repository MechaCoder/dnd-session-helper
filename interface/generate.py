from faker import Faker
from rich.text import Text
from rich.console import Console, RenderGroup
from rich.panel import Panel

from random import choice, choices, randint

import interface.generate_data as data

def choosers(l:list):
    pool = choices(l, k=500)
    return choice(pool)

def genAge(info):
    r = info['races']
    if r == 'Dragonborn':
        return randint(15, 80)
    if r == 'Dwarf':
        return randint(18, 350)
    if r == 'Elf':
        return randint(100, 750)
    if r == 'Gnome':
        return randint(40, 400)
    if r == 'Half-Elf':
        return randint(20, 180)
    if r == 'Halfling':
        return randint(20, 250)
    if r == 'Half-Orc':
        return randint(14, 75)
    if r == 'Human':
        return randint(18, 90)
    if r == 'Tiefling':
        return randint(18, 100)




def simpleProfileNPC():
    factory = Faker()

    profile = {}
    profile['gender'] = choosers(data.gender_data)
    
    if profile['gender'] == 'masculine':
        profile['name'] = factory.name_male()
    if profile['gender'] == 'feminine':
        profile['name'] = factory.name_female()
    if profile['gender'] == 'non-binary':
        profile['name'] = factory.name_nonbinary()

    profile['appearance'] = choosers(data.appearance_data) + ', ' + choosers(data.appearance_data)


    return profile

def complexProfileNPC():

    profile = {}
    for d in dir(data):
        l = getattr(data, d)
        if '_data' not in d:
            continue
        tag = d.split('_')[0: -1]
        tag ='_'.join(tag)

        profile[tag] = choosers(l)
    profile.update(simpleProfileNPC())
    
    return profile


def displaySimpleNPC():
    info = simpleProfileNPC()
    name = info['name']
    nameRow = f'[bold]Name:[/bold] [yellow]{name}[/yellow]'

    gender = info['gender']

    c = ''
    if gender[0] == 'm':
        c = 'blue'
    
    if gender[0] == 'f':
        c = 'red'
    
    if gender[0] == 'n':
        c = 'purple'
    
    nameRow = f'[bold]Name:[/bold] [yellow]{name}[/yellow]'
    genderRow = f'[bold]Presentation[/bold] [{c}]{gender}[/{c}]'
    appearanceRow = '[bold]appearance:[/bold] ' + info['appearance']

    pannel = RenderGroup(nameRow, genderRow, appearanceRow)

    con = Console()
    con.print(pannel)


def displayComplexNPC():
    info = complexProfileNPC()
    name = info['name']
    nameRow = f'[bold]Name:[/bold] [yellow]{name}[/yellow]'

    gender = info['gender']

    c = ''
    if gender[0] == 'm':
        c = 'blue'
    
    if gender[0] == 'f':
        c = 'red'
    
    if gender[0] == 'n':
        c = 'purple'
    
    nameRow = f'[bold]Name:[/bold] [yellow]{name}[/yellow]'
    genderRow = f'[bold]Presentation[/bold] [{c}]{gender}[/{c}]'
    appearanceRow = '[bold]appearance:[/bold] ' + info['appearance']
    strengthRow = '[bold]stength ability: [/bold]' + info['abilities_high']
    weakerRow = '[bold]stength ability: [/bold]' + info['abilities_lower']
    talentRow = '[bold]talent: [/bold]' + info['talent']
    mannerRow = '[bold]mannerism: [/bold]' + info['mannerisms']
    traitRow = '[bold]trait: [/bold]' + info['trait']
    bondRow = '[bold]bonds: [/bold]' + info['bonds']
    flawsRow = '[bold]flaws: [/bold]' + info['flaws']
    alignmentRow = '[bold]Alignment: [/bold]' + info['alignment_x'] + ', ' + info['alignment_y']

    ideal = ''
    
    if info['alignment_x'] == 'Chaotic':
        ideal += info['chaotic_ideal']

    if info['alignment_x'] == 'Neutral':
        ideal += info['neutral_ideal']

    ideal += ', '

    if info['alignment_y'] == 'Good':
        ideal += info['good_ideal']

    if info['alignment_y'] == 'Neutral':
        ideal += info['neutral_ideal']

    if info['alignment_y'] == 'Evil':
        ideal += info['evil_ideal']

    ideal += ', ' + info['other_ideal']

    idealRow = '[bold]Ideals: [/bold]' + ideal
    bondRow = '[bold]Bond: [/bold]' + info['bond']
    secretRow = '[bold]secret: [/bold]' + info['secret']
    raceRow = '[bold]race: [/bold]' + info['races']

    jobsRow = '[bold]Jobs: [/bold]' + info['jobs']
    ageRow = '[bold]Age: [/bold]' + str(genAge(info=info))
    
    pannel = RenderGroup(
        nameRow, 
        genderRow,
        appearanceRow,
        strengthRow,
        weakerRow,
        talentRow,
        mannerRow,
        traitRow,
        bondRow,
        flawsRow,
        alignmentRow,
        idealRow,
        bondRow,
        secretRow,
        raceRow,
        jobsRow,
        ageRow
    )

    con = Console()
    con.print(pannel)

