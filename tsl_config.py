import tkinter as tk
from tkinter import messagebox

def main():
    stat_import = []
    # Default values
    defaults = {'Attack': 700, 'Crit. Chance': 0.42, 'Crit. Damage': 1.65, \
                    'Cooldown': 0.19, 'Resonance': 1000, 'Fight Dur.': 90, '# of Sims': 100, \
                    'External Raid Buffs': "Yes", 'Start w/ Inscription': "Yes", \
                    'GS Dmg EoD': 0, '30% GS EoD': 0, \
                    'JT Dmg EoD': 0, '30% JT EoD': 0, \
                    'JS Dmg EoD': 0, '30% JS EoD': 0, \
                    'EQ Dmg EoD': 0, '30% EQ EoD': 0, \
                    'GS Echo Stack': 0, 'JT Echo Stack': 3, \
                    'JS Echo Stack': 3, 'EQ Echo Stack': 0, \
                    'ToR Bonus ATK': 150, 'ToR Bonus %': 0.06}

    # Create labels and entry fields for each variable with default values
    labels = ['Attack', 'Crit. Chance', 'Crit. Damage', 'Cooldown', 'Resonance', \
            'Fight Dur.', '# of Sims', 'External Raid Buffs', 'Start w/ Inscription', \
            'GS Dmg EoD', '30% GS EoD', 'JT Dmg EoD', '30% JT EoD', 'JS Dmg EoD', \
            '30% JS EoD', 'EQ Dmg EoD', '30% EQ EoD', 'GS Echo Stack', 'JT Echo Stack', \
            'JS Echo Stack', 'EQ Echo Stack', 'ToR Bonus ATK', 'ToR Bonus %']
    entries = []

    def submit_value():
        try:
            for i in range(len(entries)):
                if i <=3:
                    stat_import.append(float(entries[i].get()))
                elif 4 <= i <= 6:
                    stat_import.append(int(entries[i].get()))
                if 7 <= i <= 8:
                    stat_import.append(entries[i].get())

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values.")
            return
        
        root.destroy()

    # Create main window
    root = tk.Tk()
    root.title("Sim Settings")

    for i, label_text in enumerate(labels):
        label = tk.Label(root, text=label_text + ":")
        if i<=8:
            label.grid(row=i, column=0)
        elif 8<i<=16:
            label.grid(row=i-9, column=2)
        elif i>16:
            label.grid(row=i-17, column=4)
        entry = tk.Entry(root, width=8)
        entry.insert(0, str(defaults[label_text]))
        if i<=8:
            entry.grid(row=i, column=1)
        elif 8<i<=16:
            entry.grid(row=i-9, column=3)
        elif i>16:
            entry.grid(row=i-17, column=5)
        entries.append(entry)

    # Create submit button
    submit_button = tk.Button(root, text="Submit", command=submit_value, width=30)
    submit_button.grid(row=len(labels), column=0, columnspan=6)
    root.geometry("420x260+1400+200")
    root.mainloop()
    
    #edit this range once I fix additional stats in main.py
    return stat_import[0:9]

#Runs script when executed directly.
if __name__ == "__main__":
	main()
	print(talent_index)