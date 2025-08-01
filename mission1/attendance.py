SILVER_LEVEL = 30
GOLD_LEVEL = 50
players = {}
id_cnt = 0

points = [0] * 100
grade = [0] * 100
names = [''] * 100
attended_on_wed = [0] * 100
attended_on_weeken = [0] * 100

attendances = []

def get_point(name, day_of_week):
    idx = get_idx(name)

    if day_of_week == "wednesday":
        points[idx] += 3
        attended_on_wed[idx] += 1
    elif day_of_week == "saturday" or day_of_week == "sunday":
        points[idx] += 2
        attended_on_weeken[idx] += 1
    else:
        points[idx] += 1


def get_idx(name):
    global id_cnt
    if name not in players:
        id_cnt += 1
        players[name] = id_cnt
        names[id_cnt] = name
    return players[name]

def run():
    read_file()
    get_score()
    get_grade()
    get_removed_player()


def get_score():
    for attend in attendances:
        get_point(attend[0], attend[1])

    get_bonus_point()


def read_file():
    try:
        with open("attendance_weekday_500.txt", encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    attendances.append([parts[0], parts[1]])
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

def get_removed_player():
    print("\nRemoved player")
    print("==============")
    for i in range(1, id_cnt + 1):
        if grade[i] not in ("GOLD", "SILVER") and attended_on_wed[i] == 0 and attended_on_weeken[i] == 0:
            print(names[i])


def get_grade():
    for i in range(1, id_cnt + 1):
        if points[i] >= GOLD_LEVEL:
            grade[i] = "GOLD"
        elif points[i] >= SILVER_LEVEL:
            grade[i] = "SILVER"
        else:
            grade[i] = "NORMAL"

        print(f"NAME : {names[i]}, POINT : {points[i]}, GRADE : {grade[i]}",)


def get_bonus_point():
    for i in range(1, id_cnt + 1):
        if attended_on_wed[i] > 9:
            points[i] += 10
        if attended_on_weeken[i] > 9:
            points[i] += 10


if __name__ == "__main__":
    run()