# Tarisland
Tarisland Paladin Spreadsheet found here: https://docs.google.com/spreadsheets/d/14vKUGiKxMA5A0mZxaB9TpaurQAhtFDvvU1SopLGmPcE/edit#gid=0

4/13/24: Talent Point Calculator WIP:
    For now, just edit talent matrix within TSL_Pal.py
    Ordered similarly to actual talents.
          talent_index = [0,1,3,1,3,3,0,3,1,0,0,0,3,2,0,3,0,2,0,2,3,2]
    
Currently has arbitrary raid buffs with 120 sec CD
    6 Players each providing: +32 ATK, +2% Crit chance, and +2% ATK buff
    Can edit this within TSL_Pal()
              if cd_raid_buff <= 0 and ext_raid_buff in [1,"Yes"]:
                cd_raid_buff = 120  * (1-stat_cdr)
                raid_buff_dur = 12
                raid_atk = (63*6*0.5) + ((stat_atk * 0.04)*6*0.5)
                raid_chc = (0.04*6*0.5)

Missing stacking Inscription Echos buff that converts to Echo of Destiny.
Missing Special Aptitude lines. (Unsure of a clean way to allow user-input as there are 25+ SA lines.)
    May just have User input total +dmg mods for each skill. TBD
