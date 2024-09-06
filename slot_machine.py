import random
import csv
import os

# 슬롯 머신 심볼
symbols = ["🍒", "🍋", "🍊", "🍉", "🔔", "⭐", "7️⃣"]

# 사용자 데이터 저장을 위한 딕셔너리
users_data = {}

CSV_FILE = "users_data.csv"

def spin_slot_machine():
    # 슬롯 머신의 각 릴을 무작위로 회전
    reel1 = random.choice(symbols)
    reel2 = random.choice(symbols)
    reel3 = random.choice(symbols)
    return reel1, reel2, reel3

def display_reels(reels):
    # 릴 결과를 출력
    print(f"{reels[0]} | {reels[1]} | {reels[2]}")

def check_win(reels):
    # 모든 릴이 같은 경우에만 승리
    return reels[0] == reels[1] == reels[2]

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

        if check_win(reels):
            print("축하합니다! 승리하셨습니다!")
            user_data['balance'] += bet * 10  # 승리 시 배팅 금액의 10배를 지급
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

# 	1.	CSV 파일에서 사용자 데이터 불러오기 (load_user_data):
# 	•	프로그램 시작 시 load_user_data() 함수가 호출되어 users_data.csv 파일에서 사용자 데이터를 읽어옵니다. 파일이 존재하지 않으면 무시하고, 존재할 경우 사용자 정보를 딕셔너리에 로드합니다.
# 	2.	CSV 파일에 사용자 데이터 저장하기 (save_user_data):
# 	•	프로그램이 종료될 때 save_user_data() 함수가 호출되어 모든 사용자 데이터를 users_data.csv 파일에 저장합니다.
# 	3.	사용자 데이터 관리:
# 	•	get_user_data(user_id) 함수는 사용자가 이미 존재하는지 확인하고, 존재하지 않으면 초기 데이터를 생성합니다.
# 	4.	게임 실행 순서:
# 	•	사용자 ID를 입력받고, 해당 ID에 따라 데이터를 로드합니다.
# 	•	게임이 진행되는 동안 사용자의 잔액과 릴 회전 횟수가 업데이트됩니다.
# 	•	게임 종료 시 사용자 데이터를 CSV 파일에 저장합니다.