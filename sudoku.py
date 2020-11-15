from tkinter import *
import keyboard as kb
from random import shuffle

window = Tk()
window.title("Sudoku! (Hints: Blue = Naive, Red = Look Ahead)")

active_square = None

def deactivate():
	try:
		kb.unhook_all_hotkeys()
	except:
		pass

	try:
		active_square['state'] = 'normal'
		active_square.note_button0.destroy()
		active_square.note_button1.destroy()
		active_square.note_button2.destroy()
		active_square.note_button3.destroy()
		active_square.note_button4.destroy()
		active_square.note_button5.destroy()
		active_square.note_button6.destroy()
		active_square.note_button7.destroy()
		active_square.note_button8.destroy()
	except:
		pass
	
	
def set_value(square, value, color='black'):
	square.config(width=3, height=1, font="14", fg=color, text=value, padx=1, pady=1)
	if value.isdigit():
		square.val = int(value)
		square.possibilities = set()
	elif value == ' ':
		square.val = 0
		square.possibilities = set(range(1,10))
	deactivate()
	
	square.notes = ['  ' for x in range(9)]


class NoteButton(Button):
	def __init__(self, box, square, note, **kwargs):
		super().__init__(box, text=square.notes[note], font=('Arial', '5'), width=1, relief=FLAT, **kwargs)


def create_note(square, note, value):
	if square.notes[note] == value:
		square.notes[note] = '  '
	else:
		square.notes[note] = value

	square.note_button0['text'] = square.notes[0]
	square.note_button1['text'] = square.notes[1]
	square.note_button2['text'] = square.notes[2]
	square.note_button3['text'] = square.notes[3]
	square.note_button4['text'] = square.notes[4]
	square.note_button5['text'] = square.notes[5]
	square.note_button6['text'] = square.notes[6]
	square.note_button7['text'] = square.notes[7]
	square.note_button8['text'] = square.notes[8]

	square.config(font=('Helvetica', '5'), height=5, width=8, justify=LEFT, padx=3, pady=2)

	x = square.notes

	square['text'] = str('     '.join(x[:3]) + '\n \n' + '     '.join(x[3:6]) + '\n \n' + '     '.join(x[6:]))

	
def activate(square, box, r, c):

	deactivate()
	global active_square
	active_square = square
	
	kb.add_hotkey('1', lambda: set_value(square, '1'))
	kb.add_hotkey('2', lambda: set_value(square, '2'))
	kb.add_hotkey('3', lambda: set_value(square, '3'))
	kb.add_hotkey('4', lambda: set_value(square, '4'))
	kb.add_hotkey('5', lambda: set_value(square, '5'))
	kb.add_hotkey('6', lambda: set_value(square, '6'))
	kb.add_hotkey('7', lambda: set_value(square, '7'))
	kb.add_hotkey('8', lambda: set_value(square, '8'))
	kb.add_hotkey('9', lambda: set_value(square, '9'))
	kb.add_hotkey(14, lambda: set_value(square, ' ')) #-- backspace

# ---- Creating note buttons on top of the selected square. ----
	if not str(square['text']).isdigit():
		square.note_button0 = NoteButton(box, square, 0, command=lambda: create_note(square, 0, '1'))
		square.note_button1 = NoteButton(box, square, 1, command=lambda: create_note(square, 1, '2'))
		square.note_button2 = NoteButton(box, square, 2, command=lambda: create_note(square, 2, '3'))
		square.note_button3 = NoteButton(box, square, 3, command=lambda: create_note(square, 3, '4'))
		square.note_button4 = NoteButton(box, square, 4, command=lambda: create_note(square, 4, '5'))
		square.note_button5 = NoteButton(box, square, 5, command=lambda: create_note(square, 5, '6'))
		square.note_button6 = NoteButton(box, square, 6, command=lambda: create_note(square, 6, '7'))
		square.note_button7 = NoteButton(box, square, 7, command=lambda: create_note(square, 7, '8'))
		square.note_button8 = NoteButton(box, square, 8, command=lambda: create_note(square, 8, '9'))

		square.note_button0.grid(row=r, column=c)
		square.note_button1.grid(row=r, column=c+1)
		square.note_button2.grid(row=r, column=c+2)
		square.note_button3.grid(row=r+1, column=c)
		square.note_button4.grid(row=r+1, column=c+1)
		square.note_button5.grid(row=r+1, column=c+2)
		square.note_button6.grid(row=r+2, column=c)
		square.note_button7.grid(row=r+2, column=c+1)
		square.note_button8.grid(row=r+2, column=c+2)

	square['state'] = 'disabled'


class Square(Button):
	def __init__(self, box, r, c):
		super().__init__(box, text=' ', width=3, font="14", command=lambda: activate(self, box, r, c))
		self.grid(row=r, column=c, rowspan=3, columnspan=3)
		
		self.notes = ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']

		self.note_button0 = None
		self.note_button1 = None
		self.note_button2 = None
		self.note_button3 = None
		self.note_button4 = None
		self.note_button5 = None
		self.note_button6 = None
		self.note_button7 = None
		self.note_button8 = None

		self.val = 0
		self.possibilities = set(range(1,10))


class Box(Frame):
	def __init__(self, r, c, **kw):
		super().__init__(window, bd=2, bg='green', **kw)
		self.grid(row=r, column=c)
		self.squares = [Square(self, x // 3 * 3, x % 3 * 3) for x in range(9)]
		

boxes = [Box(x // 3 + 1, x % 3) for x in range(9)]


rows = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
cols = [(0, 3, 6), (1, 4, 7), (2, 5, 8)]


def scan(square, sector='all'):
	# ---- Check box ----
	if sector == 'box' or sector == 'all':
		for other_sq in square.master.squares:
			if not other_sq is square:
				yield other_sq

	box = boxes.index(square.master)

	for x in range(3):
		if box in rows[x]: box_row = rows[x]
		for y in rows[x]:
			if square is square.master.squares[y]:
				square_row = rows[x]
		if box in cols[x]: box_col = cols[x]
		for y in cols[x]:
			if square is square.master.squares[y]:
				square_col = cols[x]

	# ---- Check row ----
	if sector == 'row' or sector == 'all':
		for x in box_row:
			for y in square_row:
				if boxes[x].squares[y] != square:
					yield boxes[x].squares[y]

	# ---- Check col  ----
	if sector == 'col' or sector == 'all':
		for x in box_col:
			for y in square_col:
				if boxes[x].squares[y] != square: 
					yield boxes[x].squares[y]

def reset():
	for box in boxes:
		for square in box.squares:
			if not square.val:
				square.possibilities = set(range(1,10))
	for box in boxes:
		for square in box.squares:
			for x in scan(square):
				if x.val in square.possibilities:
					square.possibilities.remove(x.val)		

def naive(square):
	if len(square.possibilities) == 1:
		return str(square.possibilities.pop())
	
	for x in square.possibilities:		
		if not any(x in y.possibilities for y in scan(square, 'box')):
			return str(x)

	for x in square.possibilities:		
		if not any(x in y.possibilities for y in scan(square, 'row')):
			return str(x)

	for x in square.possibilities:		
		if not any(x in y.possibilities for y in scan(square, 'col')):
			return str(x)

	return False

def get_blanks():
	for box in boxes:
		for square in box.squares:
			if not square.val: yield square
	yield False		

def get_choices():
	reset()
	choices = []
	for square in get_blanks():
		if not square: break
	for square in get_blanks():
		if not square: break
		choices.append(square)
	choices.sort(key=lambda sq: len(sq.possibilities))
	return choices

def solve():
	if not next(get_blanks()):
		return True
	reset()
	for square in get_blanks():
		if not square: break
		value = naive(square)
		if value:
			set_value(square, value, '#00aaff')
			if solve(): return True
			set_value(square, ' ')
			return False
	choices = get_choices()
	if choices:
		choice = choices[0]
		if not choice.possibilities: return False
		for x in [y for y in choice.possibilities]:
			set_value(choice, str(x), '#d52a00')
			if solve(): return True
		set_value(choice, ' ')
		return False

def make_copy():
	copy = set()
	for box in boxes:
		for square in box.squares:
			copy.add((square, square.val))
	return copy

def revert(copy, color=None):
	for x in copy:
		square = x[0]
		if not x[1]:
			value = ' '
			clr = 'black'
		else:
			value = str(x[1])
			clr = color
		set_value(square, value, clr)

def single():
	reset()
	for square in get_blanks():
		if not square: break
		value = naive(square)
		if value:
			return (square, value, '#00aaff')
	copy = make_copy()
	choices = get_choices()
	if choices:
		choice = choices[0]
		if not choice.possibilities: return
		for x in [y for y in choice.possibilities]:
			set_value(choice, str(x))
			if solve(): break
		revert(copy)
		return (choice, str(x), '#d52a00')

def hint():
	hint = single()
	if hint:
		x, y, z = hint
		set_value(x, y, z)

def clear():
	for x in range(9):
		for y in range(9):
			set_value(boxes[x].squares[y], ' ')

def naive_loop():
	for square in get_blanks():
		if not square: break
		value = naive(square)
		if value:
			set_value(square, value)
			reset()
			naive_loop()

def one_solution():
	solutions = 0
	reset()
	copy = make_copy()
	naive_loop()
	if not next(get_blanks()):
		revert(copy)
		reset()
		return True
	
	temp = make_copy()
	choices = get_choices()
	if choices:
		for choice in choices:
			for x in [y for y in choice.possibilities]:
				set_value(choice, str(x))
				if solve():
					solutions += 1
					revert(temp)
				set_value(choice, ' ')
				reset()
				if solutions > 1:
					revert(copy)
					reset()
					return False
	revert(copy)
	reset()
	return bool(solutions)

def remove_squares(mode):
	all_squares = [square for box in boxes for square in box.squares]
	shuffle(all_squares)

	if not mode == 'hard':
		for square in all_squares:
			temp = square.val
			set_value(square, ' ')
			reset()
			if not naive(square): set_value(square, str(temp))
			reset()
			
	if mode == 'medium' or mode == 'hard':
		erasures = 0
		for square in all_squares:
			if mode == 'medium' and erasures > 6: break
			if square.val:
				temp = square.val
				set_value(square, ' ')
				print('removing number - ' + str(erasures))
				erasures += 1
				reset()
				if not one_solution():
					print('replacing number')
					set_value(square, str(temp))
					erasures -= 1

	copy = make_copy()
	revert(copy, '#007e02')

def puzzle(mode='easy'):
	clear()
	order = list(range(1, 10))
	shuffle(order)
	for square, x in zip(boxes[0].squares, order):
		set_value(square, str(x))
	shuffle(order)
	for square, x in zip(boxes[8].squares, order):
		set_value(square, str(x))
	solve()
	remove_squares(mode)


top_pannel = Frame(window, bg='green', padx=2, pady=1)
top_pannel.grid(row=0, column=0, columnspan=3)

hint_button = Button(top_pannel, text='Hint', font='14', bg='#d2f1d2', command=hint, width=8)
hint_button.grid(row=0, column=2, padx=1)

solve_button = Button(top_pannel, text='Solve', font='14', bg='#bdefbd', command=solve, width=8)
solve_button.grid(row=0, column=3, padx=1)

clear_button = Button(top_pannel, text='Clear', font='14', bg='#eafcea', command=clear, width=8)
clear_button.grid(row=0, column=1, padx=1)

new_button = Menubutton(top_pannel, text='New', font='14', bg='#f3fdf3', width=7, pady=8, relief=RAISED)
new_button.grid(row=0, column=0, padx=1)

new_button.menu = Menu(new_button, tearoff=0, font=('Helvetica', '12'), bd=2)
new_button['menu'] = new_button.menu
new_button.menu.add_command(label="Easy", command = puzzle)
new_button.menu.add_command(label="Medium", command = lambda: puzzle('medium'))
new_button.menu.add_command(label="Hard", command = lambda: puzzle('hard'))


window.mainloop()

# By: Calvin Storoschuk