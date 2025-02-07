# THIS CODE IS COMMENTED AND PRODUCES CONSOLE OUTPUT IN CZECH

import os
import shutil

class Folder:
    def __init__(self, str):
        self.path = str
        self.items = {'txt': 0, 'jpg': 0, 'png': 0, 'dir': 0}

    def _countDots(self, strin):
        cnt = 0
        for c in strin:
            if c == '.':
                cnt += 1
        return cnt

    def getFormat(self, strin):
        strng = ''
        marker = self._countDots(strin)

        for c in range(len(strin)):
            if strin[c] == '.':
                marker -=1
            if marker == 0:
                for i in range(c+1, len(strin)):
                    strng += strin[i]
                else:
                    break
        return strng

    def count(self):
        directory = os.listdir(self.path)

        for el in directory:
            pathName = self.path + '\\' + el
            if os.path.isdir(pathName): 
                self.items['dir'] += 1
            elif os.path.isfile(pathName):
                if self.getFormat(pathName) in self.items.keys():
                    self.items[self.getFormat(pathName)] = self.items.get(self.getFormat(pathName)) + 1     # lze zjednodušit pomocí metody setdefault(x, y)
                else:
                    self.items.update({self.getFormat(pathName): 1})

        return self.items
    
    def createFolder(self, name):
        # creates folder and moves all files that are type: .str (e.g. '.txt') to it
        name = self.path + '\\' + name
        os.makedirs(name)
        print(f'Vytvořil jsem dir: {name}')

    def _transportFileTo(self, file, destination):
        shutil.copy(file, destination)
        print(f'Zkopíroval jsem soubor: {file} na adresu: {destination}')
        os.remove(file)
        print(f'Smazán soubor {file}')

    def autoClean(self):
        for key, val in self.items.items():
            if key != 'dir':
                if val > 1:
                    self.createFolder(key + '_docs')
                    newDir = self.path + '\\' + key + '_docs'
                    for el in os.listdir(self.path):
                        
                        if not os.path.isdir(self.path + '\\' + el):
                            print('This is a file: '+ self.path + '\\' + el)
                            if self.getFormat(self.path + '\\' + el) == key:
                                self._transportFileTo(self.path + '\\' + el, newDir)

    def assistedClean():
        pass

    def cleanUp(self):
        pass
    
if __name__ == '__main__':
    # !!! replace /folder/ with directory you want to clean
    f = Folder('/folder/')

    print(f.count())
    f.autoClean()