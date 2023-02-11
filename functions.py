def valid_register(username, password):
    with open('users.txt', 'r', encoding='cp949') as f:
        flag = 0
        for i in f.readlines():
            if username == i.split()[0]:
                flag = 1
                break
        if flag == 1:
            return False
        else:
            return True


def register_user(username, password):
    with open('users.txt', 'a', encoding='cp949') as f:
        f.write(f'{username} {password} \n')


def valid_login(username, password):
    with open('users.txt', 'r', encoding='cp949') as f:
        for i in f.readlines():
            if username == i.split()[0] and password == i.split()[1]:
                return True
        return False


def view_self_book(username):
    with open(f'user_books/{username}.txt', 'r', encoding='utf-8') as f:
        return f.read()


def valid_book(bookname):
    with open('allbooks.txt', 'r', encoding='utf-8') as f:
        for i in f.readlines():
            if bookname + '\n' == i:
                return True
        return False
