from pymongo import MongoClient


class Repository:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.db
        self.shopping_list = self.db.shopping_list

    def add_items(self):
        item = "New"
        while item:
            item = input('Введите название товара: ')
            if item:
                self.shopping_list.insert_one({'name': item.capitalize()})

    def delete_item(self):
        item = input('Введите название товара: ')
        self.shopping_list.delete_one({'name': item.capitalize()})

    def show_items(self):
        print('\nВаш список содержит: \n')
        for item in self.shopping_list.find():
            print(item.get('name'))


def shop_list():
    db = Repository()
    while True:

        print('\nМеню\n')
        choices = {
            0: ('Добавить товары', db.add_items),
            1: ('Удалить товар', db.delete_item),
            2: ('Показать список', db.show_items),
            3: ('Выход', quit),
        }
        for key, value in choices.items():
            print(f'{key} = {value[0]}')
        choice = int(input('Ваш выбор: '))
        if choice in choices.keys():
            print(f'Вы выбрали пункт "{choices[choice][0]}"')
            choices[choice][1]()
        else:
            print('Ошибка.\nПопробуйте снова...')


if __name__ == "__main__":
    shop_list()
