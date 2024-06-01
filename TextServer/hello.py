from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        my_text = request.form['my_text']
        with open('logs/text.txt', 'w', encoding='utf-8') as fp:
            fp.write(my_text)

        f = request.files['my_file']
        if f.content_length > 0:
            f.save('logs/uploaded_file.txt')
        return redirect('/show')
    else:
        return render_template("home.html")

@app.route('/show')
def show(): # 不知道这个@app.route('/show')和def show():的要不要一致都是show
    with open('logs/text.txt', 'r', encoding='utf-8') as fp:
        my_text = fp.readlines()
    # data是在text_show.html中的{{data}}的名字，随便起，只要一致
    return render_template('text_show.html', data=my_text)


if __name__ == '__main__':

    # host : 默认为127.0.0.1（localhost）
    # port 默认值为5000

    # 内部， 
    #  * Running on http://127.0.0.1:8080
    # app.run(port=8080)


    # 外部
    # 设置为'0.0.0.0'或者本机的'192.168.0.2'都行，前者写起来简单
    # app.run(host='192.168.211.225', port=8888)
    app.run(host='0.0.0.0', port=8888)





##########################
'''
python hello.py
'''
# 确保防火墙关闭了
##########################
