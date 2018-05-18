class Test():
    def __init__(self):
        self.method = "recv"
        getattr(self, self.method, "none")

    def recv(self):
        """ferfr"""
        return 1

if __name__ == '__main__':
    test = Test()
    print test.recv()