"""
2. 클래스 레벨리팩토링
D2 - Regression Test를 위한 Unit Test 개발
D3 – 확장성을 고려한설계, 정책과 등급이추가되더라도Client Code에 변경이 없도록 한다.
3. 디자인 패턴사용하기
D4 - 리팩토링에 디자인패턴을적용한다.
4. 코드 커버리지100%
D5 - 리팩토링이 끝난코드에, 코드 커버리지가100% 되어야한다

추상 클래스.
디자인 패턴

"""
import abc


class BaseClass:
    @abc.abstractmethod
    def get_name(self):
        pass

class Gold(BaseClass):
    def __init__(self, grade_score, name):
        self.grade_score = grade_score
        self.name = name

    def get_grade_score(self):
        return self.grade_score

    def get_name(self):
        return self.name

class Silver(BaseClass):
    def __init__(self, grade_score, name):
        self.grade_score = grade_score
        self.name = name

    def get_grade_score(self):
        return self.grade_score

    def get_name(self):
        return self.name

class Normal(BaseClass):
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

class Player:
    def __init__(self, name, id):
        self.name = name
        self.id = id

        self.point = 0
        self.grade = None

        self.attended_on_wed = 0
        self.attended_on_weeken = 0


class PlayerManager():
    def __init__(self):
        self.players = {}

    def enroll_player(self, name):
        global id_cnt
        if name not in self.players:
            id_cnt += 1
            self.players[name] = Player(name = name, id=id_cnt)
            print(self.players[name].name, self.players[name].id)
        return self.players[name]

    def get_score(self):
        for attend in attendances:
            self.enroll_player(attend[0])

        for attend in attendances:
            self.get_point(attend[0], attend[1])


        self.get_bonus_point()

        for k,v in self.players.items():
            print( k, v.point)

    def get_point(self, name, day_of_week):
        player = self.players[name]
        if day_of_week == "wednesday":
            player.point += 3
            player.attended_on_wed +=1
        elif day_of_week == "saturday" or day_of_week == "sunday":
            player.point += 2
            player.attended_on_weeken +=1
        else:
            player.point += 1

    def get_bonus_point(self):
        for name, player in self.players.items():
            if player.attended_on_wed > 9:
                player.point += 10
            if player.attended_on_weeken > 9:
                player.point += 10


SILVER_LEVEL = 30
GOLD_LEVEL = 50
player_list = {}
players = {}
id_cnt = 0

points = [0] * 100
grade = [0] * 100
names = [''] * 100
attended_on_wed = [0] * 100
attended_on_weeken = [0] * 100

attendances = []

def score(name, day_of_week):
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
        return id_cnt
    return players[name]

def run():
    read_file()

    player_manager = PlayerManager()
    player_manager.get_score()


    # get_score()
    # get_grade()
    # get_removed_player()


def get_score():
    for attend in attendances:
        score(attend[0], attend[1])
        # player_list.append(Player
    get_bonus_point()


def get_removed_player():
    print("\nRemoved player")
    print("==============")
    for i in range(1, id_cnt + 1):
        if grade[i] not in ("GOLD", "SILVER") and attended_on_wed[i] == 0 and attended_on_weeken[i] == 0:
            print(names[i])


def get_grade():
    gold = Gold(50, "GOLD")
    silver = Silver(30, "SILVER")
    normal = Normal("NORMAL")

    for i in range(1, id_cnt + 1):
        if points[i] >= gold.get_grade_score():
            grade[i] = gold.get_name()
        elif points[i] >= silver.get_grade_score():
            grade[i] = silver.get_name()
        else:
            grade[i] = normal.get_name()

        print(f"NAME : {names[i]}, POINT : {points[i]}, GRADE : {grade[i]}",)


def get_bonus_point():
    for i in range(1, id_cnt + 1):
        if attended_on_wed[i] > 9:
            points[i] += 10
        if attended_on_weeken[i] > 9:
            points[i] += 10

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

if __name__ == "__main__":
    run()