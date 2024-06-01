import time

'''
def timestamp2struct_time(self, timestamp=time.time()):

这是错的，只会一直是程序最初运行的时间。因为timestamp=time.time()，这个是写死的，编译器就会固定。
'''
class TimeTransformer:
    def timestamp2struct_time(self, timestamp=None):
        if timestamp == None:
            timestamp = time.time()
        return time.localtime(timestamp)

    def struct_time2timestamp(self, struct_time=None):
        if struct_time == None:
            struct_time = time.localtime()
        return time.mktime(struct_time)

    def struct_time2str_time(self, format_st='%Y-%m-%d %H:%M:%S', struct_time=None):
        if struct_time == None:
            struct_time = time.localtime()
        return time.strftime(format_st, struct_time)

    def str_time2struct_time(self, format_st='%Y-%m-%d %H:%M:%S', str_time=None):
        if str_time == None:
            str_time = self.struct_time2str_time()
        return time.strptime(str_time, format_st)

    def timestamp2str_time(self, timestamp=None, format_st='%Y-%m-%d %H:%M:%S'):
        if timestamp == None:
            timestamp = time.time()
        return self.struct_time2str_time(format_st, self.timestamp2struct_time(timestamp))

    def str_time2timestamp(self, format_st='%Y-%m-%d %H:%M:%S', str_time=None):
        if str_time == None:
            str_time = self.struct_time2str_time()
        return self.struct_time2timestamp(self.str_time2struct_time(format_st, str_time))

    def GMTplus8(self, format_st, str_time):
        return self.timestamp2str_time(self.str_time2timestamp(format_st, str_time) + 8 * 60 * 60)