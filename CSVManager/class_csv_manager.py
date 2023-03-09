import math
import pathlib
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.ttk import *
class CSVManager:
    def __init__(self) -> None:
        self.way_journal_file=pathlib.Path(__file__).parent.joinpath('current_file.txt')
        self.sep_journal_file=pathlib.Path(__file__).parent.joinpath('separator.txt')
        self.root_w=Tk()
        self.root_w.title("CSVManager")
        self.root_w.geometry('500x500')        
        mainmenu=Menu(self.root_w)
        self.root_w.config(menu=mainmenu)        
        filemenu = Menu(mainmenu, tearoff=0)
        filemenu.add_command(label='Choose File', command=self.choose_file)
        filemenu.add_command(label='Create File', command=self.create_file_keys)
        filemenu.add_command(label='Change separator', command=self.choose_new_separator)
        mainmenu.add_cascade(label='File',menu=filemenu)
        btn_new_person=Button(self.root_w, text='New_Person', command=self.add_new_person)
        btn_read_to_dict=Button(self.root_w, text='View File', command=self.view_file_data)
        find_person_btn=Button(self.root_w, text="Find person", command=self.find_person)
        btn_new_person.grid(row=0, column=0)
        btn_read_to_dict.grid(row=1, column=0)
        find_person_btn.grid(row=2, column=0)
        self.main_file=self.current_file_way()
        self.separator=self.current_separator()
        self.create_key_list()
        self.start_message()
        self.root_w. mainloop()
        pass        
    def start_message(self):
            messagebox.showinfo(message=f'Current file is {self.main_file}\n Separator is "{self.separator}"')
            pass
    def current_file_way(self):
        with open (self.way_journal_file, 'r') as w:
            way=w.read()
            if pathlib.Path(way).is_file()==True: return(way)
            else: way=pathlib.Path(__file__).parent.joinpath('testdata.csv') 
            print(way)
            return(way)
    def current_separator(self):       
        with open (self.sep_journal_file, 'r') as w:
            sep=w.read()
            print(sep)
        return(sep)
    def find_person(self):
        find_w=Toplevel()
        find_w.geometry('600x400')
        find_label=Label(find_w, text='Find by:')
        find_key_val_l=Label(find_w, text='Key value: ')
        find_key_val_e=Entry(find_w)
        sep_label=Label(find_w, text=f'Separator: "{self.separator}"')
        find_label.grid(row=0, column=0, columnspan=3, sticky='ns')
        find_key_val_l.grid(row=1,column=0, sticky='e')
        find_key_val_e.grid(row=1, column=1)
        sep_label.grid(row=1,column=2)
        row_for_listbox=math.ceil(len(self.key_list)/4)+2
        print(row_for_listbox)
        krow=2
        kcol=0
        for next_key in self.key_list:
            key=Button(find_w, text=next_key, command=lambda window=find_w, k=next_key, val=find_key_val_e, lbrow=row_for_listbox, lbcol=0, : self.find_by_key(window,k, val, lbrow, lbcol))
            key.grid(row=krow, column=kcol, sticky='ns', padx=10)
            kcol+=1
            if kcol>3:
                krow+=1
                kcol=0
        pass
    def find_by_key(self,window, key, val, lbrow, lbcol):
        data_dict=self.readToDict(key)
        key_val=val.get()
        val_list=key_val.strip().split(self.separator)
        rows_list=[]
        for value in val_list:
            row_list=[]
            person_dict=data_dict[value]
            for v in person_dict.values():
                row_list.append(v)
            rows_list.append(row_list)

        listbox = Listbox(window,selectmode=SINGLE)

        listbox.bind("<<ListboxSelect>>", self.on_select_function)
        listbox.bind("<Return>", self.choose_person)
        listbox.grid(row=lbrow, column=lbcol,padx=10, columnspan=2, sticky='w')
        for row in rows_list:
            
            listbox.insert(END, row)
        pass       
    def choose_new_separator(self):
        sep_w=Toplevel()
        sep_label=Label(sep_w, text='Take a new separator')
        sep_entry=Entry(sep_w)
        sep_but=Button(sep_w, text='Save', command=lambda sep=sep_entry :self.save_new_separator(sep, sep_w))
        sep_label.grid(row=0,column=1, sticky='ns')
        sep_entry.grid(row=1,column=1, sticky='ns')
        sep_but.grid(row=2,column=1, sticky='ns')
    def save_new_separator(self, separator, wind):
        self.separator=separator.get()
        with open(self.sep_journal_file, 'w') as j: j.write(self.separator)
        messagebox.showinfo(message=f'New separator is "{self.separator}"')
        wind.destroy()
    def create_file_keys(self):
        keys_w=Toplevel()
        keys_label=Label(keys_w, text=f'Enter keywords for headers \nSeparator: {self.separator}')
        keys_entry=Entry(keys_w)
        id_label=Label(keys_w, text='First kewrord always "id" ')
        create_btn=Button(keys_w,text='Create', command=lambda headers=keys_entry: self.create_file(headers, keys_w))
        keys_label.grid(row=0,column=0, columnspan=2, sticky='ns')
        keys_entry.grid(row=1,column=0, columnspan=2, sticky='ns')
        id_label.grid(row=2,column=0, columnspan=2, sticky='ns')
        create_btn.grid(row=3,column=0, columnspan=2, sticky='ns')
        pass
    def create_file(self, headers, wind):
        headers=headers.get()
        headers_list=['id']
        for i in headers.strip().split(self.separator):
            headers_list.append(i)
        print(headers_list)
        filetypes = (
        ("CSV files", "*.csv"),
        )

        file_name = asksaveasfilename(
        title="Select file",
        filetypes=filetypes
        )
        print(file_name)        
        with open(file_name, "w") as f: 
            for key in headers_list[0:-1]:
                f.write(key+self.separator)
            for key in headers_list[-1]:
                f.write(key)
        new_currrent_file=messagebox.askyesno(message=f'File {file_name} created!\n Do you want to make this file current?')
        if new_currrent_file==True: 
            self.main_file=file_name
            with open (self.way_journal_file, 'w') as j: j.write(str(self.main_file))
            self.create_key_list()
            messagebox.showinfo(message=f'New current file is {self.main_file}')
        wind.destroy()
        pass
    def choose_file(self):
        filetypes = (
        ("CSV files", "*.csv"),
        )
        file_name = askopenfilename(
        title="Select file to open",
        filetypes=filetypes
        )        
        if file_name!='':
            self.main_file=file_name
            self.create_file_keys        
            with open (self.way_journal_file, 'w') as j: j.write(str(self.main_file))
            self.create_key_list()
            messagebox.showinfo(message=f'New current file is: {self.main_file}')
        pass
    def create_key_list(self):
        self.key_list=[]
        with open (self.main_file) as mf:
            headers = mf.readline()
        for key in headers.strip().split(self.separator):
            self.key_list.append(key)
        return self.key_list
    def readToList(self) -> list[list[str]]:
        with open (self.main_file) as mf:
            headers = mf.readline()
            persons = mf.readlines()
        result_list=[] 
        for next_person in persons:
            result_list.append(next_person.strip().split(self.separator))
        return result_list
    def readToDict(self, key_word):
        persons_list=[]
        result_dict={}
        with open (self.main_file) as mf:
            headers = mf.readline()
            persons = mf.readlines()
        for next_person in persons:
            persons_list.append(next_person.strip().split(self.separator))
        for person in persons_list:
            person_dict = {}
            for val in person:
                person_dict[self.key_list[person.index(val)]] = val           
            result_dict[person_dict[key_word]]=person_dict


            



        return result_dict
    def add_new_person(self):
        
        new_person_w=Toplevel(self.root_w)
        

        new_person_label=Label(new_person_w, text='Create a new person ')
        new_person_label.grid(row=0, column=0,columnspan=2, sticky='ns')
        entries=[]
        for key in self.key_list[1:]:
            key_label=Label(new_person_w, text= key)

            key_label.grid(column=0, row=self.key_list.index(key))
            entries.append(Entry(new_person_w, width=15, font='Arial 12'))
        for entry in entries:
            entry.grid(row=entries.index(entry)+1, column=1)
        
        create_new_person_btn=Button(new_person_w, text='Save person', command=lambda entry_list=entries: self.save_person(entry_list, new_person_w))
        create_new_person_btn.grid(row=1,column=3,padx=10)
        pass
    def save_person(self,parametrs_obj:list, new_person_w):
        person_parametrs=[]
        person_dict={'id':len(self.readToList())+1}
        for obj in parametrs_obj:
            person_parametr=obj.get()
            person_parametrs.append(person_parametr)
        for parametr in person_parametrs:
            person_dict[self.key_list[person_parametrs.index(parametr)+1]]=parametr
        print(person_dict)
        self.saving(person_dict, new_person_w)

        return person_dict
    def saving(self, save_data, new_person_w):
        if type(save_data)==dict:
            new_data=[]
            for i in save_data.values():
                new_data.append(i)
            save_data=new_data.copy()
        ask_box=messagebox.askyesnocancel(title='How to save',message='Do you want to save in current file?')
        if ask_box==True: self.save_in_current_file(save_data)
        elif ask_box==False: self.save_in_other_file(save_data)
        new_person_w.destroy()

        pass
    def save_in_current_file(self, save_data):
        with open (self.main_file, 'a') as mf:
            mf.write('\n')
            for i in save_data[0:-1]:
                mf.write(str(i)+self.separator)

            for i in save_data[-1]:
                mf.write(i)

        pass
    def save_in_other_file(self, save_data):
        filetypes = (     
        ("CSV files", "*.csv"),
            )
        file_name = askopenfilename(
        title="Select file to write",
        filetypes=filetypes

    )
        with open (file_name, 'a') as mf:
            mf.write('\n')
            for i in save_data[0:-1]:
                mf.write(str(i)+self.separator)

            for i in save_data[-1]:
                mf.write(i)

        messagebox.showinfo(title='Show_info', message=f'Saved in {file_name}')
        pass
    def view_file_data(self):
        self.root_w.grid_columnconfigure(0, weight=0)
        self.root_w.grid_columnconfigure(1, weight=1)
        self.root_w.grid_rowconfigure(1, weight=1)
        self.root_w.grid_rowconfigure(2, weight=1)
        self.root_w.grid_rowconfigure(3, weight=1)
        data_list=self.readToList()
        scrollbar = Scrollbar()
        scrollbar.grid(row=0, column=2)
        listbox = Listbox(yscrollcommand=scrollbar.set, selectmode=SINGLE)

        listbox.bind("<<ListboxSelect>>", self.on_select_function)
        listbox.bind("<Return>", self.choose_person)
        listbox.grid(row=0, column=1,rowspan=10,padx=10, columnspan=3, sticky=(N,S,W,E))
        scrollbar.config(command= listbox.yview)
        for row in data_list:
            listbox.insert(END, row)
        pass
    def on_select_function(self, event):
        for i in event.widget.curselection() :
            print (event.widget.get(i))
        pass
    def choose_person(self, event):
        for i in event.widget.curselection() :
            person_list= event.widget.get(i)
        person_dict={}
        for val in person_list:

                person_dict[self.key_list[person_list.index(val)]] = val
        

        self.create_person_wind(person_dict)
    def create_person_wind(self, person_dict:dict):
        person_wind=Toplevel()
        person_wind.geometry('500x700')
        k_row=0
        k_column=0
        v_row=0
        v_column=1
        for k,v in person_dict.items():
            key_lab=Label(person_wind,text=f'{k}: ')
            val_lab=Label(person_wind,text=v)
            key_lab.grid(row=k_row, column=k_column, sticky='w')
            val_lab.grid(row=v_row, column=v_column, sticky='w')
            k_column+=2
            v_column+=2
            if k_column>=4:
                k_row+=1
                v_row+=1
                k_column=0
                v_column=1
        edit_btn=Button(person_wind,text="Edit person", command=lambda person=person_dict: self.edit_person(person, person_wind))
        edit_btn.grid(column=0, row=k_row+1, padx=10)
            

        pass
    def edit_person(self, person_dict:dict, person_wind):
        edit_person_w=Toplevel()
        edit_person_w.geometry('700x700')
        k_row=0
        k_column=0
        v_row=0
        v_column=1
        enteries=[]
        for k,v in person_dict.items():
            key_lab=Label(edit_person_w,text=f'{k}: ')
            val_ent=Entry(edit_person_w)
            enteries.append(val_ent)
            val_ent.insert(0,v)
            key_lab.grid(row=k_row, column=k_column, sticky='w')
            val_ent.grid(row=v_row, column=v_column, sticky='w')
            k_column+=2
            v_column+=2
            if k_column>=4:
                k_row+=1
                v_row+=1
                k_column=0
                v_column=1
        
        edit_btn=Button(edit_person_w,text="Save", command=lambda person_list=enteries: self.save_to_file(person_list, edit_person_w))
        edit_btn.grid(column=0, row=k_row+1, padx=10) 
        person_wind.destroy()
    def save_to_file(self, person_list:list,edit_person_w):
        header_data=[]
        person_data=[]
        save_data=[]
        all_persons_list=self.readToList()
        for key in self.key_list:
            header_data.append(key)
        # save_data.append(header_data)
        
        for person in all_persons_list:
            save_data.append(person)
        
        for i in person_list:
            person_data.append(i.get())
        id_person=int(person_data[0])-1
        print(id_person)
        print
        save_data[id_person]=person_data
        with open(self.main_file, 'w') as mf:
            for i in header_data[0:-1]:
                mf.write(str(i)+self.separator)
            for i in header_data[-1]:
                mf.write(str(i))
        for i in save_data:
            self.save_in_current_file(i)
        messagebox.showinfo(message=f'Saved in {self.main_file}')
        edit_person_w.destroy()

    pass
