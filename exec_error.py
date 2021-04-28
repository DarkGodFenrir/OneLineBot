from mysql import Sqldb


def block_user(param):
    Sqldb.block_user(param)
    dell_group = Sqldb.get_group(param)
    if dell_group is not None and dell_group != "None":
        dell_group = dell_group.split()
        if "None" in dell_group:
            dell_group.remove("None")
        if "None_p" in dell_group:
            dell_group.remove("None_p")
    for dell in dell_group:
        if str(dell).find("_p") > -1:
            param_for_dell = ["del", str(dell)[len(str(dell)) - 2:], "p", param]
        else:
            param_for_dell = ["del", dell, param]
        Sqldb.edit_list(param_for_dell)


def exec_error(self, param):
    if str(self.args[0]).find('bot was blocked by the user') > -1:
        block_user(param)
    if str(self.args[0]).find('chat not found'):
        block_user(param)
    else:
        error_text = "Произошла ошибка: " + str(self.args[0]) + f"\n{self}"
        print(error_text)
        return error_text
