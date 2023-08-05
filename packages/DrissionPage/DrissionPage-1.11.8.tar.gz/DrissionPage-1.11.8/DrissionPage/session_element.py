# -*- coding:utf-8 -*-
"""
@Author  :   g1879
@Contact :   g1879@qq.com
@File    :   session_element.py
"""
from re import match, DOTALL, sub
from typing import Union, List, Tuple
from urllib.parse import urlparse, urljoin, urlunparse

from lxml.etree import tostring
from lxml.html import HtmlElement, fromstring

from .base import DrissionElement
from .common import str_to_loc, translate_loc, format_html


class SessionElement(DrissionElement):
    """session模式的元素对象，包装了一个lxml的Element对象，并封装了常用功能"""

    def __init__(self, ele: HtmlElement, page=None):
        super().__init__(ele, page)

    def __repr__(self):
        attrs = [f"{attr}='{self.attrs[attr]}'" for attr in self.attrs]
        return f'<SessionElement {self.tag} {" ".join(attrs)}>'

    def __call__(self, loc_or_str: Union[Tuple[str, str], str], mode: str = 'single', timeout: float = None):
        """在内部查找元素                                            \n
        例：ele2 = ele1('@id=ele_id')                               \n
        :param loc_or_str: 元素的定位信息，可以是loc元组，或查询字符串
        :param mode: 'single' 或 'all'，对应查找一个或全部
        :param timeout: 不起实际作用，用于和父类对应
        :return: SessionElement对象
        """
        return super().__call__(loc_or_str, mode, timeout)

    @property
    def tag(self) -> str:
        """返回元素类型"""
        return self._inner_ele.tag

    @property
    def html(self) -> str:
        """返回元素outerHTML文本"""
        html = format_html(tostring(self._inner_ele, method="html").decode())
        return html[:html.rfind('>') + 1]  # tostring()会把跟紧元素的文本节点也带上，因此要去掉

    @property
    def inner_html(self) -> str:
        """返回元素innerHTML文本"""
        r = match(r'<.*?>(.*)</.*?>', self.html, flags=DOTALL)
        return '' if not r else r.group(1)

    @property
    def attrs(self) -> dict:
        """返回元素所有属性及值"""
        return {attr: self.attr(attr) for attr, val in self.inner_ele.items()}

    @property
    def text(self) -> str:
        """返回元素内所有文本"""

        # 为尽量保证与浏览器结果一致，弄得比较复杂
        def get_node(ele, pre: bool = False):
            str_list = []
            if ele.tag == 'pre':
                pre = True

            current_tag = None
            for el in ele.eles('xpath:./text() | *'):
                if current_tag in ('br', 'p') and str_list and str_list[-1] != '\n':
                    str_list.append('\n')

                if isinstance(el, str):
                    if sub('[ \n]', '', el) != '':
                        if pre:
                            str_list.append(el)
                        else:
                            str_list.append(el.replace('\n', ' ').strip(' \t'))

                    elif '\n' in el and str_list and str_list[-1] != '\n':
                        str_list.append('\n')
                    else:
                        str_list.append(' ')
                    current_tag = None
                else:
                    str_list.extend(get_node(el, pre))
                    current_tag = el.tag

            return str_list

        re_str = ''.join(get_node(self))
        re_str = sub(r' {2,}', ' ', re_str)
        return format_html(re_str, False)

    @property
    def raw_text(self) -> str:
        """返回未格式化处理的元素内文本"""
        return str(self._inner_ele.text_content())

    def parents(self, num: int = 1):
        """返回上面第num级父元素                                         \n
        :param num: 第几级父元素
        :return: SessionElement对象
        """
        return self.ele(f'xpath:..{"/.." * (num - 1)}')

    def attr(self, attr: str) -> Union[str, None]:
        """返回attribute属性值                           \n
        :param attr: 属性名
        :return: 属性值文本，没有该属性返回None
        """
        # 获取href属性时返回绝对url
        if attr == 'href':
            link = self.inner_ele.get('href')

            # 若为链接为None、js或邮件，直接返回
            if not link or link.lower().startswith(('javascript:', 'mailto:')):
                return link

            # 其它情况直接返回绝对url
            else:
                return self._make_absolute(link)

        elif attr == 'src':
            return self._make_absolute(self.inner_ele.get('src'))

        elif attr in ('text', 'innerText'):
            return self.text

        elif attr == 'outerHTML':
            return self.html

        elif attr == 'innerHTML':
            return self.inner_html

        else:
            return self.inner_ele.get(attr)

    def ele(self, loc_or_str: Union[Tuple[str, str], str], mode: str = None, timeout=None):
        """返回当前元素下级符合条件的子元素、属性或节点文本，默认返回第一个                                      \n
        :param loc_or_str: 元素的定位信息，可以是loc元组，或查询字符串
        :param mode: 'single' 或 'all‘，对应查找一个或全部
        :param timeout: 不起实际作用，用于和父类对应
        :return: SessionElement对象
        """
        if isinstance(loc_or_str, (str, tuple)):
            if isinstance(loc_or_str, str):
                loc_or_str = str_to_loc(loc_or_str)
            else:
                if len(loc_or_str) != 2:
                    raise ValueError("Len of loc_or_str must be 2 when it's a tuple.")
                loc_or_str = translate_loc(loc_or_str)
        else:
            raise ValueError('Argument loc_or_str can only be tuple or str.')

        element = self
        loc_str = loc_or_str[1]

        if loc_or_str[0] == 'xpath' and loc_or_str[1].lstrip().startswith('/'):
            loc_str = f'.{loc_str}'

        # 若css以>开头，表示找元素的直接子元素，要用page以绝对路径才能找到
        if loc_or_str[0] == 'css selector' and loc_or_str[1].lstrip().startswith('>'):
            loc_str = f'{self.css_path}{loc_or_str[1]}'
            element = self.page

        loc_or_str = loc_or_str[0], loc_str

        return execute_session_find(element, loc_or_str, mode)

    def eles(self, loc_or_str: Union[Tuple[str, str], str], timeout=None):
        """返回当前元素下级所有符合条件的子元素、属性或节点文本                                                   \n
        :param loc_or_str: 元素的定位信息，可以是loc元组，或查询字符串
        :param timeout: 不起实际作用，用于和父类对应
        :return: SessionElement对象组成的列表
        """
        return self.ele(loc_or_str, mode='all')

    def _get_ele_path(self, mode) -> str:
        """获取css路径或xpath路径
        :param mode: 'css' 或 'xpath'
        :return: css路径或xpath路径
        """
        path_str = ''
        ele = self

        while ele:
            if mode == 'css':
                brothers = len(ele.eles(f'xpath:./preceding-sibling::*'))
                path_str = f'>:nth-child({brothers + 1}){path_str}'
            else:
                brothers = len(ele.eles(f'xpath:./preceding-sibling::{ele.tag}'))
                path_str = f'/{ele.tag}[{brothers + 1}]{path_str}' if brothers > 0 else f'/{ele.tag}{path_str}'

            ele = ele.parent

        return path_str[1:] if mode == 'css' else path_str

    # ----------------session独有方法-----------------------
    def _make_absolute(self, link) -> str:
        """获取绝对url
        :param link: 超链接
        :return: 绝对链接
        """
        if not link:
            return link

        parsed = urlparse(link)._asdict()

        # 相对路径，与页面url拼接并返回
        if not parsed['netloc']:  # 相对路径，与
            return urljoin(self.page.url, link)

        # 绝对路径但缺少协议，从页面url获取协议并修复
        if not parsed['scheme']:
            parsed['scheme'] = urlparse(self.page.url).scheme
            parsed = tuple(v for v in parsed.values())
            return urlunparse(parsed)

        # 绝对路径且不缺协议，直接返回
        return link


def execute_session_find(page_or_ele,
                         loc: Tuple[str, str],
                         mode: str = 'single', ) -> Union[SessionElement, List[SessionElement], str, None]:
    """执行session模式元素的查找                              \n
    页面查找元素及元素查找下级元素皆使用此方法                   \n
    :param page_or_ele: SessionPage对象或SessionElement对象
    :param loc: 元素定位元组
    :param mode: 'single' 或 'all'，对应获取第一个或全部
    :return: 返回SessionElement元素或列表
    """
    mode = mode or 'single'
    if mode not in ('single', 'all'):
        raise ValueError(f"Argument mode can only be 'single' or 'all', not '{mode}'.")

    # 根据传入对象类型获取页面对象和lxml元素对象
    if isinstance(page_or_ele, SessionElement):
        page = page_or_ele.page
        page_or_ele = page_or_ele.inner_ele
    else:  # 传入的是SessionPage对象
        page = page_or_ele
        page_or_ele = fromstring(sub(r'&nbsp;?', '&nbsp;', page_or_ele.response.text))

    try:
        # 用lxml内置方法获取lxml的元素对象列表
        if loc[0] == 'xpath':
            ele = page_or_ele.xpath(loc[1])

        # 用css selector获取元素对象列表
        else:
            ele = page_or_ele.cssselect(loc[1])

        # 结果不是列表，如数字
        if not isinstance(ele, list):
            return ele

        # 把lxml元素对象包装成SessionElement对象并按需要返回第一个或全部
        if mode == 'single':
            ele = ele[0] if ele else None

            if isinstance(ele, HtmlElement):
                return SessionElement(ele, page)
            elif isinstance(ele, str):
                return ele
            else:
                return None

        elif mode == 'all':
            return [SessionElement(e, page) if isinstance(e, HtmlElement) else e for e in ele if e != '\n']

    except Exception as e:

        if 'Invalid expression' in str(e):
            raise SyntaxError(f'Invalid xpath syntax. {loc}')
        elif 'Expected selector' in str(e):
            raise SyntaxError(f'Invalid css selector syntax. {loc}')

        raise e
