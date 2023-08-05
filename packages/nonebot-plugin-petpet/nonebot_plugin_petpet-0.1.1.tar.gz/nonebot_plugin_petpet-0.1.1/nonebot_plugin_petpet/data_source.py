import base64
from nonebot.log import logger
from nonebot.adapters.cqhttp import MessageSegment

from .download import get_avatar, get_image, DownloadError
from .functions import petpet, kiss, rub, play, rip, throw, crawl, support


commands = {
    'petpet': {
        'aliases': {'摸', '摸摸', 'rua'},
        'func': petpet
    },
    'kiss': {
        'aliases': {'亲', '亲亲'},
        'func': kiss
    },
    'rub': {
        'aliases': {'贴', '贴贴', '蹭', '蹭蹭'},
        'func': rub
    },
    'play': {
        'aliases': {'顶', '玩'},
        'func': play
    },
    'rip': {
        'aliases': {'撕'},
        'func': rip
    },
    'throw': {
        'aliases': {'丢', '扔'},
        'func': throw
    },
    'crawl': {
        'aliases': {'爬'},
        'func': crawl
    },
    'support': {
        'aliases': {'精神支柱'},
        'func': support
    }
}


async def make_image(type: str, self_id: str, user_id: str = '', img_url: str = ''):
    try:
        if type not in commands:
            return None

        if user_id:
            user_img = await get_avatar(user_id)
        elif img_url:
            user_img = await get_image(img_url)
        else:
            return None

        func = commands[type]['func']

        if type in ['kiss', 'rub']:
            self_img = await get_avatar(self_id)
            result = await func(self_img, user_img)
        else:
            result = await func(user_img)
        return MessageSegment.image(f'base64://{base64.b64encode(result.getvalue()).decode()}')

    except DownloadError:
        return '下载出错，请稍后再试'
    except Exception as e:
        logger.warning(str(e))
        return '出错了，请稍后再试'
