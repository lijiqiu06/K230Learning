import _thread
import time

lock = _thread.allocate_lock()
count=0
def counter(thread_id):
    global count
    for i in range(5):
        lock.acquire()
        #临界区开始
        temp = count
        temp += 1
        count = temp
        print(f"线程{thread_id}更新count={count}"+str(time.ticks_ms()))
        #临界区结束
        lock.release()
        time.sleep(0.1)

_thread.start_new_thread(counter, (1, ))
_thread.start_new_thread(counter, (2, ))

time.sleep(3)
print("最终count值:", count)
