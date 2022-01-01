# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

VAGRANT_CATALOG = "/Users/dmitriygarbovskiy/Learning/vagrant/"
VAGRANT_TEMPLATE_NAME = "VTemplate.txt"


def open_template_file(catalog=VAGRANT_CATALOG, file=VAGRANT_TEMPLATE_NAME):
    with open(catalog + file, "r") as vagrant_template_file:
        return vagrant_template_file.read()
    # TODO: переделать вагранд-файл в шаблон j2


def create_vagrant_from_template(hostname, ip):
    print("hello world")
    #TODO: проработать структура инвентори-файла (должен быть like as ансибл)
    #TODO: компилировать вагрант-файл на основе шаблона и инвентори



def main():
    print(open_template_file())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
