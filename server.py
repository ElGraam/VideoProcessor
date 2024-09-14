import asyncio
import aiofile
import os
import time
import argparse
import logging
import multiprocessing
import shutil
import uuid

# ロギングの設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# サーバの設定
HOST = 'localhost'
BUFFER_SIZE = 1400
STORAGE_DIR = './uploads'

async def handle_client(reader, writer):
    client_id = str(uuid.uuid4())[:8]
    logging.info(f'Connected by {client_id}')

    try:
        # ファイルサイズを受信
        file_size_data = await reader.read(32)
        file_size = int.from_bytes(file_size_data, byteorder='big')
        logging.info(f'File size: {file_size} bytes')

        # 保存先ディレクトリの容量を確認
        total, used, free = shutil.disk_usage(STORAGE_DIR)
        logging.info(f'Total disk space: {total} bytes')
        logging.info(f'Used disk space: {used} bytes')
        logging.info(f'Free disk space: {free} bytes')
        if free < file_size:
            status_code = 1  # エラーを示すステータスコード
            status_message = f'{status_code:02d}Not enough disk space.'.encode()
            status_message = status_message[:16].ljust(16)  # 16バイトに切り詰めまたはパディング
            writer.write(status_message)
            await writer.drain()
            writer.close()
            return

        # ファイルデータを受信
        received_size = 0
        start_time = time.time()
        async with aiofile.async_open(os.path.join(STORAGE_DIR, f'{int(start_time)}_{client_id}.mp4'), 'wb') as f:
            while received_size < file_size:
                data = await reader.read(BUFFER_SIZE)
                if not data:
                    break
                await f.write(data)
                received_size += len(data)

        logging.info(f'File received: {received_size} bytes')

        # ステータスメッセージを送信
        status_code = 0  # 成功を示すステータスコード
        status_message = f'{status_code:02d}File uploaded successfully. Received {received_size} bytes'.encode()
        status_message = status_message[:16].ljust(16)  # 16バイトに切り詰めまたはパディング
        writer.write(status_message)
        await writer.drain()

    except Exception as e:
        logging.error(f'Error: {str(e)}')
        status_code = 99  # 未知のエラーを示すステータスコード
        status_message = f'{status_code:02d}Internal server error.'.encode()
        status_message = status_message[:16].ljust(16)  # 16バイトに切り詰めまたはパディング
        writer.write(status_message)
        await writer.drain()

    finally:
        writer.close()

async def start_server(port):
    # ディレクトリが存在しない場合は作成
    os.makedirs(STORAGE_DIR, exist_ok=True)

    server = await asyncio.start_server(handle_client, HOST, port)
    logging.info(f'Server listening on {HOST}:{port}')

    async with server:
        await server.serve_forever()

def run_server(port):
    asyncio.run(start_server(port))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File upload server')
    parser.add_argument('--port', type=int, default=65432, help='Port number')
    args = parser.parse_args()

    run_server(args.port)

    # マルチプロセスで複数のサーバインスタンスを起動
    num_processes = multiprocessing.cpu_count()
    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=run_server, args=(args.port,))
        p.start()
        processes.append(p)

    # すべてのプロセスが終了するまで待機
    for p in processes:
        p.join()