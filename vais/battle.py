# battle.py   
import os
import random  

import character

rules_file = os.getcwd() + os.sep + 'data' + os.sep + 'battle.rules'

class BattleRules(object):
    """
    Manages the parsing of rules for a battle by reading the .rules file
    """
    def __init__(self, rules_file):
        self.rules_file = rules_file
        self.all_rules = {}
        with open(rules_file, 'r') as f:
            for line in f:
                if line[0] != '#' and line.strip() != '' and line:
                    line_parts = line.split('=')
                    self.all_rules[line_parts[0].strip(' ')] = line_parts[1].strip(' ').strip('\n')
                    
    def __str__(self):
        res  = 'Battle Rules : ' + self.rules_file + '\n'
        for k, v in self.all_rules.items(): 
            res += 'Rule ' + k + ':' + v + '\n'
        return res
    

    
class BattleSimulator(object):
    """
    class to handle multiple simulation runs of Battles 
    between characters
    """
    def __init__(self, c1, c2, traits, rules, num_fights = 1000):
        self.c1 = c1
        self.c2 = c2
        self.num_fights = num_fights
        self.num_c1 = 0
        self.num_c2 = 0
        self.traits = traits
        self.rules = rules
        self.winner = 'No battles have been done'
        self.run_simulation()
    
    def __str__(self):
        res = 'After ' + str(self.num_fights) + ' fights ' + self.winner + ' wins!\n'
        res += self.c1.name + ' = ' + str(self.num_c1) + ' (' + str(round(self.num_c1*100/self.num_fights)) + '%)\n'
        res += self.c2.name + ' = ' + str(self.num_c2) + ' (' + str(round(self.num_c2*100/self.num_fights)) + '%)\n'
        
        return res
     
    def run_simulation(self):
        """
        runs the simulation
        """
        for _ in range(self.num_fights):
            # restore health between each fight
            self.c1.stats['Health'] = self.c1.stats['max_health']
            self.c2.stats['Health'] = self.c2.stats['max_health']
            
            # run the Battles
            b = Battle(self.c1, self.c2, self.traits, self.rules, print_console='No')
            #print(b)
            if b.status == self.c1.name:
                self.num_c1 += 1
            else:
                self.num_c2 += 1
                
        # tag winner        
        if self.num_c1 > self.num_c2:
            self.winner = self.c1.name
        else:
            self.winner = self.c2.name
    
class Battle(object):
    """
    manages a fight between 2 rpg characters
    """
    def __init__(self, char1, char2, traits, rules, print_console='Yes'):
        self.c1 = char1
        self.c2 = char2
        self.log = []
        self.traits = traits
        self.rules = rules
        self.status = self.fight(100, print_console)
        
    def __str__(self):
        res  = 'Battle Status : ' + self.status + ' Wins\n'
        res += 'Character 1 =  ' + self.c1.name + '\n'
        res += 'Character 2 =  ' + self.c2.name + '\n'
        return res
        
    
    def fight(self, moves, print_console):
        """
        runs a series of fights - TODO switch order 
        of who attacks first, as this has an effect 
        on win rate over 1000 fights
        """
        for _ in range(1, moves):
            #if i == 1 and random.randint(1,100) > 50:   # randomly choose who moves first
            # player 1
            result, dmg = self.calc_move(self.c1)
            self.show_message(self.c1, self.c2, result, dmg, print_console)
            self.take_damage(self.c2, dmg)
            if self.is_character_dead(self.c2):
                #print(self.c2.name + ' has died')
                return self.c1.name
                
            # player 2
            result, dmg = self.calc_move(self.c2)
            self.show_message(self.c2, self.c1, result, dmg, print_console)
            self.take_damage(self.c1, dmg)
            if self.is_character_dead(self.c1):
                #print(self.c1.name + ' has died')
                return self.c2.name
    
    def take_damage(self, c, dmg):
        """
        wrapper to apply damage taken to a character
        """
        if c.name == self.c1.name:
            self.c1.stats['Health'] = self.c1.stats['Health'] - dmg
        else:
            self.c2.stats['Health'] = self.c2.stats['Health'] - dmg
        
    
    def show_message(self, c_attack, c_defend, result, dmg, print_console='Yes'):
        """
        function to wrap the display of the battle messages
        """
        perc_health_att = '[' + str(round((c_attack.stats['Health']*100) / c_attack.stats['max_health'] )) + '%]'
        perc_health_def = '[' + str(round((c_defend.stats['Health']*100) / c_defend.stats['max_health'] )) + '%]'
        if result == 'Miss':
            txt = c_attack.name + ' ' + perc_health_att.rjust(6) + ' miss ' + c_defend.name + ' ' + perc_health_def.rjust(6)
        elif result == 'Crit':
            txt = c_attack.name + ' ' + perc_health_att.rjust(6) + ' CRIT ' + c_defend.name + ' ' + perc_health_def.rjust(6)
            txt +=  ' for ' + str(dmg)   
        else:
            txt = c_attack.name + ' ' + perc_health_att.rjust(6) + ' hits ' + c_defend.name + ' ' + perc_health_def.rjust(6) 
            txt +=  ' for ' + str(dmg)   
        
        if print_console == 'Yes':
            print(txt)
            
    def calc_move(self, c):
        """
        calculate the amount of damage down using the battle.rules file
        WARNING - shitty eval functions - careful with user input.
        TODO = max_hit = parser.parse(self.rules['hit_max']).to_pyfunc()
        """
        
        # first get local variables the same as battle.rules file so parser can interpret.
        AGI = c.stats['AGI']
        INT = c.stats['INT']
        STR = c.stats['STR']
        #STA = c.stats['STA']
        #print('calc move : self.rules.all_rules[hit_min] = ', self.rules.all_rules['hit_min'])
        #print('calc move : self.rules.all_rules[hit_max] = ', self.rules.all_rules['hit_max'])
        #print('calc move :  = self.rules.all_rules[hit_limit]', self.rules.all_rules['hit_limit'])
        hit_min   = float(self.rules.all_rules['hit_min'])
        
        hit_AGI_mult   = float(self.rules.all_rules['hit_AGI_mult'])
        hit_INT_mult   = float(self.rules.all_rules['hit_INT_mult'])
        hit_AGI_add   = float(self.rules.all_rules['hit_AGI_add'])
        hit_INT_add   = float(self.rules.all_rules['hit_INT_add'])
        hit_overall_add   = float(self.rules.all_rules['hit_overall_add'])
        
        #  hit_max = round(INT/2) + round(AGI/2) + 1
        hit_max = round(INT*(hit_INT_mult + hit_INT_add)) + round(AGI*(hit_AGI_mult + hit_AGI_add)) + hit_overall_add
        
        hit_limit = float(self.rules.all_rules['hit_limit']) 
        if hit_max > hit_limit:
            hit_max = hit_limit
        chance_hit = random.randint(hit_min,hit_max)
        
        dmg_min   = float(self.rules.all_rules['dmg_min'])
        #dmg_max   = eval(self.rules.all_rules['dmg_max'])
        calc_agi = round((AGI + float(self.rules.all_rules['dmg_AGI_add'])) * float(self.rules.all_rules['dmg_AGI_mult']))
        calc_int = round((INT + float(self.rules.all_rules['dmg_INT_add'])) * float(self.rules.all_rules['dmg_INT_mult']))
        calc_str = round((STR + float(self.rules.all_rules['dmg_STR_add'])) * float(self.rules.all_rules['dmg_STR_mult'])) 
        #print('TESTING CALC_MOVE : calc_agi', calc_agi, 'calc_int',calc_int ,'calc_str',calc_str )
        dmg_max = round((calc_agi + calc_int + calc_str) * float(self.rules.all_rules['dmg_overall_mult']) + float(self.rules.all_rules['dmg_overall_add']))

        #print('hit_min  =',hit_min  , 'hit_max = ',hit_max  )
        #print('dmg_min  =',dmg_min  , 'dmg_max = ',dmg_max  )
        amount_dmg = random.randint(dmg_min, dmg_max)
        
        if chance_hit > float(self.rules.all_rules['shot_crit_greater_than']):
            return 'Crit', amount_dmg * float(self.rules.all_rules['dmg_mult_crit'])
        elif chance_hit < float(self.rules.all_rules['shot_hit_greater_than']):
            return 'Miss', amount_dmg * float(self.rules.all_rules['dmg_mult_miss'])
        else:
            return 'Hit', amount_dmg * float(self.rules.all_rules['dmg_mult_hit'])
            
    def is_character_dead(self, c):
        """
        check to see if a character is dead
        """
        if c.stats['Health'] < 1:
            return True
        else:
            return False


            