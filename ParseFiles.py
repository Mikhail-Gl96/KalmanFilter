import numpy as np
import math
import random

class File:
    def __init__(self):
        """Инициализация всх переменных в экземпляре класса"""
        self.File_extension = '.' + 'txt'
        self.FileName_INS = "ИНС И21" + self.File_extension
        self.FileName_BINS = "БИНС КомпаНав-5.2" + self.File_extension
        self.openSettings = 'r'

        self.data_INS = []    # храним здесь информацию от ИНС
        self.data_BINS = []   # ХРАНИМ ЗДЕСЬ ИНФОРМАЦИЮ ОТ БИНС
        self.bothFiles = [self.data_INS, self.data_BINS]
        self.mask_for_newData = []

        self.columns_names = []       # Названия столбиков в массиве [INS_data, BINS_data]
        self.num_AllPositions = []    # Максимальное количество строк в файле [INS_data, BINS_data]

        self.dataArr_INS = []
        self.dataArr_BINS = []
        self.dataArr_INS_numpyArr = None
        self.dataArr_BINS_numpyArr = None

        #  INS
        self.INS_I21_UTC = None
        self.INS_I21_Heading = None
        self.INS_I21_Roll = None
        self.INS_I21_Pitch = None
        self.INS_I21_Lat = None
        self.INS_I21_Lon = None
        self.INS_I21_VN = None
        self.INS_I21_VE = None

        # BINS
        self.BINS_UTC = None
        self.BINS_Wx = None
        self.BINS_Wy = None
        self.BINS_Wz = None
        self.BINS_Ax = None
        self.BINS_Ay = None
        self.BINS_Az = None
        self.BINS_Heading = None
        self.BINS_Roll = None
        self.BINS_Pitch = None
        self.BINS_Latitude = None
        self.BINS_Longitude = None
        self.BINS_VN = None
        self.BINS_VE = None

    def give_BINS_V_E_null_data(self, data, start_pos=66000):
        """Получаем -1 элемент до начала синхронизированного ряда V East"""
        data_analyse = data[start_pos - 1]
        return data_analyse

    def give_BINS_V_N_null_data(self, data, start_pos=66000):
        """Получаем -1 элемент до начала синхронизированного ряда V North"""
        data_analyse = data[start_pos - 1]
        return data_analyse

    def give_INS_V_E_null_data(self, data, start_pos=4006):
        """Получаем -1 элемент до начала синхронизированного ряда V East"""
        data_analyse = data[start_pos - 1]
        return data_analyse

    def give_INS_V_N_null_data(self, data, start_pos=4006):
        """Получаем -1 элемент до начала синхронизированного ряда V North"""
        data_analyse = data[start_pos - 1]
        return data_analyse

    def give_active_bins_data_sync(self, data, start_pos=66000, freq=1):
        """Функция для пост обработки и выдачи данных с БИНС готовых к дальнейшей работе"""
        data_analyse = data[start_pos:525400:freq]
        return data_analyse

    def give_active_ins_data_sync_time(self, data, start_pos=4006, freq=10):
        arr_to_use = data[start_pos:len(data) - 4]
        local_data = arr_to_use.copy()  # Копия выборки для безопасного использования
        local_arr_out = []                             # хранение новых данных для дальнейшей отправки при помощи return
        local_mask_arr_out = []
        buffer_10elements = []                         # буфер для текущей выборки в 10 элементов
        prev_element = local_data[0]                   # предыдущее значение (нулевое значение равно первому элементу выборки)
        for i in local_data:
            roundMin_current_element = self.round_min(i)
            roundMIN_previous_element = self.round_min(prev_element)
            if roundMin_current_element == roundMIN_previous_element:
                buffer_10elements.append(i)
                prev_element = i
            if roundMin_current_element != roundMIN_previous_element:
                data_out = self.reorg_arr_10elements_time(buffer_10elements.copy())
                for i_parse in data_out[0]:
                    local_arr_out.append(i_parse)
                for i_parse in data_out[1]:
                    local_mask_arr_out.append(i_parse)
                buffer_10elements.clear()
                buffer_10elements.append(i)
                prev_element = i
        self.mask_for_newData = local_mask_arr_out
        # print(f' mask len = {len(local_mask_arr_out)}    len ideal = {len(local_data)}   len localout = {len(local_arr_out)}')
        data_analyse = np.array(local_arr_out, dtype='float32').repeat(freq)
        return data_analyse

    def reorg_arr_10elements_time(self, data):
        """Функция для корректировки массивов ИНС времени UTC в 10 элементов и составления таблицы маски
        для дальнейших постобработок других данных экземпляра"""
        local_data = data.copy()
        len_data = len(local_data)
        if len_data == 10:              # Если внутри 10 элементов, то все ок, возвращаем
            mask_arr = [1 for a in range(len_data)]
            answer_arr = local_data.copy()
            return answer_arr, mask_arr
        elif len_data < 10:
            additional_data_len = 10 - len_data
            answer_arr = local_data.copy()
            mask_arr = [1 for a in range(len_data)]
            for i in range(additional_data_len):
                answer_arr.append(local_data[-1])
                mask_arr.append(0)
            return answer_arr, mask_arr
        elif len_data > 10:
            additional_data_len_overflow = len_data - 10
            mask_arr = [1 for a in range(len_data)]
            answer_arr = local_data.copy()
            for i in range(additional_data_len_overflow):  # выбираем рандомно какие из точек удалим из выборки
                del_pos = random.randint(1, len_data - 1)
                answer_arr.pop(del_pos)      # рандомно выбираем индекс внутри последовательности и удаляем его
                mask_arr[del_pos] = -1
            return answer_arr, mask_arr
        else:
            print('Error')
            return None, None

    def give_active_ins_data_sync(self, data, start_pos=4006, freq=10):
        """Функция обработки данных для всех данных экземпляра класса кроме времени"""
        arr_to_use = data[start_pos:len(data) - 4]
        local_data = arr_to_use.copy()  # Копия выборки для безопасного использования
        local_local_data = []
        for i in local_data:
            local_local_data.append(i)
        local_arr_out = []  # хранение новых данных для дальнейшей отправки при помощи return
        local_mask = self.mask_for_newData.copy()
        prev_element = local_local_data[0]  # предыдущее значение (нулевое значение равно первому элементу выборки)
        for i in range(len(local_mask)):
            if local_mask[i] == 1:
                local_inside_data = local_local_data.pop(0)
                local_arr_out.append(local_inside_data)
                prev_element = local_inside_data
            elif local_mask[i] == -1:
                continue
            elif local_mask[i] == 0:
                local_arr_out.append(prev_element)
        data_analyse = np.array(local_arr_out, dtype='float32').repeat(freq)
        return data_analyse

    def round_min(self, data):
        """Функция округления числа в меньшую сторону"""
        return math.floor(data)

    def openFile(self):
        """Функция открывает файл и выгружает данные"""
        # local_file_INS, local_file_BINS = None, None
        try:
            local_file_INS = open(self.FileName_INS, self.openSettings)
            local_file_BINS = open(self.FileName_BINS, self.openSettings)

        except FileNotFoundError:
            print("No file Found")
        else:
            self.data_INS = local_file_INS
            self.data_BINS = local_file_BINS
            self.bothFiles = [self.data_INS, self.data_BINS]
        # finally:
        #     local_file_BINS.close()
        #     local_file_INS.close()

    def getFile_INS(self):
        return self.data_INS

    def getFile_BINS(self):
        return self.data_BINS

    def clearString(self, string):
        split_symbol = ' '
        null_symbol = ''
        local_string = string.replace('\n', null_symbol).split(split_symbol)
        return local_string

    def clearNullStrings(self, inputString):
        null_symbol = ''
        num_null_columns = inputString.count(null_symbol)
        for i in range(num_null_columns):
            inputString.remove(null_symbol)
        return inputString

    def analyzeColumns(self):
        local_arr_Output_data = []  # [self.dataArr_INS, self.dataArr_BINS]
        # первым ИНС, потом БИНС
        for localFile in self.bothFiles:        # Пройдемся по каждому файлу
            local_data = []          # здесь лежат числовые данные
            # first_string = None      # локальная переменная для хранения названий строчек
            flag_FirstString = 0     # фаг прочтения первой строки
            for current_string in localFile:    # Копаемся внутри каждого файла
                if flag_FirstString == 0:      # Если первая строка
                    # first_string = self.clearString(current_string)
                    first_string = self.clearNullStrings(self.clearString(current_string))
                    self.columns_names.append(first_string)
                    self.num_AllPositions.append(len(first_string))
                    flag_FirstString = 1
                else:                           # Обрабатываем данные
                    local_data_str = self.clearNullStrings(self.clearString(current_string))
                    local_data.append(local_data_str)
            # print(f'local_data = {local_data}')
            local_arr_Output_data.append(local_data)
        self.dataArr_INS = local_arr_Output_data[0]         # столбики ИНС
        self.dataArr_BINS = local_arr_Output_data[1]        # столбики БИНС
        self.convertStrToNumpyArr()
        self.create_individual_columns_data()

    def convertStrToNumpyArr(self):
        self.dataArr_INS_numpyArr = np.array(self.dataArr_INS)
        self.dataArr_BINS_numpyArr = np.array(self.dataArr_BINS)

    def getFloatArr_INS(self):
        return self.dataArr_INS_numpyArr

    def getFloatArr_BINS(self):
        return self.dataArr_BINS_numpyArr
    """                 GETTER                  """
    """
        INS COLUMNS
            0 - I21_UTC         время
            1 - I21_Heading     Курс
            2 - I21_Roll        Крен
            3 - I21_Pitch       Тангаж
            4 - I21_Lat         Широта 
            5 - I21_Lon         Долгота
            6 - I21_VN          Скорость по северному направлению
            7 - I21_VE          Скорость по восточному направлению
    """

    def get_INS_I21_UTC(self):
        return self.INS_I21_UTC

    def get_INS_I21_Heading(self):
        return self.INS_I21_Heading

    def get_INS_I21_Roll(self):
        return self.INS_I21_Roll

    def get_INS_I21_Pitch(self):
        return self.INS_I21_Pitch

    def get_INS_I21_Lat(self):
        return self.INS_I21_Lat

    def get_INS_I21_Lon(self):
        return self.INS_I21_Lon

    def get_INS_I21_VN(self):
        return self.INS_I21_VN

    def get_INS_I21_VE(self):
        return self.INS_I21_VE

    """
            BINS COLUMNS
                0 - BINS_UTC                    Время
                1 - BINS_Wx                     Угловая скорость по оси OX
                2 - BINS_Wy                     Угловая скорость по оси OY
                3 - BINS_Wz (BINS_Wy ???)       Угловая скорость по оси OZ
                4 - BINS_Ax                     Угловое ускорение по оси OX
                5 - BINS_Ay                     Угловое ускорение по оси OY
                6 - BINS_Az                     Угловое ускорение по оси OZ
                7 - BINS_Heading                Курс
                8 - BINS_Roll                   Крен
                9 - BINS_Pitch                  Тангаж
                10 - BINS_Latitude              Широта   
                11 - BINS_Longitude             Долгота
                12 - BINS_VN                    Линейная скорость северного направления
                13 - BINS_VE                    Линейная скорость восточного направления
        """

    def get_BINS_UTC(self):
        return self.BINS_UTC

    def get_BINS_Wx(self):
        return self.BINS_Wx

    def get_BINS_Wy(self):
        return self.BINS_Wy

    def get_BINS_Wz(self):
        return self.BINS_Wz

    def get_BINS_Ax(self):
        return self.BINS_Ax

    def get_BINS_Ay(self):
        return self.BINS_Ay

    def get_BINS_Az(self):
        return self.BINS_Az

    def get_BINS_Heading(self):
        return self.BINS_Heading

    def get_BINS_Roll(self):
        return self.BINS_Roll

    def get_BINS_Pitch(self):
        return self.BINS_Pitch

    def get_BINS_Latitude(self):
        return self.BINS_Latitude

    def get_BINS_Longitude(self):
        return self.BINS_Longitude

    def get_BINS_VN(self):
        return self.BINS_VN

    def get_BINS_VE(self):
        return self.BINS_VE

    """                 SETTER                  """

    def create_individual_columns_data(self):
        # INS
        local_I21_UTC = []
        local_I21_Heading = []
        local_I21_Roll = []
        local_I21_Pitch = []
        local_I21_Lat = []
        local_I21_Lon = []
        local_I21_VN = []
        local_I21_VE = []

        # BINS
        local_BINS_UTC = []
        local_BINS_Wx = []
        local_BINS_Wy = []
        local_BINS_Wz = []
        local_BINS_Ax = []
        local_BINS_Ay = []
        local_BINS_Az = []
        local_BINS_Heading = []
        local_BINS_Roll = []
        local_BINS_Pitch = []
        local_BINS_Latitude = []
        local_BINS_Longitude = []
        local_BINS_VN = []
        local_BINS_VE = []

        for arr in self.dataArr_INS_numpyArr:
            local_I21_UTC.append(arr[0])
            local_I21_Heading.append(arr[1])
            local_I21_Roll.append(arr[2])
            local_I21_Pitch.append(arr[3])
            local_I21_Lat.append(arr[4])
            local_I21_Lon.append(arr[5])
            local_I21_VN.append(arr[6])
            local_I21_VE.append(arr[7])

        for arr in self.dataArr_BINS_numpyArr:
            local_BINS_UTC.append(arr[0])
            local_BINS_Wx.append(arr[1])
            local_BINS_Wy.append(arr[2])
            local_BINS_Wz.append(arr[3])
            local_BINS_Ax.append(arr[4])
            local_BINS_Ay.append(arr[5])
            local_BINS_Az.append(arr[6])
            local_BINS_Heading.append(arr[7])
            local_BINS_Roll.append(arr[8])
            local_BINS_Pitch.append(arr[9])
            local_BINS_Latitude.append(arr[10])
            local_BINS_Longitude.append(arr[11])
            local_BINS_VN.append(arr[12])
            local_BINS_VE.append(arr[13])

        dtype_type = "float32"
        self.set_INS_I21_UTC(np.array(local_I21_UTC, dtype=f"{dtype_type}"))
        self.set_INS_I21_Heading(np.array(local_I21_Heading, dtype=f"{dtype_type}"))
        self.set_INS_I21_Roll(np.array(local_I21_Roll, dtype=f"{dtype_type}"))
        self.set_INS_I21_Pitch(np.array(local_I21_Pitch, dtype=f"{dtype_type}"))
        self.set_INS_I21_Lat(np.array(local_I21_Lat, dtype=f"{dtype_type}"))
        self.set_INS_I21_Lon(np.array(local_I21_Lon, dtype=f"{dtype_type}"))
        self.set_INS_I21_VN(np.array(local_I21_VN, dtype=f"{dtype_type}"))
        self.set_INS_I21_VE(np.array(local_I21_VE, dtype=f"{dtype_type}"))

        self.set_BINS_UTC(np.array(local_BINS_UTC, dtype=f"{dtype_type}"))
        self.set_BINS_Wx(np.array(local_BINS_Wx, dtype=f"{dtype_type}"))
        self.set_BINS_Wy(np.array(local_BINS_Wy, dtype=f"{dtype_type}"))
        self.set_BINS_Wz(np.array(local_BINS_Wz, dtype=f"{dtype_type}"))
        self.set_BINS_Ax(np.array(local_BINS_Ax, dtype=f"{dtype_type}"))
        self.set_BINS_Ay(np.array(local_BINS_Ay, dtype=f"{dtype_type}"))
        self.set_BINS_Az(np.array(local_BINS_Az, dtype=f"{dtype_type}"))
        self.set_BINS_Heading(np.array(local_BINS_Heading, dtype=f"{dtype_type}"))
        self.set_BINS_Roll(np.array(local_BINS_Roll, dtype=f"{dtype_type}"))
        self.set_BINS_Pitch(np.array(local_BINS_Pitch, dtype=f"{dtype_type}"))
        self.set_BINS_Latitude(np.array(local_BINS_Latitude, dtype=f"{dtype_type}"))
        self.set_BINS_Longitude(np.array(local_BINS_Longitude, dtype=f"{dtype_type}"))
        self.set_BINS_VN(np.array(local_BINS_VN, dtype=f"{dtype_type}"))
        self.set_BINS_VE(np.array(local_BINS_VE, dtype=f"{dtype_type}"))

    """
        INS COLUMNS
            0 - I21_UTC
            1 - I21_Heading
            2 - I21_Roll
            3 - I21_Pitch
            4 - I21_Lat
            5 - I21_Lon
            6 - I21_VN
            7 - I21_VE
    """

    def set_INS_I21_UTC(self, input_data):
        self.INS_I21_UTC = input_data

    def set_INS_I21_Heading(self, input_data):
        self.INS_I21_Heading = input_data

    def set_INS_I21_Roll(self, input_data):
        self.INS_I21_Roll = input_data

    def set_INS_I21_Pitch(self, input_data):
        self.INS_I21_Pitch = input_data

    def set_INS_I21_Lat(self, input_data):
        self.INS_I21_Lat = input_data

    def set_INS_I21_Lon(self, input_data):
        self.INS_I21_Lon = input_data

    def set_INS_I21_VN(self, input_data):
        self.INS_I21_VN = input_data

    def set_INS_I21_VE(self, input_data):
        self.INS_I21_VE = input_data

    """
            BINS COLUMNS
                0 - BINS_UTC
                1 - BINS_Wx
                2 - BINS_Wy
                3 - BINS_Wz (BINS_Wy ???)
                4 - BINS_Ax
                5 - BINS_Ay
                6 - BINS_Az
                7 - BINS_Heading
                8 - BINS_Roll
                9 - BINS_Pitch
                10 - BINS_Latitude
                11 - BINS_Longitude
                12 - BINS_VN
                13 - BINS_VE
        """

    def set_BINS_UTC(self, input_data):
        self.BINS_UTC = input_data

    def set_BINS_Wx(self, input_data):
        self.BINS_Wx = input_data

    def set_BINS_Wy(self, input_data):
        self.BINS_Wy = input_data

    def set_BINS_Wz(self, input_data):
        self.BINS_Wz = input_data

    def set_BINS_Ax(self, input_data):
        self.BINS_Ax = input_data

    def set_BINS_Ay(self, input_data):
        self.BINS_Ay = input_data

    def set_BINS_Az(self, input_data):
        self.BINS_Az = input_data

    def set_BINS_Heading(self, input_data):
        self.BINS_Heading = input_data

    def set_BINS_Roll(self, input_data):
        self.BINS_Roll = input_data

    def set_BINS_Pitch(self, input_data):
        self.BINS_Pitch = input_data

    def set_BINS_Latitude(self, input_data):
        self.BINS_Latitude = input_data

    def set_BINS_Longitude(self, input_data):
        self.BINS_Longitude = input_data

    def set_BINS_VN(self, input_data):
        self.BINS_VN = input_data

    def set_BINS_VE(self, input_data):
        self.BINS_VE = input_data






# test = File()
# test.openFilenp.array(()
# print(test.getFile_INS().read())
# print(test.bothFiles)
# test.analyzeColumns()
# print(f"test.columns_names = {test.columns_names}")
# print(f"test.num_AllPositions = {test.num_AllPositions}")
# print(f"test.getFloatArr_INS() = {test.getFloatArr_INS()}")