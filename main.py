import tkinter as tk 
from tkinter import messagebox
from tkinter.messagebox import askyesno
import shelve
from datetime import date, datetime
from tkcalendar import Calendar, DateEntry

class MainFrame(tk.Tk):
	def __init__(self,window_type):
		super().__init__()
		self.implement_skeleton(window_type)

	# works like init for main frame or root
	def design_mainframe(self):
		self.cool_color = '#26292C'
		little_white = '#D9D6D3'
		self.general_font = ('Courier', 16)
		self.title('DPlanner')
		self.configure(background = '#000000')
		self.geometry('1000x600')
		self.resizable(height = 0, width = 0)
		self.protocol("WM_DELETE_WINDOW", self.close_root)

		tk.Label(self, text = 'Deadline Planner', font = ('Courier', 25, 'bold'), bg = '#000000',
			fg = '#dfdfff').place(x = 30, y = 20)

		tk.Label(self, text = 'Scroll up or down to view more entry', font = ('Courier', 16), bg = '#000000',
			fg = '#dfdfff').place(x = 250, y = 520)
		tk.Label(self, text = 'Copyright '+chr(169)+' 2022, Soumitra Dx', font = ('Courier', 11), bg = '#000000',
			fg = '#dfdfff').place(x = 350, y = 550)

		self.add_new_button = tk.Button(self, text = 'Add New', height = 1, width = 8, font = self.general_font,
								 bg = self.cool_color, fg = little_white, command = lambda : self.add_new_button_command(),
								 activebackground = self.cool_color)
		self.add_new_button.place(x = 800, y = 25) #520


		self.deadline_container_frame = tk.Frame(self, height = 400, width = 1000, bg = self.cool_color)
		self.deadline_container_frame.place(x = 0, y = 100)
		self.add_deadline_window_active = False
		self.deatils_window_active = False

		self.deadline_container_frame.bind_all('<MouseWheel>', self.mousewheel_handler)

		self.card_modified = True
		self.show_deadline_cards()

	#handler for root closing
	def close_root(self):
		self.card_db.close()
		self.destroy()

	#handler to handle mose wheel
	def mousewheel_handler(self, event):
		if event.delta == -120:
			if self.current_show_end<len(self.card_db)-1:
				self.current_show_start+= 1
				self.current_show_end+= 1
				self.card_modified = True
		elif event.delta == 120:
			if self.current_show_start>0:
				self.current_show_start-= 1
				self.current_show_end-= 1
				self.card_modified = True
		if self.card_modified:
			self.show_card()
			self.card_modified = False

	# works like init for sub window to take deadlines
	def design_add_deadline(self):
		self.temp_label_title = tk.Label(self.add_deadline, text = 'Title ')
		self.temp_label_title.place(x = 40, y = 100)
		self.temp_titile = tk.Text(self.add_deadline, width = 60, height = 1)
		self.temp_titile.place(x = 150, y = 100)

		self.temp_label_details = tk.Label(self.add_deadline, text = 'Details ')
		self.temp_label_details.place(x = 40, y = 150)
		self.temp_details = tk.Text(self.add_deadline, width = 60, height = 3)
		self.temp_details.place(x = 150, y = 150)

		self.temp_label_date = tk.Label(self.add_deadline, text = 'Date')
		self.temp_label_date.place(x = 40, y = 235)
		self.temp_date = DateEntry(self.add_deadline, width= 16, background= "magenta3", foreground= "white",bd=2)
		self.temp_date.place(x = 150, y = 235)

		self.temp_label_time = tk.Label(self.add_deadline, text = 'Time(24h format)')
		self.temp_label_time.place(x = 40, y = 285)

		self.temp_hour = tk.Entry(self.add_deadline,width = 8, justify= 'center')
		self.temp_hour.place(x = 150, y = 285)
		self.temp_hour.insert(0,'23')
		self.temp_label_hour = tk.Label(self.add_deadline, text = 'hour')
		self.temp_label_hour.place(x = 210, y = 285)

		self.temp_minute = tk.Entry(self.add_deadline,width = 8, justify= 'center')
		self.temp_minute.place(x = 250, y = 285)
		self.temp_minute.insert(0,'59')
		self.temp_label_minute = tk.Label(self.add_deadline, text = 'minute')
		self.temp_label_minute.place(x = 310, y = 285)

		self.temp_button = tk.Button(self.add_deadline, text = 'Add', command = self.add_deadline_add_button,
									height = 2, width = 8)
		self.temp_button.place(x = 330, y = 380)

	# command for 'add new' button
	def add_new_button_command(self):
		self.implement_skeleton(1)

	# command for the add button in the temporary deadline adding window
	def add_deadline_add_button(self):
		temp_hour = self.temp_hour.get()
		temp_minute = self.temp_minute.get()
		if not temp_hour.isdigit():
			temp_hour = '24'
		if not temp_minute.isdigit():
			temp_minute = '60'
		if 0<=int(temp_hour)<=23 and 0<=int(temp_minute)<=59:
			temp_data = [self.temp_titile.get('1.0',tk.END)[:-1].strip(),
				self.temp_details.get('1.0',tk.END)[:-1].strip(),
				self.temp_date.get().strip(),
				self.temp_hour.get().strip()+':'+self.temp_minute.get().strip()]
			if temp_data not in self.card_db.values():
				self.card_db[str(self.total_deadline_number)] = temp_data
				self.total_deadline_number+= 1
				if self.current_show_end -self.current_show_start <5:
					self.current_show_end+=1
				# sorting card_db
				sorted_idx= sorted(dict(self.card_db), key = lambda x: self.calculate_time_left(int(x))) ################
				temp_db = []
				for i in sorted_idx:
					temp_db.append(self.card_db[i])
				for i in range(len(temp_db)):
					self.card_db[str(i)]= temp_db[i]
				self.show_card()
				self.add_deadline.destroy() 
				self.add_deadline_window_active = False
			else:
				messagebox.showinfo('Information', 'Entry already exists',parent = self.add_deadline)
		else:
			messagebox.showwarning('Warning', 'Enter valid time', parent = self.add_deadline)

	# event hadler for closing the add deadline window
	def add_deadline_close_button(self):
		self.add_deadline.destroy()
		self.add_deadline_window_active = False

	# initiates and shows already existing cards
	def show_deadline_cards(self):
		self.deadline_container = {}
		self.open_shelf()
		self.show_card()
		self.card_modified = False

	# method to make a card enter diffrent card number to add successfully
	def card(self,card_number):
		dim_color = '#46504C'
		self.deadline_container[card_number] = tk.Frame(self.deadline_container_frame, height = 50, width = 780, bg = dim_color)
		self.deadline_container[card_number].place(x = 110, y = 14*card_number+50*(card_number-1))

		tk.Button(self.deadline_container[card_number],text = 'Details', font = ('Courier',12), 
			activebackground= '#76798C', width = 8, height = 1, bg = '#76798C',
			command = lambda : self.details_handler(self.current_show_start+card_number)).place(x = 660, y = 12)

		card_title = self.card_db[str(self.current_show_start+card_number-1)][0]
		if len(card_title)>20:
			card_title = card_title[:17]+'...'
		elif len(card_title) == 0:
			card_title = 'NO TITLE'
		card_date  = self.card_db[str(self.current_show_start+card_number-1)][2]
		card_time  = self.card_db[str(self.current_show_start+card_number-1)][3]

		tk.Label(self.deadline_container[card_number], bg = dim_color, fg = '#ffffff', font = ('Courier', 16),
			text = str(self.current_show_start+card_number)+'.').place(x = 20, y = 10)

		tk.Label(self.deadline_container[card_number], bg = dim_color, fg = '#ffffff', font = ('Courier', 16),
			text = card_title).place(x = 70, y = 10)

		tk.Label(self.deadline_container[card_number], bg = dim_color, fg = '#ffffff', font = ('Courier', 16),
			text = card_date).place(x = 400, y = 10)

		tk.Label(self.deadline_container[card_number], bg = dim_color, fg = '#ffffff', font = ('Courier', 16),
			text = card_time).place(x = 550, y = 10)

		# tk.Label(self.deadline_container[card_number])

	# handler for details button
	def details_handler(self,deadline_pos):
		self.implement_skeleton([2,deadline_pos])

	# method to open the storage shelf
	def open_shelf(self):
		self.card_db = shelve.open('db')
		self.current_show_start = 0
		if len(self.card_db)<6:
			self.current_show_end = len(self.card_db)-1
		else:
			self.current_show_end = 5
		self.total_deadline_number = len(self.card_db)
	
	# shows at most 6 cards top to bottom
	def show_card(self):
		for i in self.deadline_container:
			self.deadline_container[i].destroy()
		if len(self.card_db)>0:
			for i in range(self.current_show_end - self.current_show_start+1):
				self.card(i+1)

	#designs see details window
	def design_see_details(self, card_db_entry_no):
		title   = self.card_db[str(card_db_entry_no)][0]
		details = self.card_db[str(card_db_entry_no)][1]
		date    = self.card_db[str(card_db_entry_no)][2]
		time    = self.card_db[str(card_db_entry_no)][3]
		t_left  = self.calculate_time_left(card_db_entry_no)
		t_lft_s = str(t_left//1440)+' days, '+str((t_left%1440)//60)+' hour, '+str(t_left%60)+' minutes'
		if title == '':
			title = 'NO TITLE'
		elif len(title)>60:
			title = title[:57]+'...'
		if details == '':
			details = 'NO DETAILS AVAILABLE'
		tk.Label(self.see_details,text = 'Title   : '+title, font = ('Courier',11)).place(x = 30, y =30)
		tk.Label(self.see_details,text = 'Details : '+details[:50], font = ('Courier',11)).place(x = 30, y =60)
		details_rest = len(details)-50
		details_line = 1
		while(details_rest>0):
			details = details[50:]
			tk.Label(self.see_details,text = details[:50], 
			font = ('Courier',11)).place(x = 100, y =60+25*details_line)
			details_rest-=50
			details_line+= 1

		tk.Label(self.see_details,text = 'Date    : '+date, font = ('Courier',11)).place(x = 30, y =60+25*details_line+5)
		tk.Label(self.see_details,text = 'Time    : '+time, font = ('Courier',11)).place(x = 30, y =60+25*details_line+35)
		tk.Label(self.see_details,text = 'TIme Left :'+ t_lft_s, font = ('Courier',11)).place(x = 30, y = 230)

	# details close button
	def see_details_close_button(self):
		self.see_details.destroy()
		self.deatils_window_active = False

	#delete entry event handler
	def delete_entry(self, card_db_entry_no):
		confirmation = askyesno(title = 'Confirmation', 
			message = 'Are you sure you want to delete this entry?', parent = self.see_details)
		if confirmation:
			while(card_db_entry_no<len(self.card_db)-1):
				self.card_db[str(card_db_entry_no)] = self.card_db[str(card_db_entry_no+1)]
				card_db_entry_no+= 1
			del self.card_db[str(len(self.card_db)-1)]
			self.total_deadline_number-= 1
			if len(self.card_db)<6:
				self.current_show_end = len(self.card_db)-1
			self.show_card()
			self.deatils_window_active = False
			self.see_details.destroy()

	# returns time left in minute
	def calculate_time_left(self,card_db_entry_no):
		deadline_time = MainFrame.calculete_minute_from_0(self.card_db[str(card_db_entry_no)][2],
			self.card_db[str(card_db_entry_no)][3])
		current_time = MainFrame.calculete_minute_from_0(date.today().strftime('%m/%d/%Y'), 
			datetime.now().strftime('%H:%M'))
		return deadline_time - current_time

	#calculates time from 0/0/2000, 0:0
	@staticmethod
	def calculete_minute_from_0(date, time):
		m = [0,31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
		month, day, year = list(map(int, date.split('/')))
		year = year%100
		hour, minute = list(map(int, time.split(':')))
		ans = (year-1)*365+(year-1)//4+m[month-1]+day-1
		if month>2 and year%4 == 0:
			ans +=1
		ans = ans*24 + hour 
		ans = ans*60 + minute
		return ans

	# implements all main stuff
	def implement_skeleton(self,window_type):
		if window_type == 0:
			# for main frame
			self.design_mainframe()
		elif window_type == 1:
			# for sub window to take deadline
			if not self.add_deadline_window_active:
				self.add_deadline = tk.Toplevel(self)
				self.add_deadline.geometry('720x480+'+str(self.winfo_x()+100)+'+'+str(self.winfo_y()+40))
				self.add_deadline.grab_set()
				self.add_deadline.resizable(height = 0, width = 0)
				self.add_deadline.title('Add a deadline')
				self.add_deadline_window_active = True
				self.add_deadline.protocol("WM_DELETE_WINDOW", self.add_deadline_close_button)
				self.design_add_deadline()
				self.add_deadline.mainloop()
			else:
				pass
		elif window_type[0] == 2:
			# for sub window to show  details
			if not self.deatils_window_active:
				self.see_details = tk.Toplevel(self)
				self.see_details.geometry('640x320+'+str(self.winfo_x()+200)+'+'+str(self.winfo_y()+80))
				self.see_details.grab_set()
				self.see_details.resizable(height = 0, width = 0)
				self.see_details.title('Details')
				self.deatils_window_active = True
				self.see_details.protocol("WM_DELETE_WINDOW", self.see_details_close_button)
				self.see_details_delete_entry = tk.Button(self.see_details, text = 'Delete Entry', height = 1,
					width = 8, command = lambda : self.delete_entry(window_type[1]-1)).place(x = 290, y = 270)
				self.design_see_details(window_type[1]-1)
				self.see_details.mainloop()


if __name__ == '__main__':
	root = MainFrame(0)
	root.mainloop()