import _thread
import time

def task(thread_id, delay):
    for i in range(3):
        time.sleep(delay)
        print(f"线程{thread_id}执行第{i+1}次"+str(time.ticks_ms()))

_thread.start_new_thread(task, (1, 1.0))
_thread.start_new_thread(task, (2, 0.5))
