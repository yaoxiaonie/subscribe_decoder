import os
import time
import urllib.parse as urlparse
from base64 import b64encode, b64decode
from fnmatch import fnmatch
from json import loads
from urllib import request
from urllib.request import urlopen

from pywebio import *
from pywebio.input import input_group, input, TEXT, NUMBER
from pywebio.output import put_markdown, put_table, put_buttons, put_tabs, toast
from pywebio.pin import *
from pywebio.session import *

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}
TROJAN_DEFAULT_CONFIG = {"add": "example.com", "id": "", "port": "443", "ps": "", }
SS_DEFAULT_CONFIG = {"add": "example.com", "passwd": "", "port": "443", "scy": "", "ps": "", }
curdir = os.path.split(os.path.abspath(__file__))[0]
subscribe_url_decode_data = []


def save_to_local():
    encode_data = ''
    for subscribe_url_decode_data_number in range(len(subscribe_url_decode_data)):
        if subscribe_url_decode_data[subscribe_url_decode_data_number] != 'removed':
            if subscribe_url_decode_data[subscribe_url_decode_data_number]['protocol'] == 'vmess':
                encode_data += 'vmess://'
                encode_data += b64encode(
                    str(subscribe_url_decode_data[subscribe_url_decode_data_number]).replace('True', 'true').replace(
                        'False', 'false').replace("'", '"').replace('"{', "'{").replace('}"', "}'").encode()).decode()
                encode_data += '\n\n'
            elif subscribe_url_decode_data[subscribe_url_decode_data_number]['protocol'] == 'trojan':
                encode_data += 'trojan://'
                encode_data += subscribe_url_decode_data[subscribe_url_decode_data_number]['id']
                encode_data += '@'
                encode_data += subscribe_url_decode_data[subscribe_url_decode_data_number]['add']
                encode_data += ':'
                encode_data += subscribe_url_decode_data[subscribe_url_decode_data_number]['port']
                encode_data += '#'
                encode_data += urlparse.quote(subscribe_url_decode_data[subscribe_url_decode_data_number]['ps'])
                encode_data += '\n\n'
    curdate = time.strftime('%Y%m%d')
    with open(f'{curdir}/static/{curdate}.html', 'w') as file:
        file.write(b64encode(encode_data.encode()).decode())
        file.close()
        toast('保存成功！')


def url_encode():
    encode_data = ''
    for subscribe_url_decode_data_number in range(len(subscribe_url_decode_data)):
        if subscribe_url_decode_data[subscribe_url_decode_data_number] != 'removed':
            if subscribe_url_decode_data[subscribe_url_decode_data_number]['protocol'] == 'vmess':
                encode_data += 'vmess://'
                encode_data += b64encode(
                    str(subscribe_url_decode_data[subscribe_url_decode_data_number]).replace('True', 'true').replace(
                        'False', 'false').replace("'", '"').replace('"{', "'{").replace('}"', "}'").encode()).decode()
                encode_data += '\n\n'
            elif subscribe_url_decode_data[subscribe_url_decode_data_number]['protocol'] == 'trojan':
                encode_data += 'trojan://'
                encode_data += subscribe_url_decode_data[subscribe_url_decode_data_number]['id']
                encode_data += '@'
                encode_data += subscribe_url_decode_data[subscribe_url_decode_data_number]['add']
                encode_data += ':'
                encode_data += subscribe_url_decode_data[subscribe_url_decode_data_number]['port']
                encode_data += '#'
                encode_data += urlparse.quote(subscribe_url_decode_data[subscribe_url_decode_data_number]['ps'])
                encode_data += '\n\n'
            elif subscribe_url_decode_data[subscribe_url_decode_data_number]['protocol'] == 'ss':
                encode_data += 'ss://'
                encode_data += b64encode(str(f"{subscribe_url_decode_data[subscribe_url_decode_data_number]['scy']}:{subscribe_url_decode_data[subscribe_url_decode_data_number]['passwd']}").encode()).decode()
                encode_data += '@'
                encode_data += subscribe_url_decode_data[subscribe_url_decode_data_number]['add']
                encode_data += ':'
                encode_data += subscribe_url_decode_data[subscribe_url_decode_data_number]['port']
                encode_data += '#'
                encode_data += urlparse.quote(subscribe_url_decode_data[subscribe_url_decode_data_number]['ps'])
                encode_data += '\n\n'
    pin.convert_result = b64encode(encode_data.encode()).decode()
    toast('转换成功！')


def url_del():
    global subscribe_url_decode_data
    subscribe_delete = input_group('删除节点', [input(name='number', label='序号', type=NUMBER)])
    url_number = subscribe_delete.get('number')
    if url_number != '':
        if subscribe_url_decode_data[url_number - 1] != 'removed':
            subscribe_url_decode_data[url_number - 1] = 'removed'
            toast('删除成功！')
        else:
            toast('该节点已被删除，不能重复操作！')
    else:
        toast('序号不能为空！')


def url_edit():
    global subscribe_url_decode_data
    subscribe_editor = input_group('编辑别名', [input(name='number', label='序号', type=NUMBER),
                                                input(name='name', label='新别名', type=TEXT)])
    url_number = subscribe_editor.get('number')
    url_name = subscribe_editor.get('name')
    if url_number != '':
        if subscribe_url_decode_data[url_number - 1] != 'removed':
            subscribe_url_decode_data[url_number - 1]['ps'] = url_name
            toast('命名成功！')
        else:
            toast('命名失败，该节点已被删除！')
    else:
        toast('序号不能为空！')


def edit_ss(subscribe_data):
    subscribe_data['ps'] = input(label='新别名', type=TEXT)
    ss_url = 'ss://'
    ss_url += b64encode(str(f"{subscribe_data['scy']}:{subscribe_data['passwd']}").encode()).decode()
    ss_url += '@'
    ss_url += subscribe_data['add']
    ss_url += ':'
    ss_url += subscribe_data['port']
    ss_url += '#'
    ss_url += subscribe_data['ps']
    pin.convert_result = ss_url
    toast('命名并转换成功！')


def edit_trojan(subscribe_data):
    subscribe_data['ps'] = input(label='新别名', type=TEXT)
    trojan_url = 'trojan://'
    trojan_url += subscribe_data['id']
    trojan_url += '@'
    trojan_url += subscribe_data['add']
    trojan_url += ':'
    trojan_url += subscribe_data['port']
    trojan_url += '#'
    trojan_url += subscribe_data['ps']
    pin.convert_result = trojan_url
    toast('命名并转换成功！')


def edit_vmess(subscribe_data):
    subscribe_data['ps'] = input(label='新别名', type=TEXT)
    pin.convert_result = f'> vmess://{b64encode(str(subscribe_data).encode()).decode()}'
    toast('命名并转换成功！')


def back_main():
    run_js("location.href=url", url='/?app=index')


def enter_app(url_content: str, url_type: str):
    if url_content != '':
        if url_type == '订阅模拟':
            run_js("location.href=url", url=f'/?app=subscribe&subscribe={urlparse.quote(url_content)}')
        else:
            run_js("location.href=url", url=f'/?app=result&content={urlparse.quote(url_content)}&type={urlparse.quote(url_type)}')
    else:
        toast('链接不可以为空！')


def subscribe():
    filename = input(label='订阅文件名', type=TEXT, required=True)
    run_js("location.href=url", url=f'/static/{filename}.html')


@config(title='V2ray订阅解析结果', theme='minty')
def result():
    run_js("""
    $('head meta[name="keywords"]').remove();
    $('footer').remove();
    """)
    global subscribe_url_decode_data
    subscribe_url_decode_data = []
    url_content = urlparse.unquote(eval_js("new URLSearchParams(window.location.search).get('content')"))
    url_type = urlparse.unquote(eval_js("new URLSearchParams(window.location.search).get('type')"))
    if url_type == 'URL':
        subscribe_url_number = 0
        if fnmatch(url_content, 'http*'):
            subscribe_url_encode_data = b64decode(
                urlopen(request.Request(url=url_content, headers=HEADERS)).read()).decode().split()
            put_markdown('# 输出配置')
            for subscribe_url_encode_protocol_url in subscribe_url_encode_data:
                if subscribe_url_encode_protocol_url.split('://')[:1][0] == 'vmess':
                    subscribe_url_number += 1
                    subscribe_data = loads(b64decode(subscribe_url_encode_protocol_url.split('://')[1:][0]).decode())
                    subscribe_keys = ['add', 'port', 'id', 'aid', 'scy', 'net', 'type', 'host', 'path', 'tls', 'ps']
                    for key in subscribe_keys:
                        if key not in subscribe_data.keys():
                            subscribe_data[f'{key}'] = ''
                    subscribe_data['protocol'] = 'vmess'
                    subscribe_data['sn'] = subscribe_url_number
                    put_markdown(f"## 节点{subscribe_data['sn']}")
                    put_tabs([
                        {'title': '简略信息', 'content': [
                            put_table([
                                ['信息', '数据'],
                                ['别名/备注', subscribe_data['ps']],
                                ['协议类型', subscribe_data['protocol']]
                            ])
                        ]},
                        {'title': '详细信息', 'content': [
                            put_table([
                                ['信息', '数据'],
                                ['协议类型', subscribe_data['protocol']],
                                ['服务器地址', subscribe_data['add']],
                                ['服务器端口', subscribe_data['port']],
                                ['用户ID（UUID）', subscribe_data['id']],
                                ['额外ID', subscribe_data['aid']],
                                ['加密方式（自选）', subscribe_data['scy']],
                                ['传输协议', subscribe_data['net']],
                                ['伪装类型', subscribe_data['type']],
                                ['伪装域名', subscribe_data['host']],
                                ['伪装路径', subscribe_data['path']],
                                ['底层传输', subscribe_data['tls']],
                                ['别名/备注', subscribe_data['ps']]
                            ])
                        ]},
                    ])
                    put_markdown('---')
                    subscribe_url_decode_data.append(subscribe_data)
                elif subscribe_url_encode_protocol_url.split('://')[:1][0] == 'trojan':
                    subscribe_url_number += 1
                    subscribe_data = TROJAN_DEFAULT_CONFIG.copy()
                    subscribe_keys = ['add', 'port', 'id', 'ps']
                    for key in subscribe_keys:
                        if key not in subscribe_data.keys():
                            subscribe_data[f'{key}'] = ''
                    subscribe_data['protocol'] = 'trojan'
                    subscribe_data['sn'] = subscribe_url_number
                    put_markdown(f"## 节点{subscribe_data['sn']}")
                    subscribe_data['id'] = urlparse.unquote(
                        subscribe_url_encode_protocol_url.split('://')[1:][0].split('@')[:1][0])
                    subscribe_data['add'] = \
                        subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[:1][0].split('@')[1:][0]
                    subscribe_data['port'] = \
                        subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[1:][0].split('#')[:1][0]
                    subscribe_data['ps'] = urlparse.unquote(
                        subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[1:][0].split('#')[1:][
                            0]).replace('+', ' ')
                    put_tabs([
                        {'title': '简略信息', 'content': [
                            put_table([
                                ['信息', '数据'],
                                ['别名/备注', subscribe_data['ps']],
                                ['协议类型', subscribe_data['protocol']]
                            ])
                        ]},
                        {'title': '详细信息', 'content': [
                            put_table([
                                ['信息', '数据'],
                                ['协议类型', subscribe_data['protocol']],
                                ['服务器地址', subscribe_data['add']],
                                ['服务器端口', subscribe_data['port']],
                                ['用户ID（UUID）', subscribe_data['id']],
                                ['别名/备注', subscribe_data['ps']]
                            ])
                        ]},
                    ])
                    put_markdown('---')
                    subscribe_url_decode_data.append(subscribe_data)
                elif subscribe_url_encode_protocol_url.split('://')[:1][0] == 'ss':
                    subscribe_url_number += 1
                    subscribe_data = SS_DEFAULT_CONFIG.copy()
                    subscribe_keys = ['add', 'port', 'passwd', 'scy', 'ps']
                    for key in subscribe_keys:
                        if key not in subscribe_data.keys():
                            subscribe_data[f'{key}'] = ''
                    subscribe_data['protocol'] = 'ss'
                    subscribe_data['sn'] = subscribe_url_number
                    put_markdown(f"## 节点{subscribe_data['sn']}")
                    subscribe_data['add'] = subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[:1][0].split('@')[1:][0]
                    subscribe_data['port'] = subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[1:][0].split('#')[:1][0]
                    subscribe_data['passwd'] = b64decode(
                        subscribe_url_encode_protocol_url.split('://')[1:][0].split('@')[:1][0]).decode().split(':')[1:][0]
                    subscribe_data['scy'] = b64decode(
                        subscribe_url_encode_protocol_url.split('://')[1:][0].split('@')[:1][0]).decode().split(':')[:1][0]
                    subscribe_data['ps'] = urlparse.unquote(
                        subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[1:][0].split('#')[1:][0]).replace('+', ' ')
                    put_tabs([
                        {'title': '简略信息', 'content': [
                            put_table([
                                ['信息', '数据'],
                                ['别名/备注', subscribe_data['ps']],
                                ['协议类型', subscribe_data['protocol']]
                            ])
                        ]},
                        {'title': '详细信息', 'content': [
                            put_table([
                                ['信息', '数据'],
                                ['协议类型', subscribe_data['protocol']],
                                ['服务器地址', subscribe_data['add']],
                                ['服务器端口', subscribe_data['port']],
                                ['密码', subscribe_data['passwd']],
                                ['加密方式（自选）', subscribe_data['scy']],
                                ['别名/备注', subscribe_data['ps']]
                            ])
                        ]},
                    ])
                    put_markdown('---')
                    subscribe_url_decode_data.append(subscribe_data)
            put_markdown(f'### 共{len(subscribe_url_decode_data)}个节点')
            put_buttons(['编辑别名', '删除节点', '转换编码', '转换编码并保存到服务器', '返回主页'],
                        onclick=[url_edit, url_del, url_encode, save_to_local, back_main])
            put_markdown('---')
            put_textarea(label='转换结果显示在这里', name='convert_result', value='', readonly=True)
        elif fnmatch(url_content, '*http*'):
            for subscribe_url in url_content.replace("'", '').split(' '):
                if fnmatch(subscribe_url, 'http*'):
                    subscribe_url_encode_data = b64decode(
                        urlopen(request.Request(url=subscribe_url, headers=HEADERS)).read()).decode().split()
                    put_markdown(f'# {subscribe_url}的输出配置')
                    for subscribe_url_encode_protocol_url in subscribe_url_encode_data:
                        if subscribe_url_encode_protocol_url.split('://')[:1][0] == 'vmess':
                            subscribe_url_number += 1
                            subscribe_data = loads(
                                b64decode(subscribe_url_encode_protocol_url.split('://')[1:][0]).decode())
                            subscribe_keys = ['add', 'port', 'id', 'aid', 'scy', 'net', 'type', 'host', 'path', 'tls',
                                              'ps']
                            for key in subscribe_keys:
                                if key not in subscribe_data.keys():
                                    subscribe_data[f'{key}'] = ''
                            subscribe_data['protocol'] = 'vmess'
                            subscribe_data['sn'] = subscribe_url_number
                            put_markdown(f"## 节点{subscribe_data['sn']}")
                            put_tabs([
                                {'title': '简略信息', 'content': [
                                    put_table([
                                        ['信息', '数据'],
                                        ['别名/备注', subscribe_data['ps']],
                                        ['协议类型', subscribe_data['protocol']]
                                    ])
                                ]},
                                {'title': '详细信息', 'content': [
                                    put_table([
                                        ['信息', '数据'],
                                        ['协议类型', subscribe_data['protocol']],
                                        ['服务器地址', subscribe_data['add']],
                                        ['服务器端口', subscribe_data['port']],
                                        ['用户ID（UUID）', subscribe_data['id']],
                                        ['额外ID', subscribe_data['aid']],
                                        ['加密方式（自选）', subscribe_data['scy']],
                                        ['传输协议', subscribe_data['net']],
                                        ['伪装类型', subscribe_data['type']],
                                        ['伪装域名', subscribe_data['host']],
                                        ['伪装路径', subscribe_data['path']],
                                        ['底层传输', subscribe_data['tls']],
                                        ['别名/备注', subscribe_data['ps']]
                                    ])
                                ]},
                            ])
                            put_markdown('---')
                            subscribe_url_decode_data.append(subscribe_data)
                        elif subscribe_url_encode_protocol_url.split('://')[:1][0] == 'trojan':
                            subscribe_url_number += 1
                            subscribe_data = TROJAN_DEFAULT_CONFIG.copy()
                            subscribe_keys = ['add', 'port', 'id', 'ps']
                            for key in subscribe_keys:
                                if key not in subscribe_data.keys():
                                    subscribe_data[f'{key}'] = ''
                            subscribe_data['protocol'] = 'trojan'
                            subscribe_data['sn'] = subscribe_url_number
                            put_markdown(f"## 节点{subscribe_data['sn']}")
                            subscribe_data['id'] = urlparse.unquote(
                                subscribe_url_encode_protocol_url.split('://')[1:][0].split('@')[:1][0])
                            subscribe_data['add'] = \
                                subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[:1][0].split('@')[1:][
                                    0]
                            subscribe_data['port'] = \
                                subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[1:][0].split('#')[:1][
                                    0]
                            subscribe_data['ps'] = urlparse.unquote(
                                subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[1:][0].split('#')[1:][
                                    0]).replace('+', ' ')
                            put_tabs([
                                {'title': '简略信息', 'content': [
                                    put_table([
                                        ['信息', '数据'],
                                        ['别名/备注', subscribe_data['ps']],
                                        ['协议类型', subscribe_data['protocol']]
                                    ])
                                ]},
                                {'title': '详细信息', 'content': [
                                    put_table([
                                        ['信息', '数据'],
                                        ['协议类型', subscribe_data['protocol']],
                                        ['服务器地址', subscribe_data['add']],
                                        ['服务器端口', subscribe_data['port']],
                                        ['用户ID（UUID）', subscribe_data['id']],
                                        ['别名/备注', subscribe_data['ps']]
                                    ])
                                ]},
                            ])
                            put_markdown('---')
                            subscribe_url_decode_data.append(subscribe_data)
                        elif subscribe_url_encode_protocol_url.split('://')[:1][0] == 'ss':
                            subscribe_url_number += 1
                            subscribe_data = SS_DEFAULT_CONFIG.copy()
                            subscribe_keys = ['add', 'port', 'passwd', 'scy', 'ps']
                            for key in subscribe_keys:
                                if key not in subscribe_data.keys():
                                    subscribe_data[f'{key}'] = ''
                            subscribe_data['protocol'] = 'ss'
                            subscribe_data['sn'] = subscribe_url_number
                            put_markdown(f"## 节点{subscribe_data['sn']}")
                            subscribe_data['add'] = subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[:1][0].split('@')[1:][0]
                            subscribe_data['port'] = subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[1:][0].split('#')[:1][0]
                            subscribe_data['passwd'] = b64decode(
                                subscribe_url_encode_protocol_url.split('://')[1:][0].split('@')[:1][0]).decode().split(':')[1:][0]
                            subscribe_data['scy'] = b64decode(
                                subscribe_url_encode_protocol_url.split('://')[1:][0].split('@')[:1][0]).decode().split(':')[:1][0]
                            subscribe_data['ps'] = urlparse.unquote(
                                subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[1:][0].split('#')[1:][0]).replace('+', ' ')
                            put_tabs([
                                {'title': '简略信息', 'content': [
                                    put_table([
                                        ['信息', '数据'],
                                        ['别名/备注', subscribe_data['ps']],
                                        ['协议类型', subscribe_data['protocol']]
                                    ])
                                ]},
                                {'title': '详细信息', 'content': [
                                    put_table([
                                        ['信息', '数据'],
                                        ['协议类型', subscribe_data['protocol']],
                                        ['服务器地址', subscribe_data['add']],
                                        ['服务器端口', subscribe_data['port']],
                                        ['密码', subscribe_data['passwd']],
                                        ['加密方式（自选）', subscribe_data['scy']],
                                        ['别名/备注', subscribe_data['ps']]
                                    ])
                                ]},
                            ])
                            put_markdown('---')
                            subscribe_url_decode_data.append(subscribe_data)
            put_markdown(f'### 共{len(subscribe_url_decode_data)}个订阅')
            put_buttons(['编辑别名', '删除节点', '转换编码', '转换编码并保存到服务器', '返回主页'],
                        onclick=[url_edit, url_del, url_encode, save_to_local, back_main])
            put_markdown('---')
            put_textarea(label='转换结果显示在这里', name='convert_result', value='', readonly=True)
        else:
            toast('请输入正确的URL！')
    elif url_type == 'VMESS':
        if fnmatch(url_content, 'vmess://*'):
            subscribe_data = loads(b64decode(url_content.split('://')[1:][0]).decode())
            subscribe_keys = ['add', 'port', 'id', 'aid', 'scy', 'net', 'type', 'host', 'path', 'tls', 'ps']
            for key in subscribe_keys:
                if key not in subscribe_data.keys():
                    subscribe_data[f'{key}'] = ''
            put_markdown('# 输出配置')
            put_tabs([
                {'title': '简略信息', 'content': [
                    put_table([
                        ['信息', '数据'],
                        ['别名/备注', subscribe_data['ps']]
                    ])
                ]},
                {'title': '详细信息', 'content': [
                    put_table([
                        ['信息', '数据'],
                        ['服务器地址', subscribe_data['add']],
                        ['服务器端口', subscribe_data['port']],
                        ['用户ID（UUID）', subscribe_data['id']],
                        ['额外ID', subscribe_data['aid']],
                        ['加密方式（自选）', subscribe_data['scy']],
                        ['传输协议', subscribe_data['net']],
                        ['伪装类型', subscribe_data['type']],
                        ['伪装域名', subscribe_data['host']],
                        ['伪装路径', subscribe_data['path']],
                        ['底层传输', subscribe_data['tls']],
                        ['别名/备注', subscribe_data['ps']]
                    ])
                ]},
            ])
            put_buttons(['编辑别名并转换编码', '返回主页'], [lambda: edit_trojan(subscribe_data), lambda: back_main()])
            put_markdown('---')
            put_textarea(label='转换结果显示在这里', name='convert_result', value='', readonly=True)
        else:
            toast('请输入正确的VMESS链接！')
    elif url_type == 'TROJAN':
        if fnmatch(url_content, 'trojan://*'):
            subscribe_data = TROJAN_DEFAULT_CONFIG.copy()
            subscribe_keys = ['add', 'port', 'id', 'ps']
            for key in subscribe_keys:
                if key not in subscribe_data.keys():
                    subscribe_data[f'{key}'] = ''
            subscribe_data['id'] = urlparse.unquote(url_content.split('://')[1:][0].split('@')[:1][0])
            subscribe_data['add'] = url_content.split('://')[1:][0].split(':')[:1][0].split('@')[1:][0]
            subscribe_data['port'] = url_content.split('://')[1:][0].split(':')[1:][0].split('#')[:1][0]
            subscribe_data['ps'] = urlparse.unquote(
                url_content.split('://')[1:][0].split(':')[1:][0].split('#')[1:][0]).replace('+', ' ')
            put_tabs([
                {'title': '简略信息', 'content': [
                    put_table([
                        ['信息', '数据'],
                        ['别名/备注', subscribe_data['ps']]
                    ])
                ]},
                {'title': '详细信息', 'content': [
                    put_table([
                        ['信息', '数据'],
                        ['服务器地址', subscribe_data['add']],
                        ['服务器端口', subscribe_data['port']],
                        ['用户ID（UUID）', subscribe_data['id']],
                        ['别名/备注', subscribe_data['ps']]
                    ])
                ]},
            ])
            put_buttons(['编辑别名并转换编码', '返回主页'], [lambda: edit_trojan(subscribe_data), lambda: back_main()])
            put_markdown('---')
            put_textarea(label='转换结果显示在这里', name='convert_result', value='', readonly=True)
        else:
            toast('请输入正确的TROJAN链接！')
    elif url_type == 'SS':
        if fnmatch(url_content, 'ss://*'):
            subscribe_data = SS_DEFAULT_CONFIG.copy()
            subscribe_keys = ['add', 'port', 'passwd', 'scy', 'ps']
            for key in subscribe_keys:
                if key not in subscribe_data.keys():
                    subscribe_data[f'{key}'] = ''
            subscribe_data['add'] = url_content.split('://')[1:][0].split(':')[:1][0].split('@')[1:][0]
            subscribe_data['port'] = url_content.split('://')[1:][0].split(':')[1:][0].split('#')[:1][0]
            subscribe_data['passwd'] = b64decode(
                url_content.split('://')[1:][0].split('@')[:1][0]).decode().split(':')[1:][0]
            subscribe_data['scy'] = b64decode(
                url_content.split('://')[1:][0].split('@')[:1][0]).decode().split(':')[:1][0]
            subscribe_data['ps'] = urlparse.unquote(
                url_content.split('://')[1:][0].split(':')[1:][0].split('#')[1:][0]).replace('+', ' ')
            put_tabs([
                {'title': '简略信息', 'content': [
                    put_table([
                        ['信息', '数据'],
                        ['别名/备注', subscribe_data['ps']]
                    ])
                ]},
                {'title': '详细信息', 'content': [
                    put_table([
                        ['信息', '数据'],
                        ['服务器地址', subscribe_data['add']],
                        ['服务器端口', subscribe_data['port']],
                        ['密码', subscribe_data['passwd']],
                        ['加密方式（自选）', subscribe_data['scy']],
                        ['别名/备注', subscribe_data['ps']]
                    ])
                ]},
            ])
            put_buttons(['编辑别名并转换编码', '返回主页'], [lambda: edit_ss(subscribe_data), lambda: back_main()])
            put_markdown('---')
            put_textarea(label='转换结果显示在这里', name='convert_result', value='', readonly=True)
        else:
            toast('请输入正确的SS链接！')


@config(title='V2ray订阅解析', theme='minty')
def index():
    run_js("""
    $('head meta[name="keywords"]').remove();
    $('footer').remove();
    """)
    global subscribe_url_decode_data
    subscribe_url_decode_data = []
    put_markdown('# V2ray订阅解析')
    put_input(label='链接或订阅名', name='content', type=TEXT)
    put_radio(label='类型', options=['URL', 'VMESS', 'TROJAN', 'SS'], inline=True, name="type", value='URL')
    put_buttons(['生成', '订阅模拟'], [lambda: enter_app(pin.content, pin.type), lambda: subscribe()])
    put_markdown('## 如何输入多链接？')
    put_markdown("链接需要用''来围住，链接和链接之间还需用一个空格来隔开!")
    put_markdown('### 实例：')
    put_markdown("> 'https://cn.bing.com' 'https://google.com'")


start_server([index, result], port='4089', host='0.0.0.0', debug=True, static_dir=f'{curdir}/static', auto_open_webbrowser=True)