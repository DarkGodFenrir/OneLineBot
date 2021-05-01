from mysql import Sqldb

def exec_error(self, param):
    error_text = f"Произошла перехваченная ошибка: {self.args[0]}"
    if str(self.args[0]).find('bot was blocked by the user') > -1:
        Sqldb.block_user(param)
    elif str(self.args[0]).find('chat not found') > -1:
        Sqldb.block_user(param)
    elif str(self.args[0]).find('No user has') > -1:
        return 3
    else:
        error_text = "Произошла ошибка: " + str(self.args[0]) + f"\n{self}"
    print(error_text)
    return error_text
