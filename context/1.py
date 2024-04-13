def is_nickname(line):
    if (len(line) < 8):
        return False
    if line == line.lower() or line == line.upper():
        return False
    if not any(map(lambda x: x in '1234567890', line)):
        return False
    return True


nickname = input()
if (is_nickname(nickname)):
    print("YES")
else:
    print("NO")





