import os
from email import policy
from email.parser import BytesParser
import shutil

def eml_to_txt_batch(eml_folder_path, txt_folder_path):
    """
    フォルダ内の全EMLファイルをTXTファイルに変換する。

    :param eml_folder_path: EMLファイルが含まれるフォルダのパス。
    :param txt_folder_path: 生成されたTXTファイルを保存するフォルダのパス。
    """

    # フォルダ内の各EMLファイルを処理
    file_list = os.listdir(eml_folder_path)
    print("フォルダ内のファイルは、" + str(len(file_list)) + "個ありました。")
    for file_name in file_list:
        if file_name.endswith(".eml"):
            eml_file_path = os.path.join(eml_folder_path, file_name)
            txt_file_name = file_name.replace('.eml', '.txt')
            txt_file_path = os.path.join(txt_folder_path, txt_file_name)

            with open(eml_file_path, 'rb') as f:
                msg = BytesParser(policy=policy.default).parse(f)

            # メールから日付、件名、送信者、受信者、本文を抽出
            content = f"Date: {msg['date']}\n"
            content += f"Subject: {msg['subject']}\n"
            content += f"From: {msg['from']}\n"
            content += f"To: {msg['to']}\n"
            content += f"Message-Id: {msg['Message-Id']}\n"
            content += f"In-Reply-To: {msg['In-Reply-To']}\n"
            content += f"References: {msg['References']}\n"
            content += "\n" + msg.get_body(preferencelist=('plain',)).get_content()
    
            # 内容をテキストファイルに書き込む
            with open(txt_file_path, "w") as txt_file:
                txt_file.write(content)

    return txt_folder_path

eml_folder_path = "./eml_folder"
txt_folder_path = "./txt_folder"

# emlフォルダが存在しない場合は作成
if not os.path.exists(txt_folder_path):
    os.makedirs(txt_folder_path)
    print("フォルダが存在しなかったので作成しました。")

# txtフォルダが存在しない場合は作成
if not os.path.exists(txt_folder_path):
    os.makedirs(txt_folder_path)
    print("フォルダが存在しなかったので作成しました。")

# サンプルEMLファイル用のフォルダを作成
#sample_eml_folder = "/mnt/data/sample_emls"
#os.makedirs(sample_eml_folder, exist_ok=True)

# サンプルEMLファイルをフォルダにコピー
#shutil.copy("/mnt/data/sample.eml", os.path.join(sample_eml_folder, "sample1.eml"))
#shutil.copy("/mnt/data/sample_with_date.eml", os.path.join(sample_eml_folder, "sample2.eml"))

# 変換されたTXTファイル用のフォルダ
#txt_folder_path = "/mnt/data/converted_txts"
#os.makedirs(txt_folder_path, exist_ok=True)

# フォルダ内の全EMLファイルをTXTファイルに変換
converted_txt_folder = eml_to_txt_batch(eml_folder_path, txt_folder_path)
converted_txt_folder
