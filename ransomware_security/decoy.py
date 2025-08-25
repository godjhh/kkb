import os
import hashlib
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DECOY_FILES = {
    ".txt": "txt decoy",
    ".doc": "word decoy",
    ".pdf": "pdf decoy",
    ".jpg": "jpg decoy"
}

#   key: 미끼 파일 경로
#   value: 미끼 파일 원본 해시
original_hashes = {}

def create_decoy():
    # decoy_savepath: 미끼 파일 생성할 디렉토리 경로
    decoy_savepath = [
        os.path.abspath(os.sep),
        os.getenv('TEMP'),
        os.path.join(os.path.expanduser('~'), 'Desktop')
    ]

    for directory in decoy_savepath:
        for ext, content in DECOY_FILES.items():
            # ext: 파일 확장자
            # content: 해당 확장자에 맞는 미끼 파일 내용
            file_path = os.path.join(directory, f"AAAA_decoy{ext}")
            byte_content = content.encode("utf-8")
            
            # 미끼파일에 내용 작성
            with open(file_path, "wb") as f:
                f.write(byte_content)
                
            # 미끼파일 해시 값
            file_hash = hashlib.sha256(byte_content).hexdigest()

            # 미끼파일 경로:해시 값 저장
            original_hashes[file_path] = file_hash
            print("미끼 파일 생성 완료", file_path)

class DecoyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # 파일이 아닌 디렉토리면 걍 함수 끝내고
        if event.is_directory:
            return
        # modified 이벤트 발생 파일 절대 경로가 미끼파일 딕셔너리에 있는지 확인
        if os.path.abspath(event.src_path) in original_hashes:
            print("미끼 파일 변조 탐지: ", event.src_path)
            
            with open(event.src_path, "rb") as f:
                # 변조된 미끼파일 해시
                current_hash = hashlib.sha256(f.read()).hexdigest()
        
            # 변조된 미끼파일 해시와 원본 해시 비교
            if current_hash != original_hashes.get(os.path.abspath(event.src_path)):
                print("해시 값이 변조됨")

    def on_deleted(self, event):
        if not event.is_directory and os.path.abspath(event.src_path) in original_hashes:
            print("미끼 파일 삭제됨: ",event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            if os.path.abspath(event.src_path) in original_hashes:
                print("미끼 파일 이름 변경: ", event.src_path, "→", event.dest_path)

if __name__ == "__main__":
    create_decoy()
    
    event_handler = DecoyHandler()
    observer = Observer()
    
    # 미끼 파일 존재하는 디렉토리 리스트 생성
    paths_to_watch = list(set(os.path.dirname(p) for p in original_hashes.keys()))
    
    # 미끼파일 존재하는 디렉토리 감시
    for path in paths_to_watch:
        # recursive=False 하위 디렉토리 탐지X
        observer.schedule(event_handler, path, recursive=False) 

    print("랜섬웨어 탐지 시작 (Ctrl+C 종료)\n")
    observer.start()
    
    try:
        while observer.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()