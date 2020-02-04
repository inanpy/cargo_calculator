from data_settings import *
from terminaltables import AsciiTable
import sys


def exit_script(error):
    # hata mesajini basarak cikis yapiyoruz.
    print error
    sys.exit()


def validate_data():
    # Gelen data atalarini kontrol ediyoruz.
    if not type(price_data) == dict:
        exit_script('price_data type error (only dict)')
    if not type(country_data) == list:
        exit_script('country_data type error (only list)')
    if not type(cargo_companies) == list:
        exit_script('cargo_companies type error (only list)')
    if not type(send_cargo_per_country) == dict:
        exit_script('send_cargo_per_country type error (only dict)')
    if not type(currency_type) == str:
        exit_script('currency_type type error (only string)')
    if not type(table_heading) == list:
        exit_script('table_heading type error (only list)')
    if len(price_data) == 0:
        exit_script('price_data: no content')
    if len(country_data) == 0:
        exit_script('country_data: no content')
    if len(cargo_companies) == 0:
        exit_script('cargo_companies: no content')
    if len(send_cargo_per_country) == 0:
        exit_script('send_cargo_per_country: no content')
    if len(currency_type) == 0:
        exit_script('currency_type: no content')
    if len(table_heading) == 0:
        exit_script('table_heading: no content')
    if len(table_heading) < 4:
        exit_script('table_heading: add some heading')


def price_calculator(data):
    count_cargo_company = {}
    from_send_data = {}
    clear_data = {}
    # gelen degeri kargo firmalarina esit dagitmak icin boluyoruz.
    sum_count, other_sum = divmod(sum(data.values()), len(cargo_companies))
    # KARGO ADETLERI
    if sum_count:
        for cargo in cargo_companies:
            count_cargo_company[cargo] = sum_count
    # Eger cargo sayisina boldugumuzde kalan varsa
    if other_sum:
        for_count = other_sum
        cargo_comp = price_data.get(data.keys()[-1])
        best_price = \
            sorted(cargo_comp.iteritems(),
                   key=lambda x: x[1])
        for cargo in best_price:
            if for_count > 0:
                for_count -= 1
                count_cargo_company[cargo[0]] += cargo[1]
    # TO_SHIP DATASI
    # sorted sekilde verilen send_cargo_per_country icerisinde donuyoruz.
    for k, v in sorted(data.items()):
        pop_country = data.pop(k)
        to_country = []
        count = int(pop_country)
        # w_result => kac defa for donmemiz gerekiyor
        w_result, w_other_result = divmod(count, len(data.keys()))
        w_count = w_result
        while w_count > 0:
            w_count -= 1
            # liste icerisinde kendi degerini cikararak diger tum ulkeleri
            # donuyoruz.
            for country in sorted(data):
                if count > 0:
                    count -= 1
                    to_country.append(country)
        # w_result tam bolunmediyse kalan kismini donuyoruz.
        if w_other_result:
            # f_count => kalan ulkeleri kontrol etmek icin.
            f_count = 0
            # tum ulkeleri donuyoruz kalan kismini append ediyoruz
            for country in data:
                if f_count < w_other_result:
                    f_count += 1
                    to_country.append(country)
        data[k] = pop_country
        from_send_data[k] = to_country
    # TO_SHIP ve COUNTRY BILGILERI ILE CARGO SETLEMELERI
    for k, v in from_send_data.items():
        cargo_companies_for_country = price_data.get(k)
        cargo_data = []
        # result => to_ship datasini cargo firmalarina bolerek kac defa for
        # donecek hesaplaniyor
        result, other_result = divmod(len(v), len(cargo_companies))
        # best_price => en ucuzdan pahaliya kargo firmalari siralaniyor.
        best_price = \
            sorted(cargo_companies_for_country.iteritems(),
                   key=lambda x: x[1])
        while_count = result
        while while_count > 0:
            while_count -= 1
            for_count = 0
            # tum kargo ve fiyatlarini while_count'a gore donuyoruz.
            for cargo, price in cargo_companies_for_country.items():
                # kargo sayilarina gore kontrol ediyoruz.
                if count_cargo_company[cargo] > 0:
                    count_cargo_company[cargo] -= 1
                    for_count += 1
                    cargo_data.append({cargo: price})
            # tum kargolari donmemize ragmen count 0 olan kargolari
            # kacirmamak icin tekrar kargo sayisini kontrol ediyoruz.
            if for_count < 3:
                for cargo in best_price:
                    if count_cargo_company[cargo[0]] > 0:
                        count_cargo_company[cargo[0]] -= 1
                        for_count += 1
                        cargo_data.append({cargo[0]: cargo[1]})
        # Tum kargo firmalarini dondukten sonra kalan degeri en ucuz kargo
        # firmasina atamaya calisiyoruz
        if other_result:
            count = other_result
            for cargo in best_price:
                # kargo sayilarina gore kontrol ediyoruz.
                if count_cargo_company[cargo[0]] > 0 and count > 0:
                    count_cargo_company[cargo[0]] -= 1
                    count -= 1
                    cargo_data.append({cargo[0]: cargo[1]})
        clear_data[k] = v, cargo_data

    return print_table(clear_data)


def print_table(data):
    table_data = [
        table_heading
    ]
    # TABLO OLUSTURUYORUZ.
    for from_country, data in data.items():
        for index, to_country in enumerate(data[0]):
            data_index = data[1][index]
            table_data.append([from_country, to_country, data_index.keys()[0], \
                               "{}".format(str(data_index.values()[0]) +
                                           currency_type)])
    table = AsciiTable(table_data)
    print table.table


validate_data()
price_calculator(send_cargo_per_country)
