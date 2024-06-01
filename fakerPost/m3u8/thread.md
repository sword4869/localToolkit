# what's join

Let the main thread wait for the execution of the child thread to finish before running the main thread.

> without join

```
print('hello')
t1.start()
t2.start()
print('world')
'''
hello
world
t1/t2
t2/t1
'''
```

After the main thread is firsly executed and exited, the child thread is then executed.

When child thread are executed, they may have different ordersthey are in casual sequence.

And after all child thread are exited, the program then exits.

> with join

```
print('hello')
t1.start()
t2.start()
t1.join()
t2.join()
print('world')
'''
hello
t1/t2
t2/t1
world
'''
```

1. Main thread is firstly executed because we don't start the part of thread.
2. `t1.start()`,`t2.start()`, t1 and t2 are executed at the same time without waiting for each other.
3. Keep in mind that `join` don't make a child thread wait for another child thread, that **makes main thread wait for the child thread.**

 `t1.join()` makes the main thread wait until t1 child thread finished, so does t2.

4. When all child thread are executed, the main thread can continue to execute.
5. Program exits.

PS: I always confuse a situation.

If t1 need 1 seconds to execute and t2 need 10 seconds,  `t1.join()` makes the main thread wait for t1, when t1 finished, main thread execute `t2.join()` during t2 is executing, it is ok to make the main thread wait for t2.

But if t1 need 10 seconds to execute and t2 only need 1 seconds,  `t1.join()` makes the main thread wait for t1, t2 finished during 10 seconds, is `t2.join()` meaningless because there is no need to make main thread wait for a finished threat t2?

The answer is NO. The join makes the main thread wait for all child threads, so it is ok to make the main thread wait for the maximum time thread. When main thread executes `t2.join()`, it quickly checks t2 is finished and not waits anymore.

# position of start & join

> wrong

```
t1.start();
t1.join();

t2.start();
t2.join();

'''
t1
t2
'''
```

As a result, T2 is executed after T1, which becomes a single thread.

> right

```
t1.start();
t2.start();

t1.join();
t2.join();
'''
t2/t1
t1/t2
'''
```

# 2 architecture

## Each task starts a thread.

Using `threading` module.

When the number of tasks is low, it is ok. But when we have too many tasks, it may be stuck.

```python
import threading
import time
import random


class myThread(threading.Thread):
    def __init__(self, task):
        threading.Thread.__init__(self)
        self.task = task

    def run(self):
        time.sleep(random.random())
        print(self.task)
        pass

if __name__ == '__main__':
    print('main')
    threads = []
    for i in range(5):
        thread = myThread(i)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join(10)
  
    print('main exit')
```

## Set a size limit of threads.

For 100 tasks, `while` only execute 10 tasks at the same time.

Using `concurrent.futures` module.


```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def spider(page):
    time.sleep(5)
    print(f"crawl task{page} finished")
    return page

def main():
    with ThreadPoolExecutor(max_workers=5) as t:
        obj_list = []
        for page in range(1, 10):
            obj = t.submit(spider, page)
            obj_list.append(obj)

        for future in as_completed(obj_list):
            data = future.result()
            print(f"main: {data}")

main()
```
