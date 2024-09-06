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

def calculate_win(reels):
    # 슬롯 머신에서 당첨 배수를 계산하는 함수
    total_multiplier = 0
    winning_lines = []

    # 가로 라인 검사
    for row in reels:
        if row[0] == row[1] == row[2]:
            winning_lines.append(row[0])
    
    # 세로 라인 검사
    for col in range(3):
        if reels[0][col] == reels[1][col] == reels[2][col]:
            winning_lines.append(reels[0][col])
    
    # 대각선 검사
    if reels[0][0] == reels[1][1] == reels[2][2]:
        winning_lines.append(reels[0][0])
    if reels[0][2] == reels[1][1] == reels[2][0]:
        winning_lines.append(reels[0][2])

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
    
    bet = 10  # 베팅 금액
    
    while user_data['balance'] >= bet:
        input("슬롯을 돌리려면 Enter 키를 누르세요...")

        # 릴 회전
        reels = spin_slot_machine()
        display_reels(reels)

        user_data['spin_count'] += 1  # 릴을 돌린 횟수 증가

        multiplier = calculate_win(reels)
        if multiplier > 0:
            winnings = bet * multiplier
            print(f"축하합니다! 승리하셨습니다! 보상: {winnings} (배당률 {multiplier}배)")
            user_data['balance'] += winnings
        else:
            print("아쉽게도, 다시 도전하세요.")
            user_data['balance'] -= bet  # 패배 시 배팅 금액 차감
        
        print(f"현재 잔액: ${user_data['balance']}")
        print(f"총 릴 돌린 횟수: {user_data['spin_count']}")
        
        if user_data['balance'] < bet:
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

# 추가된 기능 설명

# 	1.	3x3 슬롯머신:
# 	•	spin_slot_machine() 함수는 이제 3x3 형태의 2차원 리스트를 반환하여 슬롯 머신 릴의 결과를 표현합니다.
# 	2.	심볼 별 당첨 배수 설정:
# 	•	symbol_multipliers 딕셔너리는 각 심볼에 대한 배당률을 정의합니다. 예를 들어, “🍒”는 2배, “7️⃣”는 10배 등의 배당률을 가집니다.
# 	3.	당첨 계산 함수 (calculate_win):
# 	•	3x3 슬롯머신에서 가로, 세로, 대각선으로 일치하는 라인을 확인하여 승리 여부를 결정합니다.
# 	•	각 당첨 라인에 따라 해당 심볼의 배당률을 합산하여 총 배당률을 계산합니다.
# 	4.	게임 결과 및 보상 계산:
# 	•	사용자가 슬롯을 돌린 후 calculate_win() 함수를 통해 당첨 배수를 계산하고, 해당 배수에 따라 보상을 지급합니다.
# 	•	보상이 있으면 잔액을 증가시키고, 보상이 없으면 베팅 금액을 차감합니다.