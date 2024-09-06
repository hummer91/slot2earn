import random
import time

# 슬롯 머신 심볼
symbols = ["🍒", "🍋", "🍊", "🍉", "🔔", "⭐", "7"]

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

def play_slot_machine():
    balance = 100  # 초기 잔액
    bet = 10       # 베팅 금액

    print("슬롯 머신에 오신 것을 환영합니다!")
    print(f"현재 잔액: ${balance}")
    
    while balance >= bet:
        input("슬롯을 돌리려면 Enter 키를 누르세요...")

        print("슬롯 돌리는 중...")
        time.sleep(1)  # 효과를 위해 잠시 대기
        
        reels = spin_slot_machine()
        display_reels(reels)

        if check_win(reels):
            print("축하합니다! 승리하셨습니다!")
            balance += bet * 10  # 승리 시 배팅 금액의 10배를 지급
        else:
            print("아쉽게도, 다시 도전하세요.")
            balance -= bet  # 패배 시 배팅 금액 차감
        
        print(f"현재 잔액: ${balance}")
        
        if balance < bet:
            print("잔액이 부족합니다. 게임 종료.")
            break
        
        play_again = input("다시 플레이하시겠습니까? (y/n): ")
        if play_again.lower() != 'y':
            break
    
    print("게임이 종료되었습니다. 감사합니다!")

if __name__ == "__main__":
    play_slot_machine()


# 코드 설명

# 	1.	심볼 설정: 슬롯 머신의 심볼을 리스트로 정의합니다.
# 	2.	슬롯 머신 회전 함수 (spin_slot_machine): 각 릴을 무작위로 선택하여 반환합니다.
# 	3.	릴 결과 출력 함수 (display_reels): 릴의 결과를 형식에 맞게 출력합니다.
# 	4.	승리 조건 확인 함수 (check_win): 모든 릴의 결과가 동일한 경우를 승리로 간주합니다.
# 	5.	메인 게임 함수 (play_slot_machine): 게임의 로직을 담당합니다. 초기 잔액을 설정하고 사용자의 입력을 받아 슬롯을 돌립니다. 
#       게임이 진행되는 동안 승리 및 패배 여부를 확인하고 잔액을 업데이트합니다. 사용자가 다시 플레이할지 여부를 선택할 수 있습니다.