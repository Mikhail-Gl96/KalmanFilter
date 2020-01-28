import numpy as np
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.mplot3d import Axes3D

import ParseFiles
import math
import WhiteNoise
import MathModel as mModel

colors_graph = ['red', 'blue', 'violet', 'green', 'black', 'brown', 'yellow', 'orange']


def make_graph(title, data_time, data_DATA, colors, labels):
    """Функция создает на выходе график с кривыми
        на вход: название, массив[время графика 1, время графика 2, ...],
                           массив[информация график 1, итнформация график 2, ...], цвета графиков, названия кривых"""
    plt.cla()
    plt.title(title)
    data_number = len(data_DATA)
    for i in range(data_number):
        plt.plot(data_time[i], data_DATA[i], color=colors[i], label=labels[i])
    plt.legend()
    plt.grid()
    plt.xlabel("Time")
    plt.ylabel('Data')
    plt.show()


example1 = ParseFiles.File()        # Создаем экземпляр с названием example1
example1.openFile()                 # Открываем и читаем файлы
example1.analyzeColumns()           # Собираем информацию в переменные

time_bins = example1.get_BINS_UTC()                         # Вытащили все время по БИНС
time_bins = example1.give_active_bins_data_sync(time_bins)  # Получаем кусок времени, синхронизированный с часами И21

time_ins = example1.get_INS_I21_UTC()                           # Вытащили все время по ИНС
time_ins = example1.give_active_ins_data_sync_time(time_ins)    # Получаем кусок времени, синхронизированный с часами БИНС

v_e_bins = example1.get_BINS_VE()                           # Вытаскиваем V east из всего массива БИНС
v_e_bins = example1.give_active_bins_data_sync(v_e_bins)    # Получаем кусок данных, синхронизированный по времени

v_e_ins = example1.get_INS_I21_VE()                         # Вытаскиваем V east из всего массива ИНС
v_e_ins = example1.give_active_ins_data_sync(v_e_ins)       # Получаем кусок данных, синхронизированный по времени

v_n_bins = example1.get_BINS_VN()                           # Вытаскиваем V north из всего массива БИНС
v_n_bins = example1.give_active_bins_data_sync(v_n_bins)    # Получаем кусок данных, синхронизированный по времени

v_n_ins = example1.get_INS_I21_VN()                         # Вытаскиваем V north из всего массива ИНС
v_n_ins = example1.give_active_ins_data_sync(v_n_ins)       # Получаем кусок данных, синхронизированный по времени

# ___________________________________________
delta_v_east = -v_e_bins + v_e_ins                          # Разница в скоростях EAST
delta_v_north = -v_n_bins + v_n_ins                         # Разница в скоростях NORTH

#Получаем -1 элемент до начала синхронизированного ряда V East
null_delta_v_east = -example1.give_BINS_V_E_null_data(v_e_bins) + example1.give_INS_V_E_null_data(v_e_ins)
# Получаем -1 элемент до начала синхронизированного ряда V North
null_delta_v_north = -example1.give_BINS_V_N_null_data(v_n_bins) + example1.give_INS_V_N_null_data(v_n_ins)
# ___________________________________________


bins_heading = example1.get_BINS_Heading()
bins_heading = example1.give_active_bins_data_sync(bins_heading)

ins_heading = example1.get_INS_I21_Heading()
ins_heading = example1.give_active_ins_data_sync(ins_heading)

bins_roll = example1.get_BINS_Roll()
bins_roll = example1.give_active_bins_data_sync(bins_roll)

ins_roll = example1.get_INS_I21_Roll()
ins_roll = example1.give_active_ins_data_sync(ins_roll)

bins_pitch = example1.get_BINS_Pitch()
bins_pitch = example1.give_active_bins_data_sync(bins_pitch)

ins_pitch = example1.get_INS_I21_Pitch()
ins_pitch = example1.give_active_ins_data_sync(ins_pitch)

# ___________________________________________
delta_heading = bins_heading - ins_heading
delta_roll = bins_roll - ins_roll
delta_pitch = bins_pitch - ins_pitch
# ___________________________________________

# Выводим графики до фильтра
# make_graph('V_east', [time_bins, time_ins, time_bins], [v_e_bins, v_e_ins, delta_v_east],
#            colors_graph, ['BINS', 'INS', 'delta'])
# make_graph('V_north', [time_bins, time_ins, time_bins], [v_n_bins, v_n_ins, delta_v_north],
#            colors_graph, ['BINS', 'INS', 'delta'])
# make_graph("heading", [time_bins, time_ins, time_bins], [bins_heading, ins_heading, delta_heading],
#            colors_graph, ['BINS', 'INS', 'delta'])
# make_graph("roll", [time_bins, time_ins, time_bins], [bins_roll, ins_roll, delta_roll],
#            colors_graph, ['BINS', 'INS', 'delta'])
# make_graph("pitch", [time_bins, time_ins, time_bins], [bins_pitch, ins_pitch, delta_pitch],
#            colors_graph, ['BINS', 'INS', 'delta'])
# Конец вывода графиков до фильтра

arr_acc_e = []
arr_acc_n = []
arr_dot_F_East = []
arr_dot_F_North = []

samples_number = len(time_bins)
# Создали экземпляр мат модели и передали в него кол-во элемнтов равное кол-ву измерений в БИНС
example1_model = mModel.MathModel(samples_number)
# Начинаем идти по шагам

print(null_delta_v_north, null_delta_v_east)

for i in range(samples_number):
    if i == 0:      # Если первый шаг
        # Передали в экземпляр начальные значения
        example1_model.activate_start_values(null_delta_v_east, delta_v_east[0],
                                             null_delta_v_north, delta_v_north[0])
        # print(f'current_step = {example1_model.current_step}  '
        #       f'd_V_East = {example1_model.d_V_East}  '
        #       f'd_V_North = {example1_model.d_V_North}  '
        #       f'Acc_East = {example1_model.Acc_East}  '
        #       f'Acc_North = {example1_model.Acc_North}  ')
        example1_model.solve_SystemEquations()  # Решение уравнений мат модели ошибок

        arr_acc_e.append(example1_model.Acc_East)
        arr_acc_n.append(example1_model.Acc_North)
        arr_dot_F_East.append(example1_model.dot_F_East)
        arr_dot_F_North.append(example1_model.dot_F_North)
    else:
        # Подаем новые значения по шагу
        example1_model.new_step_data_input(delta_v_east[i], delta_v_north[i])
        # print(f'current_step = {example1_model.current_step}  '
        #       f'd_V_East = {example1_model.d_V_East}  '
        #       f'd_V_North = {example1_model.d_V_North}  '
        #       f'Acc_East = {example1_model.Acc_East}  '
        #       f'Acc_North = {example1_model.Acc_North}  ')
        example1_model.solve_SystemEquations()  # Решение уравнений мат модели ошибок

        arr_acc_e.append(example1_model.Acc_East)
        arr_acc_n.append(example1_model.Acc_North)
        arr_dot_F_East.append(example1_model.dot_F_East)
        arr_dot_F_North.append(example1_model.dot_F_North)

make_graph('Acc_east', [time_bins], [arr_acc_e],
           colors_graph, [''])
make_graph('Acc_north', [time_bins], [arr_acc_n],
           colors_graph, [''])

make_graph('dot_F_East', [time_bins], [arr_dot_F_East],
           colors_graph, [''])
make_graph('dot_F_North', [time_bins], [arr_dot_F_North],
           colors_graph, [''])









