from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageDraw, ImageGrab
import time
import os
import io
import sys
import random
import math
from Algebra_To_Function_ver5 import Algebra_Simplfy

global root
global canvas
global final_output
global saved_file
global file_name
global name
global img
global img2
#圖片
global input_gate_image
global output_gate_image
global and_gate_image
global or_gate_image
global not_gate_image

global input_image
global output_image
global and_image
global or_image
global not_image


global all_gate
global all_gate_num
global gate_choose

global all_line
global all_line_num

global mode
global start_end
global start_gate_end_num
global touched_end_id
global finish_end
global start_gate_num
global finish_gate_num
global line_id

global drawing
global rightMenu


class treeNode:
    def __init__(self, val):
        self.val = val
        self.left_node = None
        self.right_node = None

    def insertLeft(self, t):
        if self.left_node == None:
            self.left_node = t
    
    def insertRight(self, t):
        if self.right_node == None:
            self.right_node = t
def print_tree(tree):
    if(tree.left_node!=None):
        print_tree(tree.left_node)
    print(tree.val)
    if(tree.right_node!=None):
        print_tree(tree.right_node)
def tree():
    global all_gate
    global all_gate_num
    
    for i in range(all_gate_num):
        if(all_gate[i].name=="output"):
            tree=treeNode('')
            tree.insertLeft(insert_all_node(all_gate[i].inNum[0]))
            return tree
def insert_all_node(i):
    global all_gate
    if(all_gate[i].name!="input"):
        t=treeNode(all_gate[i].logic)
    else:
        t=treeNode(all_gate[i].outString)
        return t
        
        
    
    if(all_gate[i].inNum[0]!=-1):
        t.insertLeft(insert_all_node(all_gate[i].inNum[0]))
    if(all_gate[i].inNum[1]!=-1):
        t.insertRight(insert_all_node(all_gate[i].inNum[1]))

    
    return t

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class endP():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.id=canvas.create_rectangle(self.x, self.y, self.x+5, self.y+5, fill='black')

class logit_gate():
    def __init__(self, name, x, y, output):
        self.x = x
        self.y = y
        self.name = name
        self.all_end={}        
        self.outString=output
        
        if(name=="input"):
            self.id=canvas.create_image(x,y, image=input_image)
            self.end_num=1
            self.all_end[0]=endP(self.x+25, self.y-3)
            self.nameid = canvas.create_text(self.x-50, self.y-1, font=20, text=self.outString)
        elif(name=="output"):
            self.id=canvas.create_image(x,y, image=output_image)
            self.end_num=1
            self.all_end[0]=endP(self.x-35, self.y-3)
            self.nameid = canvas.create_text(self.x+60, self.y-1, font=20, text=self.outString)            
        elif(name=="and"):
            self.logic="*"
            self.id=canvas.create_image(x,y, image=and_image)
            self.end_num=3
            self.all_end[0]=endP(self.x-30, self.y-15)
            self.all_end[1]=endP(self.x-30, self.y+10)
            self.all_end[2]=endP(self.x+24, self.y-3)
        elif(name=="or"):
            self.logic="+"
            self.id=canvas.create_image(x,y, image=or_image)
            self.end_num=3
            self.all_end[0]=endP(self.x-30, self.y-15)
            self.all_end[1]=endP(self.x-30, self.y+10)
            self.all_end[2]=endP(self.x+24, self.y-3)
        elif(name=="not"):
            self.logic="-"
            self.id=canvas.create_image(x,y, image=not_image)
            self.end_num=2
            self.all_end[0]=endP(self.x-30, self.y-3)
            self.all_end[1]=endP(self.x+24, self.y-3)
        
        
        
        
        self.inNum=[]
        self.in_endNum=[]
        self.inString=[]
        for i in range(2):
            self.inNum.append(-1)
            self.in_endNum.append(-1)
            self.inString.append("")

class new_G():

    
    def __init__(self, name, gate_name, x, y, input_end_num, output_end_num, input_name, output_name, output):
        self.x = x
        self.y = y
        self.name = name
        self.gate_name = gate_name
        self.id=canvas.create_rectangle(x,y,x+100,y+100,fill='white')
        self.end_num=input_end_num+output_end_num
        self.input_end_num=input_end_num
        self.output_end_num=output_end_num
        self.all_end={}
        self.inNum=[]
        self.in_endNum=[]
        self.inString=[]
        self.origin_output=output
        self.outString=[]
        self.input_name=input_name
        self.output_name=output_name
        self.nameid=[]
        for i in range(input_end_num):
            self.all_end[i]=(endP(self.x-5, 80/input_end_num*i+self.y+10))
            self.inNum.append(-1)
            self.in_endNum.append(-1)
            self.inString.append("")
            a=canvas.create_text(self.x+15, 80/input_end_num*i+self.y+15, font=10, text=input_name[i])
            self.nameid.append(a)
        for i in range(input_end_num,self.end_num):
            self.outString.append("")
            self.all_end[i]=(endP(self.x+100, 80/output_end_num*(i-input_end_num)+self.y+10))
            a=canvas.create_text(self.x+85, 80/output_end_num*(i-input_end_num)+self.y+5, font=10, text=output_name[i-input_end_num])
            self.nameid.append(a)
        



class line():
    def __init__(self,start,finish):
        self.start=start
        self.finish=finish
        self.line_id={}
        self.line_id[0]=canvas.create_line((self.start.x+5, self.start.y+2.5, (self.start.x+5+self.finish.x)/2, self.start.y+2.5),width=2,capstyle='round')
        self.line_id[1]=canvas.create_line(((self.start.x+5+self.finish.x)/2, self.start.y+2.5, (self.start.x+5+self.finish.x)/2, self.finish.y+2.5),width=2,capstyle='round')
        self.line_id[2]=canvas.create_line(((self.start.x+5+self.finish.x)/2, self.finish.y+2.5, self.finish.x, self.finish.y+2.5),width=2,capstyle='round')
    def recreate_line(self):
        canvas.delete(self.line_id[0])
        canvas.delete(self.line_id[1])
        canvas.delete(self.line_id[2])
        self.line_id[0]=canvas.create_line((self.start.x+5, self.start.y+2.5, (self.start.x+5+self.finish.x)/2, self.start.y+2.5),width=2,capstyle='round')
        self.line_id[1]=canvas.create_line(((self.start.x+5+self.finish.x)/2, self.start.y+2.5, (self.start.x+5+self.finish.x)/2, self.finish.y+2.5),width=2,capstyle='round')
        self.line_id[2]=canvas.create_line(((self.start.x+5+self.finish.x)/2, self.finish.y+2.5, self.finish.x, self.finish.y+2.5),width=2,capstyle='round')
    def length(self):
        len=0
        a=abs((self.start.x+5+self.finish.x)/2-(self.start.x+5))
        b=abs(self.finish.y+2.5-(self.start.y+2.5))
        c=abs(self.finish.x-((self.start.x+5+self.finish.x)/2))
        len+=a+b+c
        
        return len

def new_file():
    global root
    global canvas
    global file_name
    global all_gate
    global all_gate_num
    global all_line
    global all_line_num
    
    file_name=""
    root.title('新文件 - Q3 GUI')
    canvas.delete("all")
    for i in range(all_gate_num):
        for j in range(all_gate[i].end_num):
            del all_gate[i].all_end[j]
        del all_gate[i]
    for i in range(all_line_num):
        del all_line[i]
        
    
    all_gate_num=0
    all_line_num=0
    final_output.configure(state='normal')
    final_output.delete("1.0","end")
    final_output.configure(state='disabled')
    
    
def open_file():
    global root
    global canvas
    global file_name
    global all_gate
    global all_gate_num
    global all_line
    global all_line_num
    
    
    
    file=askopenfilename(filetypes=[('TXT','*.txt')])
    
    if(file!=""):
        new_file()#清空畫面
        all_gate={} 
        all_line={}
        all_gate_num=0
        all_line_num=0
        
        f_name_split=file.split('/')
        f_name=f_name_split[len(f_name_split)-1]
        
        file_name=f_name.split('.')[0]
        
        root.title(file_name+' - Q3 GUI')
       
        f = open(f_name, 'r')
        
        for l in f.readlines():
            name = l.split(",")[0]
            x = l.split(",")[1]
            y = l.split(",")[2]
            if(name == "input"):
                create_logit_gate("input",int(x),int(y),l.split(",")[3].split("\n")[0])
            elif(name == "new"):
                gate_name=l.split(",")[3]
                input_end_num=int(l.split(",")[4])
                output_end_num=int(l.split(",")[5])
                inNum=[]
                in_endNum=[]
                input_name=[]
                for i in range(input_end_num):
                    inNum.append(int(l.split(",")[6+i]))
                    in_endNum.append(int(l.split(",")[6+i+input_end_num]))
                    input_name.append(l.split(",")[6+i+input_end_num*2])
                output_name=[]
                output=[]
                for i in range(output_end_num):
                    output_name.append(l.split(",")[6+i+input_end_num*3])
                    output.append(l.split(",")[6+i+input_end_num*3+output_end_num].split("\n")[0])
                create_new_gate(gate_name, int(x) ,int(y) ,input_end_num ,output_end_num ,input_name, output_name,output)
                all_gate[all_gate_num-1].inNum=inNum
                all_gate[all_gate_num-1].in_endNum=in_endNum
            else:                
                if(name == "output"):
                    create_logit_gate("output",int(x),int(y),l.split(",")[7].split("\n")[0])
                elif(name == "and"):
                    create_logit_gate("and",int(x),int(y),"")   
                elif(name == "or"):
                    create_logit_gate("or",int(x),int(y),"")
                elif(name == "not"):
                    create_logit_gate("not",int(x),int(y),"")
                all_gate[all_gate_num-1].inNum[0]=int(l.split(",")[3])
                all_gate[all_gate_num-1].inNum[1]=int(l.split(",")[4])
                all_gate[all_gate_num-1].in_endNum[0]=int(l.split(",")[5])
                all_gate[all_gate_num-1].in_endNum[1]=int(l.split(",")[6])
                
        f.close()
        
        for i in range(all_gate_num):
            if(all_gate[i].name == "new"):
                for j in range(all_gate[i].input_end_num):
                    num=all_gate[i].inNum[j]
                    if(all_gate[i].in_endNum[j]==-1):
                        all_line[all_line_num]=line(all_gate[num].all_end[all_gate[num].end_num-1],all_gate[i].all_end[j])
                        all_line_num=all_line_num+1
                    else:
                        all_line[all_line_num]=line(all_gate[num].all_end[all_gate[i].in_endNum[j]],all_gate[i].all_end[j])
                        all_line_num=all_line_num+1
            elif(all_gate[i].name != "input"):
                if(all_gate[i].inNum[0]!=-1):
                    num1=all_gate[i].inNum[0]
                    if(all_gate[i].in_endNum[0]==-1):
                        all_line[all_line_num]=line(all_gate[num1].all_end[all_gate[num1].end_num-1],all_gate[i].all_end[0])
                        all_line_num=all_line_num+1
                    else:
                        all_line[all_line_num]=line(all_gate[num1].all_end[all_gate[i].in_endNum[0]],all_gate[i].all_end[0])
                        all_line_num=all_line_num+1
                if(all_gate[i].inNum[1]!=-1):
                    num2=all_gate[i].inNum[1]
                    if(all_gate[i].in_endNum[1]==-1):
                        all_line[all_line_num]=line(all_gate[num2].all_end[all_gate[num2].end_num-1],all_gate[i].all_end[1])
                        all_line_num=all_line_num+1
                    else:
                        all_line[all_line_num]=line(all_gate[num2].all_end[all_gate[i].in_endNum[1]],all_gate[i].all_end[1])
                        all_line_num=all_line_num+1

def save_file():
    global name
    global file_name
    
    
    set_name=Tk()
    set_name.title('設定檔案名稱')
    set_name.geometry('+500+300')
    set_name.resizable(width=0, height=0)
    set_name.wm_attributes('-topmost',1)
    
    
    name=Text(set_name, height=1, width=40)
    name.pack(side=TOP)
    if(file_name!=""):
        name.insert("insert",file_name)
    
    Button(set_name, text='確認', command=lambda:start_save_file(name.get(1.0, END+"-1c"),set_name)).pack(side=BOTTOM)
    set_name.mainloop()
    
def start_save_file(t,set_name):
    global root
    global file_name
    global canvas
    
    global all_gate
    global all_gate_num
    global all_line
    global all_line_num
    
    if(t!=""):
    
        set_name.destroy()
        time.sleep(1)
        file_name=t
        
             

        f = open(file_name+".txt",'w')
        for i in range (all_gate_num):
            f.writelines([all_gate[i].name,",",str(all_gate[i].x),",",str(all_gate[i].y)])
            
            if(all_gate[i].name=="new"):
                f.writelines([",",all_gate[i].gate_name])
                f.writelines([",",str(all_gate[i].input_end_num), ",", str(all_gate[i].output_end_num)])
                for j in range(all_gate[i].input_end_num):
                    f.writelines([",", str(all_gate[i].inNum[j])])
                for j in range(all_gate[i].input_end_num):
                    f.writelines([",", str(all_gate[i].in_endNum[j])])
                for j in range(all_gate[i].input_end_num):
                    f.writelines([",", all_gate[i].input_name[j]])
                for j in range(all_gate[i].output_end_num):
                    f.writelines([",", all_gate[i].output_name[j]])
                for j in range(all_gate[i].output_end_num):
                    f.writelines([",", all_gate[i].origin_output[j]])
                f.writelines(["\n"])
            elif(all_gate[i].name!="input"):
                f.writelines([",",str(all_gate[i].inNum[0]), ",", str(all_gate[i].inNum[1])])
                f.writelines([",",str(all_gate[i].in_endNum[0]), ",", str(all_gate[i].in_endNum[1])])
                if(all_gate[i].name=="output"):
                    f.writelines([",", all_gate[i].outString])
                f.writelines(["\n"])
            else:
                f.writelines([",",all_gate[i].outString,"\n"])
                
       
        
        f.close()
        root.title(file_name+' - Q3 GUI')
        
        
        
    else:
        messagebox.showinfo("提示", "檔案名稱不可空白")

    

def create_input_or_output_gate(name):
    global mode
    mode=0
    
    set_name=Tk()
    set_name.title('設定名稱')
    set_name.geometry('+500+300')
    set_name.resizable(width=0, height=0)
    set_name.wm_attributes('-topmost',1)
    
    
    output=Text(set_name, height=1, width=40)
    output.pack(side=TOP)
    
    Button(set_name, text='確認', command=lambda:start_create_input_or_output_gate(name,set_name,output.get(1.0, END+"-1c"))).pack(side=BOTTOM)
    set_name.mainloop()
def start_create_input_or_output_gate(name, set_name, output):
    global all_gate
    global all_gate_num
    global canvas
    
    
    if(output!=""):
        set_name.destroy()
        newgate=logit_gate(name,100,100,output)
        
        all_gate[all_gate_num]=newgate
        all_gate_num=all_gate_num+1
    else:
        messagebox.showinfo("提示", "名稱不可空白")

def create_logit_gate(name, x, y, output):
    global all_gate
    global all_gate_num
    global mode
    global canvas
    mode=0
    canvas.config(cursor="arrow")
    new_logit=logit_gate(name, x,y,output)
    
    all_gate[all_gate_num]=new_logit
    all_gate_num=all_gate_num+1

def mouse():
    global mode
    global canvas
    
    canvas.config(cursor="arrow")
    mode=0


def change_mode():
    

    global mode
    global canvas
    if(mode==0):
        mode=1
        canvas.config(cursor="crosshair")
    else:
        mode=0
        canvas.config(cursor="arrow")
    
def delete_gate(gate):
    global canvas
    global all_gate
    global all_gate_num
    global all_line
    global all_line_num
    
    canvas.delete(gate.id)
    del all_gate[gate.id]
    if(gate.name=="input"):
        canvas.delete(gate.nameid)
    for i in range(gate.end_num):
        canvas.delete(gate.all_end[i].id)
        for j in range(all_line_num):
            if((all_line[j].start==gate.all_end[i])|(all_line[j].finish==gate.all_end[i])):
                canvas.delete(all_line[j].line_id[0])
                canvas.delete(all_line[j].line_id[1])
                canvas.delete(all_line[j].line_id[2])
                
    all_gate_num=all_gate_num-1
    all_line_num=all_line_num-1

def compile_q():
    global all_gate
    global all_gate_num
    total_output=0
    output_finish=0
    for i in range(all_gate_num):
        if(all_gate[i].name=="output"):
            total_output+=1
    
    output=""
    #
    while(output_finish<total_output):
        for i in range(all_gate_num):
            if(all_gate[i].name=="new"):
                all_have_output=1
                for j in range(all_gate[i].input_end_num):
                    inN=all_gate[i].inNum[j]
                    if(all_gate[inN].outString==""):
                        all_have_output=0
                        break
                
                if(all_have_output==1):
                    for j in range(all_gate[i].output_end_num):
                        all_gate[i].outString[j]=all_gate[i].origin_output[j]
                    for j in range(all_gate[i].output_end_num):
                        for k in range(all_gate[i].input_end_num):
                            if(all_gate[all_gate[i].inNum[k]].name!="new"):
                                a=all_gate[i].outString[j].replace(all_gate[i].input_name[k], all_gate[all_gate[i].inNum[k]].outString)
                                all_gate[i].outString[j]=a
                            else:
                                end_num=all_gate[i].in_endNum[k]-all_gate[all_gate[i].inNum[k]].input_end_num
                                a=all_gate[i].outString[j].replace(all_gate[i].input_name[k], all_gate[all_gate[i].inNum[k]].outString[end_num])
                                all_gate[i].outString[j]=a
                
            elif(all_gate[i].name!="input"):
                in1=all_gate[i].inNum[0]
                in2=all_gate[i].inNum[1]
                outString1=""
                outString2=""
                if(in1!=-1):
                    if((all_gate[in1].name!="new")&(all_gate[in1].outString!="")):
                        outString1=all_gate[in1].outString
                    if(all_gate[in1].name=="new"):
                        if(all_gate[in1].outString[all_gate[i].in_endNum[0]-all_gate[in1].input_end_num]!=""):
                            outString1=all_gate[in1].outString[all_gate[i].in_endNum[0]-all_gate[in1].input_end_num]
                if(in2!=-1):
                    if((all_gate[in2].name!="new")&(all_gate[in2].outString!="")):
                        outString2=all_gate[in2].outString
                    if(all_gate[in2].name=="new"):
                        if(all_gate[in2].outString[all_gate[i].in_endNum[1]-all_gate[in2].input_end_num]!=""):
                            outString2=all_gate[in2].outString[all_gate[i].in_endNum[1]-all_gate[in2].input_end_num]
                
                
                if(all_gate[i].name=="output"):
                    if(outString1!=""):
                        all_gate[i].inString=outString1
                        output = output + all_gate[i].outString+"="+all_gate[i].inString+"\n"
                        output_finish+=1
                elif(all_gate[i].name=="and"):
                    if((outString1!="")&(outString2!="")):
                        all_gate[i].outString="("+outString1+"*"+outString2+")"
                elif(all_gate[i].name=="or"):
                    if((outString1!="")&(outString2!="")):
                        all_gate[i].outString="("+outString1+"+"+outString2+")"
                elif(all_gate[i].name=="not"):
                    if(outString1!=""):
                        all_gate[i].outString="(-"+outString1+")"
    return output
    
def print_output():
    global final_output
    final_output.configure(state='normal')
    final_output.delete("1.0","end")    
    final_output.insert("insert", compile_q())
    final_output.configure(state='disabled')
    
    
def export_g():
    global name
    global file_name
    
    
    set_name=Tk()
    set_name.title('設定名稱')
    set_name.geometry('+500+300')
    set_name.resizable(width=0, height=0)
    set_name.wm_attributes('-topmost',1)
    
    
    name=Text(set_name, height=1, width=40)
    name.pack(side=TOP)
    if(file_name!=""):
        name.insert("insert",file_name)
    
    Button(set_name, text='確認', command=lambda:start_export_g(name.get(1.0, END+"-1c"),set_name)).pack(side=BOTTOM)
    set_name.mainloop()
    
def start_export_g(t,set_name):
    global root
    global file_name
    global canvas
    
    global all_gate
    global all_gate_num
    global all_line
    global all_line_num
    
    #global img
    
    if(t!=""):
    
        set_name.destroy()
        time.sleep(1)
        file_name=t
        
             

        f = open(file_name+".txt",'w')
        for i in range(all_gate_num):
            if(all_gate[i].name=="input"):
                f.writelines([all_gate[i].outString,"\n"])
        f.writelines([compile_q()])
       
        
        f.close()
        root.title(file_name+' - Q3 GUI')
        
        
        
    else:
        messagebox.showinfo("提示", "檔案名稱不可空白")

def import_g():
    global canvas
    global all_gate
    global all_gate_num
    global mode
    mode=0
    

    
    
    file=askopenfilename(filetypes=[('TXT','*.txt')])
    
    f_name_split=file.split('/')
    f_name=f_name_split[len(f_name_split)-1]
    
    file_name=f_name.split('.')[0]
    gate_name=file_name
    
    if(file!=""):
        
        f_name_split=file.split('/')
        f_name=f_name_split[len(f_name_split)-1]
        f = open(f_name, 'r')
        input_end_num=0
        output_end_num=0
        input_name=[]
        output_name=[]
        output=[]
        for l in f.readlines():
            #print()
            if(len(l.split("="))==1):
                input_end_num+=1
                input_name.append(l.split("\n")[0])
            else:
                output_end_num+=1
                output_name.append(l.split("=")[0])
                output.append(l.split("=")[1].split("\n")[0])
        f.close()
    newgate=new_G("new", gate_name, 200 ,100 ,input_end_num ,output_end_num ,input_name, output_name,output)
    
    all_gate[all_gate_num]=newgate
    all_gate_num=all_gate_num+1

def create_new_gate(gate_name, x ,y ,input_end_num ,output_end_num ,input_name, output_name,output):
    global all_gate
    global all_gate_num
    global mode
    mode=0
    
    newgate=new_G("new", gate_name, x ,y ,input_end_num ,output_end_num ,input_name, output_name,output)
    
    all_gate[all_gate_num]=newgate
    all_gate_num=all_gate_num+1
    

def simplify():
    global final_output
    s=""
    for i in range(len(compile_q().split("\n"))-1):
        bool_expr=compile_q().split("\n")[i].split("=")[1]
        a=Algebra_Simplfy(bool_expr)
        s=s+compile_q().split("\n")[i].split("=")[0]+"="+a+"\n"
    
    final_output.configure(state='normal')
    final_output.delete("1.0","end")    
    final_output.insert("insert", s)
    final_output.configure(state='disabled')


def energy():
    global all_line
    global all_line_num
    
    length=0
    for i in range(all_line_num):
        
        length+=all_line[i].length()
        
    return length

def energy_r(a,x,y):
    top=-1
    bottom=-1
    left=-1
    right=-1
    for i in range(x):
        for j in range(y):
            if(a[i][j]!=-1):
                right=i
                if(left==-1):
                    left=i
    for i in range(y):
        for j in range(x):
            if(a[j][i]!=-1):
                bottom=i
                if(top==-1):
                    top=i
    r=(bottom-top)*(right-left)
    return r
    
    
def move_gate(gate_choose,x,y):
    global canvas
    global all_gate
    global all_line
    global all_line_num
    
    lastx=all_gate[gate_choose].x
    lasty=all_gate[gate_choose].y
    canvas.move(all_gate[gate_choose].id,x-lastx, y-lasty) 
    all_gate[gate_choose].x= all_gate[gate_choose].x+x-lastx
    all_gate[gate_choose].y= all_gate[gate_choose].y+y-lasty
    if((all_gate[gate_choose].name=="input")|(all_gate[gate_choose].name=="output")):
        canvas.move(all_gate[gate_choose].nameid,x-lastx, y-lasty)
    if(all_gate[gate_choose].name=="new"):
        for i in range(all_gate[gate_choose].end_num):
            canvas.move(all_gate[gate_choose].nameid[i],x-lastx, y-lasty)
            canvas.tag_raise(all_gate[gate_choose].nameid[i])
    for i in range(all_gate[gate_choose].end_num):
        canvas.move(all_gate[gate_choose].all_end[i].id,x-lastx, y-lasty)
        all_gate[gate_choose].all_end[i].x=all_gate[gate_choose].all_end[i].x +x-lastx
        all_gate[gate_choose].all_end[i].y=all_gate[gate_choose].all_end[i].y +y-lasty
    for i in range(all_line_num):
        all_line[i].recreate_line()

def print_energy():
    print("energy:",energy())

def placement():
    global canvas
    global all_gate
    global all_gate_num
    global all_line
    global all_line_num
    
    x_grid=9
    y_grid=6
    grid_size=int(500/y_grid)
    
    gate_grid=[[-1]*y_grid for i in range(x_grid)]
    
    input_count=0
    for gate_choose in range(all_gate_num):
        again=1
        while(again==1):
            again=0
            b=random.randint(0,y_grid-1)
            if(all_gate[gate_choose].name=="input"):
                input_count+=1
                a=0
            elif(all_gate[gate_choose].name=="output"):
                a=x_grid-1
            else:
                a=random.randint(1,x_grid-2)
                
            if(gate_grid[a][b]==-1):
                gate_grid[a][b]=gate_choose
                break
            else:
                again=1
            
        x=a*grid_size+100
        y=b*grid_size+30
       
        move_gate(gate_choose,x,y)
    print("initial")
    predict_energy=100*all_gate_num*input_count*9
    while(energy()*energy_r(gate_grid,x_grid,y_grid)>predict_energy):
        T_start=4000000
        T_min=0.1
        T=T_start
        step=100
        
        now_energy=energy()*energy_r(gate_grid,x_grid,y_grid)
        
        while((T>T_min)|step>0):
            #new placement
            
            #print(T)
            mode=random.random()
            if(mode<0.5):
                #switch
                choose=1
                while(choose==1):
                    choose=0
                    again=1
                    while(again==1):
                        again=0
                        a1=random.randint(0,x_grid-1)
                        b1=random.randint(0,y_grid-1)
                        if(gate_grid[a1][b1]!=-1):
                            g1=gate_grid[a1][b1]
                            break
                        else:
                            again=1
                    again=1
                    while(again==1):
                        again=0
                        b2=random.randint(0,y_grid-1)
                        if(all_gate[g1].name=="input"):
                            a2=0
                        elif(all_gate[g1].name=="output"):
                            a2=x_grid-1
                        else:
                            a2=random.randint(1,x_grid-2)
                        if(gate_grid[a2][b2]!=-1):
                            g2=gate_grid[a2][b2]
                            break
                        else:
                            again=1
                    if(g1==g2):
                        choose=1
                
                x1=all_gate[g1].x
                y1=all_gate[g1].y
                x2=all_gate[g2].x
                y2=all_gate[g2].y        
                for i in range(2):
                    if(i==0):
                        x=x2
                        y=y2
                        gate_choose=g1
                        gate_grid[a2][b2]=g1
                    else:   
                        x=x1
                        y=y1
                        gate_choose=g2
                        gate_grid[a1][b1]=g2
                    move_gate(gate_choose,x,y)
                    
            else:#move
                again=1
                while(again==1):
                    again=0
                    a=random.randint(0,x_grid-1)
                    b=random.randint(0,y_grid-1)
                    if(gate_grid[a][b]!=-1):
                        gate_choose=gate_grid[a][b]
                        break
                    else:
                        again=1
                again=1
                while(again==1):
                    again=0
                    if(all_gate[gate_choose].name=="input"):
                        x=0
                    elif(all_gate[gate_choose].name=="output"):
                        x=0
                    else:
                        x=random.randint(-1*(x_grid-1),x_grid-1)
                        while( ((a+x)>=(x_grid-1)) | ((a+x)<=0)):
                            x=random.randint(-1*(x_grid-1),x_grid-1)
                    y=random.randint(-1*(y_grid-1),y_grid-1)
                    if(((a+x)>(x_grid-1)) | ((a+x)<0) | ((b+y)>(y_grid-1)) | ((b+y)<0)):
                        again=1
                    else:
                        if(gate_grid[a+x][b+y]!=-1):
                            again=1
                    
                #print("a+x",a+x,"b+y",b+y)
                gate_grid[a][b]=-1
                gate_grid[a+x][b+y]=gate_choose
                new_x=(a+x)*grid_size+100
                new_y=(b+y)*grid_size+30
                
                
                move_gate(gate_choose,new_x,new_y)
            
            new_energy=energy()*energy_r(gate_grid,x_grid,y_grid)
            if(new_energy<now_energy):
                now_energy=new_energy
            else:
                if(random.random()<math.exp(-(new_energy-now_energy)/T)):
                    now_energy=new_energy
                else:
                    if(mode<0.5):
                        for i in range(2):
                            if(i==0):
                                x=x1
                                y=y1
                                gate_choose=g1
                                gate_grid[a1][b1]=g1
                            else:   
                                x=x2
                                y=y2
                                gate_choose=g2
                                gate_grid[a2][b2]=g2
                            move_gate(gate_choose,x,y)
                    else:
                        move_gate(gate_choose,a*grid_size+100,b*grid_size+30)
                        gate_grid[a][b]=gate_choose
                        gate_grid[a+x][b+y]=-1
            T*=0.9
            step-=1 
    for i in range(x_grid):
        for j in range(y_grid):
            if(gate_grid[i][j]!=-1):
                if(all_gate[gate_grid[i][j]].name=="output"):
                    m=i
                    while(m>0):
                        m-=1
                        clear=1
                        for k in range(y_grid):
                            if(gate_grid[m][k]!=-1):
                                clear=0
                        if(clear==0):
                            m+=1
                            break
                    move_gate(gate_grid[i][j],m*grid_size+100,j*grid_size+30)
    print("finish")
    print("energy:",energy()*energy_r(gate_grid,x_grid,y_grid))

def main():
    global root
    global canvas
    global final_output
    global file_name
    global img
    global img2
    
    #圖片
    global input_gate_image
    global output_gate_image
    global and_gate_image
    global or_gate_image
    global not_gate_image
    
    global input_image
    global output_image
    global and_image
    global or_image
    global not_image
    
    global all_gate
    global all_gate_num
    global gate_choose
    
    global all_line
    global all_line_num
    
    global mode
    global start_end
    global touched_end_id
    global finish_end
    global line_id
    global drawing
    global rightMenu

    line_id={}
    line_id[0]=""
    line_id[1]=""
    line_id[2]=""
    
    mode=0
    drawing=0
    gate_choose=-1
    all_gate={} 
    all_line={}
    all_gate_num=0
    all_line_num=0
    lasty, lastx = 0, 0
    touched_end_id=""
    
    
    def xy(event):
        nonlocal lasty, lastx
        global all_gate
        global all_gate_num
        global gate_choose
        global start_end
        global start_gate_end_num
        global finish_end
        global start_gate_num
        global drawing
        start_end=-1
        drawing=0
        if(mode==0):
            gate_choose=-1
            
            for i in range(all_gate_num):
                #print(all_gate_num)
                if(all_gate[i].name!="new"):
                    if((event.x<=all_gate[i].x+30)&(event.x>=all_gate[i].x-30)
                    &(event.y<=all_gate[i].y+30)&(event.y>=all_gate[i].y-30)):
                        gate_choose=i
                        #置頂
                        canvas.tag_raise(all_gate[gate_choose].id)
                        for i in range(all_gate[gate_choose].end_num):
                            canvas.tag_raise(all_gate[gate_choose].all_end[i].id)
                        for j in range(all_line_num):
                            all_line[j].recreate_line()
                        break
                else:
                    if((event.x<=all_gate[i].x+70)&(event.x>=all_gate[i].x+30)
                    &(event.y<=all_gate[i].y+70)&(event.y>=all_gate[i].y+30)):
                        gate_choose=i
                        #置頂
                        canvas.tag_raise(all_gate[gate_choose].id)
                        for i in range(all_gate[gate_choose].end_num):
                            canvas.tag_raise(all_gate[gate_choose].all_end[i].id)
                        for j in range(all_line_num):
                            all_line[j].recreate_line()
                        break
            
        elif(mode==1):
            for i in range(all_gate_num):
                for j in range(all_gate[i].end_num):
                    if((event.x<=all_gate[i].all_end[j].x+10)&(event.x>=all_gate[i].all_end[j].x)
                    &(event.y<=all_gate[i].all_end[j].y+10)&(event.y>=all_gate[i].all_end[j].y)):
                        start_gate_num=i
                        if(all_gate[i].name=="new"):
                            start_gate_end_num=j
                        else:
                            start_gate_end_num=-1
                        start_end=all_gate[i].all_end[j]
                        drawing=1
                        finish_end=start_end
                        
                        break
        
        #print(gate_choose)
        lastx = event.x
        lasty = event.y

    def addLine(event):
        nonlocal lasty, lastx
        global canvas
        global all_gate
        global all_gate_num
        global all_line
        global all_line_num
        global touched_end_id
        global line_id
        #print(gate_choose)
        
        if(mode==0):#移動
            if(gate_choose!=-1):
                canvas.move(all_gate[gate_choose].id,event.x-lastx, event.y-lasty) 
                all_gate[gate_choose].x= all_gate[gate_choose].x+event.x-lastx
                all_gate[gate_choose].y= all_gate[gate_choose].y+event.y-lasty
                if((all_gate[gate_choose].name=="input")|(all_gate[gate_choose].name=="output")):
                    canvas.move(all_gate[gate_choose].nameid,event.x-lastx, event.y-lasty)
                if(all_gate[gate_choose].name=="new"):
                    for i in range(all_gate[gate_choose].end_num):
                        canvas.move(all_gate[gate_choose].nameid[i],event.x-lastx, event.y-lasty)
                        canvas.tag_raise(all_gate[gate_choose].nameid[i])
                for i in range(all_gate[gate_choose].end_num):
                    canvas.move(all_gate[gate_choose].all_end[i].id,event.x-lastx, event.y-lasty)
                    all_gate[gate_choose].all_end[i].x=all_gate[gate_choose].all_end[i].x +event.x-lastx
                    all_gate[gate_choose].all_end[i].y=all_gate[gate_choose].all_end[i].y +event.y-lasty
                for i in range(all_line_num):
                    all_line[i].recreate_line()
                
        elif(mode==1):#畫線
            if(line_id[0]!=""):
                canvas.delete(line_id[0])
                canvas.delete(line_id[1])
                canvas.delete(line_id[2])
            if(drawing==1):
                line_id[0]=canvas.create_line((start_end.x+5, start_end.y+2.5, (start_end.x+5+event.x)/2, start_end.y+2.5),width=2,capstyle='round')
                line_id[1]=canvas.create_line(((start_end.x+5+event.x)/2, start_end.y+2.5, (start_end.x+5+event.x)/2, event.y),width=2,capstyle='round')
                line_id[2]=canvas.create_line(((start_end.x+5+event.x)/2, event.y, event.x, event.y),width=2,capstyle='round')
            
            if(touched_end_id!=""):
                canvas.delete(touched_end_id)
            for i in range(all_gate_num):
                for j in range(all_gate[i].end_num):
                    if((event.x<=all_gate[i].all_end[j].x+10)&(event.x>=all_gate[i].all_end[j].x)
                    &(event.y<=all_gate[i].all_end[j].y+10)&(event.y>=all_gate[i].all_end[j].y)):
                        if(start_end!=all_gate[i].all_end[j]):
                            touched_end=all_gate[i].all_end[j]
                            touched_end_id=canvas.create_rectangle(touched_end.x, touched_end.y, touched_end.x+5, touched_end.y+5, fill='red')                        
                            
                            break                
        
        
        
        lasty = event.y
        lastx = event.x
    
    def draw(event):
        global mode
        global all_gate
        global start_gate_end_num
        global start_end
        global touched_end_id
        global finish_end
        global finish_gate_num
        global line_id
        global all_line_num
        global drawing
        finish_gate_num=-1
        if(line_id[0]!=""):
            canvas.delete(line_id[0])
            canvas.delete(line_id[1])
            canvas.delete(line_id[2])
        if(touched_end_id!=""):
            canvas.delete(touched_end_id)
        if(mode==1):
            if(drawing==1):
                for i in range(all_gate_num):
                    for j in range(all_gate[i].end_num):
                        if((event.x<=all_gate[i].all_end[j].x+10)&(event.x>=all_gate[i].all_end[j].x)
                        &(event.y<=all_gate[i].all_end[j].y+10)&(event.y>=all_gate[i].all_end[j].y)):
                            if(start_end!=all_gate[i].all_end[j]):
                                finish_gate_num=i
                                finish_end=all_gate[i].all_end[j]
                                all_line[all_line_num]=line(start_end,finish_end)
                                all_line_num=all_line_num+1
                                if(start_gate_end_num==-1):
                                    if(all_gate[finish_gate_num].inNum[j]==-1):
                                        all_gate[finish_gate_num].inNum[j]=start_gate_num
                                else:
                                    if(all_gate[finish_gate_num].inNum[j]==-1):
                                        all_gate[finish_gate_num].inNum[j]=start_gate_num
                                        all_gate[finish_gate_num].in_endNum[j]=start_gate_end_num
                                break

                
                
        drawing=0
    
    def right_menu(event):
        global rightMenu
        global gate_choose
        
        
        rightMenu.post(event.x_root, event.y_root)
        gate_choose=-1
            
        for i in range(all_gate_num):
            #print(all_gate_num)
            if((event.x<=all_gate[i].x+30)&(event.x>=all_gate[i].x-30)
            &(event.y<=all_gate[i].y+30)&(event.y>=all_gate[i].y-30)):
                gate_choose=i
                break
    
    
    
    
    
    
    file_name="新文件"

    root = tk.Tk()
    root.title('新文件 - Q3 GUI')
    root.geometry('+100+20')
    root.resizable(width=0, height=0)
    
    frame_left = tk.Frame(root)
    frame_right = tk.Frame(root)
    
    
    frame_left.pack(side=tk.LEFT)
    frame_right.pack(side=tk.RIGHT)
    
    frame_canvas = tk.Frame(frame_right)
    frame_bottom = tk.Frame(frame_right)
    
    frame_canvas.pack(side=tk.TOP)
    frame_bottom.pack(side=tk.BOTTOM)
    
    
    #圖片
    #big
    mouse_image = tk.PhotoImage(file='gate_image/mouse.png')
    input_gate_image = tk.PhotoImage(file='gate_image/input_b.png')
    output_gate_image = tk.PhotoImage(file='gate_image/output_b.png')
    and_gate_image = tk.PhotoImage(file='gate_image/and_b.png')
    or_gate_image = tk.PhotoImage(file='gate_image/or_b.png')
    not_gate_image = tk.PhotoImage(file='gate_image/not_b.png')
    line_image = tk.PhotoImage(file='gate_image/line.png')
    
    
    input_image = tk.PhotoImage(file='gate_image/input.png')
    output_image = tk.PhotoImage(file='gate_image/output.png')
    and_image = tk.PhotoImage(file='gate_image/and.png')
    or_image = tk.PhotoImage(file='gate_image/or.png')
    not_image = tk.PhotoImage(file='gate_image/not.png')
    
    #按鈕
    tk.Button(frame_left, image=mouse_image, command = mouse).pack(side=tk.TOP)
    tk.Button(frame_left, image=input_gate_image, command = lambda:create_input_or_output_gate("input")).pack(side=tk.TOP)
    tk.Button(frame_left, image=output_gate_image, command = lambda:create_input_or_output_gate("output")).pack(side=tk.TOP)
    tk.Button(frame_left, image=and_gate_image, command = lambda:create_logit_gate("and",200,100,"")).pack(side=tk.TOP)
    tk.Button(frame_left, image=or_gate_image, command = lambda:create_logit_gate("or",200,100,"")).pack(side=tk.TOP)
    tk.Button(frame_left, image=not_gate_image, command = lambda:create_logit_gate("not",200,100,"")).pack(side=tk.TOP)
    tk.Button(frame_left, image=line_image, command = change_mode).pack(side=tk.TOP)
    tk.Button(frame_left, text='start', font=('微軟正黑體', 20, 'bold'), command = print_output).pack(side=tk.TOP)
    
    
    
    
    #frame_canvas
    canvas = tk.Canvas(frame_canvas, width=900, height=500, bg="white", cursor="arrow")
    canvas.bind('<Button-1>', xy)
    canvas.bind('<B1-Motion>', addLine)
    canvas.bind('<ButtonRelease-1>', draw)
    #canvas.bind('<Button-3>', right_menu)
    canvas.pack()
    
    
    
    #frame_bottom
    final_output_t=tk.Label(frame_bottom, text="Output")
    final_output_t.pack(side=tk.LEFT)
    final_output = tk.Text(frame_bottom, width=100, height=5)
    final_output.configure(state='disabled')
    final_output.pack(side=tk.LEFT)
    
    
    
    
    #選單
    mainmenu=Menu(root)
    root.config(menu=mainmenu)
    menu1=Menu(mainmenu ,tearoff=0)
    menu1.add_command(label="新增檔案", command=new_file)
    menu1.add_command(label="開啟檔案", command=open_file)
    menu1.add_command(label="儲存檔案", command=save_file)
    #,accelerator="Ctrl+S")
    menu1.add_command(label="匯出元件", command=export_g)
    menu1.add_command(label="匯入元件", command=import_g)
    #menu1.add_command(label="印出tree", command=lambda:print_tree(tree()))
    menu1.add_command(label="簡化", command=simplify)
    menu1.add_command(label="放置", command=placement)
    menu1.add_command(label="能量", command=print_energy)
    root.bind_all("<Control-s>", save_file)

    mainmenu.add_cascade(label="檔案",menu=menu1)
    #/選單
    
    rightMenu = Menu(canvas,tearoff=0)
    rightMenu.add_command(label="刪除", command=lambda:delete_gate(all_gate[gate_choose]))
    #rightMenu.add_separator()
    
    
    
    root.mainloop()


if __name__ == '__main__':
    main()