import csv
import re
import os
import shutil

def read_email_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def parse_email(email):
    fields = ['From', 'To', 'Date', 'Subject', 'Message-Id', 'In-Reply-To', 'References', 'Body']
    parsed_email = {}

    # ヘッダと本文を分割
    parts = email.split("\n\n", 1)
    header, body = parts if len(parts) == 2 else (email, "")

    # ヘッダの処理
    for field in fields[:-1]:
        field_value = re.search(f"{field}: (.+)", header)
        parsed_email[field] = field_value.group(1) if field_value else ""

    # 本文の処理（引用部分を除外）
    body_lines = [line for line in body.split("\n") if not line.strip().startswith(">")]
    parsed_email['Body'] = "\n".join(body_lines).strip()

    return parsed_email

def process_emails_in_folder(folder_path, csv_file_path):
    fields = ['From', 'To', 'Date', 'Subject', 'Message-Id', 'In-Reply-To', 'References', 'Body']
    rows = []

    file_list = os.listdir(folder_path)
    print("フォルダ内のファイルは、" + str(len(file_list)) + "個ありました。")
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            email_content = read_email_from_file(file_path)
            parsed_email = parse_email(email_content)
            rows.append(parsed_email)
            print(file_name + " をCSVに変換しました。")
            shutil.move(file_path, appended_folder_path)
            print(file_name + " を移動しました。")

    # CSVファイルに保存（"a"で追記、"w"で上書き）
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        if write_header == True:
            writer.writeheader()
        writer.writerows(rows)
    
    print("フォルダ内のファイル" + str(len(file_list)) + "個をCSVに変換して移動しました。")

# メールデータが保存されているフォルダのパス
folder_path = './txt_folder'
appended_folder_path = './appended_folder'
csv_file_path = './emails.csv'

# csvファイルの確認
fields = ['From', 'To', 'Date', 'Subject', 'Message-Id', 'In-Reply-To', 'References', 'Body']
is_file = os.path.isfile(csv_file_path)
if is_file:
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
        if len(rows) == 0:
                print("データなし")
                write_header = True
        elif fields == rows[0] and rows[1]:
                print("Headerとデータがありますので、csvファイルに追記します。")
                write_header = False
else:
    print("csvファイルを作成します。")
    write_header = True
                
# フォルダ内のメールを処理してCSVファイルに変換
process_emails_in_folder(folder_path, csv_file_path)
