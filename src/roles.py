class Roles:
    def __init__(self):
        self.data = {
            "administrator": ["foo", "bar.foobar"],
            "developer": ["...somthing"],
            "developer_readonly": ["hoge.fuga", "fuga"],
        }

    def get_role(self, role_name):
        return self.data.get(role_name, [])
