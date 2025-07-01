from tkinter import *
from tkinter import ttk, filedialog
import pandas as pd

class Main_Window(Frame):
    def select_base(self):
        local = filedialog.askopenfilename(title='Selecione um arquivo')
        self.op_base.set(local) 
        self.btn_load['state'] = 'normal'

    def load_data(self):
        self.btn_load['state'] = 'disabled'

        self.df = pd.read_csv(self.op_base.get(), encoding='latin1', sep=',', decimal='.')
        self.colunas = self.df.columns.values.tolist()

        self.df['Order Date Converted'] = pd.to_datetime(self.df['Order Date'], format='mixed')
        self.df['Year'] = self.df['Order Date Converted'].dt.year
        self.df['Moth'] = self.df['Order Date Converted'].dt.month
        self.df['Day'] = self.df['Order Date Converted'].dt.day
        self.data_interface()


    def data_interface(self):
        filtros = ['Segment', 'City', 'State', 'Category']
        map_filt = dict()
        for tipo in filtros: map_filt[tipo] = sorted(pd.unique(self.df[tipo]).tolist())

        lbf_select_data = LabelFrame(self.master, text='Filtrar dados', font=self.font_1b)
        lbf_select_data.grid(row=1, column=0, sticky='NEWS', padx=10, pady=10)

        self.ent_fdata = [StringVar() for _ in filtros]
        for i in range(len(filtros)):
            Label(lbf_select_data, text=filtros[i], font=self.font_1).grid(row=i,column=0, sticky='WS', pady=10, padx=10)
            ttk.Combobox(lbf_select_data, textvariable=self.ent_fdata[i], values=map_filt[filtros[i]], font=self.font_1,  width=53).grid(row=i, column=1, pady=10, sticky='NEWS', padx=10)
    
    
        

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, master=None, bg='white')
        self.master.title("Super Store - Tkinter Version")
        self.master.geometry("1200x800+100+120")
        self.master.resizable(False, False)

        self.font_1 = 'Arial 10'
        self.font_1b = 'Arial 10 bold'

        lbf_load_data = LabelFrame(self.master, text='Carregar dados', font=self.font_1b)
        lbf_load_data.grid(row=0, column=0, sticky='NEWS', padx=10, pady=10)

        self.op_base = StringVar(value=r'F:\Projetos\Programação\SuperStore_study\docs\train.csv')
        Label(lbf_load_data, text='Local:', font=self.font_1).grid(row=0, column=0, sticky='WS', padx=10)
        Entry(lbf_load_data, textvariable=self.op_base, font=self.font_1, width=45, state='readonly').grid(row=1, column=0, sticky='NEWS', padx=10)
        Button(lbf_load_data, text='Selecionar Arquivo', fg='white', bg='Blue', font=self.font_1b, command=self.select_base).grid(row=1, column=1, sticky='NEWS', padx=10)
        self.btn_load = Button(lbf_load_data, text='Carregar', fg='white', bg='Blue', font=self.font_1b, command=self.load_data) #, state='disabled')
        self.btn_load.grid(row=2, column=0, columnspan=2, sticky='NEWS', padx=10, pady=10)
       




if __name__ == '__main__':
    mainwindow = Main_Window()
    mainwindow.mainloop()

