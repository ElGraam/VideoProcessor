import os
import socket
import argparse
from tqdm import tqdm

# サーバの設定
SERVER_HOST = 'localhost'
SERVER_PORT = 65432
BUFFER_SIZE = 1400
TIMEOUT = 10  # タイムアウト時間（秒）

def is_mp4_file(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lower() == '.mp4'

def send_file(file_path):
    # ファイルがmp4形式であることを確認
    if not is_mp4_file(file_path):
        print('Error: File must be in mp4 format.')
        return
    
    # ファイルサイズを取得
    file_size = os.path.getsize(file_path)
    
    try:
        # サーバに接続
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)  # タイムアウトを設定
            s.connect((SERVER_HOST, SERVER_PORT))
            
            # ファイルサイズを送信
            s.sendall(file_size.to_bytes(32, byteorder='big'))
            
            # ファイルを読み込んで送信
            progress_bar = tqdm(total=file_size, unit='B', unit_scale=True)
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(BUFFER_SIZE)
                    if not data:
                        break
                    s.sendall(data)
                    progress_bar.update(len(data))
            progress_bar.close()
            
            # レスポンスを受信
            response = s.recv(16)
            status_code = int(response[:2])
            status_message = response[2:].decode().strip()
            
            if status_code == 0:
                print('File uploaded successfully.')
            else:
                print(f'Error: {status_message}')
    
    except socket.timeout:
        print('Error: Connection timed out.')
    
    except socket.error as e:
        print(f'Error: {str(e)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File upload client')
    parser.add_argument('file', help='File to upload')
    args = parser.parse_args()
    
    send_file(args.file)