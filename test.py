import sys


def test():
    print("Hello World")
    return 1

def write():
    file1 = open("log.txt", "a")  # append mode
    L = ["This is Delhi \n", "This is Paris \n", "This is London \n"]
    file1.writelines(L)
    file1.close()


if __name__ == "__main__":
    test()
    write()