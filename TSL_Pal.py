#import modules
import random
import statistics
import math
import numpy as np

#Takes user-submitted values for starting stats
import subprocess
output = subprocess.check_output(["python", "TSL_Pal_Config.py"]).decode().splitlines()
stat_atk = float(output[0])
stat_chc = float(output[1])
stat_chd = float(output[2])
stat_cdr = float(output[3])
stat_reso = int(output[4])
sim_dur = int(output[5])
sim_iter = int(output[6])
ext_raid_buff = output[7]
'''
#loads Talent Point calculator
output = subprocess.check_output(["python", "TSL_Pal_Config_Talents.py"]).decode().splitlines()
talent_index = output
'''
#load talents- "t-row-column"
#first talent point is dummy value
talent_index = [0,1,3,\
                1,3,3,\
                0,3,1,\
                0,0,\
                0,3,2,\
                0,3,\
                0,2,\
                0,2,\
                3,2]
#Greedy Solo DPS Talents
#talent_index = [0,1,3,1,3,3,0,3,1,0,0,0,3,2,0,3,0,2,0,2,3,2]
if sum(talent_index)>32:
    print(sum(talent_index)-32," too many Talent Points.")
    quit()
elif sum(talent_index)<32:
    print("Missing ",32-sum(talent_index)," Talent Points.")
    quit()
elif sum(talent_index)==32:
    print("Talent Points Loaded Succesfully.\n")

#Default Stats w/o user import
'''
stat_atk = 700
stat_chc = 0.43
stat_chd = 1.65
stat_cdr = 0.19
stat_reso = 1000
sim_dur = 110
sim_iter = 100
'''
results,sim_res_gs,sim_res_jt, \
    sim_res_js,sim_res_eq,sim_res_aa,sim_res_all, \
    sim_res_dps = [],[],[],[],[],[],[],[]

sim_res_gs_ct,sim_res_jt_ct,sim_res_js_ct,sim_res_eq_ct,sim_res_aa_ct = [],[],[],[],[]
res_act_ct = []

def Sim_run(until):

    for i in range(until):
        #define variables, \ to add line breaks
        cd_gs,cd_jt,cd_js,cd_eq,PoG,Verdict,cd_aa,cd_tor,tor_dur,tor_haste=(0,0,0,0,0,0,0,0,0,0)
        js_bonus1,js_bonus2,gs_crit_ct,eq_dur,reso_dur = (0,0,0,0,0) 
        gcd,a_gcd,jt_ct,gs_ct=(1-stat_cdr,1-stat_cdr,2,2)
        tor_atk,tor_chc,tor_haste =(0,0,0)
        gs_mod,jt_mod,js_mod,eq_mod,aa_mod=(1,1,1,1,1)
        #Raid buffs
        cd_raid_buff,raid_buff_dur,raid_chc,raid_atk = (0,0,0,0)
        #1000 = starts with resonance
        pVerdict, verdict_bonus,reso_res, res_count = (0,0,0,0)

        duration = sim_dur
        
        sim_dmg_all,sim_dmg_gs,sim_dmg_jt,sim_dmg_js,sim_dmg_eq,sim_dmg_aa = [],[],[],[],[],[]

        #allows sim to loop in 0.05 second intervals
        increment = 0.05

        for _ in range((sim_dur*int(1/increment)*2)):
            #breaks loop for this iteration when fight ends
            if duration<=0:
                break
            duration -= increment  

            #Resonance Inscription activation
            if reso_res >= 1000:
                reso_dur = 6
            #Passive Resonance Energy Gain (Default = None)
            elif reso_res < 1000 and reso_dur <= 0:
                reso_res += 0 * increment * (1+(stat_reso*(0.00135)))
            #Logs activation of Resonance for tracking purposes
            if reso_dur > 0 and reso_res>0:
                res_count += 1
                reso_res = 0
            #Grants stack of Justice Thump if 0 sec CD
            if cd_jt <= 0 and jt_ct <=talent_index[8]:
                jt_ct += 1
                cd_jt = 10*(1-stat_cdr)   
            #Grants stack of Glory Strike if 0 sec CD
            if cd_gs <= 0:
                gs_ct += 1
                cd_gs = 3*(1-stat_cdr)
            #Grants buff based on Glory Judgement consecutive procs
            if pVerdict != 0 and pVerdict == Verdict:
                verdict_bonus = 1
            elif pVerdict != 0 and pVerdict != Verdict:
                verdict_bonus = 2
            #Activates Trial of Rage, sets duration, crit chance and cooldown
            if cd_tor <= 0:
                cd_tor = (120 - (15 * talent_index[19])) * (1-stat_cdr)
                tor_dur = 15 + (1.5 * talent_index[19])
                tor_atk = (63 + (stat_atk * 0.04) + 90 + 90 + 60 + 60) * (1+(0.23*3))
                tor_chc = 0.12
                tor_haste = 0.12
            #disable buffs while ToR is inactive
            if tor_dur <= 0:    
                tor_chc = 0
                tor_haste = 0
            #Activates Raid Buffs, sets duration, crit chance and cooldown
            if cd_raid_buff <= 0 and ext_raid_buff in [1,"Yes"]:
                cd_raid_buff = 120  * (1-stat_cdr)
                raid_buff_dur = 12
                raid_atk = (63*6*0.5) + ((stat_atk * 0.04)*6*0.5)
                raid_chc = (0.04*6*0.5)
            #disable Raid buffs
            if raid_buff_dur <= 0 and ext_raid_buff in [1,"Yes"]:
                raid_atk = 0
                raid_chc = 0
            #Tracks Trial of Rage and other buffs
            fstat_chc = stat_chc + tor_chc + raid_chc + (talent_index[3]*0.015) +\
                  ((verdict_bonus==1)*talent_index[12]*0.1)
            fstat_gcd = gcd - tor_haste
            fstat_atk = stat_atk + tor_atk + raid_atk
            #resets damage output of skills
            dmg_gs,dmg_jt,dmg_js,dmg_eq,dmg_aa = 0,0,0,0,0
            #generates +/-5% damage variance
            dmg_variance = (random.randint(95,105)/100)
            #updates skill damage values based on dynamic buffs
            GS = dmg_variance * ((1.07 * fstat_atk) +280) 
            JT = dmg_variance * ((1.42 * fstat_atk) +371) 
            JS = dmg_variance * ((2.65 * fstat_atk) +693) 
            EQ = dmg_variance * ((3.49 * fstat_atk) +434) 
            AA = dmg_variance * (0.35 * fstat_atk)

            #main Rotation EQ>JS>JT>GS+AA, accounts for GCD + haste
                #e.g. cannot cast both EQ and JS in 1 GCD
            if cd_eq <= 0:
                if a_gcd <= 0:
                    #EQ damage buff
                    eq_mod *= (1+(talent_index[17]*0.10))
                    eq_dur = 4
                    #ToR stacking buff
                    tor_chc += (0.0125 * talent_index[21])
                    tor_haste += (0.0125 * talent_index[21])
                    a_gcd = fstat_gcd
                    cd_eq = 30*(1-stat_cdr)
                    #EQ grants random Verdict, prioritizes skill w/o Verdict
                    if random.randint(1,100)<=math.floor(talent_index[7]*33.4):
                        if Verdict == 1 or 2:
                            pVerdict = 3- Verdict
                            Verdict = 3
                        else:
                            Verdict = random.randint(1,2)
                    if fstat_chc>=(random.randint(1,100)/100):
                        dmg_eq=EQ * (stat_chd + (js_bonus1 * talent_index[5] * 0.04))
                    else:
                        dmg_eq=EQ
            #Judgement Strike
            if cd_js <= 0:
                if a_gcd <= 0:               
                    #ToR stacking buff
                    tor_chc += (0.0125 * talent_index[21])
                    tor_haste += (0.0125 * talent_index[21])
                    a_gcd = fstat_gcd
                    cd_js = 10*(1-stat_cdr)    
                    if Verdict == 2 or 3:
                        Verdict += -2
                        #Up to 10% to gain 1 Power of Glory when consuming Verdict
                        if random.randint(1,3) <= talent_index[4]:
                            PoG += 1
                        if fstat_chc>=(random.randint(1,100)/100):
                            dmg_js=(JS * (stat_chd+0.15+(js_bonus1 * talent_index[5] * 0.04)))*1.15
                            #Crits reduces cooldown by up to 3 seconds
                            cd_js -= talent_index[15]
                            #Crits increase next skill damage
                            js_bonus2 = 1
                        else:
                            dmg_js=JS*1.15
                    elif Verdict == 0 or 1:
                        if (fstat_chc+(talent_index[13]*0.03))>=(random.randint(1,100)/100):
                            dmg_js=JS * (stat_chd+(js_bonus1 * talent_index[5] * 0.04))
                            #Crits reduces cooldown by up to 3 seconds
                            cd_js -= talent_index[15]
                            #Crits increase next skill damage
                            js_bonus2 = 1
                        else:
                            dmg_js=JS
                    #JS provides % dmg bonus and critical strike dmg to next skill cast
                    js_bonus1 = 1
            #Justice Thump
            if jt_ct >= 1:
                if a_gcd <= 0:
                    #uses charge of Justice Thump
                    jt_ct += -1
                    #ToR stacking buff
                    tor_chc += (0.0125 * talent_index[21])
                    tor_haste += (0.0125 * talent_index[21])
                    a_gcd = fstat_gcd
                    if Verdict == 1 or 3:
                        Verdict += -1
                        #Up to 10% to gain 1 Power of Glory when consuming Verdict
                        if random.randint(1,3) <= talent_index[4]:
                            PoG += 1
                        if fstat_chc>=(random.randint(1,100)/100):
                            dmg_jt=JT * (stat_chd+(js_bonus1 * talent_index[5] * 0.04)) * (1+(talent_index[2]*0.10))
                            if fstat_chc>=(random.randint(1,100)/100):
                                dmg_jt+=JT * (stat_chd+(js_bonus1 * talent_index[5] * 0.04)) * (1+(talent_index[2]*0.10))
                        else:
                            dmg_jt=JT * (1+(talent_index[2]*0.10))
                            if fstat_chc>=(random.randint(1,100)/100):
                                dmg_jt+=JT * (stat_chd+(js_bonus1 * talent_index[5] * 0.04)) * (1+(talent_index[2]*0.10))
                    elif Verdict == 0 or 2:
                        if fstat_chc>=(random.randint(1,100)/100):
                            dmg_jt = JT * (stat_chd+(js_bonus1 * talent_index[5] * 0.04)) * (1+(talent_index[2]*0.06))
                        else:
                            dmg_jt = JT * (1+(talent_index[2]*0.06))
            if gs_ct >= 1:
                if a_gcd <= 0:
                    #uses charge of Glory Strike
                    gs_ct += -1
                    #Resonance/Inscription gain from Glory Strike
                    if reso_dur <=0:
                        reso_res += 30.0 * (1 + (stat_reso*(0.00135)))
                    #Tracks GS (Every 4th GS +X% Crit)
                    gs_crit_ct += 1
                    #Trial of Rage stacking buff
                    tor_chc += (0.0125 * talent_index[21])
                    tor_haste += (0.0125 * talent_index[21])
                    a_gcd = fstat_gcd
                    if reso_dur > 0:
                        PoG += 1
                    #Glory Strike has x% to reset Justice Thump CD or grant charge
                    #and double the damage of the next Justice Thump                   
                    if fstat_chc>=0.50:
                        if random.randint(1,100) <= 15:
                            jt_mod *= 2  
                            if talent_index[8]==1 and jt_ct <2:
                                jt_ct += 1
                            elif talent_index[8]==0:
                                cd_jt = 0           
                    elif fstat_chc>=0.42:
                        if random.randint(1,100) <= 12:
                            jt_mod *= 2
                            if talent_index[8]==1 and jt_ct <2:
                                jt_ct += 1
                            elif talent_index[8]==0:
                                cd_jt = 0  
                    elif fstat_chc>=0.34:
                        if random.randint(1,100) <= 9:
                            jt_mod *= 2
                            if talent_index[8]==1 and jt_ct <2:
                                jt_ct += 1
                            elif talent_index[8]==0:
                                cd_jt = 0  
                    elif fstat_chc>=0.25:
                        if random.randint(1,100) <= 6:
                            jt_mod *= 2
                            if talent_index[8]==1 and jt_ct <2:
                                jt_ct += 1
                            elif talent_index[8]==0:
                                cd_jt = 0  
                    elif fstat_chc>=0.16:
                        if random.randint(1,100) <= 3:
                            jt_mod *= 2
                            if talent_index[8]==1 and jt_ct <2:
                                jt_ct += 1
                            elif talent_index[8]==0:
                                cd_jt = 0  
                    #4th Glory Strike has X% additional crit chance            
                    if (fstat_chc+((gs_crit_ct==4)*(talent_index[10]*0.15)))>=(random.randint(1,100)/100):
                        dmg_gs = GS * (stat_chd+(js_bonus1 * talent_index[5] * 0.04))
                        PoG += 2
                    else:
                        dmg_gs = GS
                        PoG += 1 
                    #Reset GS track to 0 regardless of crit
                    if gs_crit_ct==4:
                        gs_crit_ct=0
            #Power of Glory 5th stack grants random Glory Verdict
            if PoG >= 5:
                PoG += -5
                if Verdict == 1 or 2:
                    Verdict = 3
                else:
                    Verdict = random.randint(1,2)
                if Verdict == 2 or 3:
                    cd_js -= talent_index[15]   
            #Auto attack always applies every GCD, does not incur GCD timer
            if cd_aa <=0:
                cd_aa = 1*(1-stat_cdr)
                if fstat_chc>=(random.randint(1,100)/100):
                    dmg_aa = AA * stat_chd
                else:
                    dmg_aa = AA
            #Tallies GS damage and consume JS bonus damage
            if dmg_gs!=0:
                #GS Talent Bonus
                gs_mod *= 1 + (talent_index[1] * 0.05)
                #JS Bonus, JS Crit Bonus, EQ Bonus, Verdict Bonus
                gs_mod *= (1+(js_bonus1 * talent_index[5] * 0.04)) * (1+(js_bonus2 * talent_index[13] * 0.05))\
                        * (1+((eq_dur>0) * talent_index[17] * 0.07)) * (1+((verdict_bonus==2)*talent_index[12]*0.12))
                sim_dmg_gs.append(int(dmg_gs * gs_mod * (1+((reso_dur>0)*stat_reso*0.0007))))
                sim_dmg_all.append(sim_dmg_gs[-1])
                gs_mod = 1
                js_bonus1 = 0
                js_bonus2 = 0
            #Tallies JT damage and consume JS bonus damage
            if dmg_jt!=0:
                #JS Bonus, JS Crit Bonus, EQ Bonus, Verdict Bonus
                jt_mod *= (1+(js_bonus1 * talent_index[5] * 0.04)) * (1+(js_bonus2 * talent_index[13] * 0.05))\
                        * (1+((eq_dur>0) * talent_index[17] * 0.07)) * (1+((verdict_bonus==2)*talent_index[12]*0.12))
                sim_dmg_jt.append(int(dmg_jt * jt_mod * (1+((reso_dur>0)*stat_reso*0.0007))))
                sim_dmg_all.append(sim_dmg_jt[-1])
                jt_mod = 1
                js_bonus1 = 0
                js_bonus2 = 0
            #Tallies JS damage and consume JS bonus damage
            if dmg_js!=0:
                #JS Talent Bonus
                js_mod *= 1 + (talent_index[15] * 0.04)
                #JS Bonus, JS Crit Bonus, EQ Bonus, Verdict Bonus
                js_mod *= (1+(js_bonus1 * talent_index[5] * 0.04)) * (1+(js_bonus2 * talent_index[13] * 0.05))\
                        * (1+((eq_dur>0) * talent_index[17] * 0.07)) * (1+((verdict_bonus==2)*talent_index[12]*0.12))
                sim_dmg_js.append(int(dmg_js * js_mod * (1+((reso_dur>0)*stat_reso*0.0007))))
                sim_dmg_all.append(sim_dmg_js[-1])
                js_mod = 1
                js_bonus1 = 0
                js_bonus2 = 0
            #Tallies EQ damage and consume JS bonus damage
            if dmg_eq!=0:
                #JS Bonus, JS Crit Bonus, [Impossible to get EQ bonus w/o 87% CDR], Verdict Bonus
                eq_mod *= (1+(js_bonus1 * talent_index[5] * 0.04)) * (1+(js_bonus2 * talent_index[13] * 0.05))\
                        * (1+((verdict_bonus==2)*talent_index[12]*0.12))
                sim_dmg_eq.append(int(dmg_eq * eq_mod * (1+((reso_dur>0)*stat_reso*0.0007))))
                sim_dmg_all.append(sim_dmg_eq[-1])
                eq_mod = 1
                js_bonus1 = 0
                js_bonus2 = 0
            #Tallies AA damage
            if dmg_aa!=0:
                #ToR stacking crit/haste buff
                tor_chc += (0.0125 * talent_index[21])
                tor_haste += (0.0125 * talent_index[21])
                sim_dmg_aa.append(int(dmg_aa * aa_mod * (1+((reso_dur>0)*stat_reso*0.0007))))
                sim_dmg_all.append(sim_dmg_aa[-1])
                aa_mod = 1                
            #Increments cooldowns and buffs
            cd_gs -= increment
            cd_jt -= increment
            cd_js -= increment
            cd_eq -= increment
            cd_aa -= increment
            cd_tor -= increment
            tor_dur -= increment
            a_gcd -= increment
            eq_dur -= increment
            reso_dur -= increment
            cd_raid_buff -= increment
            raid_buff_dur -= increment

        #Tracks total GS/JT/JS/EQ/AA damage from each sim
        sim_res_gs.append(int(sum(sim_dmg_gs)))
        sim_res_jt.append(int(sum(sim_dmg_jt)))
        sim_res_js.append(int(sum(sim_dmg_js)))
        sim_res_eq.append(int(sum(sim_dmg_eq)))
        sim_res_aa.append(int(sum(sim_dmg_aa)))
        #Tracks # of GS/JT/JS/EQ/AA hits from each sim
        sim_res_gs_ct.append(len(sim_dmg_gs))
        sim_res_jt_ct.append(len(sim_dmg_jt))
        sim_res_js_ct.append(len(sim_dmg_js))
        sim_res_eq_ct.append(len(sim_dmg_eq))
        sim_res_aa_ct.append(len(sim_dmg_aa))
        #Tracks total damage from each sim
        sim_res_all.append(int(sum(sim_dmg_all)))
        #Calcualtes DPS from each sim
        sim_res_dps.append(int(sum(sim_dmg_all)/sim_dur))
        #Tracks Resonance/Inscription Activations
        res_act_ct.append(res_count)
        #Shows Progress of Simulation
        print("Iteration ",i,"/",until,end="\r")

Sim_run(sim_iter)

print(f"{1-stat_cdr:,.3f} GCD time          ")   
print(f"{sim_iter:,.0f} Simulations")
print(f"{sim_dur:,.0f} Second Fight Duration\n")

#shows +/- Damage capturing 90% of damage range
def dmg_spread(x,y=None,a=0.5,b=0.05,c=0.95):
    if y is None:
        stats_dmg = np.quantile(x,[a,b,c],method="nearest")
    else:
        stats_dmg = np.quantile([int(i / j) if j!=0 else 0 for i, j in zip(x,y)],[a,b,c],method="nearest")
    return "{:,.0f} +/- {:,.0f}".format(stats_dmg[0], (stats_dmg[2] - stats_dmg[1]) / 2)

print(" Damage Stats  Damage (95% Spread)")
print("   GS Damage: ",dmg_spread(sim_res_gs,sim_res_gs_ct,0.5,0.05,0.95))
print("   JT Damage: ",dmg_spread(sim_res_jt,sim_res_jt_ct,0.5,0.05,0.95))
print("   JS Damage: ",dmg_spread(sim_res_js,sim_res_jt_ct,0.5,0.05,0.95))
print("   EQ Damage: ",dmg_spread(sim_res_eq,sim_res_eq_ct,0.5,0.05,0.95))
print("Total Damage: ",dmg_spread(sim_res_all,None,0.5,0.05,0.95))
print("Avg. Sim Dmg: ",dmg_spread(sim_res_dps,None,0.5,0.05,0.95))

#To check Skill Cast Frequency
'''
print("# of GS Hits: ",sim_res_gs_ct)
print("# of JT Hits: ",sim_res_jt_ct)
print("# of JS Hits: ",sim_res_js_ct)
print("# of EQ Hits: ",sim_res_eq_ct)
print("# of AA Hits: ",sim_res_aa_ct)
print("# of inscription: ",res_act_ct)
'''
# if no values in list, skips quartile, common with short fight durations
# Shows more detailed statistics
'''
print(" Damage Stats   Min, 25%, 50%, 75%, Max")
print("   GS Damage: ",np.quantile([int(i / j) if j!=0 else 0 for i, j in zip(sim_res_gs, sim_res_gs_ct)],[0,0.25,0.50,0.75,1.00],method="nearest"))
print("   JT Damage: ",np.quantile([int(i / j) if j!=0 else 0 for i, j in zip(sim_res_jt, sim_res_jt_ct)],[0,0.25,0.50,0.75,1.00],method="nearest"))
print("   JS Damage: ",np.quantile([int(i / j) if j!=0 else 0 for i, j in zip(sim_res_js, sim_res_js_ct)],[0,0.25,0.50,0.75,1.00],method="nearest"))
print("   EQ Damage: ",np.quantile([int(i / j) if j!=0 else 0 for i, j in zip(sim_res_eq, sim_res_eq_ct)],[0,0.25,0.50,0.75,1.00],method="nearest"))
print("   AA Damage: ",np.quantile([int(i / j) if j!=0 else 0 for i, j in zip(sim_res_aa, sim_res_aa_ct)],[0,0.25,0.50,0.75,1.00],method="nearest"))
print("Total Damage: ",np.quantile(sim_res_all,[0,0.25,0.50,0.75,1.00],method="nearest"))
print("Avg. Sim DPS: ",np.quantile(sim_res_dps,[0,0.25,0.50,0.75,1.00],method="nearest"))
'''