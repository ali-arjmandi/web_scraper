import os
import argparse

parser = argparse.ArgumentParser(description='Generate Web Scrapers.')
parser.add_argument('--input', type=str, help='name of arj file')
args = parser.parse_args()
args = vars(args)

def arjParser(order):
    lines = order.split("\n")
    arr = []
    for line in lines:
        if line == "": break
        contents = line.split(":")
        if line[0] != ' ':
            arr.append(contents[0]+':')
            if len(contents[1:]) != 0:
                arr[-1] += ':'.join(contents[1:])
        else:
            arr[-1] += '\n' + line
    for i in range(len(arr)):
        key = arr[i].split(":")[0]
        value = ":".join(arr[i].split(":")[1:])[1:]
        if '\n' in value:
            value = arjParser("\n".join(list(map(lambda line: line[4:],value.split("\n")))))
        elif value[0] == ' ':
            value = arjParser(value[4:])
        arr[i] = {key: value}
    return arr

def translater(order, variable="driver"):
    code = ""
    for itm in order:
        for k, v in itm.items():
            if k == "open":
                code += f"with open('{args['input']}.json', 'w') as f:\n\tf.write('[ ]')\nbase_url = '{v}'\ndriver.get(base_url)\n"
            elif k == "print":
                d = {
                    "attribute": None,
                    "path": None,
                }
                for i in v:
                    if list(i.keys())[0] == "attribute": d['attribute'] = list(i.values())[0]
                    if list(i.keys())[0] == "path": d['path'] = list(i.values())[0]
                if not d['attribute']: code += f"print(seleniumUtils.find_by_xpath({variable}, '{d['path']}').text)\n"
                else: code += f"print(seleniumUtils.find_by_xpath({variable}, '{d['path']}').get_attribute('{d['attribute']}'))\n"
            elif k == "loop":
                code += "while True:\n"
                code += "\n".join(list(map(lambda line: "\t"+line, translater(v).split('\n'))))
            elif k == "loopOver":
                d = {
                    "over": None,
                    "value": None,
                    "type": None,
                    "then": None,
                    "hasNewObject": None,
                }
                for i in v:
                    if list(i.keys())[0] == "over": d['over'] = list(i.values())[0]
                    if list(i.keys())[0] == "value": d['value'] = list(i.values())[0]
                    elif list(i.keys())[0] == "type": d['type'] = list(i.values())[0]
                    elif list(i.keys())[0] == "then": d['then'] = list(i.values())[0]
                    elif list(i.keys())[0] == "hasNewObject": d['hasNewObject'] = list(i.values())[0]
                code += f"element = seleniumUtils.find_by_xpath({variable}, '{d['over']}')\n"
                code += "if not element: break\n"
                code += f"elements = seleniumUtils.find_by_{d['type']}({variable}, '{d['value']}', multi=True)\n"
                code += "if not elements: break\n"
                code += "for element in elements:\n"
                if d['then']:
                    if d['hasNewObject']: code += "\tobj = {}\n"
                    code += "\n".join(list(map(lambda line: "\t"+line, translater(d['then'], 'element').split('\n'))))
                    if d['hasNewObject']:
                        code += "objs.append(obj)\n"
                        code += "\tappend2file(obj, '"+args['input']+"')\n"
                else: code += "\tpass\n"
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
                code += f"element = seleniumUtils.find_by_{d['type']}({variable}, '{d['value']}')\n"
                code += "if not element: break\n"
                code += "element.click()\n"
                if d['then']:
                    code += translater(d['then'])
            elif k == "clickNewTab":
                d = {
                    "value": None,
                    "type": None,
                    "then": None
                }
                for i in v:
                    if list(i.keys())[0] == "value": d['value'] = list(i.values())[0]
                    elif list(i.keys())[0] == "type": d['type'] = list(i.values())[0]
                    elif list(i.keys())[0] == "then": d['then'] = list(i.values())[0]
                code += f"element = seleniumUtils.find_by_{d['type']}({variable}, '{d['value']}')\n"
                code += "if not element: break\n"
                code += "element.send_keys(Keys.CONTROL + Keys.SHIFT + Keys.RETURN)\n"
                code += "driver.switch_to.window(driver.window_handles[-1])\n"
                code += "seleniumUtils.wait_until_load(driver)\n"
                if d['then']:
                    code += translater(d['then'])+"\n"
                code += "driver.close()\n"
                code += "driver.switch_to.window(driver.window_handles[-1])\n"
            elif k == "addToObject":
                code += "key = None\n"
                code += "val = None\n"
                code += translater(v, variable)
                code += "if key and val: obj[key] = val\n"
            elif k == "key":
                d = {
                    "attribute": None,
                    "path": None,
                    "slice": None
                }
                try:
                    for i in v:
                        if list(i.keys())[0] == "attribute": d['attribute'] = list(i.values())[0]
                        if list(i.keys())[0] == "slice": d['slice'] = list(i.values())[0]
                        if list(i.keys())[0] == "path": d['path'] = list(i.values())[0]
                    if not d['attribute']: code += f"key = seleniumUtils.find_by_xpath({variable}, '{d['path']}').text\n"
                    else: code += f"key = seleniumUtils.find_by_xpath({variable}, '{d['path']}').get_attribute('{d['attribute']}')\n"
                    if d['slice']: code += f"key = key{d['slice']}\n"
                except:
                    code += f"key = '{v}'\n"
            elif k == "val":
                d = {
                    "attribute": None,
                    "path": None,
                    "slice": None,
                    "array": None,
                    "value": None,
                    "type": None,
                }
                try:
                    for i in v:
                        if list(i.keys())[0] == "attribute": d['attribute'] = list(i.values())[0]
                        if list(i.keys())[0] == "slice": d['slice'] = list(i.values())[0]
                        if list(i.keys())[0] == "path": d['path'] = list(i.values())[0]
                        if list(i.keys())[0] == "array": d['array'] = list(i.values())[0]
                        if list(i.keys())[0] == "value": d['value'] = list(i.values())[0]
                        if list(i.keys())[0] == "type": d['type'] = list(i.values())[0]
                    if not d['array']:
                        if not d['attribute']: code += f"val = seleniumUtils.find_by_xpath({variable}, '{d['path']}').text\n"
                        elif d['attribute'] and d['path']: code += f"val = seleniumUtils.find_by_xpath({variable}, '{d['path']}').get_attribute('{d['attribute']}')\n"
                        if d['slice']: code += f"val = val{d['slice']}\n"
                    else:
                        code += "val = []\n"
                        code += f"element = seleniumUtils.find_by_xpath({variable}, '{d['path']}')\n"
                        code += "if not element: break\n"
                        code += f"elements = seleniumUtils.find_by_{d['type']}(element, '{d['value']}', multi=True)\n"
                        code += "if not elements: break\n"
                        code += "for element in elements:\n"
                        if not d['attribute']: code += f"\ttmpVal = element.text\n"
                        elif d['attribute']: code += f"\ttmpVal = element.get_attribute('{d['attribute']}')\n"
                        code += "\tval.append(tmpVal)\n"
                except:
                    code += f"val = '{v}'\n"
                
    return code


os.makedirs('./arjs', exist_ok=True)
try:
    with open('./arjs/'+args['input']+'.arj') as f:
        order = f.read()
except FileNotFoundError:
    print("File not found")
    exit()
with open('base.txt') as f:
    base = f.read()

res = ""

order = arjParser(order)
res = translater(order)
output = base.replace("@@code@@", res)

with open('scraper.py', 'w') as f:
    f.write(output)
import scraper
