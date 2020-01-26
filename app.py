from flask import Flask
from flask import render_template
import data
from my_tools import get_rus_case

app = Flask(__name__)


@app.route('/')
def main():
    # сформируем данные. Сначала распродажа и реклама, потом релевантные
    part_tours = dict()
    while len(part_tours) < 6:
        for k in data.sale_action_id:
            if k in data.tours:
                part_tours[k] = data.tours[k]
                if len(part_tours) > 5:
                    break
        for k,v in data.tours.items():
            if k not in part_tours:
                part_tours[k] = v
                if len(part_tours) > 5:
                    break

    return render_template("index.html", main=data.main_data, tours=part_tours)


@app.route('/from/<depart_from>/')
def start_from(depart_from):

    if depart_from not in data.departures:
        # TODO: Понять что делать в случае ссылки на несуществующее направление
        depart_from = "msk"
    part_tours = { k:v for k,v in data.tours.items() if v['departure'] == depart_from}
    total = {"length": len(part_tours), "name_obj":get_rus_case(len(part_tours),["туров","тур","тура"]),
             "min_nights":1000, "max_nights":0, "min_price":1000000, "max_price":0}

    for t in part_tours.values():
        total["min_nights"] = min(total["min_nights"], t["nights"])
        total["max_nights"] = max(total["max_nights"], t["nights"])
        total["min_price"] = min(total["min_price"], t["price"])
        total["max_price"] = max(total["max_price"], t["price"])

    if len(part_tours)>1:
        total["txt_price"] = "от {0:,} ".format(total["min_price"]).replace(',',' ') + \
                             "до {0:,} ".format(total["max_price"]).replace(',', ' ') + \
                             get_rus_case(total["max_price"], ["рублей","рубля","рублей"])
        total["txt_nights"] = "от {0:} до {1:} ".format( total["min_nights"], total["max_nights"]) +\
                          get_rus_case(total["max_nights"],["ночей","ночи","ночей"])
    else:
        total["txt_price"] = "{0:,}".format(total["min_price"]).replace(',',' ') + \
                             get_rus_case(total["max_price"], ["рублей", "рубль", "рубля"])
        total["txt_nights"] = "{0:} ".format(total["max_nights"]) + \
                              get_rus_case(total["max_nights"], ["ночей", "ночь", "ночи"])

    return render_template("direction.html", main=data.main_data, direction=data.departures[depart_from], tours=part_tours, summary=total)


@app.route('/tours/<int:id_tour>/')
def tours(id_tour):
    if id_tour not in data.tours:
        # TODO: Понять что делать в случае ссылки на тур, которого нет
        id_tour = 1
    depart_from = data.departures[data.tours[id_tour]['departure']]
    return render_template("tour.html", main=data.main_data, tour=data.tours[id_tour], depart_from=depart_from)


app.run(debug=True)
