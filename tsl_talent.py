import tkinter as tk
from tkinter import messagebox
from functools import partial

talent_index = []
entries = [0]
max_pt = 0

def submit_values():   
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
	'''
	label = tk.Label(root, text = t_name,bg=root["bg"])
	label.grid(row = rowpos, column = (4*colpos)-2, sticky="nsew")
	tooltip = None
	label.bind("<Enter>", lambda event: setattr(label, 'tooltip', show_tooltip(label, e)))
	label.bind("<Leave>", lambda event: hide_tooltip(getattr(label, 'tooltip')))
	'''


talent("Glory\nStrike: ",1,1,1,3,\
       "Glory Strike's base damage is increased by 5/10/15%.\nFor the next 6 seconds, you gain 2/4/6% haste.")
talent("Justice\nThump Dmg%: ",1,1,2,3,\
       "Justice Thump's damage is increased by 6/12/18%.\nWhen enhanced, it is increased by 10/20/30% instead.")
talent("Critical\nStrike: ",2,2,1,3,\
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
talent("Judgement\nSword: ",0,4,1,1,\
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

