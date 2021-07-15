import threading
 
class ThreadVariable():
    def __init__(self):
        self.lock = threading.Lock()
        self.lockedValue = 0
 
    # 한 Thread만 접근할 수 있도록 설정한다
    def plus(self, value):

        self.lock.acquire()
        try:
            self.lockedValue += value
        finally:
            # Lock을 해제해서 다른 Thread도 사용할 수 있도록 만든다.
            self.lock.release()
 
class CounterThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name='Timer Thread')
 
    # CounterThread가 실행하는 함수
    def run(self):
        global totalCount
 
        # 25,000번 카운트 시작
        for _ in range(250000):
            totalCount.plus(1)
        print('250,000번 카운팅 끝!')
 
if __name__ == '__main__':
    print("쓰레드 40개 실행")
    global totalCount
    totalCount = ThreadVariable()
 
    for _ in range(40):
        timerThread = CounterThread()
        timerThread.start()
 
    mainThread = threading.currentThread()
    for thread in threading.enumerate():
        # 카운팅을 완료하고 끝날 때 까지 기다린다.
        if thread is not mainThread:
            thread.join()
 
    print('totalCount = ' + str(totalCount.lockedValue))