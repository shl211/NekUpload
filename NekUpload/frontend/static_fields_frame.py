from tkinter import * 
import tkinter.ttk as ttk
from datetime import date

class StaticFieldsFrame(ttk.LabelFrame):
    def __init__(self,parent: ttk.Frame):
        super().__init__(parent, text="Basic Info")
        
        self._is_read_user_guide: StringVar = StringVar()
        self._api_key_env_var: StringVar = StringVar()
        self._host_name: StringVar = StringVar()
        self._community_slug: StringVar = StringVar()
        self._title: StringVar = StringVar()
        self._publication_date: StringVar = StringVar()

        #tick box to serve as reminder for user to set host name environment variable
        read_user_info_check: ttk.Checkbutton = ttk.Checkbutton(self,text="Have you read User Guide for setting up environment variables?",
                                       command=None,variable=self._is_read_user_guide,
                                       onvalue="True",offvalue="False")
        read_user_info_check.grid(row=0,column=0,sticky=W,padx=5,pady=.5)

        #ask user for what the environment variables are for the api key
        api_key_env_label = ttk.Label(self,text="Environment Variable for API Key: ")
        api_key_env_label.grid(row=1,column=0,sticky=W,padx=5,pady=.5)
        api_key_entry = ttk.Entry(self,textvariable=self._api_key_env_var)
        api_key_entry.grid(row=1,column=1,sticky=E,padx=5,pady=.5)

        #ask user for host name
        host_label = ttk.Label(self,text="Host Name URL: ")
        host_label.grid(row=2,column=0,sticky=W,padx=5,pady=.5)
        host_name_entry = ttk.Entry(self,textvariable=self._host_name)
        host_name_entry.grid(row=2,column=1,sticky=E,padx=5,pady=.5)

        #ask user for community url slug
        community_label = ttk.Label(self,text="Community (URL slug or UUID): ")
        community_label.grid(row=3,column=0,sticky=W,padx=5,pady=.5)
        community_entry = ttk.Entry(self,textvariable=self._community_slug)
        community_entry.grid(row=3,column=1,sticky=E,padx=5,pady=.5)

        #ask for title of the dataset
        title_label: ttk.Label = ttk.Label(self, text="Title: ")
        title_label.grid(row=4, column=0, sticky=W, padx=5, pady=.5)
        title_widget: ttk.Entry = ttk.Entry(self, textvariable=self._title) 
        title_widget.grid(row=4, column=1, sticky=E, padx=5, pady=.5)

        #ask for publication date, pre-populate with current date
        publication_date_label: ttk.Label = ttk.Label(self, text="Publication Date: ") 
        publication_date_label.grid(row=5, column=0, sticky=W, padx=5, pady=.5)
        self._publication_date.set(self._get_current_iso8601_date())  
        publication_date_widget: ttk.Entry = ttk.Entry(self, textvariable=self._publication_date) 
        publication_date_widget.grid(row=5, column=1, sticky=E, padx=5, pady=.5)
    @property
    def is_read_user_guide(self):
        return self._is_read_user_guide.get()

    @is_read_user_guide.setter
    def is_read_user_guide(self, value: str):
        self._is_read_user_guide.set(value)

    @property
    def api_key_env_var(self):
        return self._api_key_env_var.get()

    @api_key_env_var.setter
    def api_key_env_var(self, value: str):
        self._api_key_env_var.set(value)

    @property
    def host_name(self):
        return self._host_name.get()

    @host_name.setter
    def host_name(self, value: str):
        self._host_name.set(value)

    @property
    def community_slug(self):
        return self._community_slug.get()

    @community_slug.setter
    def community_slug(self, value: str):
        self._community_slug.set(value)

    @property
    def title(self):
        return self._title.get()

    @title.setter
    def title(self, value: str):
        self._title.set(value)

    @property
    def publication_date(self):
        return self._publication_date.get()

    @publication_date.setter
    def publication_date(self, value: str):
        self._publication_date.set(value)

    def _get_current_iso8601_date(self) -> str:
        today: date = date.today() 
        return today.isoformat()
