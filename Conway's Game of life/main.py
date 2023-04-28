import tkinter
import gol
import attributes

def start_simulation(patternid):
    attributes.grid_size = int(gridSize.get())
    attributes.simulation_speed = int(simulation_speed.get())
    attributes.paused = bool(paused_variable.get())
    gol.run_simulation(patternid)

def set_rule(*args):
    attributes.rule_set = rules.get()
    print(attributes.rule_set)

root = tkinter.Tk()
#root.geometry("500x500")

gridSize = tkinter.StringVar()
simulation_speed = tkinter.StringVar()

gridSize.set("100")
simulation_speed.set("0")

# Grid size configuration
tkinter.Label(root, text="Grid size: ").grid(row=0, column=0, padx=5, pady=5)
tkinter.Entry(root, textvariable=gridSize, width=10).grid(row=0, column=1, padx=5, pady=5)
# Simulation speed configuration
tkinter.Label(root, text="Simulation speed: ").grid(row=0, column=2, padx=5, pady=5)
tkinter.Entry(root, textvariable=simulation_speed, width=10).grid(row=0, column=3, padx=5, pady=5)

# Pattern creation buttons

# Simple pattern
tkinter.Button(root, text="Simple", width=10 ,command=lambda:start_simulation("simple")).grid(row=1, column=0, sticky="W", padx=5, pady=5)
# R-Pentomino
tkinter.Button(root, text="R-pentomino", width=10, command=lambda:start_simulation("rpentomino")).grid(row=1, column=1, sticky="W", padx=5, pady=5)
# F-Pentomino
tkinter.Button(root, text="F-pentomino", width=10, command=lambda:start_simulation("fpentomino")).grid(row=2, column=0, sticky="W", padx=5, pady=5)
# Glider
tkinter.Button(root, text="Glider", width=10, command=lambda:start_simulation("glider")).grid(row=2, column=1, sticky="W", padx=5, pady=5)
# Glider
tkinter.Button(root, text="Gosper GG", width=10, command=lambda:start_simulation("gospergg")).grid(row=1, column=2, sticky="W", padx=5, pady=5)
# minimal infinite growth
tkinter.Button(root, text="Min Inf", width=10, command=lambda:start_simulation("mininf")).grid(row=2, column=2, sticky="W", padx=5, pady=5)
# Still lifes
tkinter.Button(root, text="Still Life", width=10, command=lambda:start_simulation("stillife")).grid(row=3, column=0, sticky="W", padx=5, pady=5)
# Test lifes
tkinter.Button(root, text="Test", width=10, command=lambda:start_simulation("test")).grid(row=3, column=1, sticky="W", padx=5, pady=5)

# Paused checkbox
paused_variable = tkinter.BooleanVar()
tkinter.Checkbutton(root, 
    text="Paused", 
    width=10,
    variable=paused_variable,
    onvalue=False,
    offvalue=True
).grid(row=3, column=2, sticky="W", padx=5, pady=5)

# Rules
radio_button_frame = tkinter.Frame(root, highlightbackground="black", highlightthickness=1)
radio_button_frame.grid(row=1, column=3, rowspan=3)
# These are the round buttons on the side used to update the "update" rules 
rules = tkinter.StringVar()
classic_rb = tkinter.Radiobutton(radio_button_frame, text="Classic Rules", variable=rules, value="classic", command=set_rule)
new_rule_rb = tkinter.Radiobutton(radio_button_frame, text="Pattern Rule", variable=rules, value="new_rule", command=set_rule)
brain_rule_rb = tkinter.Radiobutton(radio_button_frame, text="Brain Rule", variable=rules, value="brain", command=set_rule)
spark_rule_rb = tkinter.Radiobutton(radio_button_frame, text="Spark Rule", variable=rules, value="spark", command=set_rule)
block_rule_rb = tkinter.Radiobutton(radio_button_frame, text="Block Rule", variable=rules, value="block", command=set_rule)
# This is just where all the round buttons are layed out
classic_rb.grid(row=0, column=0, sticky="W")
new_rule_rb.grid(row=1, column=0, sticky="W")
brain_rule_rb.grid(row=2, column=0, sticky="W")
spark_rule_rb.grid(row=3, column=0, sticky="W")
block_rule_rb.grid(row=4, column=0, sticky="W")
# Function which is necessary to run the GUI
root.mainloop()