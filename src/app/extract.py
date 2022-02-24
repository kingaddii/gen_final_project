import csv

def raw_data_extract(file_root):
    raw_data = []
    try:
        with open(file_root, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                column = {
                        'date':         row[0],
                        'location':     row[1],
                        'customer':     row[2],
                        'products':     row[3],
                        'total_cost':   row[4],
                        'pay_method':   row[5],
                        'card_no':      row[6]
                        }
                raw_data.append(column)
    except FileNotFoundError as fnfd:
        print("File not found" + str(fnfd))
    except Exception as e:
        print("Something went wrong" + str(e))
    return raw_data
