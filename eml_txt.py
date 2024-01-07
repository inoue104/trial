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
    
            # 内容をテキストファイルに書き込む（"a"で追記、"w"で上書き）
            with open(txt_file_path, "a") as txt_file:
                txt_file.write(content)
            print(file_name + " をTXTに変換しました。")

            # TXT変換処理が完了したファイルを移動
            shutil.move(eml_file_path, converted_eml_folder_path)
            print(file_name + " を移動しました。")

    print("フォルダ内のファイル" + str(len(file_list)) + "個を変換して移動しました。")

    return txt_folder_path


eml_folder_path = "./eml_folder"
converted_eml_folder_path = "./converted_folder"
txt_folder_path = "./txt_folder"

# emlフォルダが存在しない場合は作成
if not os.path.exists(eml_folder_path):
    os.makedirs(eml_folder_path)
    print("フォルダが存在しなかったので作成しました。")

# txtフォルダが存在しない場合は作成
if not os.path.exists(txt_folder_path):
    os.makedirs(txt_folder_path)
    print("フォルダが存在しなかったので作成しました。")

# convertedフォルダが存在しない場合は作成
if not os.path.exists(converted_eml_folder_path):
    os.makedirs(converted_eml_folder_path)
    print("フォルダが存在しなかったので作成しました。")

# フォルダ内の全EMLファイルをTXTファイルに変換
converted_txt_folder = eml_to_txt_batch(eml_folder_path, txt_folder_path)
converted_txt_folder
