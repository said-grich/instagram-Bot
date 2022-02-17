

if __name__=='__main__':
    with open('message.txt', 'r') as file:
        data = file.read().rstrip()
        print(data)