from tkinter import * 
import tkinter.ttk as ttk
from typing import Dict,Any

class DynamicFieldsFrame(ttk.LabelFrame):
    def __init__(self,root: Tk, parent: ttk.Frame):
        super().__init__(parent, text="Author(s)")

        #root window
        self.root = root

        #authors
        self.authors: Dict[str,Any] = []

        #allow addition of author as a person
        create_author_person_button: ttk.Button = ttk.Button(self,text="Add Person",command=self._create_author_person)
        create_author_person_button.grid(row=0,column=0,sticky=W)

        #allow additiong of author as an organisation
        create_author_org_button: ttk.Button = ttk.Button(self,text="Add Org",command=self._create_author_org)
        create_author_org_button.grid(row=0,column=1,sticky=W)

        #have a listbox to specify the creation
        self.author_listbox: Listbox = Listbox(self,selectmode=EXTENDED)
        scrollbar_y: Scrollbar = Scrollbar(self,command=self.author_listbox.yview)
        scrollbar_x: Scrollbar = Scrollbar(self,command=self.author_listbox.xview,orient=HORIZONTAL)
        self.author_listbox.config(yscrollcommand=scrollbar_y.set,xscrollcommand=scrollbar_x)
        scrollbar_y.config(command=self.author_listbox.yview)
        scrollbar_x.config(command=self.author_listbox.xview)

        self.author_listbox.grid(row=1,column=0,columnspan=2,sticky=(N,S))
        scrollbar_x.grid(row=2,column=0,columnspan=2,sticky=(W,E))
        scrollbar_y.grid(row=1,column=2,sticky=(N,S))

        #add a delete button
        delete_button = ttk.Button(self,text="Delete",command=self._delete_selected_author)
        delete_button.grid(row=3,column=1)

    def _create_author_person(self) -> None:
        new_window = Toplevel(self.root)
        new_window.title("Specify Author Information") 
        new_window.grid_rowconfigure(0,weight=1)
        new_window.grid_columnconfigure(0,weight=1)

        content_frame = ttk.Frame(new_window,padding=20)
        content_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        content_frame.grid_rowconfigure(0,weight=1)
        content_frame.grid_columnconfigure(0,weight=1)

        title_label = ttk.Label(content_frame,text="Add Person Info")
        title_label.grid(row=0,column=0)

        ####### Mandatory Info
        mandatory_frame = ttk.Labelframe(content_frame,text="Mandatory Info")
        mandatory_frame.grid(column=0,row=1,sticky=(N,W,E,S))

        #ask for given name
        given_name_label = ttk.Label(mandatory_frame,text="Given Name: ")
        given_name_label.grid(row=1,column=0)
        given_name = StringVar()
        given_name_entry = ttk.Entry(mandatory_frame,textvariable=given_name)
        given_name_entry.grid(row=1,column=1)

        #ask for last name
        last_name_label = ttk.Label(mandatory_frame,text="Last Name: ")
        last_name_label.grid(row=2,column=0)
        last_name = StringVar()
        last_name_entry = ttk.Entry(mandatory_frame,textvariable=last_name)
        last_name_entry.grid(row=2,column=1)

        #########Optional
        #optional arguments: ORCID and affiliations
        optional_frame = ttk.Labelframe(content_frame,text="Optional")
        optional_frame.grid(column=0,row=2,sticky=(N,W,E,S))
        
        affiliation_label = ttk.Label(optional_frame,text="Affiliation(s): ")
        affiliation_label.grid(row=3,column=0)
        affiliation = StringVar()
        affiliation_entry = ttk.Entry(optional_frame,textvariable=affiliation)
        affiliation_entry.grid(row=3,column=1)

        id_type = StringVar()
        id_type_combobox = ttk.Combobox(optional_frame,
                                        textvariable=id_type,
                                        values=('ORCID',),
                                        state="readonly")
        id_type_combobox.grid(row=4,column=0)
        new_window.after(1, lambda: id_type_combobox.current(0))
        id = StringVar()
        id_entry = ttk.Entry(optional_frame,textvariable=id)
        id_entry.grid(row=4,column=1)

        author_data = {}
        def submit_author_info():
            author_data['type'] = 'personal'
            author_data['given_name'] = given_name_entry.get()
            author_data['last_name'] = last_name.get()
            author_data['name'] = f"{author_data['given_name']} {author_data['last_name']}"
            author_data['affiliation'] = affiliation_entry.get()
            author_data['id_type'] = id_type.get()
            author_data['id'] = id_entry.get()

            print("Author Data: ", author_data)

            self.authors.append(author_data)
            self.author_listbox.insert(END,f"{author_data['name']}")
            
            new_window.destroy()

        submit_button = ttk.Button(content_frame,text="Submit",command=submit_author_info)
        submit_button.grid(row=10,column=0,pady=10)

    def _create_author_org(self) -> None:
        new_window = Toplevel(self.root)
        new_window.title("Specify Author Information") 
        new_window.grid_rowconfigure(0,weight=1)
        new_window.grid_columnconfigure(0,weight=1)

        content_frame = ttk.Frame(new_window,padding=20)
        content_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        content_frame.grid_rowconfigure(0,weight=1)
        content_frame.grid_columnconfigure(0,weight=1)

        title_label = ttk.Label(content_frame,text="Add Organisation Info")
        title_label.grid(row=0,column=0)

        ####### Mandatory Info
        mandatory_frame = ttk.Labelframe(content_frame,text="Mandatory Info")
        mandatory_frame.grid(column=0,row=1,sticky=(N,W,E,S))

        #ask for org name
        name_label = ttk.Label(mandatory_frame,text="Name: ")
        name_label.grid(row=1,column=0)
        name = StringVar()
        name_entry = ttk.Entry(mandatory_frame,textvariable=name)
        name_entry.grid(row=1,column=1)

        #########Optional
        #optional arguments: ORCID and affiliations
        optional_frame = ttk.Labelframe(content_frame,text="Optional")
        optional_frame.grid(column=0,row=2,sticky=(N,W,E,S))
        
        affiliation_label = ttk.Label(optional_frame,text="Affiliation(s): ")
        affiliation_label.grid(row=3,column=0)
        affiliation = StringVar()
        affiliation_entry = ttk.Entry(optional_frame,textvariable=affiliation)
        affiliation_entry.grid(row=3,column=1)

        id_type = StringVar()
        id_type_combobox = ttk.Combobox(optional_frame,
                                        textvariable=id_type,
                                        values=('ORCID',),
                                        state="readonly")
        id_type_combobox.grid(row=4,column=0)
        new_window.after(1, lambda: id_type_combobox.current(0))
        id = StringVar()
        id_entry = ttk.Entry(optional_frame,textvariable=id)
        id_entry.grid(row=4,column=1)

        author_data = {}
        def submit_author_info():
            author_data['type'] = 'organizational'
            author_data['name'] = name.get()
            author_data['affiliation'] = affiliation_entry.get()
            author_data['id_type'] = id_type.get()
            author_data['id'] = id_entry.get()

            print("Author Data: ", author_data)

            self.authors.append(author_data)
            self.author_listbox.insert(END,f"{author_data['name']}")
            
            new_window.destroy()

        submit_button = ttk.Button(content_frame,text="Submit",command=submit_author_info)
        submit_button.grid(row=10,column=0,pady=10)

    def _delete_selected_author(self) -> None:
        selection_indices = self.author_listbox.curselection()
        if selection_indices:
            # 1. Get the items to delete *before* modifying the listbox
            items_to_delete = [self.author_listbox.get(index) for index in selection_indices]

            # 2. Delete from the listbox (reverse order to prevent issues with shifting indices)
            for index,item in zip(sorted(selection_indices, reverse=True),sorted(items_to_delete,reverse=True)):
                self.author_listbox.delete(index)

                #delete from self.authors using the index
                # self.authors should mirror same order as listbox
                try:
                    self.authors.pop(index)
                except ValueError:
                    print(f"Warning: Item '{item}' not found in self.authors")  # Handle potential mismatch

        print(self.authors)

    @property
    def author_list(self) -> Dict[str,Any]:
        return self.authors