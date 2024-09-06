import random
import csv
import os

# 사용자 데이터 저장을 위한 딕셔너리
users_data = {}

CSV_FILE = "user_data.csv"
SYMBOLS_CSV = "symbols_data.csv"
PAYLINES_CSV = "paylines_data.csv"
LEVELS_CSV = "levels_data.csv"

# 심볼과 그들의 배당률 및 등장 확률을 저장할 딕셔너리
symbol_multipliers = {}
symbol_probabilities = {}

# 페이라인 정보를 저장할 딕셔너리
paylines = {}

# 레벨 정보를 저장할 리스트
levels = []

def load_symbol_data():
    # CSV 파일에서 심볼 데이터를 불러오기
    global symbol_multipliers, symbol_probabilities
    if os.path.exists(SYMBOLS_CSV):
        with open(SYMBOLS_CSV, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                symbol = row['symbol']
                symbol_multipliers[symbol] = int(row['multiplier'])
                symbol_probabilities[symbol] = int(row['probability'])
    else:
        print(f"{SYMBOLS_CSV} 파일을 찾을 수 없습니다.")
        exit()

def load_paylines_data():
    # CSV 파일에서 페이라인 데이터를 불러오기
    global paylines
    if os.path.exists(PAYLINES_CSV):
        with open(PAYLINES_CSV, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                payline_id = int(row['id'])
                positions = row['positions'].split(';')
                paylines[payline_id] = [tuple(map(int, pos.split('-'))) for pos in positions]
    else:
        print(f"{PAYLINES_CSV} 파일을 찾을 수 없습니다.")
        exit()

def load_levels_data():
    # CSV 파일에서 레벨 데이터를 불러오기
    global levels
    if os.path.exists(LEVELS_CSV):
        with open(LEVELS_CSV, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                level = int(row['level'])
                min_spent = int(row['min_spent'])
                levels.append((level, min_spent))
    else:
        print(f"{LEVELS_CSV} 파일을 찾을 수 없습니다.")
        exit()

def calculate_level(total_spent):
    # 총 사용 금액에 따른 레벨 계산
    current_level = 1
    for level, min_spent in sorted(levels, key=lambda x: x[1]):
        if total_spent >= min_spent:
            current_level = level
        else:
            break
    return current_level

def spin_slot_machine():
    # 3x3 슬롯 머신 릴을 무작위로 회전
    reels = []
    symbols = list(symbol_probabilities.keys())
    weights = list(symbol_probabilities.values())
    for _ in range(3):
        row = random.choices(symbols, weights, k=3)
        reels.append(row)
    return reels

def display_reels(reels):
    # 3x3 릴 결과를 출력
    for row in reels:
        print(" | ".join(row))
    print()

def calculate_win(reels, selected_paylines):
    # 슬롯 머신에서 당첨 배수를 계산하는 함수
    total_multiplier = 0
    winning_lines = []

    # 선택한 페이라인에서만 승리 계산
    for line in selected_paylines:
        positions = paylines[line]
        # 선택된 페이라인에 있는 모든 위치가 같은 심볼이면 승리
        if reels[positions[0][0]][positions[0][1]] == reels[positions[1][0]][positions[1][1]] == reels[positions[2][0]][positions[2][1]]:
            winning_symbol = reels[positions[0][0]][positions[0][1]]
            winning_lines.append(winning_symbol)

    # 각 승리 라인에 대해 당첨 심볼의 배당률을 합산
    for symbol in winning_lines:
        total_multiplier += symbol_multipliers[symbol]
    
    return total_multiplier

def load_user_data():
    # CSV 파일에서 사용자 데이터를 불러오기
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                user_id, balance, total_spent, level = row
                users_data[user_id] = {
                    "balance": int(balance),
                    "total_spent": int(total_spent),
                    "level": int(level),
                    "spin_count": 0   # 초기 릴 회전 횟수
                }

def save_user_data():
    # 사용자 데이터를 CSV 파일에 저장하기
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        for user_id, data in users_data.items():
            writer.writerow([user_id, data['balance'], data['total_spent'], data['level']])

def get_user_data(user_id):
    # 사용자의 ID로 데이터를 가져오거나, 새로 생성
    if user_id not in users_data:
        # 새로운 사용자 생성
        users_data[user_id] = {
            "balance": 100,   # 초기 잔액
            "total_spent": 0, # 초기 사용 금액
            "level": 1,       # 초기 레벨
            "spin_count": 0   # 초기 릴 회전 횟수
        }
    return users_data[user_id]

def play_slot_machine():
    user_id = input("사용자 ID를 입력하세요: ")
    
    # CSV에서 사용자 데이터 로드
    load_user_data()
    
    user_data = get_user_data(user_id)

    print(f"슬롯 머신에 오신 것을 환영합니다, {user_id}!")
    print(f"현재 잔액: ${user_data['balance']}")
    print(f"현재 레벨: {user_data['level']} (총 사용 금액: ${user_data['total_spent']})")
    
    # 페이라인 선택
    while True:
        try:
            num_paylines = int(input("몇 개의 페이라인에 베팅하시겠습니까? (1-5): "))
            if 1 <= num_paylines <= len(paylines):
                break
            else:
                print(f"1에서 {len(paylines)} 사이의 숫자를 입력하세요.")
        except ValueError:
            print("유효한 숫자를 입력하세요.")
    
    selected_paylines = list(range(1, num_paylines + 1))
    base_bet = 10  # 기본 베팅 금액
    total_bet = base_bet * num_paylines  # 총 베팅 금액

    print(f"총 베팅 금액은 ${total_bet}입니다. (페이라인 수: {num_paylines})")
    
    while user_data['balance'] >= total_bet:
        input("슬롯을 돌리려면 Enter 키를 누르세요...")

        # 릴 회전
        reels = spin_slot_machine()
        display_reels(reels)

        user_data['spin_count'] += 1  # 릴을 돌린 횟수 증가
        user_data['total_spent'] += total_bet  # 총 사용 금액 증가

        multiplier = calculate_win(reels, selected_paylines)
        if multiplier > 0:
            winnings = total_bet * multiplier
            print(f"축하합니다! 승리하셨습니다! 보상: {winnings} (배당률 {multiplier}배)")
            user_data['balance'] += winnings
        else:
            print("아쉽게도, 다시 도전하세요.")
            user_data['balance'] -= total_bet  # 패배 시 총 베팅 금액 차감
        
        # 레벨 업데이트
        user_data['level'] = calculate_level(user_data['total_spent'])

        print(f"현재 잔액: ${user_data['balance']}")
        print(f"총 릴 돌린 횟수: {user_data['spin_count']}")
        print(f"총 사용 금액: ${user_data['total_spent']}, 현재 레벨: {user_data['level']}")
        
        if user_data['balance'] < total_bet:
            print("잔액이 부족합니다. 게임 종료.")
            break
        
        play_again = input("다시 플레이하시겠습니까? (y/n): ")
        if play_again.lower() != 'y':
            break
    
    print(f"게임이 종료되었습니다, {user_id}. 감사합니다!")
    print(f"최종 잔액: ${user_data['balance']}, 총 릴 돌린 횟수: {user_data['spin_count']}, 총 사용 금액: ${user_data['total_spent']}, 최종 레벨: {user_data['level']}")
    
    # 게임 종료 후 사용자 데이터를 CSV 파일에 저장
    save_user_data()

if __name__ == "__main__":
    # 프로그램 시작 시 심볼 데이터, 페이라인 데이터, 레벨 데이터를 로드
    load_symbol_data()
    load_paylines_data()
    load_levels_data()
    play_slot_machine()

# 추가된 기능 설명

# 	1.	사용자 데이터 구조 업데이트:
# 	•	사용자 데이터에 total_spent(여태까지 슬롯머신에 사용한 비용)과 level(현재 레벨)을 추가했습니다.
# 	2.	레벨 계산 기능 (calculate_level):
# 	•	calculate_level 함수는 사용자가 사용한 총 금액을 기반으로 현재 레벨을 결정합니다.
# 	•	levels_data.csv 파일에서 레벨 기준을 로드하고, 사용 금액에 따라 적절한 레벨을 설정합니다.
# 	3.	CSV 파일 업데이트 및 로드:
# 	•	user_data.csv 파일이 각 사용자의 ID, 잔액, 사용 금액, 레벨을 저장합니다.
# 	•	levels_data.csv 파일은 레벨과 최소 사용 금액을 정의하고, 프로그램 시작 시 이를 로드합니다.
# 	4.	게임 플레이 업데이트:
# 	•	게임을 플레이할 때마다 사용자가 지출한 금액이 업데이트되고, 지출 금액에 따라 사용자의 레벨도 자동으로 업데이트됩니다.