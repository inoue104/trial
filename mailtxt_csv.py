import csv
import re
import os

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

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            email_content = read_email_from_file(file_path)
            parsed_email = parse_email(email_content)
            rows.append(parsed_email)

    # CSVファイルに保存
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

# メールデータが保存されているフォルダのパス
folder_path = './txt_folder'  # 実際のフォルダパスに置き換えてください
csv_file_path = './emails.csv'

# フォルダ内のメールを処理してCSVファイルに変換
process_emails_in_folder(folder_path, csv_file_path)
