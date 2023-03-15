import sys
import readline

from utils.utils import *
from utils.logger import *

# https://github.com/pocmo/Python-Brainfuck/blob/master/getch.py
from utils.getch import getch

class debugger:
	def __init__(self,code):
		self.code = code
		self.statut = 'stopped'
		self.bp = []
		self.init()

	def init(self):
		self.printed = ''
		self.position = 0
		self.bloc_info = False
		self.len = len(self.code)
		self.cells = [0]
		self.cellptr = 0
		self.jmp_loop(self.code)		

	def jmp_loop(self,code):
		self.jmp = {}
		tmp = []
		for a, cmd in enumerate(code):
			if cmd == "[":
				tmp.append(a)
			if cmd == "]":
				b = tmp.pop()
				self.jmp[b] = a
				self.jmp[a] = b

	def help(self):
		print('\tAvailable Commande : ')
		print('\t- i/infos         %s'%('=> Show all general informations'))
		print('\t- c/code          %s'%('=> Show the current executed code'))
		print('\t- r/run           %s'%('=> Run the programm'))
		print('\t- c/continue      %s'%('=> Resume a paused execution'))
		print('\t- ni/n/next       %s'%('=> Execute the next instruction'))
		print('\t- bp/breakpoint   %s'%('=> Show all breakpoint'))
		print('\t- bp/breakpoint * %s'%('=> Set a breakpoint to *th position'))
		print('\t- p/printed       %s'%('=> Show all printed characters'))
		print('\t- q/quit          %s'%('=> Exit the debugger'))

	def show_code(self):
		print('\n\033[4m%s\033[92m%s\033[0m\033[1m%s\033[0m\n'%(
			self.code[:self.position],
			self.code[self.position],
			self.code[self.position+1:])
		)

	def format_cells(self):
		cells = self.cells
		result = [str(x)+'(\033[94m%s\033[0m)'%(str(bytes([x]))[2:-1]) for x in cells]
		return '[%s]'%(' , '.join(result))

	def infos(self):
		print()
		logger('[%s-Summary-%s]'%('-'*25,'-'*25),'info',0,0)
		print(' '*9 +'+'+ '\tStatut = %s'%self.statut)
		print(' '*9 +'+'+ '\tPosition Pointer: %s/%s'%(self.position,self.len))
		print(' '*9 +'+'+ '\tCells = %s'%self.format_cells())
		print(' '*9 +'+'+ '\tCell pointer = %s'%self.cellptr)
		print(' '*9 +'+'+ '\tBreakpoints = %s'%self.bp)
		print(' '*9 +'+'+ '\tPrinted = "%s"'%self.printed.strip())
		logger('[%s---------%s]'%('-'*25,'-'*25),'info',0,0,False,False)

	def menu(self):
		if not self.bloc_info:
			self.infos()

		cmd = input("> ").strip()

		if cmd in ['h','help']:
			self.help()
			self.bloc_info = False

		elif cmd in ['q','quit']:
			exit(1)

		elif cmd in ['r','run']:
			self.init()
			self.statut = 'running'
			self.run()
			self.bloc_info = False

		elif cmd in ['i','infos']:
			self.infos()
			self.bloc_info = True

		elif cmd in ['c','code']:
			self.show_code()
			self.bloc_info = True

		elif cmd in ['p','printed']:
			print(' '*10 + '\tPrinted char = \'%s\''%self.printed.strip())
			self.bloc_info = False

		elif cmd in ['c','continue']:
			if self.position == 0:
				logger('You have to run the progamm first','error',0,0)
				self.bloc_info = False
			else:
				self.run_cmd()
				self.run()
				self.bloc_info = False

		elif cmd in ['ni','n','next']:
			self.run_cmd()
			self.bloc_info = False

		elif 'bp' in cmd or 'breakpoint' in cmd:
			try:
				pos = int(cmd.split(' ')[1])
				self.bp.append(pos)
				logger('Breakpoint set at %sth position'%pos,'flag',0,0,False,False)
			except:
				print(' '*10 + '\tBreakpoints = %s'%self.bp)
			self.bloc_info = True

		else:
			logger('Invalid Command ..','error',0,0)
			self.bloc_info = False

	def run(self):
		while self.position != len(self.code):
			if self.position in self.bp:
				return
			self.run_cmd()

	def run_cmd(self):
		cmd = self.code[self.position]

		if cmd == ">":
			self.cellptr += 1
			if self.cellptr == len(self.cells):
				self.cells.append(0)

		if cmd == "<":
			self.cellptr = 0 if self.cellptr <= 0 else self.cellptr - 1

		if cmd == "+":
			self.cells[self.cellptr] = self.cells[self.cellptr] + 1 & 255

		if cmd == "-":
			self.cells[self.cellptr] = self.cells[self.cellptr] - 1 if self.cells[self.cellptr] > 0 else 255

		if cmd == "[" and self.cells[self.cellptr] == 0:
			self.position = self.jmp[self.position]

		if cmd == "]" and self.cells[self.cellptr] != 0:
			self.position = self.jmp[self.position]

		if cmd == ".":
			letter = chr(self.cells[self.cellptr])
			sys.stdout.write(letter)
			self.printed += letter

		if cmd == ",":
			self.cells[self.cellptr] = ord(getch.getch())
		  
		self.position += 1

def main():
	args = parse_args()
	if not check_file(args.file):
		logger('File not found ...','error',0,0)

	code = open(args.file,'r').read()
	if not check_content(code):
		logger('Invalid file content ...','error',0,0)

	proc = debugger(code)
	while 1:
		proc.menu()
		if proc.position == len(proc.code):
			proc.statut = 'finished'
			proc.infos()
			return 1

if __name__ == '__main__': 
	main()