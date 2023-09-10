from flask import Flask, request, render_template, Response, send_file
import re
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import io

app = Flask(__name__, template_folder="templates")


def get_df(request_file):
    file = request_file
    f = file.read().decode("utf-8")
    f = f.split("\n")
    pattern = r'^\d{1,2}/\d{1,2}/\d{2}$'
    dates = []
    hours = []
    names = []
    message = []
    for line in f:
        first_half = line.split("-")[0].replace(" ", "")
        if re.match(pattern, first_half.split(",")[0]):
            try:
                second_half = line.split("-")[1].split(":", 1)
                second_half[1].lstrip(" ")
                date = first_half.split(",")[0]
                dates.append(date)
                hours.append(first_half.split(",")[1])
                names.append(second_half[0].lstrip(" "))
                message.append(second_half[1].lstrip(" "))
            except:
                print("Error")
        else:
            message[-1] = message[-1] + " " + line;

    df = pd.DataFrame(columns=["Date", "Hour", "Name", "Message"])
    df["Date"] = dates
    df["Hour"] = hours
    df["Name"] = names
    df["Message"] = message
    return df


@app.route("/")
def mainPage():
    return render_template("index.html")


@app.route("/numbers", methods=['POST'])
def simpleStats():
    df = get_df(request.files["file"])
    length = len(df)
    first_date = list(df["Date"])[0]
    last_date = list(df["Date"])[-1]

    return {"len": length, "first": first_date, "last": last_date}, 200


@app.route("/hours", methods=['POST'])
def HourDist():
    df = get_df(request.files["file"])
    hours = df["Hour"]
    dict_hours = {}
    print("hey")
    for hour in hours:
        hole = int(hour.split(":")[0])
        if hole in list(dict_hours.keys()):
            dict_hours[hole] += 1
        else:
            dict_hours[hole] = 0

    plt.figure(figsize=(10, 10))
    bars = plt.bar(list(dict_hours.keys()), list(dict_hours.values()))
    plt.xlabel("Horas")
    plt.ylabel("Numero Mensajes")
    plt.xticks(list(dict_hours.keys()), list(dict_hours.keys()))
    plt.bar_label(bars)
    plt.savefig("hours.png")
    #plt.show()
    return send_file("hours.png")
    #print("Horas")
    #print(dict_hours)


@app.route("/months", methods=['POST'])
def Monthdist():
    df = get_df(request.files["file"])
    dates = df["Date"]
    month_names = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }
    dict_date = {}
    for date in dates:
        month = int(date.split("/")[1])
        if month in list(dict_date.keys()):
            dict_date[month] += 1
        else:
            dict_date[month] = 0
    for i in list(dict_date.keys()):
        dict_date[month_names[i]] = dict_date.pop(i)
    plt.figure(figsize=(10, 10))
    bars = plt.bar(list(dict_date.keys()), list(dict_date.values()))
    plt.xlabel("Mes")
    plt.ylabel("Numero Mensajes")
    plt.bar_label(bars)
    plt.savefig("months.png")
    #plt.show()
    return send_file("months.png")
    #print("Meses")
    #print(dict_date)

@app.route("/dayDist", methods=['GET', 'POST'])
def DayDist():
    df = get_df(request.files["file"])
    dates = df["Date"]
    day_names = {
        0: "L",
        1: "M",
        2: "X",
        3: "J",
        4: "V",
        5: "S",
        6: "D"
    }
    dict_day = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    }
    for date in dates:
        day = datetime.datetime(2023, int(date.split("/")[1]), int(date.split("/")[0])).weekday()
        if day in list(dict_day.keys()):
            dict_day[day] += 1
        else:
            dict_day[day] = 0
    for i in list(dict_day.keys()):
        dict_day[day_names[i]] = dict_day.pop(i)
    plt.figure(figsize=(10, 10))
    bars = plt.bar(list(dict_day.keys()), list(dict_day.values()))
    plt.xlabel("Dia")
    plt.ylabel("Numero Mensajes")
    plt.bar_label(bars)
    plt.savefig("days.png")
    #plt.show()
    return send_file("days.png")
    #print("Dias Semana")
    #print(dict_day)


@app.route("/eachPerson", methods=['GET', 'POST'])
def EachPerson():
    df = get_df(request.files["file"])
    in_group = list(df["Name"].unique())
    names = df["Name"]
    dict_names = {}
    for name in names:
        if name in in_group:
            if name in list(dict_names.keys()):
                dict_names[name] += 1
            else:
                dict_names[name] = 0

    df_only_mul = df.loc[df["Message"] == "<Multimedia omitido>"]
    mul_names = {}
    for guy in in_group:
        own_mes = df_only_mul.loc[df_only_mul["Name"] == guy]
        mul_names[guy] = len(own_mes)
    print("Multimedia")
    print(mul_names)
    plt.figure(figsize=(10, 10))
    bars = plt.bar(list(dict_names.keys()), list(dict_names.values()), label="Mensajes Totales")
    plt.bar(list(mul_names.keys()), list(mul_names.values()), label="Mensajes Multimedia")
    plt.legend()
    plt.xlabel("Persona")
    plt.ylabel("Numero Mensajes")
    plt.bar_label(bars)
    plt.savefig("person.png", format='png')
    #plt.show()
    return send_file("person.png")
    #print("Personas")
    #print(dict_names)


@app.route("/noMess", methods=['POST'])
def NoMessage():
    df = get_df(request.files["file"])
    in_group = list(df["Name"].unique())
    days_talk = {}
    for name in in_group:
        person_df = df.loc[df["Name"] == name]
        for day in person_df["Date"]:
            print(f"{name} hablo el dia: {day}")
        print(f"Total dias hablado por {name} ---- {len(set(person_df['Date']))}")
        days_talk[name] = len(set(person_df['Date']))

    dict_days_max_no_talk = {}
    for name in in_group:
        person_df = df.loc[df["Name"] == name]
        dates = list(person_df["Date"])
        dict_days_max_no_talk[name] = 0
        for i in range(1, len(dates)):
            previous_date_split = dates[i-1].split("/")
            current_date_split = dates[i].split("/")
            previous_day = datetime.datetime(int(previous_date_split[2]), int(previous_date_split[1]), int(previous_date_split[0]))
            current_day = datetime.datetime(int(current_date_split[2]), int(current_date_split[1]), int(current_date_split[0]))
            if (current_day - previous_day).days > 1:
                if (current_day - previous_day).days > dict_days_max_no_talk[name]:
                    dict_days_max_no_talk[name] = (current_day - previous_day).days
                print(current_day)
                print(previous_day)
    print(dict_days_max_no_talk)
    print(len(set(df["Date"])))
    print(days_talk)
    # Days Talk
    plt.figure(figsize=(10, 10))
    bars = plt.bar(list(days_talk.keys()), list(days_talk.values()), label="Dias hablados")
    plt.legend()
    plt.title(f"Maximo Numero de Días = {len(list(df['Date'].unique()))} dias")
    plt.xlabel("Persona")
    plt.ylabel("Dias")
    plt.bar_label(bars)
    plt.savefig("talk.png")
    #plt.show()
    return send_file("talk.png")

@app.route("/streak", methods=['POST'])
def streak():
    df = get_df(request.files["file"])
    in_group = list(df["Name"].unique())
    dict_days_max_no_talk = {}
    for name in in_group:
        person_df = df.loc[df["Name"] == name]
        dates = list(person_df["Date"])
        dict_days_max_no_talk[name] = 0
        for i in range(1, len(dates)):
            previous_date_split = dates[i - 1].split("/")
            current_date_split = dates[i].split("/")
            previous_day = datetime.datetime(int(previous_date_split[2]), int(previous_date_split[1]),
                                             int(previous_date_split[0]))
            current_day = datetime.datetime(int(current_date_split[2]), int(current_date_split[1]),
                                            int(current_date_split[0]))
            if (current_day - previous_day).days > 1:
                if (current_day - previous_day).days > dict_days_max_no_talk[name]:
                    dict_days_max_no_talk[name] = (current_day - previous_day).days
                print(current_day)
                print(previous_day)
    # Days No Talk
    plt.figure(figsize=(10, 10))
    bars = plt.bar(list(dict_days_max_no_talk.keys()), list(dict_days_max_no_talk.values()), label="Dias NO hablados")
    plt.legend(loc="upper left")
    plt.title("Racha días seguidos sin hablar")
    plt.xlabel("Persona")
    plt.ylabel("Dias")
    plt.bar_label(bars)
    plt.savefig("streak.png")
    #plt.show()
    return send_file("streak.png")


if __name__ == '__main__':
    app.run(host="0.0.0.0")