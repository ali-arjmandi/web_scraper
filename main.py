def orderParser(order):
    lines = order.split("\n")
    arr = []
    for line in lines:
        contents = line.split(":")
        if line[0] != ' ':
            arr.append(contents[0]+':')
            if len(contents[1]) != 0:
                arr[-1] += contents[1]
        else:
            arr[-1] += '\n' + line
    for i in range(len(arr)):
        key = arr[i].split(":")[0]
        value = ":".join(arr[i].split(":")[1:])[1:]
        if '\n' in value:
            value = orderParser("\n".join(list(map(lambda line: line[4:],value.split("\n")))))
        elif value[0] == ' ':
            value = orderParser(value[4:])
        arr[i] = {key: value}
    return arr

def translater(order):
    code = ""
    for itm in order:
        for k, v in itm.items():
            if k == "open":
                code += f"print('please open {v}')\n"
            elif k == "print":
                code += f"print('{v}')\n"
            elif k == "loop":
                code += "while True:\n"
                code += "\n".join(list(map(lambda line: "\t"+line, translater(v).split('\n'))))+"\n"
            elif k == "click":
                d = {
                    "value": None,
                    "type": None,
                    "then": None
                }
                for i in v:
                    if list(i.keys())[0] == "value": d['value'] = list(i.values())[0]
                    elif list(i.keys())[0] == "type": d['type'] = list(i.values())[0]
                    elif list(i.keys())[0] == "then": d['then'] = list(i.values())[0]
                code += f"print('clicking on {d['value']} in {d['type']} sections...')\n"
                if d['then']:
                    code += translater(d['then'])

    return code

with open('order.arj') as f:
    order = f.read()



space = 0
res = ""

order = orderParser(order)
res = translater(order)
with open('scraper.py', 'w') as f:
    f.write(res)
# import scraper