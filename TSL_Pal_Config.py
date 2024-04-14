import tkinter as tk
from tkinter import messagebox

def submit_values():
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

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values.")
    root.destroy()

    print(stat_atk)
    print(stat_chc)
    print(stat_chd)
    print(stat_cdr)
    print(stat_reso)
    print(sim_dur)
    print(sim_iter)
    print(ext_raid_buff)

# Create main window
root = tk.Tk()
root.title("Userform")

# Default values
default_values = {'Attack': 700, 'Crit. Chance': 0.42, 'Crit. Damage': 1.65, \
                  'Cooldown': 0.19, 'Resonance': 1000, 'Fight Dur.': 90, '# of Sims': 100, 'External Raid Buffs': "Yes"}

# Create labels and entry fields for each variable with default values
labels = ['Attack', 'Crit. Chance', 'Crit. Damage', 'Cooldown', 'Resonance', 'Fight Dur.', '# of Sims', 'External Raid Buffs']
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