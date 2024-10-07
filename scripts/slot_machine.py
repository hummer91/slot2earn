import random
import csv
import os

# 파일 경로 설정
USER_CSV = "csv/user_data.csv"
SYMBOLS_CSV_3x3 = "csv/symbols/symbols_3x3.csv"
SYMBOLS_CSV_3x4 = "csv/symbols/symbols_3x4.csv"
SYMBOLS_CSV_3x5 = "csv/symbols/symbols_3x5.csv"
LEVELS_CSV = "csv/levels_data.csv"

# 페이라인 CSV 파일 경로 설정
PAYLINES_CSV_3x3 = "csv/paylines/paylines_3x3.csv"
PAYLINES_CSV_3x4 = "csv/paylines/paylines_3x4.csv"
PAYLINES_CSV_3x5 = "csv/paylines/paylines_3x5.csv"

# 사용자 데이터 저장을 위한 딕셔너리
users_data = {}

# 심볼과 그들의 배당률 및 등장 확률을 저장할 딕셔너리
symbol_multipliers = {}
symbol_probabilities = {}

# 페이라인 정보를 저장할 딕셔너리
paylines = {}

# 레벨 정보를 저장할 딕셔너리 (free_charges 제거)
levels = {}
free_points_per_level = {}
max_auto_spin_per_level = {}
max_paylines_per_level = {}

def load_symbol_data(board_size):
    # CSV 파일에서 심볼 데이터를 불러오기
    global symbol_multipliers, symbol_probabilities
    symbol_multipliers.clear()
    symbol_probabilities.clear()
    
    if board_size == (3, 3):
        csv_file = SYMBOLS_CSV_3x3
    elif board_size == (3, 4):
        csv_file = SYMBOLS_CSV_3x4
    elif board_size == (3, 5):
        csv_file = SYMBOLS_CSV_3x5
    else:
        print("지원되지 않는 보드 크기입니다.")
        exit()

    if os.path.exists(csv_file):
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                symbol = row['symbol']
                symbol_probabilities[symbol] = int(row['probability'])
                if board_size == (3, 3):
                    symbol_multipliers[symbol] = int(row['multiplier'])
                elif board_size == (3, 4):
                    symbol_multipliers[symbol] = {
                        4: int(row['multiplier_4']),
                        3: int(row['multiplier_3'])
                    }
                elif board_size == (3, 5):
                    symbol_multipliers[symbol] = {
                        5: int(row['multiplier_5']),
                        4: int(row['multiplier_4']),
                        3: int(row['multiplier_3'])
                    }
    else:
        print(f"{csv_file} 파일을 찾을 수 없습니다.")
        exit()

def load_paylines_data(board_size):
    # CSV 파일에서 페이라인 데이터를 불러오기
    global paylines
    paylines.clear()
    if board_size == (3, 3):
        csv_file = PAYLINES_CSV_3x3
    elif board_size == (3, 4):
        csv_file = PAYLINES_CSV_3x4
    elif board_size == (3, 5):
        csv_file = PAYLINES_CSV_3x5
    else:
        print("지원되지 않는 보드 크기입니다.")
        exit()

    if os.path.exists(csv_file):
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                payline_id = int(row['id'])
                positions = row['positions'].split(';')
                paylines[payline_id] = [tuple(map(int, pos.split('-'))) for pos in positions]
    else:
        print(f"{csv_file} 파일을 찾을 수 없습니다.")
        exit()

def load_levels_data():
    global levels, free_points_per_level, max_auto_spin_per_level, max_paylines_per_level, level_up_bonus, min_bet_per_level, bet_set_per_level
    level_up_bonus = {}
    min_bet_per_level = {}
    bet_set_per_level = {}
    if os.path.exists(LEVELS_CSV):
        with open(LEVELS_CSV, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                level = int(row['level'])
                xp_needed = int(row['xp_needed'])
                daily_free_points = int(row['daily_free_points'])
                max_auto_spin = int(row['max_auto_spin'])
                max_paylines = int(row['max_paylines'])
                bonus = int(row['level_up_bonus'])
                min_bet = int(row['min_bet'])
                bet_set = [int(bet) for bet in row['bet_set'].split(',')]
                levels[level] = xp_needed
                free_points_per_level[level] = daily_free_points
                max_auto_spin_per_level[level] = max_auto_spin
                max_paylines_per_level[level] = max_paylines
                level_up_bonus[level] = bonus
                min_bet_per_level[level] = min_bet
                bet_set_per_level[level] = bet_set
    else:
        print(f"{LEVELS_CSV} 파일을 찾을 수 없습니다.")
        exit()

def calculate_level(xp):
    # 총 사용 금액에 따른 레벨 계산
    current_level = 1
    for level, xp_needed in sorted(levels.items(), key=lambda x: x[1]):
        if xp >= xp_needed:
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

def display_reels(reels, spin_number=None):
    # 릴 결과를 출력
    if spin_number is not None:
        print(f"Spin #{spin_number}")
        print("======================================================================")
    for row in reels:
        print(" | ".join(row))
    print()

def calculate_win(reels, selected_paylines, bet_size, board_size):
    # 슬롯 머신에서 당첨 배수를 계산하는 함수
    total_winnings = 0
    winning_lines = []

    # 선택한 페이라인에서만 승리 계산
    for line in selected_paylines:
        positions = paylines[line]
        symbols_in_line = [reels[row][col] for row, col in positions]
        
        if board_size == (3, 3):
            # 3개의 연속된 항목이 모두 같은 경우
            if len(set(symbols_in_line)) == 1:
                winning_symbol = symbols_in_line[0]
                winning_lines.append((winning_symbol, 1.0))  # 100% 당첨
        elif board_size == (3, 4):
            # 4개의 연속된 항목이 모두 같은 경우
            if len(set(symbols_in_line)) == 1:
                winning_symbol = symbols_in_line[0]
                winning_lines.append((winning_symbol, 4))  # 4개 당첨
            # 3개의 연속된 항목이 같은 경우
            elif len(set(symbols_in_line[:3])) == 1 or len(set(symbols_in_line[1:])) == 1:
                winning_symbol = symbols_in_line[0] if len(set(symbols_in_line[:3])) == 1 else symbols_in_line[1]
                winning_lines.append((winning_symbol, 3))  # 3개 당첨
        elif board_size == (3, 5):
            # 5개의 연속된 항목이 모두 같은 경우
            if len(set(symbols_in_line)) == 1:
                winning_symbol = symbols_in_line[0]
                winning_lines.append((winning_symbol, 5))  # 5개 당첨
            # 4개의 연속된 항목이 같은 경우
            elif len(set(symbols_in_line[:4])) == 1 or len(set(symbols_in_line[1:])) == 1:
                winning_symbol = symbols_in_line[0] if len(set(symbols_in_line[:4])) == 1 else symbols_in_line[1]
                winning_lines.append((winning_symbol, 4))  # 4개 당첨
            # 3개의 연속된 항목이 같은 경우
            elif len(set(symbols_in_line[:3])) == 1 or len(set(symbols_in_line[2:])) == 1:
                winning_symbol = symbols_in_line[0] if len(set(symbols_in_line[:3])) == 1 else symbols_in_line[2]
                winning_lines.append((winning_symbol, 3))  # 3개 당첨

    # 각 승리 라인에 대해 당첨 심볼의 배당률을 퍼센트로 계산
    for symbol, multiplier in winning_lines:
        if board_size == (3, 3):
            total_winnings += (symbol_multipliers[symbol] / 100) * bet_size * multiplier
        else:
            total_winnings += (symbol_multipliers[symbol][multiplier] / 100) * bet_size
    
    return total_winnings

def calculate_expected_value(board_size):
    # 각 심볼의 출현 확률을 총합으로 정규화
    total_prob = sum(symbol_probabilities.values())
    normalized_probabilities = {symbol: prob / total_prob for symbol, prob in symbol_probabilities.items()}

    expected_value = 0

    # 모든 페이라인에 대해 기대값 계산
    for payline_id, positions in paylines.items():
        line_ev = 0
        for symbol, probability in normalized_probabilities.items():
            if board_size == (3, 3):
                win_probability = probability ** 3  # 당첨 확률은 각 심볼이 세 번 연속 등장할 확률
                win_multiplier = symbol_multipliers[symbol] / 100  # 배당률을 퍼센트로 해석
            elif board_size == (3, 4):
                win_probability = probability ** 4  # 당첨 확률은 각 심볼이 네 번 연속 등장할 확률
                win_multiplier = symbol_multipliers[symbol][4] / 100  # 배당률을 퍼센트로 해석
            elif board_size == (3, 5):
                win_probability = probability ** 5  # 당첨 확률은 각 심이 다섯 번 연속 등장할 확률
                win_multiplier = symbol_multipliers[symbol][5] / 100  # 배당률을 퍼센트로 해석
            line_ev += win_probability * win_multiplier

        expected_value += line_ev

    return expected_value

def load_user_data():
    # CSV 파일에서 사용자 데이터를 불러오기
    if os.path.exists(USER_CSV):
        with open(USER_CSV, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = row['user_id']
                points = float(row['points'])
                total_spent = int(row['total_spent'])
                level = int(row['level'])
                free_charges = int(row['free_charges'])
                ad_free_charges = int(row['ad_free_charges'])
                last_played_day = int(row['last_played_day'])
                xp = int(row.get('xp', 0))  # Add xp field
                users_data[user_id] = {
                    "points": points,
                    "total_spent": total_spent,
                    "level": level,
                    "spin_count": 0,
                    "free_charges": free_charges,
                    "ad_free_charges": ad_free_charges,
                    "last_played_day": last_played_day,
                    "xp": xp  # Initialize xp
                }
    else:
        print(f"{USER_CSV} 파일을 찾을 수 없습니다.")
        exit()

def save_user_data():
    # 사용자 데이터를 CSV 파일에 저장하기
    with open(USER_CSV, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['user_id', 'points', 'total_spent', 'level', 'free_charges', 'ad_free_charges', 'last_played_day', 'xp'])  # Add xp to header
        for user_id, data in users_data.items():
            writer.writerow([user_id, data['points'], data['total_spent'], data['level'], data['free_charges'], data['ad_free_charges'], data['last_played_day'], data['xp']])

def get_user_data(user_id):
    # 사용자의 ID로 데이터를 가져오거나, 새로 생성
    if user_id not in users_data:
        users_data[user_id] = {
            "points": free_points_per_level[1],
            "total_spent": 0,
            "level": 1,
            "spin_count": 0,
            "free_charges": 3,  # 기본 무료 충전 횟수
            "ad_free_charges": 3,  # 기본 광고 충전 횟수
            "last_played_day": 0,  # 0일로 초기화
            "xp": 0
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
        for board_size in [(3, 3), (3, 4), (3, 5)]:
            load_symbol_data(board_size)
            load_paylines_data(board_size)
            ev = calculate_expected_value(board_size)
            print(f"{board_size[0]}x{board_size[1]} 보드의 환수율: {ev:.4f}")
        return

    user_data = get_user_data(user_id)

    # Determine board size based on level
    if user_data['level'] >= 60:
        board_size = (3, 5)
    elif user_data['level'] >= 30:
        board_size = (3, 4)
    else:
        board_size = (3, 3)
    
    load_symbol_data(board_size)
    load_paylines_data(board_size)
    xp_needed = levels[user_data['level']+1]
    print(f"현재 포인트: {user_data['points']} //// 현재 레벨: {user_data['level']} //// 현재 경험치: {user_data['xp']} /// 필요 경험치: {xp_needed}")
    print(f"무료 충전 횟수: {user_data['free_charges']}, 광고 충전 횟수: {user_data['ad_free_charges']}, 플레이한 날: {user_data['last_played_day']}")

    max_auto_spins = max_auto_spin_per_level[user_data['level']]
    max_paylines = max_paylines_per_level[user_data['level']]
    min_bet = min_bet_per_level[user_data['level']]
    bet_set = bet_set_per_level[user_data['level']]
    
    # 배팅 금액 선택 로직
    print("배팅 금액을 선택하세요:")
    for i, bet in enumerate(bet_set, 1):
        print(f"{i}. {bet} 포인트")
    while True:
        choice = input("선택: ")
        if choice.isdigit() and 1 <= int(choice) <= len(bet_set):
            bet_size = bet_set[int(choice) - 1]
            break
        else:
            print("올바른 선택지를 입력해주세요.")
    
    selected_paylines = list(range(1, max_paylines + 1))
    total_bet = bet_size * max_paylines

    print(f"총 베팅 금액은 {bet_size}X{max_paylines} = {total_bet} 포인트입니다.")
    
    while user_data['points'] >= total_bet or user_data['free_charges'] > 0 or user_data['ad_free_charges'] > 0:
        if user_data['points'] < total_bet:
            if user_data['free_charges'] > 0:
                print("무료 충전 중...")
                user_data['free_charges'] -= 1
                user_data['points'] += free_points_per_level[user_data['level']]
                print(f"무료 충전 완료! 현재 포인트: {user_data['points']}, 남은 무료 충전 횟수: {user_data['free_charges']}")
            elif user_data['ad_free_charges'] > 0:
                print("광고 충전 중...")
                user_data['ad_free_charges'] -= 1
                user_data['points'] += free_points_per_level[user_data['level']]
                print(f"광고 충전 완료! 현재 포인트: {user_data['points']}, 남은 광고 충전 횟수: {user_data['ad_free_charges']}")
            else:
                user_data['last_played_day'] += 1
                update_user_charges(user_data)
                print(f"모든 충전이 소진되었습니다. 새로운 날로 이동. 현재 플레이한 날: {user_data['last_played_day']}")
                break
        
        input("Enter 키를 눌러 슬롯을 돌리세요...")

        for spin_number in range(1, max_auto_spins + 1):
            if user_data['points'] < total_bet:
                break

            reels = spin_slot_machine(board_size)
            display_reels(reels, spin_number)

            user_data['spin_count'] += 1
            user_data['total_spent'] += total_bet
            user_data['points'] -= total_bet
            user_data['xp'] += total_bet  # Add xp based on total_bet

            winnings = calculate_win(reels, selected_paylines, bet_size, board_size)
            if winnings > 0:
                print(f"축하합니다! 보상: {winnings} 포인트")
                user_data['points'] += winnings
            else:
                print("아쉽게도, 다시 도전하세요.")

            previous_level = user_data['level']
            user_data['level'] = calculate_level(user_data['xp'])

            if user_data['level'] > previous_level:
                print(f"레벨업! 새로운 레벨: {user_data['level']}")
                # 레벨업 보너스 추가
                user_data['points'] += level_up_bonus[user_data['level']]
                print(f"레벨업 보너스 추가! 현재 포인트: {user_data['points']}")
                # Adjust xp for the new level
                user_data['xp'] -= levels[user_data['level']]
                # Reload symbols and paylines if level changes
                if user_data['level'] >= 60:
                    board_size = (3, 5)
                elif user_data['level'] >= 30:
                    board_size = (3, 4)
                else:
                    board_size = (3, 3)
                load_symbol_data(board_size)
                load_paylines_data(board_size)
                
            xp_needed = levels[user_data['level']+1]
            print(f"총 릴 돌린 횟수: {user_data['spin_count']}")
            print(f"총 사용 금액: {user_data['total_spent']} 포인트")
            print(f"현재 포인트: {user_data['points']} //// 현재 레벨: {user_data['level']} //// 현재 경험치: {user_data['xp']} /// 필요 경험치: {xp_needed}")
        
        play_again = input("그만 플레이 하겠습니까? (y): ")
        if play_again.lower() == 'y':
            break
        print(f"======================================================================")

    print(f"게임 종료. 포인트: {user_data['points']}, 레벨: {user_data['level']}, 남은 무료 충전 횟수: {user_data['free_charges']}, 남은 광고 충전 횟수: {user_data['ad_free_charges']}, 플레이한 날: {user_data['last_played_day']}")
    
    save_user_data()

if __name__ == "__main__":
    load_levels_data()
    play_slot_machine()


# 일일 보상 시스템: 매일 로그인 시 보상을 제공하는 기능이 구현되지 않았습니다.
# 광고 시청 후 포인트 지급: 광고 시청에 대한 보상 시스템이 구현되지 않았습니다. 현재는 단순히 광고 충전 횟수만 감소시키고 있습니다.
# 특별 이벤트 또는 보너스 게임: 특별한 이벤트나 보너스 게임 기능이 구현되지 않았습니다.
# 소셜 기능: 친구 초대, 선물 주고받기 등의 소셜 기능이 구현되지 않았습니다.
# 상점 시스템: 아이템 구매나 포인트 구매 등을 할 수 있는 상점 시스템이 구현되지 않았습니다.
# 업적 시스템: 특정 조건을 달성했을 때 보상을 주는 업적 시스템이 구현되지 않았습니다.
# 통계 및 분석 기능: 플레이어의 게임 플레이 데이터를 분석하고 표시하는 기능이 구현되지 않았습니다.