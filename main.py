#import modules
import random       #RNG generation for crits and procs
import math         #for math.floor() for a few calculations
import numpy as np  #allows us to get quartile results, e.g., top 10%
#import subprocess   #in order to incorporate other scripts

#Takes user-submitted values for starting stats
import tsl_config as tconfig
all_stats = tconfig.main()
stat_atk,stat_chc,stat_chd,stat_cdr,stat_combo,stat_combo_dmg,stat_omni,stat_focus\
,stat_reso, stat_armor, sim_dur,sim_iter\
,ext_raid_buff, inscript_start, echo_start\
,sa_dmg_gs,sa_dmg_jt,sa_dmg_js,sa_dmg_eq\
,eod_dmg_gs,eod_one_gs,eod_chn_gs_dmg\
,eod_dmg_jt,eod_one_jt,eod_chn_jt_dmg\
,eod_dmg_js,eod_one_js,eod_chn_js_dmg\
,eod_dmg_eq,eod_one_eq,eod_chn_eq_dmg\
,eod_stack_gs,eod_stack_jt,eod_stack_js,eod_stack_eq\
,eod_tor_atk = all_stats
#Reduce Enemy Armor by Focus
stat_armor -= (stat_focus/4.25)
target_DR = 3155/(3155+stat_armor)
#No longer used for as of TBT Beta
eod_tor_bon = 0

#Establish starting Resonance, Inscription Stacks, and External Buffs
if inscript_start in [1,"Yes"]:
    inscript_start = 1000
else:
    inscript_start = 0
if echo_start in [15,"Yes"]:
    echo_start = 15
else:
    echo_start = 0
if ext_raid_buff in [1,"Yes"]:
    ext_raid_buff = 1
else:
    ext_raid_buff = 0

#Takes user-submitted talent points
import tsl_talent as ttalent
talent_index=(ttalent.main())

#Reference Solo DPS Talents
#talent_index = [0,1,3,1,3,3,0,3,1,0,0,0,3,2,0,3,0,2,0,2,3,2]

#Cancels script if talents are incorrect
if sum(talent_index)>32:
    print(sum(talent_index)-32," too many Talent Points.")
elif sum(talent_index)<32:
    print("Missing ",32-sum(talent_index)," Talent Points.")
elif sum(talent_index)==32:
    print("Talent Points Loaded Succesfully.\n")

#Initialize Lists Recording every simulation iteration statistics
sim_rec_gs,sim_rec_jt,sim_rec_js,sim_rec_eq,sim_rec_aa,sim_rec_all,sim_rec_dps = [],[],[],[],[],[],[]
sim_rec_gs_ct,sim_rec_jt_ct,sim_rec_js_ct,sim_rec_eq_ct,sim_rec_aa_ct = [],[],[],[],[]
sim_rec_res_ct = []
#Saves all data for Excel export. data_list is all data per sim_iter
sim_data_list = []
sim_combat_log_time,sim_combat_log_events = [],[]

def Sim_run(until):

    for i in range(until):
        #define variables
        cd_gs,cd_jt,cd_js,cd_eq,cd_aa=(0,0,0,0,0)
        #Tracks JS bonuses if talented, GS crit mod% counter, and EQ dmg% buff
        js_bonus1,js_bonus2,gs_crit_ct,eq_dur = (0,0,0,0)
        #Set charges of GS and JT (if talented)
        gs_ct,jt_ct = (2,talent_index[8]+1)
        #GCD based on CDR and adjusted GCD for haste effects 
        gcd,a_gcd=(1-stat_cdr,0)
        #Trial of Rage variables
        tor_atk,tor_chc,tor_haste,cd_tor,tor_dur =(0,0,0,0,0)
        #Base skill damage
        gs_mod,jt_mod,js_mod,eq_mod,aa_mod=(1,1,1,1,1)
        #Raid buffs
        cd_raid_buff,raid_buff_dur,raid_chc,raid_atk = (0,0,0,0)
        #Power of Glory, Verdict, previous Verdict, and talented bonus
        PoG, Verdict, pVerdict, verdict_bonus = (0,0,0,0)
        #Resonance Duration, Initial Meter, and tracker
        reso_dur, reso_res, sim_inst_res_ct = (0,inscript_start,0)
        #Set Fight Duration for each simulation
        duration = sim_dur
        #Initialize Lists Recording the current simulation's damage stats
        sim_dmg_all,sim_dmg_gs,sim_dmg_jt,sim_dmg_jt2,sim_dmg_js,sim_dmg_eq,sim_dmg_aa = [],[],[],[],[],[],[]
        #allows sim to loop in 0.10 second intervals
        increment = 0.10
        #Record cumulative damage per sim
        cml_dmg, data_list = 0, []
        #Inscription echo, set duration to 0 and reset
        echo_dur, echo_stack,echo_active = 0,echo_start,0
        #Inscript Chance% Dmg set to 0
        eod_chn_gs,eod_chn_jt,eod_chn_js,eod_chn_eq,eod_tor_ct = 0,0,0,0,0
        #SA Echo of Destiny Damage Active
        eod_one_gs_act,eod_one_jt_act,eod_one_js_act,eod_one_eq_act = 0,0,0,0

        for _ in range((sim_dur*int(1/increment)*2)):
            #breaks loop for this iteration when fight ends
            if duration<=0:
                break
            #30% to gain a stack of Inscription
            elif duration-int(duration)<increment and echo_dur<=0:
                if random.randint(1,100) <= 30:
                    echo_stack +=1
                    sim_combat_log_time.append([i+1, sim_dur-duration])
                    sim_combat_log_events.append("You gain 1 stack of Inscription Echo.")
            #Cannot build stacks while Echo is active
            if echo_dur > 0:
                echo_stack = 0 
            #Inscription Echo activation
            if echo_stack >=15:
                echo_dur = 9
                echo_active = 1
                sim_combat_log_time.append([i+1, sim_dur-duration])
                sim_combat_log_events.append("You lose "+str(echo_stack)+" stacks of Inscription Echo.")
                sim_combat_log_time.append([i+1, sim_dur-duration])
                sim_combat_log_events.append("You gain Echo of Destiny.")
                echo_stack = 0
                eod_tor_ct = 1
                eod_one_gs_act,eod_one_jt_act,eod_one_js_act,eod_one_eq_act = 1,1,1,1
                if random.randint(1,100)<=30:
                    eod_chn_gs = 1
                if random.randint(1,100)<=30:
                    eod_chn_jt = 1
                if random.randint(1,100)<=30:
                    eod_chn_js = 1
                if random.randint(1,100)<=30:
                    eod_chn_eq = 1
                if random.randint(1,100)<=30:
                    reso_res += 375
            #Deactivate Echo of Destiny
            if echo_dur <= 0 and echo_active == 1:
                echo_active = 0
                eod_chn_gs,eod_chn_jt,eod_chn_js,eod_chn_eq = 0,0,0,0
                sim_combat_log_time.append([i+1, sim_dur-duration])
                sim_combat_log_events.append("You lose Echo of Destiny.")
            #Resonance Inscription activation
            if reso_res >= 1000:
                reso_dur = 6
                reso_res = 0
                sim_inst_res_ct += 1
                sim_combat_log_time.append([i+1, sim_dur-duration])
                sim_combat_log_events.append("Inscription is active")
            #Passive Resonance Energy Gain (Default = None)
            elif reso_res < 1000 and reso_dur <= 0:
                reso_res += 0 * increment * (1+(stat_reso*(0.00135)))
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
                tor_active = 1
                cd_tor = (120 - (15 * talent_index[19])) * (1-stat_cdr)
                tor_dur = 15 + (1.5 * talent_index[19])
                tor_atk = (63 + (stat_atk * 0.04) + eod_tor_atk) * (1+(eod_tor_bon*eod_tor_ct))
                tor_chc = 0.12
                tor_haste = 0.12
                sim_combat_log_time.append([i+1, sim_dur-duration])
                sim_combat_log_events.append("You gain Trial of Rage.")
            #disable buffs while ToR is inactive
            if tor_dur <= 0 and tor_active == 1:
                tor_active = 0    
                tor_chc = 0
                tor_haste = 0
                sim_combat_log_time.append([i+1, sim_dur-duration])
                sim_combat_log_events.append("You lose Trial of Rage.")
            #Activates Raid Buffs, sets duration, crit chance and cooldown
            if cd_raid_buff <= 0 and ext_raid_buff == 1:
                cd_raid_buff = 120  * (1-stat_cdr)
                raid_buff_dur = 12
                raid_atk = (63*6*0.5) + ((stat_atk * 0.04)*6*0.5)
                raid_chc = (0.04*6*0.5)
            #disable Raid buffs
            if raid_buff_dur <= 0 and ext_raid_buff == 1:
                raid_atk = 0
                raid_chc = 0
            #Tracks Trial of Rage and other buffs
            fstat_chc = stat_chc + tor_chc + raid_chc + (talent_index[3]*0.01) +\
                  ((verdict_bonus==1)*talent_index[12]*0.10) + ((echo_dur>0)*((5.25+2.61)/39))
            fstat_chd = stat_chd + ((echo_dur>0)*0.18)
            fstat_gcd = gcd - tor_haste - ((echo_dur>0)*0.05)
            fstat_atk = stat_atk + tor_atk + raid_atk
            #Resets damage output of skills
            dmg_gs,dmg_jt,dmg_jt2,dmg_js,dmg_eq,dmg_aa = 0,0,0,0,0,0
            #generates +/-5% damage variance
            dmg_variance = (random.randint(9500,10500)/10000)
            #updates skill damage values based on dynamic buffs
            GS = dmg_variance * ((1.07 * fstat_atk) +280+sa_dmg_gs) * (1+(stat_omni/14270))
            JT = dmg_variance * ((1.42 * fstat_atk) +371+sa_dmg_jt) * (1+(stat_omni/14270)) 
            JS = dmg_variance * ((2.65 * fstat_atk) +693+sa_dmg_js) * (1+(stat_omni/14270)) 
            EQ = dmg_variance * ((3.49 * fstat_atk) +917+sa_dmg_eq) * (1+(stat_omni/14270)) 
            AA = dmg_variance * (0.35 * fstat_atk) * (1+(stat_omni/14270))

            #main Rotation EQ>JS>JT>GS+AA, accounts for GCD + haste
                #e.g. cannot cast both EQ and JS in 1 GCD
            if cd_eq <= 0:
                if a_gcd <= 0:
                    #EQ damage buff
                    eq_mod *= (1+(talent_index[17]*0.05))
                    eq_dur = 4
                    #ToR stacking buff
                    tor_chc += (0.01 * talent_index[21])
                    tor_haste += (0.01 * talent_index[21])
                    a_gcd = fstat_gcd
                    cd_eq = 30*(1-stat_cdr)
                    #EQ grants random Verdict, prioritizes skill w/o Verdict
                    if random.randint(1,100)<=math.floor(talent_index[7]*33.4):
                        if Verdict in [1,2]:
                            pVerdict = 3- Verdict
                            Verdict = 3
                        else:
                            Verdict = random.randint(1,2)
                    if fstat_chc>=(random.randint(1,100)/100):
                        dmg_eq=EQ * (fstat_chd + (js_bonus1 * talent_index[5] * 0.05))
                    else:
                        dmg_eq=EQ
            #Judgement Strike
            if cd_js <= 0:
                if a_gcd <= 0:               
                    #ToR stacking buff
                    tor_chc += (0.01 * talent_index[21])
                    tor_haste += (0.01 * talent_index[21])
                    a_gcd = fstat_gcd
                    cd_js = 10*(1-stat_cdr)    
                    if Verdict in [2,3]:
                        Verdict += -2
                        #Up to 10% to gain 1 Power of Glory when consuming Verdict
                        if random.randint(1,3) <= talent_index[4]:
                            PoG += 1
                        if fstat_chc>=(random.randint(1,100)/100):
                            dmg_js=(JS * (fstat_chd+0.15+(js_bonus1 * talent_index[5] * 0.05)))*1.15
                            #Crits reduces cooldown by up to 3 seconds
                            cd_js -= talent_index[15]
                            #Crits increase next skill damage
                            js_bonus2 = 1
                        else:
                            dmg_js=JS*1.15
                    elif Verdict in [0,1]:
                        if (fstat_chc+(talent_index[13]*0.03))>=(random.randint(1,100)/100):
                            dmg_js=JS * (fstat_chd+(js_bonus1 * talent_index[5] * 0.05))
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
                    tor_chc += (0.01 * talent_index[21])
                    tor_haste += (0.01 * talent_index[21])
                    a_gcd = fstat_gcd
                    if Verdict in [0,2]:
                        if fstat_chc>=(random.randint(1,100)/100):
                            dmg_jt = JT * (fstat_chd+(js_bonus1 * talent_index[5] * 0.05)) * (1+(talent_index[2]*0.05))
                        else:
                            dmg_jt = JT * (1+(talent_index[2]*0.05))
                    if Verdict in [1,3]:
                        Verdict += -1
                        #33/67/100% to gain 1 Power of Glory when consuming Verdict
                        if random.randint(1,3) <= talent_index[4]:
                            PoG += 1
                        if fstat_chc>=(random.randint(1,100)/100):
                            dmg_jt=JT * (fstat_chd+(js_bonus1 * talent_index[5] * 0.05)) * (1+(talent_index[2]*0.06))
                        else:
                            dmg_jt=JT * (1+(talent_index[2]*0.06))
                        #Recalculate Justice Thump damage for 2nd hit
                        JT /= dmg_variance
                        dmg_variance = (random.randint(9500,10500)/10000)
                        JT *= dmg_variance
                        if fstat_chc>=(random.randint(1,100)/100):
                            dmg_jt2 =JT * (fstat_chd+(js_bonus1 * talent_index[5] * 0.05)) * (1+(talent_index[2]*0.06))
                        else:
                            dmg_jt2 =JT * (1+(talent_index[2]*0.06))
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
                    tor_chc += (0.01 * talent_index[21])
                    tor_haste += (0.01 * talent_index[21])
                    a_gcd = fstat_gcd
                    if reso_dur > 0:
                        PoG += 1
                    #Glory Strike has x% to reset Justice Thump CD or grant charge
                    #and double the damage of the next Justice Thump  
                    passive_crit_thres = [0.5,0.42,0.34,0.25,0.16]  
                    if fstat_chc<passive_crit_thres[-1]:
                            crit_thres=0             
                    else:
                        for n in range(len(passive_crit_thres)):
                            if fstat_chc>=passive_crit_thres[n]:
                                crit_thres = 6-n
                                break
                    if random.randint(1,100) <= (crit_thres*3):
                        jt_mod *=2
                        if talent_index[8]==1 and jt_ct <2:
                            jt_ct += 1
                        elif talent_index[8]==0:
                            cd_jt = 0   
                    #4th Glory Strike has X% additional crit chance            
                    if (fstat_chc+((gs_crit_ct==4)*(talent_index[10]*0.10)))>=(random.randint(1,100)/100):
                        dmg_gs = GS * (fstat_chd+(js_bonus1 * talent_index[5] * 0.05))
                        PoG += 2
                    else:
                        dmg_gs = GS
                        PoG += 1 
                    #Reset GS track to 0 regardless of crit
                    if gs_crit_ct==4:
                        gs_crit_ct=0
            #Power of Glory 5th stack grants random Glory Verdict
            #During Inscription gaining Judgement resets cooldown
            if PoG >= 5:
                PoG += -5
                if Verdict == 0:
                    if talent_index[20]*0.33>random.randint(1,100):
                        Verdict = 3
                        if reso_dur >0:
                            cd_jt,cd_js = 0
                        else:
                            cd_js -= talent_index[15]  
                elif Verdict == 1:
                    pVerdict = 1
                    Verdict = 3
                    if reso_dur >0:
                        cd_js = 0
                    else:
                        cd_js -= talent_index[15]
                    #When you gain a Glory Judgement, you have a 3-10% to gain another 
                    if jt_ct<2:
                        if talent_index[20]*0.33>random.randint(1,100):
                            cd_jt = 0
                elif Verdict == 2:
                    pVerdict = 2
                    Verdict = 3 
                    if reso_dur >0:
                        cd_jt = 0             
                elif Verdict == 3 and jt_ct<2:
                    pVerdict = 1
                    if reso_dur >0:
                        cd_jt = 0  
            #Auto attack always applies every GCD, does not incur GCD timer
            if cd_aa <=0:
                cd_aa = 1*(1-stat_cdr)
                if fstat_chc>=(random.randint(1,100)/100):
                    dmg_aa = AA * fstat_chd
                else:
                    dmg_aa = AA
            #This assumes data_list is structured chronologically
            #Records prior 15 second damage for analytics
            if (dmg_gs+dmg_jt+dmg_js+dmg_eq+dmg_aa)!=0:   
                filter_dl = (row for row in data_list if row['Sim #'] == i+1 and\
                            row['Time'] >= (sim_dur-duration-15) and row['Time']\
                            <(sim_dur-duration))
                #Recalculates prior 15 second damage from scratch
                for row in filter_dl:
                    cml_dmg += row['Damage']
            #Checks for Combo Damage
            for combo in [dmg_eq,dmg_js,dmg_jt2,dmg_jt,dmg_gs,dmg_aa]:
                if combo != 0:
                    if stat_combo>=(random.randint(1,100)/100):
                        data_list.append({'Sim #': i+1, 'Time': sim_dur - duration, 'Skill': "Combo", 'Damage': \
                                (fstat_atk * 0.85 * (1+(stat_omni/14270)) * target_DR),'15 Sec': cml_dmg \
                                ,'ToR': tor_dur>0,'Inscription': reso_dur>0,'Echo Active': echo_dur>0})
            #Tallies GS damage and consume JS bonus damage
            if dmg_gs!=0:
                if random.randint(1,100)<=min(eod_stack_gs*100,100) and echo_dur<=0:
                    echo_stack+=1
                #GS Talent Bonus
                gs_mod *= 1 + (talent_index[1] * 0.04)
                #JS Bonus, JS Crit Bonus, EQ Bonus, Verdict Bonus
                gs_mod *= (1+(js_bonus1 * talent_index[5] * 0.05)) * (1+(js_bonus2 * talent_index[13] * 0.05))\
                        * (1+((eq_dur>0) * talent_index[17] * 0.07)) * (1+((verdict_bonus==2)*talent_index[12]*0.10))\
                        * (1+((reso_dur>0)*stat_reso*0.0007)) * (1+((echo_dur>0)*eod_dmg_gs))\
                        * (1+(eod_chn_gs * eod_chn_gs_dmg)) * (1 + (eod_one_gs * eod_one_gs_act)) * target_DR
                sim_dmg_gs.append(int(dmg_gs * gs_mod))
                sim_dmg_all.append(sim_dmg_gs[-1])
                #Record to pandas-excel
                data_list.append({'Sim #': i+1, 'Time': sim_dur - duration, 'Skill': "GS", 'Damage': \
                                 sim_dmg_gs[-1],'15 Sec': cml_dmg,'ToR': tor_dur>0,'Inscription': reso_dur>0\
                                    ,'Echo Active': echo_dur>0})
                gs_mod,js_bonus1,js_bonus2,verdict_bonus = 1,0,0,0
                eod_chn_gs,eod_one_gs_act = 0,0
            #Tallies JT damage and consume JS bonus damage
            if dmg_jt!=0:
                if random.randint(1,100)<=min(eod_stack_jt*100,100) and echo_dur<=0:
                    echo_stack+=1
                #JS Bonus, JS Crit Bonus, EQ Bonus, Verdict Bonus
                jt_mod *= (1+(js_bonus1 * talent_index[5] * 0.05)) * (1+(js_bonus2 * talent_index[13] * 0.05))\
                        * (1+((eq_dur>0) * talent_index[17] * 0.07)) * (1+((verdict_bonus==2)*talent_index[12]*0.10))\
                        * (1+((reso_dur>0)*stat_reso*0.0007)) * (1+((echo_dur>0)*eod_dmg_jt))\
                        * (1+(eod_chn_jt * eod_chn_jt_dmg)) * (1 + (eod_one_jt * eod_one_jt_act)) * target_DR
                if dmg_jt2!=0:
                    sim_dmg_jt2.append(int(dmg_jt2 * jt_mod))
                    sim_dmg_all.append(sim_dmg_jt2[-1])
                    data_list.append({'Sim #': i+1, 'Time': sim_dur - duration, 'Skill': "JT2", 'Damage': \
                            sim_dmg_jt2[-1],'15 Sec': cml_dmg,'ToR': tor_dur>0,'Inscription': reso_dur>0\
                                ,'Echo Active': echo_dur>0})
                sim_dmg_jt.append(int(dmg_jt * jt_mod))   
                sim_dmg_all.append(sim_dmg_jt[-1])            
                #Record to pandas-excel
                data_list.append({'Sim #': i+1, 'Time': sim_dur - duration, 'Skill': "JT", 'Damage': \
                            sim_dmg_jt[-1],'15 Sec': cml_dmg,'ToR': tor_dur>0,'Inscription': reso_dur>0\
                                ,'Echo Active': echo_dur>0})
                jt_mod,js_bonus1,js_bonus2,verdict_bonus = 1,0,0,0
                eod_chn_jt,eod_one_jt_act = 0,0
            #Tallies JS damage and consume JS bonus damage
            if dmg_js!=0:
                if random.randint(1,100)<=min(eod_stack_js*100,100) and echo_dur<=0:
                    echo_stack+=1
                #JS Talent Bonus
                js_mod *= 1 + (talent_index[15] * 0.03)
                #JS Bonus, JS Crit Bonus, EQ Bonus, Verdict Bonus
                js_mod *= (1+(js_bonus1 * talent_index[5] * 0.05)) * (1+(js_bonus2 * talent_index[13] * 0.05))\
                        * (1+((eq_dur>0) * talent_index[17] * 0.07)) * (1+((verdict_bonus==2)*talent_index[12]*0.10))\
                        * (1+((reso_dur>0)*stat_reso*0.0007)) * (1+((echo_dur>0)*eod_dmg_js))\
                        * (1+(eod_chn_js * eod_chn_js_dmg)) * (1 + (eod_one_js * eod_one_js_act)) * target_DR
                sim_dmg_js.append(int(dmg_js * js_mod))
                sim_dmg_all.append(sim_dmg_js[-1])
                #Record to pandas-excel
                data_list.append({'Sim #': i+1, 'Time': sim_dur - duration, 'Skill': "JS", 'Damage': \
                            sim_dmg_js[-1],'15 Sec': cml_dmg,'ToR': tor_dur>0,'Inscription': reso_dur>0\
                                ,'Echo Active': echo_dur>0})
                js_mod,js_bonus1,js_bonus2,verdict_bonus = 1,0,0,0
                eod_chn_js,eod_one_js_act = 0,0
            #Tallies EQ damage and consume JS bonus damage
            if dmg_eq!=0:
                if random.randint(1,100)<=min(eod_stack_eq*100,100) and echo_dur<=0:
                    echo_stack+=1
                #JS Bonus, JS Crit Bonus, [Impossible to get EQ bonus w/o 87% CDR], Verdict Bonus
                eq_mod *= (1+(js_bonus1 * talent_index[5] * 0.05)) * (1+(js_bonus2 * talent_index[13] * 0.05))\
                        * (1+((verdict_bonus==2)*talent_index[12]*0.10))\
                        * (1+((reso_dur>0)*stat_reso*0.0007)) * (1+((echo_dur>0)*eod_dmg_eq))\
                        * (1+(eod_chn_eq * eod_chn_eq_dmg)) * (1 + (eod_one_eq * eod_one_eq_act)) * target_DR
                sim_dmg_eq.append(int(dmg_eq * eq_mod))
                sim_dmg_all.append(sim_dmg_eq[-1])
                #Record to pandas-excel
                data_list.append({'Sim #': i+1, 'Time': sim_dur - duration, 'Skill': "EQ", 'Damage': \
                            sim_dmg_eq[-1],'15 Sec': cml_dmg,'ToR': tor_dur>0,'Inscription': reso_dur>0\
                                ,'Echo Active': echo_dur>0})
                eq_mod,js_bonus1,js_bonus2,verdict_bonus = 1,0,0,0
                eod_chn_eq,eod_one_eq_act = 0,0
            #Tallies AA damage
            if dmg_aa!=0:
                #ToR stacking crit/haste buff
                tor_chc += (0.01 * talent_index[21])
                tor_haste += (0.01 * talent_index[21])
                sim_dmg_aa.append(int(dmg_aa * aa_mod * (1+((reso_dur>0)*stat_reso*0.0007)) * target_DR))
                sim_dmg_all.append(sim_dmg_aa[-1])
                #Record to pandas-excel
                data_list.append({'Sim #': i+1, 'Time': sim_dur - duration, 'Skill': "AA", 'Damage': \
                            sim_dmg_aa[-1],'15 Sec': cml_dmg,'ToR': tor_dur>0,'Inscription': reso_dur>0\
                                ,'Echo Active': echo_dur>0})
                aa_mod = 1   
            #Increments cooldowns and buffs
            duration -= increment 
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
            echo_dur -= increment
            cd_raid_buff -= increment
            raid_buff_dur -= increment
            #Resets n-second damage. Only checks against current sim for n-15 seconds.
            #Program speed is O(N^2)
            cml_dmg = 0

        #Tracks total GS/JT/JS/EQ/AA damage from each sim
        sim_rec_gs.append(int(sum(sim_dmg_gs)))
        sim_rec_jt.append(int(sum(sim_dmg_jt)))
        sim_rec_js.append(int(sum(sim_dmg_js)))
        sim_rec_eq.append(int(sum(sim_dmg_eq)))
        sim_rec_aa.append(int(sum(sim_dmg_aa)))
        #Tracks # of GS/JT/JS/EQ/AA hits from each sim
        sim_rec_gs_ct.append(len(sim_dmg_gs))
        sim_rec_jt_ct.append(len(sim_dmg_jt))
        sim_rec_js_ct.append(len(sim_dmg_js))
        sim_rec_eq_ct.append(len(sim_dmg_eq))
        sim_rec_aa_ct.append(len(sim_dmg_aa))
        #Tracks total damage from each sim
        sim_rec_all.append(int(sum(sim_dmg_all)))
        #Calculates DPS from each sim
        sim_rec_dps.append(int(sum(sim_dmg_all)/sim_dur))
        #Tracks Resonance/Inscription Activations
        sim_rec_res_ct.append(sim_inst_res_ct)
        #Appends 15 second damage data
        #Breaking it out into per-sim lists optimizes script speed
        sim_data_list.extend(data_list)
        #Shows Progress of Simulation
        print("Iteration ",i,"/",until,end="\r")

Sim_run(sim_iter)

#Output base GCD, # of Simulations, and Fight Duration
print(f"{1-stat_cdr:,.3f} GCD time          ")   
print(f"{sim_iter:,.0f} Simulations")
print(f"{sim_dur:,.0f} Second Fight Duration\n")

#shows +/- Damage capturing 5-95% of damage range
def dmg_spread(x,y=None,a=0.5,b=0.05,c=0.95):
    if y is None:
        stats_dmg = np.quantile(x,[a,b,c],method="nearest")
    else:
        stats_dmg = np.quantile([int(i / j) if j!=0 else 0 for i, j in zip(x,y)],[a,b,c],method="nearest")
    return "{:,.0f} +/- {:,.0f}".format(stats_dmg[0], (stats_dmg[2] - stats_dmg[1]) / 2)

print(" Damage Stats  Damage (+/- 45% Spread)")
print("   GS Damage: ",dmg_spread(sim_rec_gs,sim_rec_gs_ct,0.5,0.05,0.95))
print("   JT Damage: ",dmg_spread(sim_rec_jt,sim_rec_jt_ct,0.5,0.05,0.95))
print("   JS Damage: ",dmg_spread(sim_rec_js,sim_rec_jt_ct,0.5,0.05,0.95))
print("   EQ Damage: ",dmg_spread(sim_rec_eq,sim_rec_eq_ct,0.5,0.05,0.95))
print("Total Damage: ",dmg_spread(sim_rec_all,None,0.5,0.05,0.95))
print("Avg. Sim Dmg: ",dmg_spread(sim_rec_dps,None,0.5,0.05,0.95))

#Save results to Excel
import pandas as pd
print("\nExporting data to Excel...",end="\r")
with pd.ExcelWriter("Sim Data.xlsx", engine='xlsxwriter') as writer:
    data_export = pd.DataFrame(columns=["Sim #", "Time", "Skill", "Damage","15 Sec Dmg","ToR","Inscript"])
    data_export = pd.DataFrame(sim_data_list)
    data_export.to_excel(writer, index=False, sheet_name="Sim Data")
    #Output Config Settings
    data_export_2 = pd.DataFrame(columns=["Description", "Setting"])
    data_export_2["Description"] = ['Attack', 'Crit. Chance', 'Crit. Damage', \
                    'Cooldown', 'Combo','Combo Damage', 'Omni', 'Focus', \
                    'Resonance', 'Enemy Armor', 'Fight Dur.', '# of Sims', \
                    'External Raid Buffs', 'Start w/ Inscription', 'Start w/ Echo', \
                    'GS Damage', 'JT Damage', 'JS Damage', 'EQ Damage', \
                    'GS Damage during Echo', 'x1 GS Damage after Echo', '30% Chance x1 GS Damage', \
                    'JT Damage during Echo', 'x1 JT Damage after Echo', '30% Chance x1 JT Damage', \
                    'JS Damage during Echo', 'x1 JS Damage after Echo', '30% Chance x1 JS Damage', \
                    'EQ Damage during Echo', 'x1 EQ Damage after Echo', '30% Chance x1 EQ Damage', \
                    '% Fatuina Echo w/ GS', '% Fatuina Echo w/ JT', \
                    '% Fatuina Echo w/ JS', '% Fatuina Echo w/ EQ', \
                    'Trial of Rage bonus ATK']
    data_export_2["Setting"] = (all_stats)
    data_export_2.to_excel(writer, index=False, sheet_name="Config")
    #Output Talent Settings
    data_export_3 = pd.DataFrame(columns=["Talent", "Points"])
    data_export_3["Talent"] = ["Glory Strike+","Justice Thump+","Judgement Mastery","Echo"\
                            ,"Enraged","Punitive Storm+","Eternal Glory","Power of Justice"\
                            ,"Judgement Sword","Dogma","Razor-Shape","Double Knight","Frenzy Strike"\
                            ,"Execution","Judgement Strike+","Judgement Sword+","Shatterin Slam+"\
                            ,"Field Rage","Trial of Rage","Knight's Glory","Expedition"]
    data_export_3["Points"] = talent_index[1:]
    data_export_3.to_excel(writer, index=False, sheet_name="Talents")
    #Output Combat Log
    data_export_4 = pd.DataFrame(columns=["Sim #", "Time", "Event"])
    sim_combat_log_time += [[row['Sim #'], row['Time']] for row in sim_data_list]
    sim_combat_log_events += [' '.join([row['Skill'], "deals", str(int(row['Damage'])), "Damage."]) for row in sim_data_list]
    data_export_4[['Sim #', 'Time']] = sim_combat_log_time
    data_export_4['Event'] = sim_combat_log_events
    data_export_4.sort_values(by=['Sim #', 'Time'], inplace=True)
    data_export_4.to_excel(writer, index=False, sheet_name="Combat Log")
print("Data Exported Successfully.")
#input("Press any key to exit.")