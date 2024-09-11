import csv

def convert_paylines(input_file, output_file):
    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        writer.writerow(['id', 'positions'])
        
        payline_id = 1
        board = []
        for row in reader:
            if not any(row):  # Check for empty row indicating a new board
                if board:
                    positions = []
                    for i in range(3):
                        for j in range(3):
                            if board[i][j] == '1':
                                positions.append(f"{i}-{j}")
                    writer.writerow([payline_id, ';'.join(positions)])
                    payline_id += 1
                    board = []
            else:
                board.append(row)
        
        # Handle the last board if the file does not end with an empty row
        if board:
            positions = []
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '1':
                        positions.append(f"{i}-{j}")
            writer.writerow([payline_id, ';'.join(positions)])

# 파일 경로 설정
input_file = 'csv/payline_original_3X3.csv'
output_file = 'csv/paylines_3x3_1.csv'

# 변환 함수 호출
convert_paylines(input_file, output_file)