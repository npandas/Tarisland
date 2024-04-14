# Tarisland
Tarisland Paladin Spreadsheet found here: https://docs.google.com/spreadsheets/d/14vKUGiKxMA5A0mZxaB9TpaurQAhtFDvvU1SopLGmPcE/edit#gid=0

4/13/24: Talent Point Calculator WIP:
    For now, just edit talent matrix within TSL_Pal.py
    Ordered similarly to actual talents.
'''          talent_index = [0,1,3,1,3,3,0,3,1,0,0,0,3,2,0,3,0,2,0,2,3,2]'''
    
Currently has arbitrary raid buffs with 120 sec CD
    +240 ATK, +12% Crit chance, and +12% ATK buff
    Can edit this within TSL_Pal()
'''              if cd_raid_buff <= 0:
                cd_raid_buff = 120  * (1-stat_cdr)
                raid_buff_dur = 12
                raid_atk = 240 + (stat_atk * 0.12)
                raid_chc = 0.12'''
