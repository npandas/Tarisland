#import modules
import random       #RNG generation for crits and procs
import math         #for math.floor() for a few calculations
import numpy as np  #allows us to get quartile results, e.g., top 10%
import subprocess   #in order to incorporate other scripts

import tkinter as tk
from tkinter import messagebox

#Starting Stats Init.
def submit_values():
    global stat_atk,stat_chc,stat_chd,stat_cdr,stat_reso,sim_dur,sim_iter, ext_raid_buff,inscript_start
    try:
        stat_atk = float(entries[0].get())
        stat_chc = float(entries[1].get())
        stat_chd = float(entries[2].get())
        stat_cdr = float(entries[3].get())
        stat_reso = int(entries[4].get())
        sim_dur = int(entries[5].get())
        sim_iter = int(entries[6].get())  
        ext_raid_buff = entries[7].get()
        if ext_raid_buff.isdigit():
            ext_raid_buff = int(ext_raid_buff)
        elif isinstance(ext_raid_buff, str):
            ext_raid_buff = ext_raid_buff.title()
        inscript_start = entries[8].get()
        if inscript_start.isdigit():
            inscript_start = int(inscript_start)
        elif isinstance(inscript_start, str):
            inscript_start = inscript_start.title()

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values.")
    root.destroy()

# Create main window
root = tk.Tk()
root.title("Userform")

# Default values
default_values = {'Attack': 700, 'Crit. Chance': 0.42, 'Crit. Damage': 1.65, \
                  'Cooldown': 0.19, 'Resonance': 1000, 'Fight Dur.': 90, '# of Sims': 100, \
                  'External Raid Buffs': "Yes", 'Start w/ Inscription': "Yes"}

# Create labels and entry fields for each variable with default values
labels = ['Attack', 'Crit. Chance', 'Crit. Damage', 'Cooldown', 'Resonance', \
          'Fight Dur.', '# of Sims', 'External Raid Buffs', 'Start w/ Inscription']
entries = []

for i, label_text in enumerate(labels):
    label = tk.Label(root, text=label_text + ":")
    label.grid(row=i, column=0)
    entry = tk.Entry(root)
    entry.insert(0, str(default_values[label_text]))
    entry.grid(row=i, column=1)
    entries.append(entry)

# Create submit button
submit_button = tk.Button(root, text="Submit", command=submit_values)
submit_button.grid(row=len(labels), column=0, columnspan=2)

root.geometry("+%d+%d" % (1400, 200))
root.mainloop()

if inscript_start in [1,"Yes"]:
    inscript_start = 1000
else:
    inscript_start = 0


#Talents Init.
from functools import partial
talent_index = []
entries = [0]
max_pt = 0

def submit_values():   
    global talent_index
    total_points = sum(int(i.get()) for i in entries[1:])
    if total_points > 32:
        print("Too many talent points.")
        root.destroy()
        return
    if total_points < 32:
        print("Insufficient talent points.")
        root.destroy()
        return
    else:
        talent_index = [int(i.get()) for i in entries[1:]]
    root.destroy()
    print(talent_index)
    return 

# Create main window
root = tk.Tk()
root.title("Paladin - Justice Talents")
root.geometry("480x560+1400+200")
root.configure(bg="#ffffff")

def update_total():
    total = sum(int(entry.get()) for entry in entries[1:])
    total_label.config(text=f"Total Points: {total}")

# Function to show tooltip
def show_tooltip(widget, tooltip_text):
    x, y, _, _ = widget.bbox("insert")
    x += widget.winfo_rootx() + 25
    y += widget.winfo_rooty() + 25
    
    tooltip = tk.Toplevel(widget)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry(f"+{x}+{y}")
    
    label = tk.Label(tooltip, text=tooltip_text, background="#ffffe0", relief="solid", borderwidth=1)
    label.pack(ipadx=5)

    return tooltip

# Function to hide tooltip
def hide_tooltip(tooltip):
    if tooltip:
        tooltip.destroy()

#Create entry fields
def talent(t_name="name",defval=0,rowpos=1,colpos=1,max_pt=1,e="Tooltip requires update"):
	#Create entry user input for talents
	entry = tk.Entry(root, width=6,bg=root["bg"])
	entry.insert(0, int(defval))
	entry.grid(row = rowpos*2, column = (4*colpos)-1, sticky="nsew")
	entries.append(entry)
	# Function to increment the value of the associated entry widget
	def increment_value(entry):
		current_value = int(entry.get())
		if current_value<=(max_pt-1):
			entry.delete(0, tk.END)  
			entry.insert(0, str(current_value + 1)) 
			update_total()
	# Function to decrement the value of the associated entry widget
	def decrement_value():
		current_value = int(entry.get())
		if current_value>0:
			entry.delete(0, tk.END)
			entry.insert(0, str(current_value - 1))
			update_total()

	# Create button to increment value
	increment_button = tk.Button(root, text = t_name, command=partial(increment_value, entry), width=14,bg=root["bg"])
	increment_button.grid(row=rowpos*2, column=(4*colpos)-2, sticky="nsew")
	# Bind right-click event to decrement function
	increment_button.bind("<Button-3>", lambda event: decrement_value())
	tooltip = None
	increment_button.bind("<Enter>", lambda event: setattr(increment_button, 'tooltip', show_tooltip(increment_button, e)))
	increment_button.bind("<Leave>", lambda event: hide_tooltip(getattr(increment_button, 'tooltip')))

	#Adds space between rows
	for row_index in range(1, 24, 2):
		root.grid_rowconfigure(row_index, minsize=10)
	#Adds space before first column
	root.grid_columnconfigure(0, minsize=20)
	root.grid_columnconfigure(15, minsize=20)

talent("Glory\nStrike: ",1,1,1,3,\
       "Glory Strike's base damage is increased by 5/10/15%.\nFor the next 6 seconds, you gain 2/4/6% haste.")
talent("Justice\nThump Dmg%: ",1,1,2,3,\
       "Justice Thump's damage is increased by 6/12/18%.\nWhen enhanced, it is increased by 10/20/30% instead.")
talent("Critical\nStrike: ",1,2,1,3,\
       "Increase your Critical Strike chance by 1.5/3.0/4.5%")
talent("Power of\nGlory: ",3,2,2,3,\
       "You have a 33.3/66.6/100% chance to gain 1 level\nof Power of Glory when you consume a Glory Judgement.")
talent("Judgement\nStrike: ",3,2,3,3,\
       "Judgement Strike increases the damage and\ncritical strike damage of your next skill by 4/8/12%")
talent("Punishing\nStorm: ",0,3,1,3,\
       "Your Punishing Storm deals 5/10/15% more damage.")
talent("Earthquake\nGlory: ",3,3,2,3,\
       "After you cast Earthquake, you have a 33/66/100%\nto gain a Glory Judgement (prioritizes skills that are not already enhanced.)")
talent("Justice\nThump Charges: ",1,3,3,1,\
       "Justice Thump can now store 2 charges.\nWhen Glory Strike resets the cooldown of\nJustice Thump, it grants a charge instead.")
talent("Judgement\nSword: ",1,4,1,1,\
       "Replace Judgement Strike with Judgement Sword.")
talent("Glory\nStrike x3: ",1,4,2,3,\
       "Every 3rd Glory Strike has a 15/30/45%\nincreased Critical Strike Chance.")
talent("Judgement Sword\nRecharge: ",0,5,1,3,\
       "Judgement Sword has a 10/20/30%\nto regain a charge and increase the damage of the next\nJudgement Sword by 4/8/12%.")
talent("Glory\nJudgement: ",3,5,2,3,\
       "Consecutive Glory Judgements increases your next\nskill's Critical strike chance by 10/20/30%.\nOtherwise, your next skill deals 12/24/36% increased damage.")
talent("Judgement\nStrike Dmg%: ",2,5,3,2,\
       "Your Judgement Strike's Critical Strike chance is increased by 3/6%.\nWhen Judgement Strike critically hits, your next skill deals 5/10% more damage.")
talent("Judgement\nSword CHD: ",0,6,1,3,\
       "You deal 15/30/45% increased critical damage to targets afflicted\nby Judgement Sword's damage-over-time effect.")
talent("Judgement\nStrike Crit: ",3,6,2,3,\
       "Judgement Strike deals 4/8/12% more damage.\nIf Judgement Strike critically hits or gains Glory Judgement,\nthe cooldown is reduced by 1/2/3 seconds.")
talent("Judgement\nSword DOT: ",0,7,1,3,\
       "Judgement Sword deals 10/20/30% more damage immediately,\nand the damage-over-time is increased by 30/60/90%.")
talent("Earthquake\nDmg%: ",2,7,2,2,\
       "Your Earthquake deals 10/20% more damage,\nand you deal 7/14% increased damage to affected targets for 4 seconds.")
talent("Trial of Rage\nRaid: ",0,8,2,2,\
       "Your party is affected by Trial of Rage with 25/50% effect.")
talent("Trial of Rage\nCDR: ",2,8,3,2,\
       "Trial of Rage lasts 1.5/3 seconds longer\nand its cooldown is reduced by 15/30 seconds.")
talent("Glory\nJudgement RNG ",3,9,1,3,\
       "Whenever you gain a Glory Judgement from Power of Glory,\nthere is a 3.33/6.66/10% to gain another Glory Judgement.")
talent("Trial of Rage\nStack ",2,9,3,2,\
       "While Trial of Rage is active, you gain 1.25/2.5%\ncritical strike chance and haste\nwhenever you deal damage.")

#Create total label
total_label = tk.Label(root, text="Total Points: 0", bg=root["bg"])
total_label.grid(row=24, column=5, columnspan=4)

# Create submit button
submit_button = tk.Button(root, text="Submit", command=submit_values, width = 60, bg=root["bg"], fg="#000000")
submit_button.grid(row=26, column=0, columnspan=14)

# Load default talent points total (32)
update_total()

root.mainloop()

#Adds filler 0, first element is ignored by the main simulation
talent_index.insert(0,0)

#Cancels script if talents are incorrect
if sum(talent_index)>32:
    print(sum(talent_index)-32," too many Talent Points.")
    quit()
elif sum(talent_index)<32:
    print("Missing ",32-sum(talent_index)," Talent Points.")
    quit()
elif sum(talent_index)==32:
    print("Talent Points Loaded Succesfully.\n")

#Initialize Lists Recording every simulation iteration statistics
sim_rec_gs,sim_rec_jt,sim_rec_js,sim_rec_eq,sim_rec_aa,sim_rec_all,sim_rec_dps = [],[],[],[],[],[],[]
sim_rec_gs_ct,sim_rec_jt_ct,sim_rec_js_ct,sim_rec_eq_ct,sim_rec_aa_ct = [],[],[],[],[]
sim_rec_res_ct = []
data_list = []
def Sim_run(until):

    for i in range(until):
        #define variables
        cd_gs,cd_jt,cd_js,cd_eq,cd_aa=(0,0,0,0,0)
        #Tracks JS bonuses if talented, GS crit mod% counter, and EQ dmg% buff
        js_bonus1,js_bonus2,gs_crit_ct,eq_dur = (0,0,0,0)
        #Set charges of GS and JT (if talented)
        gs_ct,jt_ct = (2,talent_index[8]+1)
        #GCD based on CDR and adjusted GCD for haste effects 
        gcd,a_gcd=(1-stat_cdr,1-stat_cdr)
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
        sim_dmg_all,sim_dmg_gs,sim_dmg_jt,sim_dmg_js,sim_dmg_eq,sim_dmg_aa = [],[],[],[],[],[]
        #allows sim to loop in 0.10 second intervals
        increment = 0.10

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
                sim_inst_res_ct += 1
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
                tor_atk = (63 + (stat_atk * 0.04) + 90 + 90 + 60 + 60)# * (1+(0.23*3))
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
                    pVerdict = 3 - Verdict
                    Verdict = 3              
                else:
                    Verdict = random.randint(1,2)
                    if pVerdict == 0:
                        pVerdict = Verdict
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
                #Record to pandas-excel
                data_list.append({'Sim #': i+1, 'Time': sim_dur - duration, 'Skill': "GS", 'Damage': \
                            dmg_gs * gs_mod * (1 + ((reso_dur > 0) * stat_reso * 0.0007))})
                gs_mod = 1
                js_bonus1 = 0
                js_bonus2 = 0
                verdict_bonus = 0
            #Tallies JT damage and consume JS bonus damage
            if dmg_jt!=0:
                #JS Bonus, JS Crit Bonus, EQ Bonus, Verdict Bonus
                jt_mod *= (1+(js_bonus1 * talent_index[5] * 0.04)) * (1+(js_bonus2 * talent_index[13] * 0.05))\
                        * (1+((eq_dur>0) * talent_index[17] * 0.07)) * (1+((verdict_bonus==2)*talent_index[12]*0.12))
                sim_dmg_jt.append(int(dmg_jt * jt_mod * (1+((reso_dur>0)*stat_reso*0.0007))))
                sim_dmg_all.append(sim_dmg_jt[-1])
                #Record to pandas-excel
                data_list.append({'Sim #': i+1, 'Time': sim_dur - duration, 'Skill': "JT", 'Damage': \
                            dmg_jt * jt_mod * (1 + ((reso_dur > 0) * stat_reso * 0.0007))})
                jt_mod = 1
                js_bonus1 = 0
                js_bonus2 = 0
                verdict_bonus = 0
            #Tallies JS damage and consume JS bonus damage
            if dmg_js!=0:
                #JS Talent Bonus
                js_mod *= 1 + (talent_index[15] * 0.04)
                #JS Bonus, JS Crit Bonus, EQ Bonus, Verdict Bonus
                js_mod *= (1+(js_bonus1 * talent_index[5] * 0.04)) * (1+(js_bonus2 * talent_index[13] * 0.05))\
                        * (1+((eq_dur>0) * talent_index[17] * 0.07)) * (1+((verdict_bonus==2)*talent_index[12]*0.12))
                sim_dmg_js.append(int(dmg_js * js_mod * (1+((reso_dur>0)*stat_reso*0.0007))))
                sim_dmg_all.append(sim_dmg_js[-1])
                #Record to pandas-excel
                data_list.append({'Sim #': i+1, 'Time': sim_dur - duration, 'Skill': "JS", 'Damage': \
                            dmg_js * js_mod * (1 + ((reso_dur > 0) * stat_reso * 0.0007))})
                js_mod = 1
                js_bonus1 = 0
                js_bonus2 = 0
                verdict_bonus = 0
            #Tallies EQ damage and consume JS bonus damage
            if dmg_eq!=0:
                #JS Bonus, JS Crit Bonus, [Impossible to get EQ bonus w/o 87% CDR], Verdict Bonus
                eq_mod *= (1+(js_bonus1 * talent_index[5] * 0.04)) * (1+(js_bonus2 * talent_index[13] * 0.05))\
                        * (1+((verdict_bonus==2)*talent_index[12]*0.12))
                sim_dmg_eq.append(int(dmg_eq * eq_mod * (1+((reso_dur>0)*stat_reso*0.0007))))
                sim_dmg_all.append(sim_dmg_eq[-1])
                #Record to pandas-excel
                data_list.append({'Sim #': i+1, 'Time': sim_dur - duration, 'Skill': "EQ", 'Damage': \
                            dmg_eq * eq_mod * (1 + ((reso_dur > 0) * stat_reso * 0.0007))})
                eq_mod = 1
                js_bonus1 = 0
                js_bonus2 = 0
                verdict_bonus = 0
            #Tallies AA damage
            if dmg_aa!=0:
                #ToR stacking crit/haste buff
                tor_chc += (0.0125 * talent_index[21])
                tor_haste += (0.0125 * talent_index[21])
                sim_dmg_aa.append(int(dmg_aa * aa_mod * (1+((reso_dur>0)*stat_reso*0.0007))))
                sim_dmg_all.append(sim_dmg_aa[-1])
                #Record to pandas-excel
                data_list.append({'Sim #': i+1, 'Time': sim_dur - duration, 'Skill': "AA", 'Damage': \
                            dmg_aa * aa_mod * (1 + ((reso_dur > 0) * stat_reso * 0.0007))})
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
        #Calcualtes DPS from each sim
        sim_rec_dps.append(int(sum(sim_dmg_all)/sim_dur))
        #Tracks Resonance/Inscription Activations
        sim_rec_res_ct.append(sim_inst_res_ct)
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
print("   GS Damage: ",dmg_spread(sim_rec_gs,sim_rec_gs_ct,0.5,0.05,0.95))
print("   JT Damage: ",dmg_spread(sim_rec_jt,sim_rec_jt_ct,0.5,0.05,0.95))
print("   JS Damage: ",dmg_spread(sim_rec_js,sim_rec_jt_ct,0.5,0.05,0.95))
print("   EQ Damage: ",dmg_spread(sim_rec_eq,sim_rec_eq_ct,0.5,0.05,0.95))
print("Total Damage: ",dmg_spread(sim_rec_all,None,0.5,0.05,0.95))
print("Avg. Sim Dmg: ",dmg_spread(sim_rec_dps,None,0.5,0.05,0.95))
#Save results to Excel
import pandas as pd
print("\nExporting data to Excel...",end="\r")
data_export = pd.DataFrame(columns=["Sim #", "Time", "Skill", "Damage"])
data_export = pd.DataFrame(data_list)
data_export.to_excel("Sim Data.xlsx", index=False)

#To check Skill Cast Frequency
'''
print("# of GS Hits: ",sim_rec_gs_ct)
print("# of JT Hits: ",sim_rec_jt_ct)
print("# of JS Hits: ",sim_rec_js_ct)
print("# of EQ Hits: ",sim_rec_eq_ct)
print("# of AA Hits: ",sim_rec_aa_ct)
print("# of inscription: ",sim_rec_res_ct)
'''
# if no values in list, skips quartile, common with short fight durations
# Shows more detailed statistics
'''
print(" Damage Stats   Min, 25%, 50%, 75%, Max")
print("   GS Damage: ",np.quantile([int(i / j) if j!=0 else 0 for i, j in zip(sim_rec_gs, sim_rec_gs_ct)],[0,0.25,0.50,0.75,1.00],method="nearest"))
print("   JT Damage: ",np.quantile([int(i / j) if j!=0 else 0 for i, j in zip(sim_rec_jt, sim_rec_jt_ct)],[0,0.25,0.50,0.75,1.00],method="nearest"))
print("   JS Damage: ",np.quantile([int(i / j) if j!=0 else 0 for i, j in zip(sim_rec_js, sim_rec_js_ct)],[0,0.25,0.50,0.75,1.00],method="nearest"))
print("   EQ Damage: ",np.quantile([int(i / j) if j!=0 else 0 for i, j in zip(sim_rec_eq, sim_rec_eq_ct)],[0,0.25,0.50,0.75,1.00],method="nearest"))
print("   AA Damage: ",np.quantile([int(i / j) if j!=0 else 0 for i, j in zip(sim_rec_aa, sim_rec_aa_ct)],[0,0.25,0.50,0.75,1.00],method="nearest"))
print("Total Damage: ",np.quantile(sim_rec_all,[0,0.25,0.50,0.75,1.00],method="nearest"))
print("Avg. Sim DPS: ",np.quantile(sim_rec_dps,[0,0.25,0.50,0.75,1.00],method="nearest"))
'''

input("Data Exported Successfully.\nPress any key to exit.")