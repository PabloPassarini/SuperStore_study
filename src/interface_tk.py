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
        self.ml_interface()


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
    
    def ml_interface(self):
        self.lbf_mkl_param = LabelFrame(self.master, text='Parâmetros do Modelo', font=self.font_1b)
        self.lbf_mkl_param.grid(row=2, column=0, sticky='NEWS', padx=10, pady=10)

        models = ['Random Forest', 'Neural Network']
        self.model_type = StringVar(value='Random Forest')
        self.model_type_ant = 'Neural Network'
        Label(self.lbf_mkl_param, text='Model:', font=self.font_1).grid(row=0, column=0, sticky='NEWS', padx=10, pady=10)
        ttk.Combobox(self.lbf_mkl_param, textvariable=self.model_type, values=models, font=self.font_1, width=30).grid(row=0, column=1, padx=10, pady=10, sticky='NEWS')
        
        hp_param = {'Param 1': [1, 2, 3], 'Param 2': [1, 2, 3], 'Param 3': [1, 2, 3], 'Param 4': [1, 2, 3], 'Param 5': [1, 2, 3], 'Param 6': [1, 2, 3]}
        linha, coluna, cont = 1, 0, 0
        self.elementos = list()
        self.cb_values = [StringVar() for _ in range(len(hp_param))]
        for key, val in hp_param.items():
            if coluna == 2:
                coluna = 0
                linha += 2
            lb = Label(self.lbf_mkl_param, text=key, font=self.font_1)
            lb.grid(row=linha, column=coluna, sticky='NEWS', padx=10)
            cb = ttk.Combobox(self.lbf_mkl_param, textvariable=self.cb_values[cont], values=val, font=self.font_1, width=30)
            cb.grid(row=linha+1, column=coluna, padx=10, pady=10, sticky='NEWS')
            self.elementos.append([lb, cb])

            coluna += 1
            cont +=1  
        self.refresh()


    def hyper_param(self):
        if self.model_type.get() == 'Random Forest':
            hp_rf_param = {'n_estimators': [100, 200, 300], 'max_depth': [None, 10, 20, 30], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4], 'max_features': ['auto', 'sqrt', 'log2'], 'bootstrap': [True, False]}
            cont = 0
            for key, val in hp_rf_param.items():
                self.elementos[cont][0]['text'] = key
                self.elementos[cont][1]['values'] = val
                self.cb_values[cont].set('- None -') 
                cont +=1        
        else:
            hp_rn_param = {'loss': ['squared_error', 'poisson'], 'activation': ['identity', 'logistic', 'tanh', 'relu'], 'solver': ['lbfgs', 'sgd', 'adam'], 'learning_rate': ['constant', 'invscaling', 'adaptive'], 'learning_rate_init': [0.1, 0.01, 0.001, 0.0001], 'n_layers': [i for i in range(1,31)]}
            cont = 0
            for key, val in hp_rn_param.items():
                self.elementos[cont][0]['text'] = key
                self.elementos[cont][1]['values'] = val
                self.cb_values[cont].set('- None -') 
                cont +=1   
    
    def refresh(self):
        if self.model_type.get() != self.model_type_ant:
            self.model_type_ant = self.model_type.get()
            self.hyper_param()



        self.after(250, self.refresh)


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

