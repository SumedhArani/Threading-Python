
import threading
import os
import fnmatch
from PIL import Image
import shutil
import sys

path = '/users/sumedh/'
os.chdir(path)
if __name__ == '__main__':
    try:
        path1  = sys.argv[1]
        path2 = 'tn_img_'+sys.argv[1]
    except IndexError:
        print "\nPlease enter a directory.\nUsage example: python img_thread.py 'directory'\n\n\n"
npath1 = path+path1
npath2 = path+path2

if not os.path.exists(path2):
    os.makedirs(path2)

class  myThread(threading.Thread):
    def __init__(self,threadID,file,func):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.file = file
        self.func = func
        
    def run(self):
        threadLock.acquire()
        self.func(self.file)
        threadLock.release()

def resize(file):
    file_name, ext = file.split('.')
    os.chdir(npath1)
    im = Image.open(file)
    im.resize((Hpixel,Wpixel)).save(file_name + 't.jpg', "JPEG")
    nim= Image.open("%st.jpg" %file_name)
    print '\tresized image'
    print '\t\tOld Size: ' ,im.size
    print '\t\tNew size: ' ,nim.size

def move(file):
    file_name, ext = file.split('.')
    new_file= file_name+'t.jpg'
    os.chdir(npath1)
    shutil.copy2(new_file, npath2)
    print '\tmoved image'

def rename_img(file):
    file_name, ext = file.split('.')
    os.chdir(npath2)
    new_file= file_name+'t.jpg'
    os.rename(new_file, file_name+'.jpg')
    print '\trenamed image'

def remove_img_copy(file):
    file_name, ext =file.split('.')
    os.chdir(npath1)
    new_file = file_name+'t.jpg'
    new_path = npath1+'/'+new_file 
    os.remove(new_path)
    print '\tremoved copy'

threadLock = threading.Lock()
Hpixel = int(raw_input('Enter height of pixels: \n'))
Wpixel = int(raw_input('Enter width of pixels: \n'))

for file in os.listdir(path1):
    
    threads= []
    if fnmatch.fnmatch(file,'*.jpg'):
        print "Image : ", file
        thread1= myThread(1, file,  resize)
        thread1.start()
        #threads.append(thread1)
        thread1.join()

        thread2= myThread(2, file, move)
        thread2.start()
        threads.append(thread2)
        
        thread3= myThread(3, file, rename_img)
        thread3.start()
        threads.append(thread3)

        thread4= myThread(4, file, remove_img_copy)
        thread4.start()
        threads.append(thread4)

    for t in threads:
        t.join()

print '\n\nExiting main thread!! '
