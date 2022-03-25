import os
import shutil
import time

#Прочитать число из файла
def read_value_from_file(filename):
    result = None
    
    f = open(filename, 'r');
    try:
        #Пытаемся прочиитать число
        result = float(f.readline().rstrip())
    except ValueError:
        #Не получилось 
        result = None
    finally:
        f.close()
    
    return result

    
def update_file(filename, value):
    f = open(filename, 'w+');
    f.write(str(value))
    f.close()

def logic(path):
    #Получаем абсолютный путь до папки
    path = os.path.abspath(path)
    
    #Переходим в каталог
    os.chdir(path)
    
    #создаем файл amperage
    update_file("amperage", '');
    
    #Создаем переменную, которая будет обновлять свое значение из файла amperage
    amperage = None
    
    conditions = {}
    #Бесконечный цикл
    while True:
        #Обходим каждый файл/папку из списка
        for (root,dirs,files) in os.walk(path, topdown = True):
            time.sleep(0.5)
            #Если находимся в корневом католге
            if root == path:
                
                #Если сила тока не задана, то делаем первое считывание файла
                if amperage is None:
                    tmp = read_value_from_file("amperage")
                    if tmp is not None:
                        amperage = tmp
                        
            #Если находимся в одной из папок созданных пользователем
            else:
                
                #Существовала ли папка ранее
                if root in conditions:
                    
                    #Проверка на перегрев
                    if "OFF" in files:
                        if conditions[root][0] > 20:
                            conditions[root][0] -= 1
                    else:
                        conditions[root][0] += 1 * conditions[root][1]
                        if conditions[root][0] > 60:
                            update_file(root + "/OFF", '')
                            
                    update_file(root + "/temperature", conditions[root][0])
                    
                    #Если файл temp удалили - то по условию удаляем папку
                    if "temperature" not in files:
                        #Обновляем силу токачм 
                        amperage += conditions[root][2]
                        update_file("amperage", amperage)
                        
                        shutil.rmtree(root)
                        conditions.pop(root, None)
                        continue
                    
                    
                #Если видим папку в первый раз, то создаем файл температура и вносим папку в conditions 
                else:
                    
                    #Создаем файл температуры
                    update_file(root + "/temperature", 20)
                    
                    #В словаре условий будем хранить букву, силу тока и состояние раб
                    #Получаем данные из названия папки
                    cd = root.split('/')[-1]
                    letter = cd[0]
                    number = int(cd[1:])
                    
                    coef = 0
                    print(letter)
                    if   letter == 'B':
                        coef = 1
                    elif letter == 'C':
                        coef = 2
                    elif letter == 'D':
                        coef = 3
                        
                    conditions[root] = [20, coef, number]
                    
                    #Обновляем силу тока
                    amperage -= number
                    update_file("amperage", amperage)
