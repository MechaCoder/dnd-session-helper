from click import option
from click.termui import confirm, secho, clear
from faker import Faker
from data.api import getProfile
from data.combat import CombatData, NpcData
from data.players import Players
from data import Screen, screen
from data.dice import roller
from data.api import MonstersIndex
from rich import prompt
from rich.console import Console, Group
from rich.layout import Layout
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.rule import Rule
from rich.table import Table
from rich import print

from simple_term_menu import TerminalMenu


def modifiers(score):

    temp = -5
    if score > 1:
        temp += 1

    if score > 3: temp += 1

    if score > 5: temp += 1

    if score > 7: temp += 1

    if score > 9: temp += 1

    if score > 11: temp += 1

    if score > 13: temp += 1

    if score > 16: temp += 1

    if score > 17: temp += 1

    if score > 19: temp += 1

    if score > 21: temp += 1

    if score > 23: temp += 1

    if score > 25: temp += 1

    if score > 27: temp += 1

    if score > 29: temp += 1

    if score > 30: temp = 10

    return temp


def combat_data(combat_id):

    combat_data = CombatData().readById(combat_id)
    screen_data = Screen().readByHex(combat_data['screen.hex'])
    npcs_data = NpcData().readByHex(combat_id=combat_id)

    npcProfiles = {}

    for npc in npcs_data:
        d = getProfile(npc['index'])
        
        d['initiative'] = (roller('1D20')['sum'] + d['dexterity'])
        d['combat_type'] = 'npc'
        npcProfiles[npc['name']] = d

    # get players
    pcProfiles = {}

    for e in Players().readByCampaignId(screen_data['campain']):

        d = {
            'initiative': IntPrompt.ask(f'enter init for ' + e['name']),
            'combat_type': 'pc'
        }

        pcProfiles[e['name']] = d

    
    # sorting player's
    order = []
    for x in npcProfiles:
        order.append(
            (x, npcProfiles[x]['initiative'], 'npc')
        )
    
    for x in pcProfiles:
        order.append(
            (x, pcProfiles[x]['initiative'], 'pc')
        )

    order.sort(
        key=lambda t:t[1]
    )

    order.reverse()

    return {
        'order': order,
        'npcs': npcProfiles
    }


class CombatDisplay():

    def __init__(self, combat_id:int):
        self.data = combat_data(combat_id)
        self.combat_id = combat_id

    def run(self):
        """runs the combat."""

        con = Console()
        while True: # runs the combat loop, loops on round

            for each in self.data['order']: #goes though the i order 

                while True:

                    if each[2] == 'npc' and self.data['npcs'][each[0]]['hit_points'] <= 0:
                        continue

                    clear()
                    con.print(
                        self.renderable(each[0])
                    )
                    x = Prompt.ask('::>>', choices=['','exit', 'hp', 'add npc'])
                    if x == '':
                        break

                    if x == 'exit':
                        exit()

                    self.combatCommands(x)


    def renderable(self, name:str):

        masterLayout = Layout(
            visible=1
        )
        masterLayout.split_row(
            Layout(
                name='order of play',
                ratio=1,
                renderable=self._screenOrderOfPlay(name)
            ),
            Layout(
                name='display profile',
                ratio=3,
                renderable=self._screenDisplayProfile(name)
            )
        )
        return masterLayout

    def _screenOrderOfPlay(self, name:str):

        tbl = Table(
            'name', 'init', 'hp', 'type', 'turn',
            title='Play Order',
            show_lines=True
        )
        
        for each in self.data['order']:
            turn = ''
            if name == each[0]:
                turn = '👈'

            type = ''
            if each[2] == 'pc':
                type = 'player'
            
            
            hp = ''
            if each[2] == 'npc':
                hp = str(self.data['npcs'][each[0]]['hit_points'])
            
            styleStr = ''
            if each[2] == 'npc' and self.data['npcs'][each[0]]['hit_points'] <= 0:
                styleStr = 'red'

            tbl.add_row(each[0], str(each[1]), hp, type, turn, style=styleStr)

        return tbl

    def _screenDisplayProfile(self, name:str):

        try:
            profile = self.data['npcs'][name]
        except KeyError as err:
            return ""

        txt = """
# {}
{} {}; {}

        """.format(
            profile['name'],
            profile['size'],
            profile['type'],
            profile['alignment']
        )

        txt = Markdown(txt)


        tbl1 = Table.grid()
        tbl1.add_row("Armour Class: ", str(profile['armor_class']) )
        tbl1.add_row("Hit Points: ", str(profile['hit_points']) + " (" + profile['hit_dice'] + ")")
        speedStr = ""

        for e in profile['speed'].keys():
            speedStr += (e + "-" + profile['speed'][e])

        tbl1.add_row("speed", speedStr)

        stats = Table(
            "str", "dex", "con", "int", "wis", "cha",
            expand=True,
        )

        stats.add_row(
            str(profile['strength']) + " [" + str(modifiers(profile['strength'])) + "]" ,
            str(profile['dexterity']) + " [" + str(modifiers(profile['dexterity'])) + "]" ,
            str(profile['constitution']) + " [" + str(modifiers(profile['constitution'])) + "]" ,
            str(profile['intelligence']) + " [" + str(modifiers(profile['intelligence'])) + "]" ,
            str(profile['wisdom']) + " [" + str(modifiers(profile['wisdom'])) + "]" ,
            str(profile['charisma']) + " [" + str(modifiers(profile['charisma'])) + "]" 
        )

        tbl2 = Table.grid()
        x = ""
        for each in profile['proficiencies']:
            x += "[red]{}[/red] (+{}), ".format(
                each['proficiency']['name'],
                each['value']
            )

        tbl2.add_row('proficiencies ', x)
        

        g = Group(
            txt,
            Rule(),
            tbl1,
            Rule(),
            stats,
            tbl2
        )

        return Panel(g)

    def combatCommands(self, command:str):

        if command == '':
            return False

        if command.lower() == 'hp':
            print('who is the target?')
            options = []
            for e in self.data['order']:
                if e[2] == 'pc':
                    continue
                options.append(e[0])

            tMenu = TerminalMenu(options)
            target = options[tMenu.show()]

            options = ['remove', 'add']
            tMenu = TerminalMenu(options)
            action =  options[tMenu.show()]
            
            
            hp = IntPrompt.ask(f'how many hp to {action}')

            
            if action == 'add':
                self.data['npcs'][target]['hit_points'] += hp
            
            if action == 'remove':
                self.data['npcs'][target]['hit_points'] -= hp

            if self.data['npcs'][target]['hit_points'] < 1:
                self.data['order']

            return False

        if command == 'add npc':
            obj = NpcData()
            
            npcIndex = MonstersIndex().readAllIndex()
            char = Prompt.ask("what type of NPC", choices=npcIndex)
            amount = IntPrompt.ask("how many to add")

            for n in range(amount):
                name = Faker().first_name()
                obj.create(name, char, self.combat_id)
                p = getProfile(char)

                self.data['npcs'][name] = p
                self.data['npcs'][name]['initiative'] = (roller('1D20')['sum'] + p['dexterity'])
                self.data['npcs'][name]['combat_type'] = 'npc'

                self.data['order'].append(
                    (name, self.data['npcs'][name]['initiative'], 'npc')
                )

            self.data['order'].sort(key=lambda t:t[1])
            self.data['order'].reverse()
            

            