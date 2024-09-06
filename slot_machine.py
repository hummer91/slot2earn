import random

# 슬롯 머신 심볼
symbols = ["🍒", "🍋", "🍊", "🍉", "🔔", "⭐", "7️⃣"]

# 사용자 데이터 저장을 위한 딕셔너리
users_data = {}

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
    if reels[0] == reels[1] == reels[2]:
        return True
    return False

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

if __name__ == "__main__":
    play_slot_machine()

# 추가된 기능 설명

# 	1.	사용자 데이터 관리:
# 	•	users_data 딕셔너리는 각 사용자의 ID를 키로 사용하여 해당 사용자의 잔액과 릴을 돌린 횟수를 저장합니다.
# 	•	get_user_data(user_id) 함수는 주어진 user_id에 대한 데이터를 검색하고, 새로운 사용자일 경우 초기 데이터를 생성합니다.
# 	2.	릴 회전 카운트:
# 	•	사용자가 릴을 돌릴 때마다 spin_count가 증가하도록 하여 사용자가 슬롯 머신을 몇 번 돌렸는지 기록합니다.
# 	3.	잔액과 릴 회전 횟수 표시:
# 	•	매번 슬롯을 돌린 후 현재 잔액과 릴을 돌린 횟수를 화면에 출력합니다.
# 	4.	대기시간 제거:
# 	•	사용자 경험을 빠르게 하기 위해 릴을 돌릴 때 대기 시간을 제거했습니다.