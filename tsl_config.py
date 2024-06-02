import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

folderpath = "talent_images/"
winsizex = 820
winsizey = 580

def main():
    #Init Lists
    stat_import = []
    entries = []
    # Create main window
    root = tk.Tk()
    root.title("Sim Settings")
    root.geometry(f"{winsizex}x{winsizey}+1400+200")

    # Load the background image
    background_image = ImageTk.PhotoImage(Image.open(folderpath+"bg.png"))
    # Create a label to display the background image
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    #Puts background image behind other button labels
    background_label.lower()
    
    # Default values
    defaults = {'Attack': 650, 'Crit. Chance': 0.42, 'Crit. Damage': 1.65, \
                    'Cooldown': 0.19, 'Combo': 0.05, 'Combo Damage': 1.50, 'Omni': 300, 'Focus': 600, \
                    'Resonance': 1200, 'Enemy Armor': 500, 'Fight Dur.': 60, '# of Sims': 100, \
                    'External Raid Buffs': "No", 'Start w/ Inscription': "No", 'Start w/ Echo': "No", \
                    'GS Damage': 325, 'JT Damage': 195, 'JS Damage': 351, 'EQ Damage': 0, \
                    'GS Damage during Echo': 0.00, 'x1 GS Damage after Echo': 0.00, '30% Chance x1 GS Damage': 0.00, \
                    'JT Damage during Echo': 0.39, 'x1 JT Damage after Echo': 0.00, '30% Chance x1 JT Damage': 0.00, \
                    'JS Damage during Echo': 0.00, 'x1 JS Damage after Echo': 0.00, '30% Chance x1 JS Damage': 1.32, \
                    'EQ Damage during Echo': 0.00, 'x1 EQ Damage after Echo': 0.00, '30% Chance x1 EQ Damage': 0.00, \
                    '% Fatuina Echo w/ GS': 0.40, '% Fatuina Echo w/ JT': 0.00, \
                    '% Fatuina Echo w/ JS': 0.00, '% Fatuina Echo w/ EQ': 0.00, \
                    'Trial of Rage bonus ATK': 132}

    # Create labels and entry fields for each variable with default values
    labels = list(defaults.keys())


    def submit_value():
        try:
            for i in range(len(entries)):
                if i <=5:
                    stat_import.append(float(entries[i].get()))
                elif 6 <= i <= 11:
                    stat_import.append(int(entries[i].get()))
                elif 12 <= i <= 14:
                    stat_import.append(entries[i].get())
                else:
                    stat_import.append(float(entries[i].get()))

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values.")
            return
        
        root.destroy()

    #General cropped label_background based on base background
    xpos1,ypos1,xpos2,ypos2 = 0,0,220,20
    bg_lbl_img=[]
    for i, label_text in enumerate(labels):
        bg_lbl_img.append(ImageTk.PhotoImage(Image.open(folderpath+"bg.png").crop((xpos1,ypos1,xpos2,ypos2))))
        ypos1 = ypos2+2
        ypos2 += 20
        if i in [14,24]:
            ypos1,ypos2=0,20
            xpos1+=223+39
            xpos2+=223+39

    #Grid Sim Settings Structure
    col_pos = 0
    row_spacer = 0
    for i, label_text in enumerate(labels):    
        if i in [15,25]:
            row_spacer = -i
            col_pos += 2
        label = tk.Label(root, text=label_text + ":",width=220,image=bg_lbl_img[i],\
                compound=tk.CENTER,bd=0,font=("Helvetica", 10,"bold"),bg="#919191",fg="#fcd317")
        label.grid(row=i+row_spacer, column = col_pos,padx=0,pady=0)
        entry = tk.Entry(root, width=6,bg="#ff5454")
        entry.insert(0, str(defaults[label_text]))
        entry.grid(row=i+row_spacer, column = col_pos+1,padx=0,pady=0)

        entries.append(entry)

    # Create submit button
    submit_button = tk.Button(root, text="Submit", command=submit_value, width=72, bg="#addded")
    submit_button.grid(row=11, rowspan=20,column=2,columnspan=8, pady=2)

    #Calls TKInter window
    root.mainloop()
    
    #edit this range once I fix additional stats in main.py
    return stat_import

#Runs script when executed directly.
if __name__ == "__main__":
	print(main())