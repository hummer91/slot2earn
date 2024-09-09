import random
import csv
import os

# 파일 경로 설정
USER_CSV = "csv/user_data.csv"
SYMBOLS_CSV = "csv/symbols_data.csv"
PAYLINES_CSV = "csv/paylines_data.csv"
LEVELS_CSV = "csv/levels_data.csv"

# 사용자 데이터 저장을 위한 딕셔너리
users_data = {}

# 심볼과 그들의 배당률 및 등장 확률을 저장할 딕셔너리
symbol_multipliers = {}
symbol_probabilities = {}

# 페이라인 정보를 저장할 딕셔너리
paylines = {}

# 레벨 정보를 저장할 딕셔너리 (free_charges 제거)
levels = {}
free_balances_per_level = {}

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
    # CSV 파일에서 레벨 데이터를 불러오기 (free_charges 제거)
    global levels, free_balances_per_level
    if os.path.exists(LEVELS_CSV):
        with open(LEVELS_CSV, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                level = int(row['level'])
                min_spent = int(row['min_spent'])
                free_balance = int(row['free_balance'])
                levels[level] = min_spent
                free_balances_per_level[level] = free_balance
    else:
        print(f"{LEVELS_CSV} 파일을 찾을 수 없습니다.")
        exit()

def calculate_level(total_spent):
    # 총 사용 금액에 따른 레벨 계산
    current_level = 0
    for level, min_spent in sorted(levels.items(), key=lambda x: x[1]):
        if total_spent >= min_spent:
            current_level = level
        else:
            break
    return current_level

def spin_slot_machine(board_size):
    # 슬롯 머신 릴을 무작위로 회전
    reels = []
    symbols = list(symbol_probabilities.keys())
    weights = list(symbol_probabilities.values())
    for _ in range(board_size[0]):
        row = random.choices(symbols, weights, k=board_size[1])
        reels.append(row)
    return reels

def display_reels(reels):
    # 릴 결과를 출력
    for row in reels:
        print(" | ".join(row))
    print()


def calculate_win(reels, selected_paylines, total_bet):
    # 슬롯 머신에서 당첨 배수를 계산하는 함수
    total_winnings = 0
    winning_lines = []

    # 선택한 페이라인에서만 승리 계산
    for line in selected_paylines:
        positions = paylines[line]
        # 선택된 페이라인에 있는 모든 위치가 같은 심볼이면 승리
        if reels[positions[0][0]][positions[0][1]] == reels[positions[1][0]][positions[1][1]] == reels[positions[2][0]][positions[2][1]]:
            winning_symbol = reels[positions[0][0]][positions[0][1]]
            winning_lines.append(winning_symbol)

    # 각 승리 라인에 대해 당첨 심볼의 배당률을 퍼센트로 계산
    for symbol in winning_lines:
        total_winnings += (symbol_multipliers[symbol] / 100) * total_bet
    
    return total_winnings

def calculate_expected_value():
    # 각 심볼의 출현 확률을 총합으로 정규화
    total_prob = sum(symbol_probabilities.values())
    normalized_probabilities = {symbol: prob / total_prob for symbol, prob in symbol_probabilities.items()}

    expected_value = 0

    # 모든 페이라인에 대해 기대값 계산
    for payline_id, positions in paylines.items():
        line_ev = 0
        for symbol, probability in normalized_probabilities.items():
            win_probability = probability ** 3  # 당첨 확률은 각 심볼이 세 번 연속 등장할 확률
            win_multiplier = symbol_multipliers[symbol] / 100  # 배당률을 퍼센트로 해석
            line_ev += win_probability * win_multiplier

        expected_value += line_ev

    print(f"슬롯 머신의 기대값: {expected_value:.4f}")

def load_user_data():
    # CSV 파일에서 사용자 데이터를 불러오기
    if os.path.exists(USER_CSV):
        with open(USER_CSV, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = row['user_id']
                balance = float(row['balance'])
                total_spent = int(row['total_spent'])
                level = int(row['level'])
                free_charges = int(row['free_charges'])
                ad_free_charges = int(row['ad_free_charges'])
                last_played_day = int(row['last_played_day'])
                users_data[user_id] = {
                    "balance": balance,
                    "total_spent": total_spent,
                    "level": level,
                    "spin_count": 0,
                    "free_charges": free_charges,
                    "ad_free_charges": ad_free_charges,
                    "last_played_day": last_played_day
                }
    else:
        print(f"{USER_CSV} 파일을 찾을 수 없습니다.")
        exit()

def save_user_data():
    # 사용자 데이터를 CSV 파일에 저장하기
    with open(USER_CSV, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['user_id', 'balance', 'total_spent', 'level', 'free_charges', 'ad_free_charges', 'last_played_day'])  # 헤더 추가
        for user_id, data in users_data.items():
            writer.writerow([user_id, data['balance'], data['total_spent'], data['level'], data['free_charges'], data['ad_free_charges'], data['last_played_day']])

def get_user_data(user_id):
    # 사용자의 ID로 데이터를 가져오거나, 새로 생성
    if user_id not in users_data:
        users_data[user_id] = {
            "balance": 100,
            "total_spent": 0,
            "level": 0,
            "spin_count": 0,
            "free_charges": 3,  # 기본 무료 충전 횟수
            "ad_free_charges": 3,  # 기본 광고 충전 횟수
            "last_played_day": 0  # 0일로 초기화
        }
    return users_data[user_id]

def update_user_charges(user_data):
    # 무료 충전과 광고 충전 횟수 리셋
    user_data['free_charges'] = 3  # 모든 유저에게 동일하게 3회 제공
    user_data['ad_free_charges'] = 3  # 광고 충전도 3회로 고정

def play_slot_machine():
    user_id = input("사용자 ID를 입력하세요: ").strip().lower()
    
    load_user_data()
    
    if user_id == "admin":
        calculate_expected_value()
        return

    user_data = get_user_data(user_id)

    print(f"현재 잔액: ${user_data['balance']}")
    print(f"현재 레벨: {user_data['level']}")
    print(f"무료 충전 횟수: {user_data['free_charges']}, 광고 충전 횟수: {user_data['ad_free_charges']}, 플레이한 날: {user_data['last_played_day']}")
    
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
    base_bet = 10
    total_bet = base_bet * num_paylines

    print(f"총 베팅 금액은 ${total_bet}입니다.")
    
    while user_data['balance'] >= total_bet or user_data['free_charges'] > 0 or user_data['ad_free_charges'] > 0:
        if user_data['balance'] < total_bet:
            if user_data['free_charges'] > 0:
                print("무료 충전 중...")
                user_data['free_charges'] -= 1
                user_data['balance'] += free_balances_per_level[user_data['level']]
                print(f"무료 충전 완료! 현재 잔액: ${user_data['balance']}, 남은 무료 충전 횟수: {user_data['free_charges']}")
            elif user_data['ad_free_charges'] > 0:
                print("광고 충전 중...")
                user_data['ad_free_charges'] -= 1
                user_data['balance'] += free_balances_per_level[user_data['level']]
                print(f"광고 충전 완료! 현재 잔액: ${user_data['balance']}, 남은 광고 충전 횟수: {user_data['ad_free_charges']}")
            else:
                user_data['last_played_day'] += 1
                update_user_charges(user_data)
                print(f"모든 충전이 소진되었습니다. 새로운 날로 이동. 현재 플레이한 날: {user_data['last_played_day']}")
                break
        
        input("Enter 키를 눌러 슬롯을 돌리세요...")
        
        # Determine board size based on level
        if user_data['level'] >= 60:
            board_size = (5, 3)
        elif user_data['level'] >= 30:
            board_size = (4, 3)
        else:
            board_size = (3, 3)
        
        reels = spin_slot_machine(board_size)
        display_reels(reels)

        user_data['spin_count'] += 1
        user_data['total_spent'] += total_bet

        winnings = calculate_win(reels, selected_paylines, total_bet)
        if winnings > 0:
            print(f"축하합니다! 보상: {winnings}")
            user_data['balance'] += winnings
        else:
            print("아쉽게도, 다시 도전하세요.")
            user_data['balance'] -= total_bet

        previous_level = user_data['level']
        user_data['level'] = calculate_level(user_data['total_spent'])

        if user_data['level'] > previous_level:
            print(f"레벨업! 새로운 레벨: {user_data['level']}")

        print(f"총 릴 돌린 횟수: {user_data['spin_count']}")
        print(f"총 사용 금액: ${user_data['total_spent']}, 현재 레벨: {user_data['level']}")
        print(f"현재 슬롯 배팅 금액: ${total_bet}")
        print(f"현재 잔액: ${user_data['balance']}")
        
        play_again = input("그만 플레이 하겠습니까? (y/n): ")
        if play_again.lower() == 'y':
            break
        print(f"======================================================================")

    print(f"게임 종료. 잔액: ${user_data['balance']}, 레벨: {user_data['level']}, 남은 무료 충전 횟수: {user_data['free_charges']}, 남은 광고 충전 횟수: {user_data['ad_free_charges']}, 플레이한 날: {user_data['last_played_day']}")
    
    save_user_data()

if __name__ == "__main__":
    load_symbol_data()
    load_paylines_data()
    load_levels_data()
    play_slot_machine()