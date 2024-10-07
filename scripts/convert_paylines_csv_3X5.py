import csv

def convert_paylines(input_file, output_file):
    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        writer.writerow(['id', 'positions'])
        
        payline_id = 1
        board = []
        all_paylines = []
        
        for row in reader:
            if not any(row):  # Check for empty row indicating a new board
                if board:
                    positions = []
                    for i in range(3):
                        for j in range(5):
                            if board[i][j] == '1':
                                positions.append(f"{i}-{j}")
                    
                    # Check for duplicate paylines
                    is_duplicate = False
                    for idx, existing_payline in enumerate(all_paylines):
                        if positions == existing_payline:
                            print(f"경고: 페이라인 {payline_id}가 페이라인 {idx + 1}과 동일합니다. 이 페이라인은 변환되지 않습니다.")
                            is_duplicate = True
                            break
                    
                    if not is_duplicate:
                        writer.writerow([payline_id, ';'.join(positions)])
                        all_paylines.append(positions)
                        payline_id += 1
                    
                    board = []
            else:
                board.append(row)
        
        # Handle the last board if the file does not end with an empty row
        if board:
            positions = []
            for i in range(3):
                for j in range(5):
                    if board[i][j] == '1':
                        positions.append(f"{i}-{j}")
            
            # Check for duplicate paylines
            is_duplicate = False
            for idx, existing_payline in enumerate(all_paylines):
                if positions == existing_payline:
                    print(f"경고: 페이라인 {payline_id}가 페이라인 {idx + 1}과 동일합니다. 이 페이라인은 변환되지 않습니다.")
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                writer.writerow([payline_id, ';'.join(positions)])

# 파일 경로 설정
input_file = 'csv/paylines/payline_original_3X5.csv'
output_file = 'csv/paylines/paylines_3x5.csv'

# 변환 함수 호출
convert_paylines(input_file, output_file)