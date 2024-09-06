import random
import csv
import os

# 슬롯 머신 심볼과 배당률 설정
symbols = ["🍒", "🍋", "🍊", "🍉", "🔔", "⭐", "7️⃣"]
symbol_multipliers = {
    "🍒": 2,
    "🍋": 3,
    "🍊": 4,
    "🍉": 5,
    "🔔": 6,
    "⭐": 7,
    "7️⃣": 10
}

# 사용자 데이터 저장을 위한 딕셔너리
users_data = {}

CSV_FILE = "users_data.csv"

def spin_slot_machine():
    # 3x3 슬롯 머신 릴을 무작위로 회전
    return [[random.choice(symbols) for _ in range(3)] for _ in range(3)]

def display_reels(reels):
    # 3x3 릴 결과를 출력
    for row in reels:
        print(" | ".join(row))
    print()

def calculate_win(reels, selected_paylines):
    # 슬롯 머신에서 당첨 배수를 계산하는 함수
    total_multiplier = 0
    winning_lines = []

    # 페이라인에 따른 당첨 계산
    paylines = {
        1: [reels[0][0], reels[0][1], reels[0][2]],  # 첫 번째 행
        2: [reels[1][0], reels[1][1], reels[1][2]],  # 두 번째 행
        3: [reels[2][0], reels[2][1], reels[2][2]],  # 세 번째 행
        4: [reels[0][0], reels[1][1], reels[2][2]],  # 왼쪽 위에서 오른쪽 아래 대각선
        5: [reels[0][2], reels[1][1], reels[2][0]],  # 오른쪽 위에서 왼쪽 아래 대각선
    }

    # 선택한 페이라인에서만 승리 계산
    for line in selected_paylines:
        if paylines[line][0] == paylines[line][1] == paylines[line][2]:
            winning_lines.append(paylines[line][0])

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
            if 1 <= num_paylines <= 5:
                break
            else:
                print("1에서 5 사이의 숫자를 입력하세요.")
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
    play_slot_machine()

# 업데이트된 기능 설명

# 	1.	페이라인 선택:
# 	•	사용자는 게임을 시작하기 전에 1에서 5 사이의 페이라인 수를 선택할 수 있습니다.
# 	•	선택한 페이라인 수는 selected_paylines 리스트에 저장됩니다.
# 	2.	베팅 금액 계산:
# 	•	베팅 금액은 기본 베팅 금액 x 선택한 페이라인 수로 계산됩니다.
# 	•	예를 들어, 기본 베팅 금액이 10이고 사용자가 3개의 페이라인을 선택하면 총 베팅 금액은 30이 됩니다.
# 	3.	페이라인에 따른 당첨 계산:
# 	•	calculate_win() 함수는 선택된 페이라인에서만 승리 여부를 확인하고, 당첨 배수를 계산합니다.
# 	•	각 페이라인에 대해 심볼이 일치하면 해당 심볼의 배당률을 합산하여 승리 배수를 결정합니다.
# 	4.	게임 진행:
# 	•	사용자는 선택한 페이라인 수에 따라 증가된 베팅 금액을 걸고, 릴을 돌립니다.
# 	•	승리하면 배당률에 따른 보상을 받고, 패배하면 베팅 금액만큼 잔액이 차감됩니다.