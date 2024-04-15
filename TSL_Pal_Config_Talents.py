import tkinter as tk
from tkinter import messagebox

talent_index = []
entries = [0]

def submit_values():   
    total_points = sum(int(entry.get()) for entry in entries[1:])
    if total_points > 32:
        root.destroy()
    if total_points < 32:
        root.destroy()
    try:
        talent_index = [int(entry.get()) for entry in entries[1:]]
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values.")
        return

    root.destroy()
    print(talent_index)

# Create main window
root = tk.Tk()
root.title("Userform")
root.geometry("490x380+1400+200")
root.configure(bg="#ffffff")

#Create total label
total_label = tk.Label(root, text="Total Points: 0", bg=root["bg"])
total_label.grid(row=11, column=5, columnspan=4)

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
def talent(a="name",b=0,c=1,d=1,e="Tooltip requires update"):
    # Function to increment the value of the associated entry widget
    def increment_value():
        current_value = int(entry.get())
        if current_value<3:
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
    increment_button = tk.Button(root, text="+/-", command=increment_value, width=2,bg=root["bg"])
    increment_button.grid(row=c, column=(4*d))
    # Bind right-click event to decrement function
    increment_button.bind("<Button-3>", lambda event: decrement_value())

    label = tk.Label(root, text=a,bg=root["bg"])
    label.grid(row = c, column = (4*d)-2, sticky="nsew")
    tooltip = None
    label.bind("<Enter>", lambda event: setattr(label, 'tooltip', show_tooltip(label, e)))
    label.bind("<Leave>", lambda event: hide_tooltip(getattr(label, 'tooltip')))
    entry = tk.Entry(root, width=6,bg=root["bg"])
    entry.insert(0, int(b))
    entry.grid(row = c, column = (4*d)-1, sticky="nsew")
    entries.append(entry)


talent("Glory\nStrike: ",1,1,1,\
       "Glory Strike's base damage is increased by 5/10/15%.\nFor the next 6 seconds, you gain 2/4/6% haste.")
talent("Justice\nThump Dmg%: ",1,1,2,\
       "Justice Thump's damage is increased by 6/12/18%.\nWhen enhanced, it is increased by 10/20/30% instead.")
talent("Critical\nStrike: ",1,2,1,\
       "Increase your Critical Strike chance by 1.5/3.0/4.5%")
talent("Power of\nGlory: ",3,2,2,\
       "You have a 33.3/66.6/100% chance to gain 1 level\nof Power of Glory when you consume a Glory Judgement.")
talent("Judgement\nStrike: ",3,2,3,\
       "Judgement Strike increases the damage and\ncritical strike damage of your next skill by 4/8/12%")
talent("Punishing\nStorm: ",0,3,1,\
       "Your Punishing Storm deals 5/10/15% more damage.")
talent("Earthquake\nGlory: ",3,3,2,\
       "After you cast Earthquake, you have a 33/66/100%\nto gain a Glory Judgement (prioritizes skills that are not already enhanced.)")
talent("Justice\nThump Charges: ",1,3,3,\
       "Justice Thump can now store 2 charges.\nWhen Glory Strike resets the cooldown of\nJustice Thump, it grants a charge instead.")
talent("Judgement\nSword: ",1,4,1,\
       "Replace Judgement Strike with Judgement Sword.")
talent("Glory\nStrike x3: ",1,4,2,\
       "Every 3rd Glory Strike has a 15/30/45%\nincreased Critical Strike Chance.")
talent("Judgement Sword\nRecharge: ",0,5,1,\
       "Judgement Sword has a 10/20/30%\nto regain a charge and increase the damage of the next\nJudgement Sword by 4/8/12%.")
talent("Glory\nJudgement: ",3,5,2,\
       "Consecutive Glory Judgements increases your next\nskill's Critical strike chance by 10/20/30%.\nOtherwise, your next skill deals 12/24/36% increased damage.")
talent("Judgement\nStrike Dmg%: ",2,5,3,\
       "Your Judgement Strike's Critical Strike chance is increased by 3/6%.\nWhen Judgement Strike critically hits, your next skill deals 5/10% more damage.")
talent("Judgement\nSword CHD: ",0,6,1,\
       "You deal 15/30/45% increased critical damage to targets afflicted\nby Judgement Sword's damage-over-time effect.")
talent("Judgement\nStrike Crit: ",3,6,2,\
       "Judgement Strike deals 4/8/12% more damage.\nIf Judgement Strike critically hits or gains Glory Judgement,\nthe cooldown is reduced by 1/2/3 seconds.")
talent("Judgement\nSword DOT: ",0,7,1,\
       "Judgement Sword deals 10/20/30% more damage immediately,\nand the damage-over-time is increased by 30/60/90%.")
talent("Earthquake\nDmg%: ",2,7,2,\
       "Your Earthquake deals 10/20% more damage,\nand you deal 7/14% increased damage to affected targets for 4 seconds.")
talent("Trial of Rage\nRaid: ",0,8,2,\
       "Your party is affected by Trial of Rage with 50% effect.")
talent("Trial of Rage\nCDR: ",2,8,3,\
       "Trial of Rage lasts 1.5/3 seconds longer\nand its cooldown is reduced by 15/30 seconds.")
talent("Glory\nJudgement RNG ",3,9,1,\
       "Whenever you gain a Glory Judgement from Power of Glory,\nthere is a 3.33/6.66/10% to gain another Glory Judgement.")
talent("Trial of Rage\nStack ",2,9,3,\
       "While Trial of Rage is active, you gain 1.25/2.5%\ncritical strike chance and haste\nwhenever you deal damage.")

# Create submit button
submit_button = tk.Button(root, text="Submit", command=submit_values, width = 60, bg=root["bg"], fg="#000000")
submit_button.grid(row=12, column=0, columnspan=14)

# Load default talent points total (32)
update_total()

root.mainloop()

