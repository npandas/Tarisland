#import modules
import random
import statistics
import math
import numpy as np

'''
stat_atk = int(input("Attack?: "))
stat_chc = float(input("Crit Hit Chance?: "))
stat_chd = float(input("Crit Damage?: "))
stat_cdr = float(input("Cooldown?: "))

sim_dur = int(input("Simulation Duration?: "))
'''

#load talents- "t-row-column"
talent_index = [3,3,0,3,3,0,0,1,0,3,0,3,2,0,3,0,2,2,2,0,2]

if sum(talent_index)>32:
    print("Too many Talent Points.")
    quit()
elif sum(talent_index)<32:
    print("Missing Talent Points.")
    quit()
elif sum(talent_index)==32:
    print("Talent Points Loaded Succesfully.\n")

stat_atk = 700
stat_chc = 0.43 + (talent_index[3]*0.015)
stat_chd = 1.65
stat_cdr = 0.192
stat_reso = 1000
sim_dur = 120
sim_iter = 100

results,sim_dmg,sim_dmg_gs,sim_dmg_jt,sim_dmg_js, \
    sim_dmg_eq,sim_dmg_aa,sim_res_gs,sim_res_jt, \
    sim_res_js,sim_res_eq,sim_res_aa,sim_res_all, \
    sim_res_dps = [],[],[],[],[],[],[],[],[],[],[],[],[],[]

sim_res_gs_ct,sim_res_jt_ct,sim_res_js_ct,sim_res_eq_ct,sim_res_aa_ct = [],[],[],[],[]
res_act_ct = []

def Sim_run(until):

    for i in range(until):
        #define variables, \ to add line breaks
        cd_gs,cd_jt,cd_js,cd_eq,PoG,Verdict,cd_aa,cd_tor,tor_dur,tor_haste=(0,0,0,0,0,0,0,0,0,0)
        gcd,tor_atk,tor_chc,tor_haste,a_gcd,jt_ct=(1-stat_cdr,163,0,0,1-stat_cdr,2)
        gs_mod,jt_mod,js_mod,eq_mod,aa_mod=(1,1,1,1,1)
        js_bonus,js_bonus2,gs_ct,eq_dur,reso_dur = (0,0,0,0,0)
        dmg_gs,dmg_jt,dmg_js,dmg_eq,dmg_aa,sim_dmg=(0,0,0,0,0,0)  
        raid_chc,raid_atk = (0,0)
        reso_res = 1000
        res_count = 0

        duration = sim_dur
        sim_dmg = []
        sim_dmg_gs = []
        sim_dmg_jt = []
        sim_dmg_js = []
        sim_dmg_eq = []
        sim_dmg_aa = []

        #allows sim to loop in 0.05 second intervals
        increment = 0.05

        for _ in range((sim_dur*int(1/increment)*2)):
            #breaks loop for this iteration when fight ends
            if duration<=0:
                break
            duration -= increment

            #Tracks Trial of Rage and other buffs
            fstat_chc = stat_chc + tor_chc + raid_chc
            fstat_gcd = gcd - tor_haste
            fstat_atk = stat_atk + tor_atk + raid_atk

            dmg_gs,dmg_jt,dmg_js,dmg_eq,dmg_aa = 0,0,0,0,0
            dmg_variance = (random.randint(95,105)/100)
            GS = dmg_variance * ((1.07 * fstat_atk) +280) 
            JT = dmg_variance * ((1.42 * fstat_atk) +371) 
            JS = dmg_variance * ((2.65 * fstat_atk) +693) 
            EQ = dmg_variance * ((3.49 * fstat_atk) +434) 
            AA = dmg_variance * (0.35 * fstat_atk)  

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

            if js_bonus2==1:
                gs_mod *= 1+(talent_index[13]*0.05)
                jt_mod *= 1+(talent_index[13]*0.05)
                js_mod *= 1+(talent_index[13]*0.05)
                eq_mod *= 1+(talent_index[13]*0.05)

            if cd_tor <= 0:
                cd_tor = ((120-(15*talent_index[19]))*(1-stat_cdr))
                tor_dur = 15 +(1.5*talent_index[19])
                tor_chc = 0.12

            #disable buffs while ToR is inactive
            if tor_dur<=0:    
                tor_chc = 0
                tor_haste = 0

            if cd_eq <= 0:
                if a_gcd <= 0:
                    eq_mod *= (1+(talent_index[17]*0.10))
                    eq_dur = 4
                    if random.randint(1,100)<=math.floor(talent_index[7]*33.4):
                        if Verdict == 1 or 2:
                            Verdict = 3
                        else:
                            Verdict = random.randint(1,2)
                    tor_chc += (0.0125 * talent_index[20])
                    tor_haste += (0.0125 * talent_index[20])
                    a_gcd = fstat_gcd
                    cd_eq = 30*(1-stat_cdr)
                    if fstat_chc>=(random.randint(1,100)/100):
                        dmg_eq=EQ * (stat_chd + (js_bonus * talent_index[5] * 0.04))
                    else:
                        dmg_eq=EQ
            if cd_js <= 0:
                if a_gcd <= 0:
                    tor_chc += (0.0125 * talent_index[20])
                    tor_haste += (0.0125 * talent_index[20])
                    a_gcd = fstat_gcd
                    cd_js = 10*(1-stat_cdr)
                    js_bonus = 1
                    if Verdict == 2 or 3:
                        Verdict += -2
                        if random.randint(1,3) <= talent_index[4]:
                            PoG += 1
                        if fstat_chc>=(random.randint(1,100)/100):
                            dmg_js=(JS * (stat_chd+0.15+(js_bonus * talent_index[5] * 0.04)))*1.15
                            cd_js -= (talent_index[15]*3)
                            js_bonus2 = 1
                        else:
                            dmg_js=JS*1.15
                    elif Verdict == 0 or 1:
                        if (fstat_chc+(talent_index[13]*0.03))>=(random.randint(1,100)/100):
                            dmg_js=JS * (stat_chd+(js_bonus * talent_index[5] * 0.04))
                            cd_js -= (talent_index[15]*3)
                            js_bonus2 = 1
                        else:
                            dmg_js=JS
            if jt_ct >= 1:
                if a_gcd <= 0:
                    jt_ct += -1
                    tor_chc += (0.0125 * talent_index[20])
                    tor_haste += (0.0125 * talent_index[20])
                    a_gcd = fstat_gcd
                    if Verdict == 1 or 3:
                        Verdict += -1
                        if random.randint(1,3) <= talent_index[4]:
                            PoG += 1
                        if fstat_chc>=(random.randint(1,100)/100):
                            dmg_jt=JT * (stat_chd+(js_bonus * talent_index[5] * 0.04)) * (1+(talent_index[2]*0.10))
                            if fstat_chc>=(random.randint(1,100)/100):
                                dmg_jt+=JT * (stat_chd+(js_bonus * talent_index[5] * 0.04)) * (1+(talent_index[2]*0.10))
                        else:
                            dmg_jt=JT * (1+(talent_index[2]*0.10))
                            if fstat_chc>=(random.randint(1,100)/100):
                                dmg_jt+=JT * (stat_chd+(js_bonus * talent_index[5] * 0.04)) * (1+(talent_index[2]*0.10))
                    elif Verdict == 0 or 2:
                        if fstat_chc>=(random.randint(1,100)/100):
                            dmg_jt = JT * (stat_chd+(js_bonus * talent_index[5] * 0.04)) * (1+(talent_index[2]*0.06))
                        else:
                            dmg_jt = JT * (1+(talent_index[2]*0.06))
            if cd_gs <= 0:
                if a_gcd <= 0:
                    if reso_dur <=0:
                        reso_res += 30.0 * (1 + (stat_reso*(0.00135)))
                    gs_ct += 1
                    tor_chc += (0.0125 * talent_index[20])
                    tor_haste += (0.0125 * talent_index[20])
                    a_gcd = fstat_gcd
                    cd_gs = 3*(1-stat_cdr)
                    if reso_dur > 0:
                        PoG += 1
                    #Glory Strike has x% to reset Justice Thump CD or grant charge
                    if talent_index[8]==1 and jt_ct <2:
                        jt_ct += 1
                    elif talent_index[8]==0:
                        cd_jt = 0 
                    if fstat_chc>=0.50:
                        if random.randint(1,100) <= 15:
                            jt_mod *= 2            
                    elif fstat_chc>=0.42:
                        if random.randint(1,100) <= 12:
                            jt_mod *= 2
                    elif fstat_chc>=0.34:
                        if random.randint(1,100) <= 9:
                            jt_mod *= 2
                    elif fstat_chc>=0.25:
                        if random.randint(1,100) <= 6:
                            jt_mod *= 2
                    elif fstat_chc>=0.16:
                        if random.randint(1,100) <= 3:
                            jt_mod *= 2
                    if (fstat_chc+((gs_ct==4)*(talent_index[11]*0.15)))>=(random.randint(1,100)/100):
                        dmg_gs = GS * (stat_chd+(js_bonus * talent_index[5] * 0.04)) * (1+(talent_index[1]*0.05))
                        PoG += 2
                    else:
                        dmg_gs = GS * (1+(talent_index[1]*0.05))
                        PoG += 1 
                    if gs_ct==4:
                        gs_ct=0
            if PoG >= 5:
                PoG += -5
                if Verdict == 1 or 2:
                    Verdict = 3
                else:
                    Verdict = random.randint(1,2)
            if cd_aa <=0:
                cd_aa = 1*(1-stat_cdr)
                if fstat_chc>=(random.randint(1,100)/100):
                    dmg_aa = AA * stat_chd
                else:
                    dmg_aa = AA

            if dmg_gs!=0:
                sim_dmg_gs.append(dmg_gs * (1+(js_bonus * talent_index[5] *0.04)) *\
                                   gs_mod * (1+(talent_index[17]*0.07*eq_dur>0))*\
                                    (1+((reso_dur>0)*stat_reso*0.0007)))
                gs_mod = 1
                js_bonus2 = 0
            if dmg_jt!=0:
                sim_dmg_jt.append(dmg_jt * (1+(js_bonus * talent_index[5] *0.04)) * jt_mod*\
                                   (1+(talent_index[17]*0.07*eq_dur>0))*\
                                    (1+((reso_dur>0)*stat_reso*0.0007)))
                jt_mod = 1
                js_bonus2 = 0
            if dmg_js!=0:
                sim_dmg_js.append(dmg_js * (1+(js_bonus * talent_index[5] *0.04)) *\
                                   (js_mod*(1+(talent_index[15]*0.04))) *\
                                    (1+(talent_index[17]*0.07*eq_dur>0))*\
                                    (1+((reso_dur>0)*stat_reso*0.0007)))
                js_mod = 1
                js_bonus2 = 0
            if dmg_eq!=0:
                sim_dmg_eq.append(dmg_eq * (1+(js_bonus * talent_index[5] *0.04)) *\
                                   eq_mod * (1+((reso_dur>0)*stat_reso*0.0007)))
                eq_mod = 1
                js_bonus2 = 0
            if dmg_aa!=0:
                tor_haste += (0.0125 * talent_index[20])
                if dmg_gs==dmg_jt==dmg_js==dmg_eq==0:
                    sim_dmg_aa.append(dmg_aa * (1+(js_bonus * talent_index[5] *0.04)) * aa_mod *\
                                       (1+(talent_index[17]*0.07*eq_dur>0))*\
                                        (1+((reso_dur>0)*stat_reso*0.0007)))
                    aa_mod = 1                    
                elif not(dmg_gs==dmg_jt==dmg_js==dmg_eq==0):
                    sim_dmg_aa.append(dmg_aa * aa_mod * (1+(talent_index[17]*0.07*eq_dur>0))*\
                                      (1+((reso_dur>0)*stat_reso*0.0007))) 
                    aa_mod = 1

            sim_dmg=sim_dmg_gs+sim_dmg_jt+sim_dmg_js+sim_dmg_eq+sim_dmg_aa

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


        sim_res_gs.append(int(sum(sim_dmg_gs)))
        sim_res_jt.append(int(sum(sim_dmg_jt)))
        sim_res_js.append(int(sum(sim_dmg_js)))
        sim_res_eq.append(int(sum(sim_dmg_eq)))
        sim_res_aa.append(int(sum(sim_dmg_aa)))

        sim_res_gs_ct.append(len(sim_dmg_gs))
        sim_res_jt_ct.append(len(sim_dmg_jt))
        sim_res_js_ct.append(len(sim_dmg_js))
        sim_res_eq_ct.append(len(sim_dmg_eq))
        sim_res_aa_ct.append(len(sim_dmg_aa))

        sim_res_all.append(int(sum(sim_dmg)))
        sim_res_dps.append(int(sum(sim_dmg)/sim_dur))

        res_act_ct.append(res_count)   

        print("Iteration ",i,"/",until,end="\r")

Sim_run(sim_iter)

print(f"{1-stat_cdr:,.3f} GCD time     ")   
print(f"{sim_iter:,.0f} Simulations")
print(f"{sim_dur:,.0f} Second Fight Duration\n")
print(" Damage Stats   Min, 25%, 50%, 75%, Max")
print("  GS  Damage: ",np.quantile([int(i / j) for i, j in zip(sim_res_gs, sim_res_gs_ct)],[0,0.25,0.50,0.75,1.00],method="nearest"))
print("  JT  Damage: ",np.quantile([int(i / j) for i, j in zip(sim_res_jt, sim_res_jt_ct)],[0,0.25,0.50,0.75,1.00],method="nearest"))
print("  JS  Damage: ",np.quantile([int(i / j) for i, j in zip(sim_res_js, sim_res_js_ct)],[0,0.25,0.50,0.75,1.00],method="nearest"))
print("  EQ  Damage: ",np.quantile([int(i / j) for i, j in zip(sim_res_eq, sim_res_eq_ct)],[0,0.25,0.50,0.75,1.00],method="nearest"))
print("  AA  Damage: ",np.quantile([int(i / j) for i, j in zip(sim_res_aa, sim_res_aa_ct)],[0,0.25,0.50,0.75,1.00],method="nearest"))
print("Total Damage: ",np.quantile(sim_res_all,[0,0.25,0.50,0.75,1.00],method="nearest"))
print("  Avg.   DPS: ",np.quantile(sim_res_dps,[0,0.25,0.50,0.75,1.00],method="nearest"))

'''
print("# of GS Hits: ",sim_res_gs_ct)
print("# of JT Hits: ",sim_res_jt_ct)
print("# of JS Hits: ",sim_res_js_ct)
print("# of EQ Hits: ",sim_res_eq_ct)
print("# of AA Hits: ",sim_res_aa_ct)
print("# of inscription: ",res_act_ct)
'''