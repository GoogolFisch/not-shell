from color import Fore, Back, Style, Cursor
import reader
import os


def true_split(message,spliting=" ",doBreak=(">",)) -> list:
	m = [""]
	b = False
	for x in message:
		if x in doBreak and not b:
			b = True
		elif x in spliting and not b:
			m.append("")
		else:
			b = False
			m[-1] += x
	return m

def in_part_off(search,off_list:list) -> list:
	l = list()
	for x in off_list:
		if search == x[:len(search)]:l.append(x)
	return l

def missing(to,complete) -> list:
	return complete[len(to):]

def replace_part_of_list(container:list,replace:dict):
	out = []
	for x in container:
		if x in replace.keys:
			out.append(replace[x])
		else:
			out.append(x)


class Main:
	__slots__ = ("sysArgs","shortcuts","__dict__","weakref")
	def __init__(self,args,shortcuts):
		self.sysArgs   = args
		self.shortcuts = shortcuts

	def getReal(self,args) -> str:
		finishingData = list()
		for metaPart in true_split(args," "):
			finishingData.append(list())
			for part in true_split(metaPart,"%",tuple()):
				# print(part)
				if part in list(self.shortcuts.keys()):
					a = self.getReal(self.shortcuts[part])
				else:
					a = part
				finishingData[-1].append(a)
			finishingData[-1] = "\\".join(finishingData[-1])
		return " ".join(finishingData)

	def run(self):
		data = ""
		cwd  = os.getcwd()

		history = ["",""]
		history_counter = 0
		edit_counter = 0
		completeG = ""

		print(Fore.CYAN + cwd + Fore.RED + "$" + Fore.RESET,end="",flush=True)
		while True:
			key = reader.readkey()
			if key is None:continue
			elif key == reader.key.ENTER:
				out = self.getReal(data)
				print("\n"+out)
				if out == "exit":return
				elif out[:3] == "cd ":
					try:
						os.chdir(out[3:])
						cwd = os.getcwd()
					except:
						print("not possible >" + out[3:] + "<",flush=True)
				elif out == "sc-1":print(self.shortcuts,flush=True)
				else:
					try:
						os.system(
							out.replace("ls-1","dir").replace("copy-1","copy").replace("mv-1","move")
						)
					except Exception as e:
						print(Fore.RED + str(e) + Fore.RESET,flush=True)
					except KeyboardInterrupt as e:
						print(Fore.RED + str(e) + Fore.RESET,flush=True)
				if out != history[-2] and data != "":
					history.append(data)
				history_counter = len(history) - 1
				data = ""
				edit_counter = 0
				print(Fore.CYAN+cwd+Fore.RED+"$"+Fore.RESET,end="",flush=True,flush=True)

			elif key == reader.key.UP:
				if history_counter > 0:
					history_counter -= 1
					data = history[history_counter]
					edit_counter = len(data)
					print(data,end="",flush=True)
			elif key == reader.key.DOWN:
				if history_counter < len(history) - 1:
					history_counter += 1
					data = history[history_counter]
					edit_counter = len(data)
					print(data,end="",flush=True)

			elif key == reader.key.LEFT:
				if edit_counter > 0:
					print("\b",end="",flush=True)
					edit_counter -= 1
			elif key == reader.key.RIGHT:
				if edit_counter < len(data):
					print(data[edit_counter],end="",flush=True)
					edit_counter += 1

			elif len(key) == 1 and (key == reader.key.BACKSPACE2):
				if 0 < edit_counter <= len(data):
					data = data[:edit_counter - 1] + data[edit_counter:]
					edit_counter -= 1
					print("\b" + data[edit_counter:],end="  \b\b" + "\b" * (len(data) - edit_counter))
					print("",end="",flush=True)

			elif len(key) == 1 and (key == "\t"):
				a = true_split(data," ")
				if a != []:
					b = in_part_off(a[-1],self.shortcuts)
					if len(b):
						c = b[0][len(a[-1]):]
						if completeG == c:
							edit_counter += len(completeG)
							data += c
							print(end=c,flush=True)
						else:
							completeG = c
							print(end=Fore.LIGHTBLACK_EX+c+"\b"*len(c)+Fore.RESET,flush=True)

			elif len(key) == 1:
				data = data[:edit_counter] + key + data[edit_counter:]
				print(data[edit_counter:],end="\b" * len(data[edit_counter + 1:]),flush=True)
				edit_counter += 1
			else:
				print([hex(ord(l)) for l in key],flush=True)
