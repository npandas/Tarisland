import tkinter as tk
from functools import partial
from PIL import Image, ImageTk

#Declare sub-folder location for images
folderpath = "talent_images/"

def main():
	entries = [0]

	def submit_values(): 
		global talent_index

		total_points = sum(int(i.get()) for i in entries[1:])
		if total_points > 32:
			print("Too many talent points.")
		if total_points < 32:
			print("Insufficient talent points.")
		talent_index = [0]
		talent_index.extend([int(i.get()) for i in entries[1:]])

		root.destroy()
		return talent_index

	# Create main window
	root = tk.Tk()
	root.title("Paladin - Justice Talents")
	root.geometry("800x600+1400+200")
	
	background_image = Image.open(folderpath+"bg.png")
	background_photo = ImageTk.PhotoImage(background_image)
	# Create a label to hold the background image
	background_label = tk.Label(root, image=background_photo)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)
	# Ensure the label stays behind all other widgets
	background_label.lower()

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
	def talent(t_image="name",defval=0,rowpos=1,colpos=1,max_pt=1,e="Tooltip requires update"):

		#Loads image and resizes to fit
		t_image_obj = ImageTk.PhotoImage(Image.open(folderpath+t_image).resize((40,40)))
		#Create entry user input for talents
		entry = tk.Entry(root, width=6,bd=0,bg="light coral")
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
		increment_button = tk.Button(root,image=t_image_obj,command=partial(increment_value, entry),bd=0,width=40,bg="#EB5B45")
		increment_button.image = t_image_obj
		increment_button.config(image=t_image_obj)
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

	talent("1.png",1,1,2,3,\
		"Glory Strike+\nGlory Strike's base damage is increased by 4/8/12%.\nFor the next 6 seconds, you gain 2/4/6% haste.")
	talent("2.png",3,1,3,3,\
		"Justice Thump+\nJustice Thump's damage is increased by 5/10/15%.\nWhen enhanced, it is increased by 6/12/18% instead.")
	talent("3.png",2,2,1,3,\
		"Judgement Mastery\nIncrease your Critical Strike chance by 1/2/3%")
	talent("4.png",3,2,2,3,\
		"Echo\nGlory Strike+\nYou have a 33.3/66.6/100% chance to gain 1 level\nof Power of Glory when you consume a Glory Judgement.")
	talent("5.png",3,2,3,3,\
		"Enraged\nJudgement Strike increases the damage and\ncritical strike damage of your next skill by 4/8/12%")
	talent("6.png",0,3,1,3,\
		"Punitive Storm+\nYour Punishing Storm deals 5/10/15% more damage.")
	talent("7.png",3,3,2,3,\
		"Eternal Glory\nAfter you cast Earthquake, you have a 33/66/100%\nto gain a Glory Judgement (prioritizes skills that are not already enhanced.)")
	talent("8.png",1,3,3,1,\
		"Power of Justice\nJustice Thump can now store 2 charges.\nWhen Glory Strike resets the cooldown of\nJustice Thump, it grants a charge instead.")
	talent("9.png",0,4,1,1,\
		"Judgement Sword\nReplace Judgement Strike with Judgement Sword.")
	talent("10.png",1,4,2,3,\
		"Dogma\nEvery 3rd Glory Strike has a 10/20/30%\nincreased Critical Strike Chance.")
	talent("11.png",0,5,1,3,\
		"Razor-Shape\nJudgement Sword has a 10/20/30%\nto regain a charge and increase the damage of the next\nJudgement Sword by 4/8/12%.")
	talent("12.png",3,5,2,3,\
		"Double Knight\nConsecutive Glory Judgements increases your next\nskill's Critical strike chance by 10/20/30%.\nOtherwise, your next skill deals 10/20/30% increased damage.")
	talent("13.png",2,5,3,2,\
		"Frenzy Strike\nYour Judgement Strike's Critical Strike chance is increased by 3/6%.\nWhen Judgement Strike critically hits, your next skill deals 5/10% more damage.")
	talent("14.png",0,6,1,3,\
	 	"Execution\nYou deal 15/30/45% increased critical damage to targets afflicted\nby Judgement Sword's damage-over-time effect.")
	talent("15.png",3,6,3,3,\
	 	"Judgement Strike+\nJudgement Strike deals 4/8/12% more damage.\nIf Judgement Strike critically hits or gains Glory Judgement,\nthe cooldown is reduced by 1/2/3 seconds.")
	talent("16.png",0,7,1,3,\
		"Judgement Sword+\nJudgement Sword deals 10/20/30% more damage immediately,\nand the damage-over-time is increased by 30/60/90%.")
	talent("17.png",3,7,2,3,\
		"Shatterin Slam+\nYour Earthquake deals 5/10/15% more damage,\nand you deal 7/14/21% increased damage to affected targets for 4 seconds.")
	talent("18.png ",0,8,2,2,\
		"Field Rage\nYour party is affected by Trial of Rage with 25/50% effect.")
	talent("19.png ",2,8,3,2,\
		"Trial of Rage+\nTrial of Rage lasts 1.5/3 seconds longer\nand its cooldown is reduced by 15/30 seconds.")
	talent("20.png",0,9,1,3,\
		"Knight's Glory\nWhenever you gain a Glory Judgement from Power of Glory,\nthere is a 3.33/6.66/10% to gain another Glory Judgement.")
	talent("21.png",2,9,3,2,\
		"Expedition\nWhile Trial of Rage is active, you gain 1.25/2.5%\ncritical strike chance and haste\nwhenever you deal damage.")

	#Create total label
	total_label = tk.Label(root, text="Total Points: 0",bd=0,bg="light coral")
	total_label.grid(row=24, column=1, columnspan=16)

	# Create submit button
	submit_button = tk.Button(root,text="Submit",command=submit_values,width=40,bd=0,bg="#EB5B45")
	submit_button.grid(row=26, column=1, columnspan=16)
	# Load default talent points total (32)
	update_total()
	root.mainloop()

	return talent_index

#Runs script when executed directly.
if __name__ == "__main__":
	print(main())
	import pandas as pd
	print("\nExporting data to Excel...",end="\r")
	with pd.ExcelWriter("Talent Points.xlsx", engine='xlsxwriter') as writer:
		data_export_3 = pd.DataFrame(columns=["Talent", "Points"])
		data_export_3["Talent"] = ["Glory Strike+","Justice Thump+","Judgement Mastery","Echo"\
								,"Enraged","Punitive Storm+","Eternal Glory","Power of Justice"\
								,"Judgement Sword","Dogma","Razor-Shape","Double Knight","Frenzy Strike"\
								,"Execution","Judgement Strike+","Judgement Sword+","Shatterin Slam+"\
								,"Field Rage","Trial of Rage","Knight's Glory","Expedition"]
		data_export_3["Points"] = talent_index[1:]
		data_export_3.to_excel(writer, index=False, sheet_name="Talents")