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
        toast('???????????????')


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
    toast('???????????????')


def url_del():
    global subscribe_url_decode_data
    subscribe_delete = input_group('????????????', [input(name='number', label='??????', type=NUMBER)])
    url_number = subscribe_delete.get('number')
    if url_number != '':
        if subscribe_url_decode_data[url_number - 1] != 'removed':
            subscribe_url_decode_data[url_number - 1] = 'removed'
            toast('???????????????')
        else:
            toast('?????????????????????????????????????????????')
    else:
        toast('?????????????????????')


def url_edit():
    global subscribe_url_decode_data
    subscribe_editor = input_group('????????????', [input(name='number', label='??????', type=NUMBER),
                                                input(name='name', label='?????????', type=TEXT)])
    url_number = subscribe_editor.get('number')
    url_name = subscribe_editor.get('name')
    if url_number != '':
        if subscribe_url_decode_data[url_number - 1] != 'removed':
            subscribe_url_decode_data[url_number - 1]['ps'] = url_name
            toast('???????????????')
        else:
            toast('???????????????????????????????????????')
    else:
        toast('?????????????????????')


def edit_ss(subscribe_data):
    subscribe_data['ps'] = input(label='?????????', type=TEXT)
    ss_url = 'ss://'
    ss_url += b64encode(str(f"{subscribe_data['scy']}:{subscribe_data['passwd']}").encode()).decode()
    ss_url += '@'
    ss_url += subscribe_data['add']
    ss_url += ':'
    ss_url += subscribe_data['port']
    ss_url += '#'
    ss_url += subscribe_data['ps']
    pin.convert_result = ss_url
    toast('????????????????????????')


def edit_trojan(subscribe_data):
    subscribe_data['ps'] = input(label='?????????', type=TEXT)
    trojan_url = 'trojan://'
    trojan_url += subscribe_data['id']
    trojan_url += '@'
    trojan_url += subscribe_data['add']
    trojan_url += ':'
    trojan_url += subscribe_data['port']
    trojan_url += '#'
    trojan_url += subscribe_data['ps']
    pin.convert_result = trojan_url
    toast('????????????????????????')


def edit_vmess(subscribe_data):
    subscribe_data['ps'] = input(label='?????????', type=TEXT)
    pin.convert_result = f'> vmess://{b64encode(str(subscribe_data).encode()).decode()}'
    toast('????????????????????????')


def back_main():
    run_js("location.href=url", url='/?app=index')


def enter_app(url_content: str, url_type: str):
    if url_content != '':
        if url_type == '????????????':
            run_js("location.href=url", url=f'/?app=subscribe&subscribe={urlparse.quote(url_content)}')
        else:
            run_js("location.href=url", url=f'/?app=result&content={urlparse.quote(url_content)}&type={urlparse.quote(url_type)}')
    else:
        toast('????????????????????????')


def subscribe():
    filename = input(label='???????????????', type=TEXT, required=True)
    run_js("location.href=url", url=f'/static/{filename}.html')


@config(title='V2ray??????????????????', theme='minty')
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
            put_markdown('# ????????????')
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
                    put_markdown(f"## ??????{subscribe_data['sn']}")
                    put_tabs([
                        {'title': '????????????', 'content': [
                            put_table([
                                ['??????', '??????'],
                                ['??????/??????', subscribe_data['ps']],
                                ['????????????', subscribe_data['protocol']]
                            ])
                        ]},
                        {'title': '????????????', 'content': [
                            put_table([
                                ['??????', '??????'],
                                ['????????????', subscribe_data['protocol']],
                                ['???????????????', subscribe_data['add']],
                                ['???????????????', subscribe_data['port']],
                                ['??????ID???UUID???', subscribe_data['id']],
                                ['??????ID', subscribe_data['aid']],
                                ['????????????????????????', subscribe_data['scy']],
                                ['????????????', subscribe_data['net']],
                                ['????????????', subscribe_data['type']],
                                ['????????????', subscribe_data['host']],
                                ['????????????', subscribe_data['path']],
                                ['????????????', subscribe_data['tls']],
                                ['??????/??????', subscribe_data['ps']]
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
                    put_markdown(f"## ??????{subscribe_data['sn']}")
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
                        {'title': '????????????', 'content': [
                            put_table([
                                ['??????', '??????'],
                                ['??????/??????', subscribe_data['ps']],
                                ['????????????', subscribe_data['protocol']]
                            ])
                        ]},
                        {'title': '????????????', 'content': [
                            put_table([
                                ['??????', '??????'],
                                ['????????????', subscribe_data['protocol']],
                                ['???????????????', subscribe_data['add']],
                                ['???????????????', subscribe_data['port']],
                                ['??????ID???UUID???', subscribe_data['id']],
                                ['??????/??????', subscribe_data['ps']]
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
                    put_markdown(f"## ??????{subscribe_data['sn']}")
                    subscribe_data['add'] = subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[:1][0].split('@')[1:][0]
                    subscribe_data['port'] = subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[1:][0].split('#')[:1][0]
                    subscribe_data['passwd'] = b64decode(
                        subscribe_url_encode_protocol_url.split('://')[1:][0].split('@')[:1][0]).decode().split(':')[1:][0]
                    subscribe_data['scy'] = b64decode(
                        subscribe_url_encode_protocol_url.split('://')[1:][0].split('@')[:1][0]).decode().split(':')[:1][0]
                    subscribe_data['ps'] = urlparse.unquote(
                        subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[1:][0].split('#')[1:][0]).replace('+', ' ')
                    put_tabs([
                        {'title': '????????????', 'content': [
                            put_table([
                                ['??????', '??????'],
                                ['??????/??????', subscribe_data['ps']],
                                ['????????????', subscribe_data['protocol']]
                            ])
                        ]},
                        {'title': '????????????', 'content': [
                            put_table([
                                ['??????', '??????'],
                                ['????????????', subscribe_data['protocol']],
                                ['???????????????', subscribe_data['add']],
                                ['???????????????', subscribe_data['port']],
                                ['??????', subscribe_data['passwd']],
                                ['????????????????????????', subscribe_data['scy']],
                                ['??????/??????', subscribe_data['ps']]
                            ])
                        ]},
                    ])
                    put_markdown('---')
                    subscribe_url_decode_data.append(subscribe_data)
            put_markdown(f'### ???{len(subscribe_url_decode_data)}?????????')
            put_buttons(['????????????', '????????????', '????????????', '?????????????????????????????????', '????????????'],
                        onclick=[url_edit, url_del, url_encode, save_to_local, back_main])
            put_markdown('---')
            put_textarea(label='???????????????????????????', name='convert_result', value='', readonly=True)
        elif fnmatch(url_content, '*http*'):
            for subscribe_url in url_content.replace("'", '').split(' '):
                if fnmatch(subscribe_url, 'http*'):
                    subscribe_url_encode_data = b64decode(
                        urlopen(request.Request(url=subscribe_url, headers=HEADERS)).read()).decode().split()
                    put_markdown(f'# {subscribe_url}???????????????')
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
                            put_markdown(f"## ??????{subscribe_data['sn']}")
                            put_tabs([
                                {'title': '????????????', 'content': [
                                    put_table([
                                        ['??????', '??????'],
                                        ['??????/??????', subscribe_data['ps']],
                                        ['????????????', subscribe_data['protocol']]
                                    ])
                                ]},
                                {'title': '????????????', 'content': [
                                    put_table([
                                        ['??????', '??????'],
                                        ['????????????', subscribe_data['protocol']],
                                        ['???????????????', subscribe_data['add']],
                                        ['???????????????', subscribe_data['port']],
                                        ['??????ID???UUID???', subscribe_data['id']],
                                        ['??????ID', subscribe_data['aid']],
                                        ['????????????????????????', subscribe_data['scy']],
                                        ['????????????', subscribe_data['net']],
                                        ['????????????', subscribe_data['type']],
                                        ['????????????', subscribe_data['host']],
                                        ['????????????', subscribe_data['path']],
                                        ['????????????', subscribe_data['tls']],
                                        ['??????/??????', subscribe_data['ps']]
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
                            put_markdown(f"## ??????{subscribe_data['sn']}")
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
                                {'title': '????????????', 'content': [
                                    put_table([
                                        ['??????', '??????'],
                                        ['??????/??????', subscribe_data['ps']],
                                        ['????????????', subscribe_data['protocol']]
                                    ])
                                ]},
                                {'title': '????????????', 'content': [
                                    put_table([
                                        ['??????', '??????'],
                                        ['????????????', subscribe_data['protocol']],
                                        ['???????????????', subscribe_data['add']],
                                        ['???????????????', subscribe_data['port']],
                                        ['??????ID???UUID???', subscribe_data['id']],
                                        ['??????/??????', subscribe_data['ps']]
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
                            put_markdown(f"## ??????{subscribe_data['sn']}")
                            subscribe_data['add'] = subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[:1][0].split('@')[1:][0]
                            subscribe_data['port'] = subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[1:][0].split('#')[:1][0]
                            subscribe_data['passwd'] = b64decode(
                                subscribe_url_encode_protocol_url.split('://')[1:][0].split('@')[:1][0]).decode().split(':')[1:][0]
                            subscribe_data['scy'] = b64decode(
                                subscribe_url_encode_protocol_url.split('://')[1:][0].split('@')[:1][0]).decode().split(':')[:1][0]
                            subscribe_data['ps'] = urlparse.unquote(
                                subscribe_url_encode_protocol_url.split('://')[1:][0].split(':')[1:][0].split('#')[1:][0]).replace('+', ' ')
                            put_tabs([
                                {'title': '????????????', 'content': [
                                    put_table([
                                        ['??????', '??????'],
                                        ['??????/??????', subscribe_data['ps']],
                                        ['????????????', subscribe_data['protocol']]
                                    ])
                                ]},
                                {'title': '????????????', 'content': [
                                    put_table([
                                        ['??????', '??????'],
                                        ['????????????', subscribe_data['protocol']],
                                        ['???????????????', subscribe_data['add']],
                                        ['???????????????', subscribe_data['port']],
                                        ['??????', subscribe_data['passwd']],
                                        ['????????????????????????', subscribe_data['scy']],
                                        ['??????/??????', subscribe_data['ps']]
                                    ])
                                ]},
                            ])
                            put_markdown('---')
                            subscribe_url_decode_data.append(subscribe_data)
            put_markdown(f'### ???{len(subscribe_url_decode_data)}?????????')
            put_buttons(['????????????', '????????????', '????????????', '?????????????????????????????????', '????????????'],
                        onclick=[url_edit, url_del, url_encode, save_to_local, back_main])
            put_markdown('---')
            put_textarea(label='???????????????????????????', name='convert_result', value='', readonly=True)
        else:
            toast('??????????????????URL???')
    elif url_type == 'VMESS':
        if fnmatch(url_content, 'vmess://*'):
            subscribe_data = loads(b64decode(url_content.split('://')[1:][0]).decode())
            subscribe_keys = ['add', 'port', 'id', 'aid', 'scy', 'net', 'type', 'host', 'path', 'tls', 'ps']
            for key in subscribe_keys:
                if key not in subscribe_data.keys():
                    subscribe_data[f'{key}'] = ''
            put_markdown('# ????????????')
            put_tabs([
                {'title': '????????????', 'content': [
                    put_table([
                        ['??????', '??????'],
                        ['??????/??????', subscribe_data['ps']]
                    ])
                ]},
                {'title': '????????????', 'content': [
                    put_table([
                        ['??????', '??????'],
                        ['???????????????', subscribe_data['add']],
                        ['???????????????', subscribe_data['port']],
                        ['??????ID???UUID???', subscribe_data['id']],
                        ['??????ID', subscribe_data['aid']],
                        ['????????????????????????', subscribe_data['scy']],
                        ['????????????', subscribe_data['net']],
                        ['????????????', subscribe_data['type']],
                        ['????????????', subscribe_data['host']],
                        ['????????????', subscribe_data['path']],
                        ['????????????', subscribe_data['tls']],
                        ['??????/??????', subscribe_data['ps']]
                    ])
                ]},
            ])
            put_buttons(['???????????????????????????', '????????????'], [lambda: edit_trojan(subscribe_data), lambda: back_main()])
            put_markdown('---')
            put_textarea(label='???????????????????????????', name='convert_result', value='', readonly=True)
        else:
            toast('??????????????????VMESS?????????')
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
                {'title': '????????????', 'content': [
                    put_table([
                        ['??????', '??????'],
                        ['??????/??????', subscribe_data['ps']]
                    ])
                ]},
                {'title': '????????????', 'content': [
                    put_table([
                        ['??????', '??????'],
                        ['???????????????', subscribe_data['add']],
                        ['???????????????', subscribe_data['port']],
                        ['??????ID???UUID???', subscribe_data['id']],
                        ['??????/??????', subscribe_data['ps']]
                    ])
                ]},
            ])
            put_buttons(['???????????????????????????', '????????????'], [lambda: edit_trojan(subscribe_data), lambda: back_main()])
            put_markdown('---')
            put_textarea(label='???????????????????????????', name='convert_result', value='', readonly=True)
        else:
            toast('??????????????????TROJAN?????????')
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
                {'title': '????????????', 'content': [
                    put_table([
                        ['??????', '??????'],
                        ['??????/??????', subscribe_data['ps']]
                    ])
                ]},
                {'title': '????????????', 'content': [
                    put_table([
                        ['??????', '??????'],
                        ['???????????????', subscribe_data['add']],
                        ['???????????????', subscribe_data['port']],
                        ['??????', subscribe_data['passwd']],
                        ['????????????????????????', subscribe_data['scy']],
                        ['??????/??????', subscribe_data['ps']]
                    ])
                ]},
            ])
            put_buttons(['???????????????????????????', '????????????'], [lambda: edit_ss(subscribe_data), lambda: back_main()])
            put_markdown('---')
            put_textarea(label='???????????????????????????', name='convert_result', value='', readonly=True)
        else:
            toast('??????????????????SS?????????')


@config(title='V2ray????????????', theme='minty')
def index():
    run_js("""
    $('head meta[name="keywords"]').remove();
    $('footer').remove();
    """)
    global subscribe_url_decode_data
    subscribe_url_decode_data = []
    put_markdown('# V2ray????????????')
    put_input(label='??????????????????', name='content', type=TEXT)
    put_radio(label='??????', options=['URL', 'VMESS', 'TROJAN', 'SS'], inline=True, name="type", value='URL')
    put_buttons(['??????', '????????????'], [lambda: enter_app(pin.content, pin.type), lambda: subscribe()])
    put_markdown('## ????????????????????????')
    put_markdown("???????????????''???????????????????????????????????????????????????????????????!")
    put_markdown('### ?????????')
    put_markdown("> 'https://cn.bing.com' 'https://google.com'")


start_server([index, result], port='4089', host='0.0.0.0', debug=True, static_dir=f'{curdir}/static', auto_open_webbrowser=True)