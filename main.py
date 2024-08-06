from bs4 import BeautifulSoup    # подключаем все нужные библиотеки
import requests
import json
import time
import params_for_programm       # сохраяем константы

# ...................................


def save_info_all_games(params: str) -> str:   # сохранение инф о играх
    all_game = []  # списк словарей с инфой о играх
    counter_games = 0          # счетчик и общее количество игр
    amount_game = -1
    finish_parsing = False     # флаг окончания парсинга, когда максимум игр привысит

    for page in range(0, 1000, 100):   # пробегаемся по 1000 играм (сохраняем первые 200)
        url = f'https://store.steampowered.com/search/?{params}start={page}&count=100&ndl=1'  # составляем url для парсинга первых 100 игр

        req = requests.get(url, headers=params_for_programm.HEADERS)  # парсим и сохраняем резульат
        # with open('index.html', 'w', encoding="utf-8") as file:  # сохраняем результат в html файл
        #     file.write(req.text)

        soup = BeautifulSoup(req.text, 'lxml')
        # with open('index.html', 'r', encoding="utf-8") as file:  # открываем html файл для BeautifulSoup
        #     soup = BeautifulSoup(file, 'lxml')

        # находим общее количество найденных игр
        if amount_game == -1:
            print()
            amount_game = int(
                soup.find_all('div', class_='search_results_filtered_warning')[1].find('div').text.split()[4].replace(
                    ',', '').replace('.', ''))
            print(f'Найдено {amount_game} игр')


        html_all_games = soup.find_all('div', class_='col search_capsule')  # находим div элемент
        for el in range(100):                         # поднимаемся у каждого элемента на вверх по дереву
            # html_all_games[el] = html_all_games[el].find_parent()  #
            result_pares_game = get_info_game(html_all_games[el].find_parent())  # возращяем инф о игре
            if len(result_pares_game) != 7:                        # парсинг игр прошел успешно
                all_game.append(result_pares_game)
                counter_games += 1
                if amount_game > 200:
                    print(f'Обработанно {counter_games}/200')
                else:
                    print(f'Обработанно {counter_games}/{amount_game}')

            time.sleep(0.2)  # таймаут для парсинга

            if counter_games == 200 or (counter_games == amount_game and amount_game < 200):  # превышение лимита игр
                finish_parsing = True
                break
        if finish_parsing:
            break

    with open('all_games.json', 'a', encoding="utf-8") as file:  # сохраняем в json
        json.dump(all_game, file, indent=4, ensure_ascii=False)

    print(len(all_game))
    return 'Сохранено в json файл'


def get_info_game(game):   # получение инф о игре
    try:
        result = {}
        url_game = game.get('href')  # получаем url на игру
        result['name'] = game.find('span', class_='title').text      # вся доступная инфа по "первому вгляду"
        result['date'] = game.find('div', class_='col search_released responsive_secondrow').text.strip()
        result['price'] = game.find('div', class_='discount_final_price').text
        result['estimation'] = game.find('div', class_='col search_reviewscore responsive_secondrow').find_next().get(
            'data-tooltip-html').split('<br>')[0]

        req = requests.get(url_game, headers=params_for_programm.HEADERS)    # парсим игру на главной странице
        soup = BeautifulSoup(req.text, 'lxml')
        result['count estimation'] = soup.find('div', class_='summary_section').find_all()[2].text.split()[1][:-1]
        result['description'] = soup.find('div', class_='game_area_description').text   # запасной вариант описание игры
        result['game orginal'] = url_game
        result['description'] = soup.find('div', class_='game_description_snippet').text.strip()

    except Exception as e:
        return result

    return result


def get_params() -> str:      # получение параметров для поиска
    params = ''
    print('Если требуется узнать все возможные категории, напишите "help", иначе перечислить через специальный знак "#"')

    print('Введите жанр. (Обязательно ввести хотя бы 1)')
    inp = input()
    if inp == 'help':
        print(', '.join(params_for_programm.NAME_ALL_CATEGORY['tags']))
        inp = input()
    params += get_index_category(inp.split('#'), 'tags')

    print('Введите поддерживаемые языки')
    inp = input()
    if inp == 'help':
        print(', '.join(params_for_programm.NAME_ALL_CATEGORY['supportedlang']))
        inp = input()
    params += get_index_category(inp.split('#'), 'supportedlang')

    print('Введите категорию')
    inp = input()
    if inp == 'help':
        print(', '.join(params_for_programm.NAME_ALL_CATEGORY['category1']))
        inp = input()
    params += get_index_category(inp.split('#'), "category1")

    print('Введите количество игроков (Наименование, а не количество)')
    inp = input()
    if inp == 'help':
        print(', '.join(params_for_programm.NAME_ALL_CATEGORY['category3']))
        inp = input()
    params += get_index_category(inp.split('#'), 'category3')

    print('Введите особенности')
    inp = input()
    if inp == 'help':
        print(', '.join(params_for_programm.NAME_ALL_CATEGORY['category2']))
        inp = input()
    params += get_index_category(inp.split('#'), 'category2')

    print('Совместимость со Steam Deck')
    inp = input()
    if inp == 'help':
        print(', '.join(params_for_programm.NAME_ALL_CATEGORY['deck_compatibility']))
        inp = input()
    params += get_index_category(inp.split('#'), 'deck_compatibility')

    print('Поддержка контроллеров')
    inp = input()
    if inp == 'help':
        print(', '.join(params_for_programm.NAME_ALL_CATEGORY['controllersupport']))
        inp = input()
    params += get_index_category(inp.split('#'), 'controllersupport')

    print('Виртуальная реальность')
    inp = input()
    if inp == 'help':
        print(', '.join(params_for_programm.NAME_ALL_CATEGORY['vrsupport']))
        inp = input()
    params += get_index_category(inp.split('#'), 'vrsupport')

    print('Желаемая операционная система')
    inp = input()
    if inp == 'help':
        print(', '.join(params_for_programm.NAME_ALL_CATEGORY['os']))
        inp = input()
    params += get_index_category(inp.split('#'), 'os')

    return params


def get_index_category(category: str, name_category: str) -> str:     # получение параметра для категории
    if category == ['']:
        return ''
    result = ''

    for element in category:
        index = params_for_programm.INDEX_ALL_CATEGORY[element]
        result += index if not result else f'%2C{index}'

    if result:
        return f'{name_category}={result}&'
    return ''

# -----------------------------------------------------------
def main():
    print('Программа парсить игры из Steam по выбранным категориям')
    print(
        'Результат программы - JSON файл с данными о 200-ти играх (если их нашлось больше или ровно 200). Файл имеет формат:',
        '"name" - Название игры',
        '"date" - Дата выхода игры',
        '"price" - Стоимость игры',
        '"estimation" - Оценка игры',
        '"count estimation" - Количество оценок',
        '"description" - Описание игры',
        '"game orginal" - URL на игру в Steam', sep='\n')
    print()

    print(save_info_all_games(get_params()))              # получаем параметры для url ссылки и парсим


if __name__ == "__main__":
    main()


