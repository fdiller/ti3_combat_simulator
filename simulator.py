from tkinter import *
import random


def roll_d10(treshold):
    roll = random.randint(1,10)
    print("roll over " + str(treshold) + " : " + str(roll) )
    return (roll >= treshold)

class ArmyFrame(Frame):
    def __init__(self, parent, ship_basic_treshold, title, grid_column_pos):
        Frame.__init__(self, parent)
        self.parent = parent
        self.title = title
        self.grid_column_pos = grid_column_pos
        self.ship_basic_treshold = ship_basic_treshold.copy()
        self.ship_treshold = ship_basic_treshold.copy()
        self.ship_labels = {}
        self.treshold_labels = {}
#        self.quantity_labels = {}
        self.quantity_entries = {}
        self.quantity_stringvar = {}
        
#        self.ship_quantity = {}
#        for ship, treshold in self.ship_treshold.items():
#            self.ship_quantity[ship] = 0
            
        self.initUI()
    
    def change_treshold(self, ship, value):
        previous_value = self.ship_treshold[ship]
        self.ship_treshold[ship]+=value
        if(self.ship_treshold[ship] > 10 or self.ship_treshold[ship] < 1):
            self.ship_treshold[ship] = previous_value
        self.treshold_labels[ship].configure( text=str(self.ship_treshold[ship]) )
        
    def change_all_treshold(self, value):
        for ship, treshold in self.ship_treshold.items():
            self.change_treshold(ship, value)
            
    def reset_all_treshold(self):
        print("reset")
        self.ship_treshold.clear()
        self.ship_treshold = self.ship_basic_treshold.copy()
        for ship, treshold_label in self.treshold_labels.items():
            print(ship + str(self.ship_treshold[ship]))
            treshold_label.configure( text=str(self.ship_treshold[ship]) )
        
    def change_quantity(self, ship, value):
        # if the entry is empty, consider it is 0
        if len(self.quantity_stringvar[ship].get()) == 0:
            self.quantity_stringvar[ship].set("0")
        
        # read the content of the entry, update it, do not let it drop under 0
        previous_value = int(self.quantity_stringvar[ship].get())
        new_value = previous_value + value
        if(new_value < 0):
            new_value = previous_value
        self.quantity_stringvar[ship].set( str(new_value) )
   
        
    def initUI(self):
        self.grid(column=self.grid_column_pos, row=0)
        self.columnconfigure(1, minsize=25)
        self.columnconfigure(4, minsize=40)
        
        i = 0
        # title label
        title_label = Label(self, text = self.title)
        title_label.grid(column=0, columnspan=2, row=i)
        i += 1
        
        # global army minus button
        global_minus_button = Button(self, text="-", width=2, command=lambda : self.change_all_treshold(-1))
        global_minus_button.grid(column=2, row=i)
        # global army plus button
        global_plus_button = Button(self, text="+", width=2,  command=lambda : self.change_all_treshold(+1))
        global_plus_button.grid(column=3, row=i)
        i += 1
        
        # reset treshold
        global_reset_button = Button(self, text="RESET", width=5,  command=self.reset_all_treshold)
        global_reset_button.grid(column=2, columnspan=2, row=i)
        i += 1
        
        vcmd = (self.register(self.OnValidate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        for ship, treshold in self.ship_treshold.items():
            #ship name
            new_ship_label = Label(self, text=ship)
            self.ship_labels[ship] = new_ship_label
            new_ship_label.grid(column=0, row=i)
            #treshold hit
            new_trshold_label = Label(self, text=str(treshold))
            self.treshold_labels[ship] = new_trshold_label
            new_trshold_label.grid(column=1, row=i)
            #minus button
            new_minus_button = Button(self, text="-", width=2, command=lambda ship=ship: self.change_treshold(ship, -1))
            new_minus_button.grid(column=2, row=i)
            # plus button
            new_plus_button = Button(self, text="+", width=2,  command=lambda ship=ship: self.change_treshold(ship, +1))
            new_plus_button.grid(column=3, row=i)
            #quantity label
            #new_quantity_label = Label(self, text="0")
            #self.quantity_labels[ship] = new_quantity_label
            #new_quantity_label.grid(column=4, row=i)
            
            #minus button 2
            new_minus_button2 = Button(self, text="-", width=3, command=lambda ship=ship: self.change_quantity(ship, -1))
            new_minus_button2.grid(column=5, row=i)
            # plus button 2
            new_plus_button2 = Button(self, text="+", width=3, command=lambda ship=ship: self.change_quantity(ship, +1))
            new_plus_button2.grid(column=6, row=i)
            
            # quantity entry
            text = StringVar()
            text.set("0")
            new_quantity_entry = Entry(self, width=4, textvariable=text, validate="key", validatecommand=vcmd)
            self.quantity_entries[ship] = new_quantity_entry  
            self.quantity_stringvar[ship] = text
            new_quantity_entry.grid(column=4, row=i)
            
            i+=1
           
        
    # valid percent substitutions (from the Tk entry man page)
    # %d = Type of action (1=insert, 0=delete, -1 for others)
    # %i = index of char string to be inserted/deleted, or -1
    # %P = value of the entry if the edit is allowed
    # %s = value of entry prior to editing
    # %S = the text string being inserted or deleted, if any
    # %v = the type of validation that is currently set
    # %V = the type of validation that triggered the callback
    #      (key, focusin, focusout, horsed)
    # %W = the tk name of the widget        
    def OnValidate(self, d, i, P, s, S, v, V, W):
        """ validates input text. Ok if empty or a number, else KO """
        if len(P) == 0:
            return True
        try:
            int(P)
        except:
            return False
        else:
            return True
            
            
class ResultPanel(Frame):
    def __init__(self, parent, atk_frame, def_frame, grid_column_pos):
        Frame.__init__(self, parent)
        self.atk_frame = atk_frame
        self.def_frame = def_frame
        self.parent = parent
        self.grid_column_pos = grid_column_pos
        self.initUI()
        
    def initUI(self):
        self.grid(column = self.grid_column_pos, row = 1, columnspan = 2)
        #Roll button 
        new_roll_button = Button(self, text="ROLL !", width=10, command= self.roll_dice)
        new_roll_button.pack(side=TOP)
        
        #text
        self.text_box = Text(self, state=DISABLED) #cannot write in the box
        self.text_box.insert("1.0", "didi")
        self.text_box.pack(side=TOP)
        
    def roll_dice(self):
        attacker_hits = {}
        defender_hits = {}
        for ship, quantity in self.atk_frame.quantity_stringvar.items():
            attacker_hits[ship] = 0
            defender_hits[ship] = 0
        #roll dice for attacker
        for ship, quantity in self.atk_frame.quantity_stringvar.items():      
            for i in range(0, int(quantity.get())):
                if roll_d10( self.atk_frame.ship_treshold[ship] ):
                    attacker_hits[ship] += 1
        #roll dice for defender
        for ship, quantity in self.def_frame.quantity_stringvar.items():      
            for i in range(0, int(quantity.get())):
                if roll_d10( self.def_frame.ship_treshold[ship] ):
                    defender_hits[ship] += 1
                    
        self.text_box.config(state=NORMAL)
        self.text_box.delete("1.0", END)
        to_print = "Attacker hits : \n"
        attacker_total_hits, defender_total_hits = 0, 0
        for ship, quantity_string in self.atk_frame.quantity_stringvar.items():
            quantity = int(quantity_string.get()) 
            if quantity > 0:
                to_print += str(quantity) + " " + ship + " inflicted " + str(attacker_hits[ship]) + " hits \n"
                attacker_total_hits += attacker_hits[ship]
        to_print += "TOTAL : " + str(attacker_total_hits) + " hits.\n"
                
        to_print += "\nDefender hits : \n"
        for ship, quantity_string in self.def_frame.quantity_stringvar.items():
            quantity = int(quantity_string.get()) 
            if quantity > 0:
                to_print += str(quantity) + " " + ship + " inflicted " + str(defender_hits[ship]) + " hits \n"
                defender_total_hits += defender_hits[ship]
        to_print += "TOTAL : " + str(defender_total_hits) + " hits.\n"
                
        self.text_box.insert(INSERT, to_print)
        self.text_box.config(state=DISABLED)
                    
        print(attacker_hits)
        print(defender_hits)
            
    def roll_volley(self, hits_dict):    
        for ship, quantity in self.atk_frame.quantity_stringvar.items():      
            for i in range(0, int(quantity.get())):
                if roll_d10( self.atk_frame.ship_treshold[ship] ):
                    hits_dict[ship] += 1
    
    
  
        
ship_basic_treshold = {"Dreadnought":5, "Carrier":9, "Cruiser":7, "Destroyer":9, "Fighter":9, "War Sun":3}
ship_basic_dice_number = {'Dreadnought':1, 'Carrier':1, 'Cruiser':1, 'Destroyer':1, 'Fighter':1, 'War Sun':3}
        
root = Tk()
frame = Frame(root)
frame.pack()

atk_army_frame = ArmyFrame(frame, ship_basic_treshold, "ATTACKER ARMY", 0)
def_army_frame = ArmyFrame(frame, ship_basic_treshold, "DEFENDER ARMY", 1 )

result_panel = ResultPanel(frame, atk_army_frame, def_army_frame, 0)

root.mainloop()