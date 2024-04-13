def check_input(word, line):
    command = ''
    result = []
    cursor = 0
    is_command = False
    for i in range(len(line)):
        if line[i].strip() not in '<>abcdefghijklmnopqrstuvwxyz':
            return False
        if line[i] == '<':
            is_command = True
            command = '<'
        elif line[i] == '>':
            is_command = False
            command += '>'
            if command == '<bspace>':
                if cursor >= 1:
                    cursor -= 1
                    del result[cursor]
            elif command == '<delete>':
                if cursor < len(result):
                    del result[cursor]
            elif command == '<left>':
                if cursor >= 1:
                    cursor -= 1
            elif command == '<right>':
                if cursor < len(result):
                    cursor += 1
            else:
                return False
        else:
            if is_command:
                command += line[i]
            else:
                result.insert(cursor, line[i])
                cursor += 1

    return word == ''.join(result)

# 123r4
# h<left><left>123<delete>r4
# aaaaa
# aaaaaa<bspace>b<bspace>
#
# a
# <left><left>ab<delete><bspace><left>
# keyboard
# keyb<left><left><left><left><left><left><left><left><right><right><right><right><right><right><right><right><right><right><right><right><right><right><right><right><right><right><right><right><right><right><right><right><right><right><right>oard

# testing
# test<delete><delete><delete><delete><delete><delete><delete><delete><delete><delete>ing
word = input().strip()
line = input().strip()

if check_input(word, line):
    print('Yes')
else:
    print('No')
