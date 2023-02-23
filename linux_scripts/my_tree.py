import os
import configargparse

# -a 显示所有文件
# -L num  显示几层 ，不显示隐藏文件

char_set = {
    "L": "└── ",
    "E": "├── ",
    "I": "│   ",
    "*": "    "
}

def parser(cmd=None):
    p = configargparse.ArgumentParser()

    p.add_argument('-L', '--max_layer', type=int, default='1', help='dont show hidden files or directories')
    p.add_argument('-a', '--is_show_hidden', action="store_true")
    p.add_argument('-c', '--is_show_compact', action="store_true")

    if cmd is None:
        return p.parse_args()
    else:
        return p.parse_args(cmd)


def get_color(color, argv):
    if color == "green":
        return f"\033[32m{argv}\033[0m"
    elif color == "red":
        return f"\033[31m{argv}\033[0m"
    elif color == "yellow":
        return f"\033[33m{argv}\033[0m"
    else:
        return argv

def is_hidden(file_path):
    file_name = os.path.basename(file_path)
    if file_name[0] == '.':
        return True
    else:
        return False



def get_len_of_listdir(lst):
    len_of_listdir = 0
    for file in lst:
        len_of_listdir += 1
    return len_of_listdir


# start from 1, must be greater than 0
def tree_dir(base_dir, layer=1, is_last_dir=False, prefix=""):
    files = sorted(os.listdir(base_dir))
    # distinguish file or directory
    file_lst=[]
    dir_lst=[]
    for item in files:
        file_path = os.path.join(base_dir, item)
        if is_hidden(file_path) and args.is_show_hidden == False:
            continue
        if os.path.isfile(file_path):
            file_lst.append(item)
        else:
            dir_lst.append(item)

    dir_lst = sorted(dir_lst)
    file_lst = sorted(file_lst)
    len_of_listdir = len(dir_lst)
    len_of_listfile = len(file_lst)
    

    for index, file in enumerate(file_lst):
        file_path = os.path.join(base_dir, file)
        
        line = ""
        if index == len_of_listfile -1 and len_of_listdir == 0:
            line = prefix + char_set["L"]
        else:
            line = prefix + char_set["E"]
        line += file 
        lines.append(line)
        if is_debug:
            print(line)

        if args.is_show_compact:
            if layer > 1 and index > 4:
                break

    for index, dir in enumerate(dir_lst):
        dir_path = os.path.join(base_dir, dir)

        next_prefix = prefix

        line = ""
        if index != len_of_listdir - 1:
            line = prefix + char_set["E"]
        else:
            line = prefix + char_set["L"]
            if layer == 1:
                is_last_dir = True

        if index != len_of_listdir - 1:
            next_prefix += char_set["I"]
        else:
            next_prefix += char_set["*"]
        
        line += get_color("green", dir)
        lines.append(line)
        if is_debug:
            print(line)

        # recursion 
        if layer < max_layer:
            tree_dir(dir_path, layer + 1, is_last_dir=is_last_dir, prefix=next_prefix)


if __name__ == '__main__':
    # is_debug = True 
    is_debug = False

    if is_debug:
        cmd = '-L 5'
        args = parser(cmd)
    else:
        args = parser()

    if args.max_layer < 1:
        print('layer >= 1')
        exit()
    else:
        max_layer = args.max_layer

    lines = []
    
    if is_debug:
        path = "/home"
        tree_dir(path)
        print()
    else:
        tree_dir('.')
        print()
    
    for line in lines:
        print(line)