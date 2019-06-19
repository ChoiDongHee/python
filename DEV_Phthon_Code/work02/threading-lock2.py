#Python Thread Synchronization(동기화) 예제2

import threading

tot = 0
lock = threading.Lock()

def add_total(amount):
    """
    쓰레드에서 실행 할 함수
    전역변수 tot에 amount 더하기
    """
    global tot
    lock.acquire()
    try:
        tot += amount
    finally:
        lock.release()
    print (threading.currentThread().getName()+' Synchronized  :',tot)

    """
    또는

    global total
    with lock:
        total += amount
    print (threading.currentThread().getName()+' Synchronized  :',tot)

    with 문으로 더 간단하게 사용 가능
    """

#동기화가 되어 있는 쓰레드 예제
if __name__ == '__main__':
    for i in range(10000):
        my_thread = threading.Thread(
            target=add_total, args=(1,))
        my_thread.start()


print(format(1.5678, '10.3f'))
print('나는 나이가 %d 이다.'%23)
print('나는 나이가 %s 이다.'%'스물셋')
print('나는 나이가 %d 이고 이름은 %s이다.'%(23, '홍길동'))
print('나는 나이가 %s 이고 이름은 %s이다.'%(23, '홍길동'))
print('나는 키가 %f이고, 에너지가 %d%%.'%(177.7, 100))
print('이름은 {0}, 나이는 {1}'.format('한국인', 33))
print('이름은 {}, 나이는 {}'.format('신선해', 33))
print('이름은 {1}, 나이는 {0}'.format(34, '강나루'))
print('이름은 {1} {1}, 나이는 {0} {0} {1}'.format(34, '강나루'))