import numpy as np
import random

import WhiteNoise as wN


class MathModel:
    def __init__(self, data_len=459400):
        # --------------------------   Константы   --------------------------
        self.gravity = 9.81                             # гравитация
        self.w_Noise = self.white_Noise(0, 1, data_len)     # Белый шум

        # --------------------------   Массивы с данными   --------------------------
        # self.data_all_Bins = data_array             # Все параметры БИНС из файла

        self.data_input_every_step_saving = []      # Тут храним все входные данные, которые подавали на вход мат модели
        self.data_output_every_step_saving = []     # Тут храним все выходные данные мат модели

        # --------------------------   переменные   --------------------------
        self.current_step = 0                       # номер шага

            # -----------   Эти переменные подаем на вход нашей мат модели на каждом шагу   -----------
        # self.current_step_input_BINS_V_East = None                   # Линейная скорость по западному каналу с БИНС
        # self.current_step_input_BINS_V_North = None                  # Линейная скорость по северному каналу с БИНС
        # self.current_step_input_delta_V_North = None            # Разность линейных скоростей БИНС и ИНС северное направление
        # self.current_step_input_delta_V_East = None             # Разность линейных скоростей БИНС и ИНС западное направление

            # -----------   Эти переменные будут выходить из мат модели на каждом шагу  -----------
        # self.current_step_output_Heading = None                 # Курс мат модели
        # self.current_step_output_Roll = None                    # Крен мат модели
        # self.current_step_output_Pitch = None                   # Тангаж мат модели

            # -----------   Эти переменные из ИНС для мат модели на каждом шагу   -----------
        # self.current_step_input_INS_V_East = None
        # self.current_step_input_INS_V_North = None

        # --------------------------   ???   --------------------------

        self.T = 0.01               # Время в сек на одно снятие
        self.H = 1.0                # ??????????????????????
        self.fi = 1.0               # ??????????????????????
        self.betta = 1.0            # ??????????????????????  период как касательная к дисперсии
        self.A = 1.0                # ??????????????????????  Дисперсия

        self.Radius = 1.0           # ?????????????????????? радиус чего

        self.V_East_delta_prev = None             # Значение скорости по EAST на предыдущем шаге
        self.V_North_delta_prev = None            # Значение скорости по NORTH на предыдущем шаге

        self.Acc_East = None             # Значение ускорения по EAST на текущем шаге
        self.Acc_North = None            # Значение ускорения по NORTH на текущем шаге

        # --------------------------   Значения, изменяемые на каждом шаге   --------------------------
        self.d_V_East = None        # Значение скорости по EAST на текущем шаге
        self.d_V_North = None       # Значение скорости по NORTH на текущем шаге

        self.F_East = None          # Значения F по EAST на текущем шаге    ??????
        self.F_North = None         # Значения F по NORTH на текущем шаге   ??????
        self.F_Up = None            # Значения F по Up на текущем шаге      ??????

        self.W_xB_dr = None         # Значения W дрейфа по xb на текущем шаге   ??????
        self.W_yB_dr = None         # Значения W дрейфа по yB на текущем шаге   ??????
        self.W_Up_dr = None         # Значения W дрейфа по Up на текущем шаге   ??????

        self.w_East_dr = None       # Значения W дрейфа по EAST на текущем шаге
        self.w_North_dr = None      # Значения W дрейфа по NORTH на текущем шаге
        # --------------------------   Значения,получаемые из мат модели   --------------------------
        self.dot_V_East = None      #
        self.dot_V_North = None     #

        self.dot_F_East = None      #
        self.dot_F_North = None     #
        self.dot_F_Up = None        #

        self.dot_w_xB_dr = None     #
        self.dot_w_yB_dr = None     #
        self.dot_w_Up_dr = None     #

        dtype_type = "float32"
        self.nonNumPy_matrix_F = None
        self.matrix_F = None
        self.nonNumPy_matrix_G = None
        self.matrix_G = None
        self.matrix_Q_value = None
        self.nonNumPy_matrix_Q = None
        self.matrix_Q = None
        self.matrix_R_value = None
        self.nonNumPy_matrix_R = None
        self.matrix_R = None
        self.matrix_P_value = None
        self.nonNumPy_matrix_P = None
        self.matrix_P = None

        # -----------------------------------------------------------------------------------

        # self.nonNumPy_matrix_F = [
        #     [1, 0, 0, -self.gravity * self.T, self.Acc_North * self.T, 0, 0, 0],
        #     [0, 1, self.gravity * self.T, 0, -self.Acc_East * self.T, 0, 0, 0],
        #     [0, -self.T * self.Radius, 1, 0, 0, self.T * np.cos(self.H), self.T * np.sin(self.H), 0],
        #     [self.T / self.Radius, 0, 0, 1, 0, -self.T * np.sin(self.H), self.T * np.cos(self.H), 0],
        #     [self.T * np.tan(self.Radius), 0, 0, 0, 1, 0, 0, self.T],
        #     [0, 0, 0, 0, 0, 1 - self.betta * self.T, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 1 - self.betta * self.T, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 1 - self.betta * self.T]
        # ]
        # self.matrix_F = np.array(self.nonNumPy_matrix_F, dtype=f"{dtype_type}")
        #
        # # -----------------------------------------------------------------------------------
        #
        # self.nonNumPy_matrix_G = [
        #     [1, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 1, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 1, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 1, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 1, 0, 0, 0],
        #     [0, 0, 0, 0, 0, self.A * np.sqrt(2 * self.betta * self.T), 0, 0],
        #     [0, 0, 0, 0, 0, 0, self.A * np.sqrt(2 * self.betta * self.T), 0],
        #     [0, 0, 0, 0, 0, 0, 0, self.A * np.sqrt(2 * self.betta * self.T)],
        # ]
        # self.matrix_G = np.array(self.nonNumPy_matrix_G, dtype=f"{dtype_type}")
        #
        # # -----------------------------------------------------------------------------------
        #
        # self.matrix_Q_value = np.array([self.d_V_East, self.d_V_North,
        #                                 self.F_East, self.F_North, self.F_Up,
        #                                 self.W_xB_dr, self.W_yB_dr, self.W_Up_dr],
        #                                dtype=f"{dtype_type}")
        # self.nonNumPy_matrix_Q = [
        #     [self.matrix_Q_value[0], 0, 0, 0, 0, 0, 0, 0],
        #     [0, self.matrix_Q_value[1], 0, 0, 0, 0, 0, 0],
        #     [0, 0, self.matrix_Q_value[2], 0, 0, 0, 0, 0],
        #     [0, 0, 0, self.matrix_Q_value[3], 0, 0, 0, 0],
        #     [0, 0, 0, 0, self.matrix_Q_value[4], 0, 0, 0],
        #     [0, 0, 0, 0, 0, self.matrix_Q_value[5], 0, 0],
        #     [0, 0, 0, 0, 0, 0, self.matrix_Q_value[6], 0],
        #     [0, 0, 0, 0, 0, 0, 0, self.matrix_Q_value[7]],
        # ]
        # self.matrix_Q = np.array(self.nonNumPy_matrix_Q, dtype=f"{dtype_type}")
        #
        # # -----------------------------------------------------------------------------------
        #
        # self.matrix_R_value = np.array([0, 0],
        #                                dtype=f"{dtype_type}")
        # self.nonNumPy_matrix_R = [
        #     [self.matrix_R_value[0], 0],
        #     [0, self.matrix_R_value[1]]
        # ]
        # self.matrix_R = np.array(self.nonNumPy_matrix_R, dtype=f"{dtype_type}")
        #
        # # -----------------------------------------------------------------------------------
        #
        # self.matrix_P_value = np.array([0, 0, 0,
        #                                 0, 0, 0,
        #                                 0, 0],
        #                                dtype=f"{dtype_type}")
        # self.nonNumPy_matrix_P = [
        #     [self.matrix_P_value[0], 0, 0, 0, 0, 0, 0, 0],
        #     [0, self.matrix_P_value[1], 0, 0, 0, 0, 0, 0],
        #     [0, 0, self.matrix_P_value[2], 0, 0, 0, 0, 0],
        #     [0, 0, 0, self.matrix_P_value[3], 0, 0, 0, 0],
        #     [0, 0, 0, 0, self.matrix_P_value[4], 0, 0, 0],
        #     [0, 0, 0, 0, 0, self.matrix_P_value[5], 0, 0],
        #     [0, 0, 0, 0, 0, 0, self.matrix_P_value[6], 0],
        #     [0, 0, 0, 0, 0, 0, 0, self.matrix_P_value[7]],
        # ]
        # self.matrix_P = np.array(self.nonNumPy_matrix_P, dtype=f"{dtype_type}")

        # -----------------------------------------------------------------------------------

    def white_Noise(self, start=0, end=1, number=1000):
        """Функция белого шума, создает сэмплы в кол-ве значения переменной number """
        wn = wN.WhiteNoise(start, end, number)
        wn.white_noise()
        samples = wn.getSamples()
        return samples

    def solve_SystemEquations(self):
        """Решение уравнений мат модели ошибок """
        self.dot_V_East = -self.gravity * self.F_North + self.Acc_North * self.F_Up + self.w_Noise[self.current_step]
        self.dot_V_North = -self.gravity * self.F_East + self.Acc_East * self.F_Up + self.w_Noise[self.current_step]

        self.dot_F_East = -self.d_V_North / self.Radius + self.w_East_dr + self.w_Noise[self.current_step]
        self.dot_F_North = self.d_V_East / self.Radius + self.w_North_dr + self.w_Noise[self.current_step]
        self.dot_F_Up = self.d_V_East / self.Radius * np.tan(self.fi) + self.W_Up_dr + self.w_Noise[self.current_step]

        self.dot_w_xB_dr = -self.betta * self.W_xB_dr + self.A * np.sqrt(2 * self.betta) * self.w_Noise[self.current_step]
        self.dot_w_yB_dr = -self.betta * self.W_yB_dr + self.A * np.sqrt(2 * self.betta) * self.w_Noise[self.current_step]
        self.dot_w_Up_dr = -self.betta * self.W_Up_dr + self.A * np.sqrt(2 * self.betta) * self.w_Noise[self.current_step]

        self.update_prev_V_delta()      # Обновляем переменную V delta current в previous в конце каждого шага
        self.current_step += 1          # Повышаем шаг исполнения на +1 после прохождения кааждой итерации

    def update_matrix(self):
        """Функция обновлят значения внутри матриц """
        dtype_type = "float32"
        # -----------------------------------------------------------------------------------
        self.nonNumPy_matrix_F = [
            [1, 0, 0, -self.gravity * self.T, self.Acc_North * self.T, 0, 0, 0],
            [0, 1, self.gravity * self.T, 0, -self.Acc_East * self.T, 0, 0, 0],
            [0, -self.T * self.Radius, 1, 0, 0, self.T * np.cos(self.H), self.T * np.sin(self.H), 0],
            [self.T / self.Radius, 0, 0, 1, 0, -self.T * np.sin(self.H), self.T * np.cos(self.H), 0],
            [self.T * np.tan(self.Radius), 0, 0, 0, 1, 0, 0, self.T],
            [0, 0, 0, 0, 0, 1 - self.betta * self.T, 0, 0],
            [0, 0, 0, 0, 0, 0, 1 - self.betta * self.T, 0],
            [0, 0, 0, 0, 0, 0, 0, 1 - self.betta * self.T]
        ]
        self.matrix_F = np.array(self.nonNumPy_matrix_F, dtype=f"{dtype_type}")
        # -----------------------------------------------------------------------------------
        self.nonNumPy_matrix_G = [
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, self.A * np.sqrt(2 * self.betta * self.T), 0, 0],
            [0, 0, 0, 0, 0, 0, self.A * np.sqrt(2 * self.betta * self.T), 0],
            [0, 0, 0, 0, 0, 0, 0, self.A * np.sqrt(2 * self.betta * self.T)],
        ]
        self.matrix_G = np.array(self.nonNumPy_matrix_G, dtype=f"{dtype_type}")
        # -----------------------------------------------------------------------------------
        self.matrix_Q_value = np.array([self.d_V_East, self.d_V_North,
                                        self.F_East, self.F_North, self.F_Up,
                                        self.W_xB_dr, self.W_yB_dr, self.W_Up_dr],
                                       dtype=f"{dtype_type}")
        self.nonNumPy_matrix_Q = [
            [self.matrix_Q_value[0], 0, 0, 0, 0, 0, 0, 0],
            [0, self.matrix_Q_value[1], 0, 0, 0, 0, 0, 0],
            [0, 0, self.matrix_Q_value[2], 0, 0, 0, 0, 0],
            [0, 0, 0, self.matrix_Q_value[3], 0, 0, 0, 0],
            [0, 0, 0, 0, self.matrix_Q_value[4], 0, 0, 0],
            [0, 0, 0, 0, 0, self.matrix_Q_value[5], 0, 0],
            [0, 0, 0, 0, 0, 0, self.matrix_Q_value[6], 0],
            [0, 0, 0, 0, 0, 0, 0, self.matrix_Q_value[7]],
        ]
        # self.nonNumPy_matrix_Q = [
        #     [self.d_V_East, 0, 0, 0, 0, 0, 0, 0],
        #     [0, self.d_V_North, 0, 0, 0, 0, 0, 0],
        #     [0, 0, self.F_East, 0, 0, 0, 0, 0],
        #     [0, 0, 0, self.F_North, 0, 0, 0, 0],
        #     [0, 0, 0, 0, self.F_Up, 0, 0, 0],
        #     [0, 0, 0, 0, 0, self.W_xB_dr, 0, 0],
        #     [0, 0, 0, 0, 0, 0, self.W_yB_dr, 0],
        #     [0, 0, 0, 0, 0, 0, 0, self.W_Up_dr],
        # ]
        self.matrix_Q = np.array(self.nonNumPy_matrix_Q, dtype=f"{dtype_type}")
        # -----------------------------------------------------------------------------------
        self.matrix_R_value = np.array([0,
                                        0],
                                       dtype=f"{dtype_type}")
        self.nonNumPy_matrix_R = [
            [self.matrix_R_value[0], 0],
            [0, self.matrix_R_value[1]]
        ]
        # [0, 0, 1, 0, 0, 0, 0, 0],
        # [0, 0, 0, 1, 0, 0, 0, 0],
        # [0, 0, 0, 0, 1, 0, 0, 0],
        # [0, 0, 0, 0, 0, 1, 0, 0],
        # [0, 0, 0, 0, 0, 0, 1, 0],
        # [0, 0, 0, 0, 0, 0, 0, 1],
        # ]
        self.matrix_R = np.array(self.nonNumPy_matrix_R, dtype=f"{dtype_type}")
        # -----------------------------------------------------------------------------------
        self.matrix_P_value = np.array([0,
                                        0,
                                        0,
                                        0,
                                        0,
                                        0,
                                        0,
                                        0],
                                       dtype=f"{dtype_type}")
        self.nonNumPy_matrix_P = [
            [self.matrix_P_value[0], 0, 0, 0, 0, 0, 0, 0],
            [0, self.matrix_P_value[1], 0, 0, 0, 0, 0, 0],
            [0, 0, self.matrix_P_value[2], 0, 0, 0, 0, 0],
            [0, 0, 0, self.matrix_P_value[3], 0, 0, 0, 0],
            [0, 0, 0, 0, self.matrix_P_value[4], 0, 0, 0],
            [0, 0, 0, 0, 0, self.matrix_P_value[5], 0, 0],
            [0, 0, 0, 0, 0, 0, self.matrix_P_value[6], 0],
            [0, 0, 0, 0, 0, 0, 0, self.matrix_P_value[7]],
        ]
        self.matrix_P = np.array(self.nonNumPy_matrix_P, dtype=f"{dtype_type}")
        # -----------------------------------------------------------------------------------

    def new_step_data_input(self, delta_V_East_current, delta_V_North_current):
        """Функция вызывается в начале каждого шага для внесения новых переменных в свойства классов """
        self.input_delta_V_East(delta_V_East_current)       # Обновляем значение в дельта V EAST
        self.input_delta_V_North(delta_V_North_current)     # Обновляем значение в дельта V NORTH

        self.input_Acc_East()       # Обновляем значение в Acc_East
        self.input_Acc_North()      # Обновляем значение в Acc_North

        self.input_F_East()         # Обновляем значение в F_East
        self.input_F_North()        # Обновляем значение в F_North
        self.input_F_Up()           # Обновляем значение в F_Up

        self.input_W_xB_dr()        # Обновляем значение в W_xB_dr
        self.input_W_yB_dr()        # Обновляем значение в W_yB_dr
        self.input_W_Up_dr()        # Обновляем значение в W_Up_dr

        self.input_w_East_dr()      # Обновляем значение в w_East_dr
        self.input_w_North_dr()     # Обновляем значение в w_North_dr

        self.update_matrix()        # Обновляем значения в матрицах F, G, Q, R, P

    # ------------------------------------------------------------------

    def activate_start_values(self, delta_V_East_prev=0, delta_V_East_current=0,
                                    delta_V_North_prev=0, delta_V_North_current=0):
        """Функция задает начальные значения для всех параметров экземпляра класса """
        self.V_East_delta_prev = delta_V_East_prev      # Значение скорости по EAST на предыдущем шаге
        self.V_North_delta_prev = delta_V_North_prev    # Значение скорости по NORTH на предыдущем шаге

        self.input_delta_V_East(delta_V_East_current)    # Вводим стартовые значения для self.d_V_East  дельта V east
        self.input_delta_V_North(delta_V_North_current)  # Вводим стартовые значения для self.d_V_North дельта V north

        self.input_Acc_East()   # self.Acc_East  # Значение ускорения по EAST на текущем шаге
        self.input_Acc_North()  # self.Acc_North  # Значение ускорения по NORTH на текущем шаге

        self.input_F_East()      # self.F_East = None
        self.input_F_North()     # self.F_North = None
        self.input_F_Up()        # self.F_Up = None
        self.input_W_xB_dr()     # self.W_xB_dr = None
        self.input_W_yB_dr()     # self.W_yB_dr = None
        self.input_W_Up_dr()     # self.W_Up_dr = None

        self.input_w_East_dr()          # self.w_East_dr  Ввводим значения для W дрейфа по EAST
        self.input_w_North_dr()         # self.w_North_dr Ввводим значения для W дрейфа по NORTH

        self.update_matrix()

    # ------------------------------------------------------------------

    def input_delta_V_East(self, delta_V_e):
        """Вносим в экземпляр текущее значение delta V east"""
        self.d_V_East = delta_V_e

    def input_delta_V_North(self, delta_V_n):
        """Вносим в экземпляр текущее значение delta V north"""
        self.d_V_North = delta_V_n
    # ------------------------------------------------------------------

    def update_prev_V_delta(self):
        """Обновляем предыдущие значения дельт скоростей по EAST и NORTH """
        self.V_East_delta_prev = self.d_V_East
        self.V_North_delta_prev = self.d_V_North
    # ------------------------------------------------------------------

    def input_Acc_East(self):
        """Функция считает текущее ускорение по EAST"""
        self.Acc_East = (self.d_V_East - self.V_East_delta_prev) / self.T

    def input_Acc_North(self):
        """Функция считает текущее ускорение по NORTH"""
        self.Acc_North = (self.d_V_North - self.V_North_delta_prev) / self.T
    # ------------------------------------------------------------------

    def input_F_East(self):
        """Функция считает текущее F по EAST"""
        self.F_East = 1
    # ------------------------------------------------------------------

    def input_F_North(self):
        """Функция считает текущее F по North"""
        self.F_North = 1
    # ------------------------------------------------------------------

    def input_F_Up(self):
        """Функция считает текущее F по Up"""
        self.F_Up = 1
    # ------------------------------------------------------------------

    def input_W_xB_dr(self):
        """Функция считает текущее W дрейфа по X """
        self.W_xB_dr = 1
    # ------------------------------------------------------------------

    def input_W_yB_dr(self):
        """Функция считает текущее W дрейфа по Y """
        self.W_yB_dr = 1
    # ------------------------------------------------------------------

    def input_W_Up_dr(self):
        """Функция считает текущее W дрейфа по Up """
        self.W_Up_dr = 1

    # ------------------------------------------------------------------

    def input_w_East_dr(self):
        """Функция считает текущее W дрейфа по EAST """
        self.w_East_dr = self.W_xB_dr * np.cos(self.H) + self.W_yB_dr * np.sin(self.H)
    # ------------------------------------------------------------------

    def input_w_North_dr(self):
        """Функция считает текущее W дрейфа по NORTH """
        self.w_North_dr = self.W_yB_dr * np.cos(self.H) - self.W_xB_dr * np.sin(self.H)
    # ------------------------------------------------------------------



