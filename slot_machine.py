import random
import csv
import os

# 사용자 데이터 저장을 위한 딕셔너리
users_data = {}

CSV_FILE = "users_data.csv"
SYMBOLS_CSV = "symbols_data.csv"
PAYLINES_CSV = "paylines_data.csv"

# 심볼과 그들의 배당률 및 등장 확률을 저장할 딕셔너리
symbol_multipliers = {}
symbol_probabilities = {}

# 페이라인 정보를 저장할 리스트
paylines = {}

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
        if reels[positions[0][0]][positions[0][1]] == reels[positions[1][0]][positions[1][1]] == reels[positions[2][0]][positions[2][1]]:
            winning_lines.append(reels[positions[0][0]][positions[0][1]])

    # 당첨 심볼의 배당률을 합산
    for symbol in winning_lines:
        total_multiplier += symbol_multipliers[symbol]
    
    return total_multiplier

def load_user_data():
    # CSV 파일에서 사용자 데이터를 불러오기
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                user_id, balance, spin_count = row
                users_data[user_id] = {
                    "balance": int(balance),
                    "spin_count": int(spin_count)
                }

def save_user_data():
    # 사용자 데이터를 CSV 파일에 저장하기
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        for user_id, data in users_data.items():
            writer.writerow([user_id, data['balance'], data['spin_count']])

def get_user_data(user_id):
    # 사용자의 ID로 데이터를 가져오거나, 새로 생성
    if user_id not in users_data:
        # 새로운 사용자 생성
        users_data[user_id] = {
            "balance": 100,   # 초기 잔액
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

        multiplier = calculate_win(reels, selected_paylines)
        if multiplier > 0:
            winnings = total_bet * multiplier
            print(f"축하합니다! 승리하셨습니다! 보상: {winnings} (배당률 {multiplier}배)")
            user_data['balance'] += winnings
        else:
            print("아쉽게도, 다시 도전하세요.")
            user_data['balance'] -= total_bet  # 패배 시 총 베팅 금액 차감
        
        print(f"현재 잔액: ${user_data['balance']}")
        print(f"총 릴 돌린 횟수: {user_data['spin_count']}")
        
        if user_data['balance'] < total_bet:
            print("잔액이 부족합니다. 게임 종료.")
            break
        
        play_again = input("다시 플레이하시겠습니까? (y/n): ")
        if play_again.lower() != 'y':
            break
    
    print(f"게임이 종료되었습니다, {user_id}. 감사합니다!")
    print(f"최종 잔액: ${user_data['balance']}, 총 릴 돌린 횟수: {user_data['spin_count']}")
    
    # 게임 종료 후 사용자 데이터를 CSV 파일에 저장
    save_user_data()

if __name__ == "__main__":
    # 프로그램 시작 시 심볼 데이터와 페이라인 데이터를 로드
    load_symbol_data()
    load_paylines_data()
    play_slot_machine()

# 추가된 기능 설명

# 	1.	심볼 데이터 로드 (load_symbol_data):
# 	•	symbols_data.csv 파일에서 각 심볼의 등장 확률과 배당률을 읽어옵니다.
# 	2.	페이라인 데이터 로드 (load_paylines_data):
# 	•	paylines_data.csv 파일에서 각 페이라인의 위치 정보를 읽어옵니다. 이 정보를 사용하여 선택된 페이라인에 따라 승리 여부를 계산합니다.
# 	3.	당첨 계산 (calculate_win):
# 	•	선택된 페이라인에서만 승리 여부를 확인하고, 해당 심볼의 배당률을 바탕으로 총 배당률을 계산합니다.