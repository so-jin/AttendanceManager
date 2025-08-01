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
    name = "GOLD"

    def __init__(self, grade_score):
        self.grade_score = grade_score

    def get_grade_score(self):
        return self.grade_score

    def get_name(self):
        return self.name

class Silver(BaseClass):
    name = "SILVER"
    def __init__(self, grade_score):
        self.grade_score = grade_score

    def get_grade_score(self):
        return self.grade_score

    def get_name(self):
        return self.name

class Normal(BaseClass):
    name = "NORMAL"
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

    def calculate_point(self, day_of_week):
        if day_of_week == "wednesday":
            self.point += 3
            self.attended_on_wed += 1
        elif day_of_week == "saturday" or day_of_week == "sunday":
            self.point += 2
            self.attended_on_weeken += 1
        else:
            self.point += 1

    def calculate_bonus_point(self):
        if self.attended_on_wed > 9:
            self.point += 10
        if self.attended_on_weeken > 9:
            self.point += 10

    def get_grade(self):
        gold = Gold(50)
        silver = Silver(30)
        normal = Normal()

        if self.point >= gold.get_grade_score():
            self.grade = gold.get_name()
        elif self.point >= silver.get_grade_score():
            self.grade = silver.get_name()
        else:
            self.grade = normal.get_name()

class PlayerManager():
    def __init__(self, attendances):
        self.players = {}
        self.attendances = attendances

    def enroll_player(self):
        global id_cnt
        for attend in self.attendances:
            name = attend[0]
            if name not in self.players:
                id_cnt += 1
                self.players[name] = Player(name = name, id=id_cnt)

    def get_players_scores(self):
        self.calculate_players_point()
        self.calculate_players_bonus_point()

    def calculate_players_point(self):
        for attend in self.attendances:
            name = attend[0]
            day_of_week = attend[1]
            player = self.players[name]
            player.calculate_point(day_of_week)


    def calculate_players_bonus_point(self):
        for name, player in self.players.items():
            player.calculate_bonus_point()

    def get_players_grade(self):
        for name, player in self.players.items():
            player.get_grade()
            print(f"NAME : {player.name}, POINT : {player.point}, GRADE : {player.grade}", )


    def get_removed_player(self):
        print("\nRemoved player")
        print("==============")
        for name, player in self.players.items():
            if player.grade not in (Gold.name, Silver.name) and player.attended_on_wed == 0 and player.attended_on_weeken == 0:
                print(name)


id_cnt = 0

def run():

    attendances = read_file("attendance_weekday_500.txt")
    player_manager = PlayerManager(attendances)
    player_manager.enroll_player()
    player_manager.get_players_scores()
    player_manager.get_players_grade()
    player_manager.get_removed_player()


def read_file(file_path):
    try:
        attendances = []
        with open(file_path, encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    attendances.append([parts[0], parts[1]])
        return attendances

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

