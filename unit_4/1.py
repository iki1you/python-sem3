import json
import re


def sub_scopes(s, count_repl):
    if count_repl == 0:
        return s
    return sub_scopes(*re.subn(r'\([^()]*\)', '', s))


def get_field(key):
    if key + ':' in fields:
        return re.findall(re.escape(key) + r':.*?;', fields)[0][:-1].split(':')
    return False


fields = input()
pointer = input().split(', ')

fields_dict = {
    'description': lambda x: (x[0], '. '.join(map(lambda y: str(y).strip().capitalize(), x[1].split('.')))),
    'salary': lambda x: (x[0], '{0:.{1}f}'.format(float(x[1].strip()), 3)),
    'key_skills': lambda x: (x[0], re.sub(r'&nbsp', ' ', x[1]).strip()),
    'key_phrase': lambda x: (x[0], x[1].upper().strip() + '!'),
    'addition': lambda x: (x[0], '...' + x[1].lower().strip() + '...'),
    'reverse': lambda x: (x[0], x[1][::-1].strip()),
    'company_info': lambda x: (x[0], sub_scopes(x[1], 1).lstrip())
}

output = [fields_dict[i](get_field(i)) for i in pointer if i + ':' in fields]

print(json.dumps(dict(output)))
