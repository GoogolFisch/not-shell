from color import Fore, Back, Style, Cursor
import reader
import os


def true_split(message,spliting=" ",doBreak=(">",)):
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

class Main:
    __slots__ = ("sysArgs","shortcuts","__dict__","weakref")
    def __init__(self,args,shortcuts):
        self.sysArgs   = args
        self.shortcuts = shortcuts

    def getReal(self,args):
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

        print(Fore.CYAN+cwd+Fore.RED+"$"+Fore.RESET,end="")
        while True:
            key = reader.readkey()
            if key == reader.key.ENTER:
                out = self.getReal(data)
                print("\n"+out)
                if out == "exit":return
                elif out[:3] == "cd ":
                    os.chdir(out[3:])
                    cwd = os.getcwd()
                elif out == "shortcuts":
                    print(self.shortcuts)
                else:
                    os.system(out)
                if out != history[-2] and data != "":
                    history.insert(-1,data)
                history_counter = len(history) - 1
                data = ""
                edit_counter = 0
                print(Fore.CYAN+cwd+Fore.RED+"$"+Fore.RESET,end="",flush=True)

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
            elif len(key) == 1:
                data = data[:edit_counter] + key + data[edit_counter:]
                print(data[edit_counter:],end="\b" * len(data[edit_counter + 1:]),flush=True)
                edit_counter += 1
            else:
                print([hex(ord(l)) for l in key])