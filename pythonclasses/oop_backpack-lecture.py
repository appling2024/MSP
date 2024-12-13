# ===========================================================

# Рассмотрим конструктор __init__()
# автоматичекси вызывается при создании нового объекта (нового экземпляра класса)
class Backpack:
    """ Рюкзак """

    def __init__(self):
        self.content = []

    def add(self, item):
        """ Положить в рюкзак """
        self.content.append(item)
        print('В рюкзак положили:', item)

    def inspect(self):
        """ Проверить содержимое """
        print('В рюкзак лежит:')
        for item in self.content:
            print('    ', item)


my_backpack = Backpack()
my_backpack.add(item='ноутбук')
my_backpack.add(item='зарядка для ноутбука')
my_backpack.inspect()

# значения по умолчанию

##    def __init__(self, gift=None):
##        self.content = []
##        if gift:
##            self.content.append(gift)



# ===========================================================
# Складывание рюкзаков (более умными словами -- эмуляция математических операций)

class Backpack:
    """ Рюкзак """

    def __init__(self, gift=None):
        self.content = []
##        if gift:
##            self.content.append(gift)

    def add(self, item):
        """ Положить в рюкзак """
        self.content.append(item)
        print('В рюкзак положили:', item)

    def __str__(self):
        return 'Backpack: ' + ', '.join(self.content)


my_backpack = Backpack(gift='телефон')
my_backpack.add(item='ноутбук')
my_backpack.add(item='зарядка для ноутбука')
print(str(my_backpack))


# аналогичные методы
# __len__ - вызывается для получения "размера" объекта с помощью функции len()
# __bool__ - вызывается для получения "истинности" объекта с помощью функции bool()

a = ''

if not a:
    print(11111)


# ДОБАВИМ ДВА МЕТОДА:

    def __bool__(self):
        return self.content != []

    def __len__(self):
        return len(self.content)



# my_backpack.add(item='ноутбук')
print(bool(my_backpack), len(my_backpack))
if my_backpack:
    print('Рюкзак не пуст!')
    print('В нем лежит', len(my_backpack), 'предметов')
else:
    print('Вот рюкзак пустой, он предмет простой...')


#+++++++

# Возможна эмуляция математических операций
# 2 + 2
# my_car + truck
#
# object.__add__(self, other) - сложение +
# object.__sub__(self, other) - вычитание -
# object.__mul__(self, other) - умножение *
# object.__truediv__(self, other) - деление /
# object.__floordiv__(self, other) - целочисленное деление //
# object.__mod__(self, other) - остаток от деления %
# object.__pow__(self, other) - возведение в степень **
#
# должны возвращать объект

class Backpack:
    """ Рюкзак """

    def __init__(self, gift=None):  
        self.content = []
        if gift:
            self.content.append(gift)

    def __str__(self):
        return 'Backpack: ' + ', '.join(self.content)

    def __add__(self, other):
        new_obj = Backpack()
        new_obj.content.extend(self.content)
        new_obj.content.extend(other.content)
        return new_obj


my_backpack = Backpack(gift='бутерброд')
his_backpack = Backpack(gift='банан')
new_backpack = my_backpack + his_backpack
print(new_backpack)

