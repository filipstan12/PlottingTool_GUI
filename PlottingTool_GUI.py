import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from scipy.optimize import curve_fit, brentq
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
import io

class GUI_interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Plotting Tool')
        self.resizable(True, True)
        self.geometry('800x520')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.count = 0

        #variables and data
        self.var = tk.Variable(value=('CH1', 'CH2'))
        self.signal = ['NTC-CH1', 'NTC-CH1', 'NTC-CH1', 'NTC-CH1']
        self.filter = np.array([0, 0])
        self.data_list = []

        #Buttons
        self.f0 = tk.Frame(self, borderwidth=1)
        self.f0.grid(column=0, row=0, padx=10, pady=10)
        self.open_button = ttk.Button(self.f0, text='Open a File', command=self.select_file)
        self.open_button.pack(side='left')



        #########Buttons for each channel########

        # for i in range(2):
        #     self.f1 = tk.Frame(self, borderwidth=1, relief='solid')
        #     self.f1.grid(column=0, row=i + 1, padx=5, pady=5)
        #     self.Data_Label1[i] = tk.Label(self.f1, text=('         {}         '.format(str(i + 1))))
        #     self.listbox1[i] = tk.Listbox(self.f1, listvariable=self.var, height=2, selectmode=tk.EXTENDED, width=10)
        #     self.Filt_Label1[i] = tk.Label(self.f1, text='Filter:', width=10)
        #     self.Filt_Entry1[i] = tk.Entry(self.f1, width=10)
        #     self.Data_Label1[i].pack(side='left')
        #     self.listbox1[i].pack(side='left')
        #     self.Filt_Label1[i].pack(side='left')
        #     self.Filt_Entry1[i].pack(side='left')

        self.f1 = tk.Frame(self, borderwidth=1, relief='solid')
        self.f1.grid(column=0, row=1, padx=5, pady=5)
        self.Data_Label1 = tk.Label(self.f1, text=('         {}         '.format(str(1))))
        self.listbox1 = tk.Listbox(self.f1, listvariable=self.var, height=2, selectmode=tk.EXTENDED, width=10)
        self.Filt_Label1 = tk.Label(self.f1, text='Filter:', width = 10)
        self.Filt_Entry1 = tk.Entry(self.f1, width = 10)
        self.Data_Label1.pack(side='left')
        self.listbox1.pack(side='left')
        self.Filt_Label1.pack(side='left')
        self.Filt_Entry1.pack(side='left')

        #Second File#
        self.f2 = tk.Frame(self, borderwidth=1, relief='solid')
        self.f2.grid(column=0, row=2, padx=5, pady=5)
        self.Data_Label2 = tk.Label(self.f2, text=('         {}         '.format(str(2))))
        self.listbox2 = tk.Listbox(self.f2, listvariable=self.var, height=2, selectmode=tk.EXTENDED, width=10)
        self.Filt_Label2 = tk.Label(self.f2, text='Filter:', width = 10)
        self.Filt_Entry2 = tk.Entry(self.f2, width = 10)
        self.Data_Label2.pack(side='left')
        self.listbox2.pack(side='left')
        self.Filt_Label2.pack(side='left')
        self.Filt_Entry2.pack(side='left')
        #self.plotButton.pack(side='left')

        #Plot button#
        self.f2 = tk.Frame(self, borderwidth=1)
        self.f2.grid(column=0, row=5, padx=10, pady=10)
        self.applyfilt = tk.Button(self.f2, width=5, command=self.applyfilter, text='apply')
        self.plotButton = ttk.Button(self.f2, text='Plot', command=self.plot, width=10)
        self.applyfilt.pack(side='left')
        self.plotButton.pack(side='left')

        #Text-Button#
        self.Print_filename = tk.Text(self, height=10, width=40, relief="solid")
        self.Print_filename.grid(column=0, row=6)

    def select_file(self):
        data_list = []

        filetypes = (('csv files', '*.dat'), ('All files', '*.*'))
        filenames = fd.askopenfilenames(title='Open a file', initialdir='/', filetypes=filetypes)
        filenames_list = self.splitlist(filenames)


        if filenames == "":
            self.Print_filename.insert('1.0', " \n Error: NO FILE LOADED")
        else:
            for i in filenames_list:
                list = []
                Cy5 = []
                Fam = []
                Time = []

                file = io.open(i, 'r', encoding='utf-16-le')

                for n, lines in enumerate(file):
                    list.append(lines.split())
                    if "TIME[sec.]" in lines:
                        cutoff = n + 2

                # code to extract the channel values into list elements with float values in them
                for n, line in enumerate(list[cutoff:]):
                    # make sure that list elements really have TRUE values in them, poor coding
                    if len(line) < 10:
                        line = list[n - 1]

                    Fam.append(float(line[4].replace(',', '.')))
                    Cy5.append(float(line[12].replace(',', '.')))
                    Time.append(float(line[0].replace(',', '.')))

                df = pd.DataFrame({'TIME[sec.]': Time, 'NTC-FAM': Fam, 'NTC-CY5': Cy5})
                data_list.append(df)

                self.Print_filename.insert('1.0', i + " was loaded ... \n\n")
        self.data_list = data_list
        return

    def applyfilter(self):
        entries = [self.Filt_Entry1.get(), self.Filt_Entry2.get()]

        for i in entries:
            if i == '':
                self.filter = [0, 0]
            else:
                self.filter[0] = int(self.Filt_Entry1.get())
                self.filter[1] = int(self.Filt_Entry2.get())

        print(self.data_list)

        for i, val in enumerate(self.data_list):
            window_size = self.filter[i]
            time_vector = val[1]
            print(time_vector)

        self.Print_filename.insert('1.0', "The new fitler vector is {} \n".format(self.filter))

    def plot(self):
        window_size = self.Filter
        diff = np.diff(self.imp_ydata)
        diff[0] = 0
        sum = 0
        suma = []
        for i in diff:
            sum = sum + i
            suma.append(sum)
        suma[0] = 0
        sum_array = np.array(suma)
        # print(sum_array)
        a2 = np.power(sum_array, 2)
        window = np.ones(window_size) / float(window_size)
        self.ydata = np.sqrt(np.convolve(a2, window, 'valid'))
        parameters, covvar = curve_fit(self.polynomial_fit, self.xdata[0:len(self.ydata)], self.ydata)
        self.fitted = self.polynomial_fit(self.xdata, parameters[0], parameters[1], parameters[2], parameters[3])
        self.find_turningpoint()
        self.plotting_fun()
        self.Print_filename.insert('1.0', " \n RMS-Filter applied \n")

        return

if __name__ == "__main__":
    app = GUI_interface()
    app.mainloop()