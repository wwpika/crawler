# crawler
python实现基于协程的异步爬虫

1.thread文件夹中：
thread.py中的threadpool是自己写的类；thread2.py中的threadpool,是用的标准库multiprocessing.pool

2.IO多路复用：首先，操作系统提供了一个功能，当某个socket可读或者可写的时候，它可以给你一个通知。这样当配合非阻塞的socket使用时，只有当系统通知我哪个描述符可读了，我才去执行read操作，可以保证每次read都能读到有效数据而不做纯返回-1和EAGAIN的无用功。操作系统的这个功能通过select/poll/epoll/kqueue之类的函数来使用，这些函数都可以同时监视多个描述符的读写就绪状况，这样，多个描述符的I/O操作都能在一个线程内并发交替地顺序完成，这就叫I/O多路复用，这里的“复用”指的是复用同一个线程

3.class selectors.BaseSelector.select():Wait until some registered file objects become ready, or the timeout expires.
