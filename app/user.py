class UserSystem:

    def __init__(self):
        self.users = {}


    def register(self, username, password):

        if username in self.users:
            return "用户已存在"

        self.users[username] = password

        return "注册成功"


    def login(self, username, password):

        if username not in self.users:
            return "用户不存在"

        if self.users[username] != password:
            return "密码错误"

        return "登录成功"