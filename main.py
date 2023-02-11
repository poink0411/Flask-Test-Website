from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for
from functions import valid_register, register_user, valid_login, view_self_book, valid_book
app = Flask(__name__)

@app.route('/')
def route():
    return redirect(url_for('index'))

@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['indextype'] == '1':
            return redirect(url_for('login'))
        else:
            return redirect(url_for('register'))
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if request.form.get('rv', False) == '2':
            return redirect(url_for('index'))
        if valid_register(request.form['username'], request.form['password']):
            register_user(request.form['username'], request.form['password'])
            open(f'user_books/{request.form["username"]}.txt', 'w')
            return redirect(url_for('index'))
        else:
            return render_template('register.html', error="이미 존재하는 회원입니다")
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return redirect(url_for('library', username=request.form['username']))
        else:
            error = "아이디 혹은 비밀번호가 잘못되었습니다"
    return render_template('login.html', error=error)


@app.route('/library/<username>', methods=['POST', 'GET'])
def library(username):
    if request.method == 'POST':
        if request.form['librarytype'] == '1':
            return render_template('view_book.html', username=username, books=view_self_book(username))
        elif request.form['librarytype'] == '2':
            return redirect(url_for('borrow', username=username))
        elif request.form['librarytype'] == '3':
            return redirect(url_for('ret', username=username))
        else:
            return redirect(url_for('inputbook'))
    return render_template('library.html', username=username)

@app.route('/inputbook', methods=['POST', 'GET'])
def inputbook():
    if request.method == 'POST':
        with open('allbooks.txt', 'a', encoding='utf-8') as f:
            f.write(request.form['bookname']+'\n')
    with open('allbooks.txt', 'r', encoding='utf-8') as f:
        return render_template('inputbook.html', all_books=f.read())

@app.route('/borrow/<username>', methods=['POST', 'GET'])
def borrow(username):
    error = None
    if request.method == 'POST':
        bookname = request.form['bookname']
        with open(f'user_books/{username}.txt', 'a+', encoding='utf-8') as f:
            if valid_book(request.form['bookname']):
                f.write(f'{bookname}\n')
        return redirect(url_for('library', username=username))
    with open('allbooks.txt', 'r', encoding='utf-8') as f:
        return render_template('borrow.html', username=username, books=f.read())

@app.route('/return/<username>', methods=['POST', 'GET'])
def ret(username):
    error = None
    if request.method == 'POST':
        bookname = request.form['bookname']
        print(bookname)
        with open(f'user_books/{username}.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            newline = []
            flag = 0
            for line in lines:
                if (bookname + '\n') != line:
                    newline.append(line)
                else:
                    flag = 1
        with open(f'user_books/{username}.txt', 'w', encoding='utf-8') as f:
            for i in newline:
                f.write(i)
        if flag == 0:
            return render_template('return.html', username=username, books=view_self_book(username), error="그런 책을 빌린적이 없습니다")
    return render_template('return.html', username=username, books=view_self_book(username))

if __name__=='__main__':
    app.run(port='5000', debug=True)