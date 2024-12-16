class User:
    def __init__(self):
        self.users = {}

    def create_user(self,user_id,password,nickname,comment):
        if user_id in self.users:
            raise ValueError("already exist")
        self.users[user_id] = {
            "password":password,
            "nickname":nickname or user_id,
            "comment":comment
        }

    def get_user(self,user_id):
        return self.users.get(user_id)
    
    def update_user(self,user_id,nickname,comment):
        if user_id not in self.users:
            return None
        if nickname:
            self.users[user_id]["nickname"] = nickname
        if comment is not None:
            self.users[user_id]["comment"] = comment
        return self.users[user_id]
    
    def delete_user(self,user_id):
        if user_id in self.users:
            del self.users[user_id]