import io
import random
import imageio
from typing import List, Tuple
from PIL.Image import Image as IMG
from PIL import Image, ImageDraw, ImageFilter

from .download import get_resource


def resize(img: IMG, size: Tuple[int, int]) -> IMG:
    return img.resize(size, Image.ANTIALIAS)


def rotate(img: IMG, angle: int, expand: bool = True) -> IMG:
    return img.rotate(angle, Image.BICUBIC, expand=expand)


def circle(img: IMG) -> IMG:
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0))
    img.putalpha(mask)
    return img


def to_gif(frames: List[IMG], duration: float) -> io.BytesIO:
    output = io.BytesIO()
    imageio.mimsave(output, frames, format='gif', duration=duration)
    return output


def to_jpg(frame: IMG) -> io.BytesIO:
    output = io.BytesIO()
    frame = frame.convert('RGB')
    frame.save(output, format='jpeg')
    return output


async def petpet(img: IMG) -> io.BytesIO:
    frames = []
    locs = [(14, 20, 98, 98), (12, 33, 101, 85), (8, 40, 110, 76),
            (10, 33, 102, 84), (12, 20, 98, 98)]
    for i in range(5):
        frame = Image.new('RGBA', (112, 112), (255, 255, 255, 0))
        x, y, l, w = locs[i]
        frame.paste(img.resize((l, w), Image.ANTIALIAS), (x, y))
        hand = await get_resource('petpet', f'{i}.png')
        frame.paste(hand, mask=hand)
        frames.append(frame)
    return to_gif(frames, 0.06)


async def kiss(self_img: IMG, user_img: IMG) -> io.BytesIO:
    user_locs = [(58, 90), (62, 95), (42, 100), (50, 100), (56, 100), (18, 120), (28, 110),
                 (54, 100), (46, 100), (60, 100), (35, 115), (20, 120), (40, 96)]
    self_locs = [(92, 64), (135, 40), (84, 105), (80, 110), (155, 82), (60, 96), (50, 80),
                 (98, 55), (35, 65), (38, 100), (70, 80), (84, 65), (75, 65)]
    frames = []
    for i in range(13):
        frame = await get_resource('kiss', f'{i}.png')
        user_head = resize(circle(user_img), (50, 50))
        frame.paste(user_head, user_locs[i], mask=user_head)
        self_head = resize(circle(self_img), (40, 40))
        frame.paste(self_head, self_locs[i], mask=self_head)
        frames.append(frame)
    return to_gif(frames, 0.05)


async def rub(self_img: IMG, user_img: IMG) -> io.BytesIO:
    user_locs = [(39, 91, 75, 75), (49, 101, 75, 75), (67, 98, 75, 75),
                 (55, 86, 75, 75), (61, 109, 75, 75), (65, 101, 75, 75)]
    self_locs = [(102, 95, 70, 80, 0), (108, 60, 50, 100, 0), (97, 18, 65, 95, 0),
                 (65, 5, 75, 75, -20), (95, 57, 100, 55, -70), (109, 107, 65, 75, 0)]
    frames = []
    for i in range(6):
        frame = await get_resource('rub', f'{i}.png')
        x, y, w, h = user_locs[i]
        user_head = resize(circle(user_img), (w, h))
        frame.paste(user_head, (x, y), mask=user_head)
        x, y, w, h, angle = self_locs[i]
        self_head = rotate(resize(circle(self_img), (w, h)), angle)
        frame.paste(self_head, (x, y), mask=self_head)
        frames.append(frame)
    return to_gif(frames, 0.05)


async def play(img: IMG) -> io.BytesIO:
    locs = [(180, 60, 100, 100), (184, 75, 100, 100), (183, 98, 100, 100),
            (179, 118, 110, 100), (156, 194, 150, 48), (178, 136, 122, 69),
            (175, 66, 122, 85), (170, 42, 130, 96), (175, 34, 118, 95),
            (179, 35, 110, 93), (180, 54, 102, 93), (183, 58, 97, 92),
            (174, 35, 120, 94), (179, 35, 109, 93), (181, 54, 101, 92),
            (182, 59, 98, 92), (183, 71, 90, 96), (180, 131, 92, 101)]
    raw_frames = []
    for i in range(23):
        raw_frame = await get_resource('play', f'{i}.png')
        raw_frames.append(raw_frame)
    img_frames = []
    for i in range(len(locs)):
        frame = Image.new('RGBA', (480, 400), (255, 255, 255, 0))
        x, y, l, w = locs[i]
        frame.paste(resize(img, (l, w)), (x, y))
        raw_frame = raw_frames[i]
        frame.paste(raw_frame, mask=raw_frame)
        img_frames.append(frame)
    frames = []
    for i in range(2):
        frames.extend(img_frames[0:12])
    frames.extend(img_frames[0:8])
    frames.extend(img_frames[12:18])
    frames.extend(raw_frames[18:23])
    return to_gif(frames, 0.06)


async def rip(img: IMG) -> io.BytesIO:
    rip = await get_resource('rip', '0.png')
    frame = Image.new('RGBA', rip.size, (255, 255, 255, 0))
    left = rotate(resize(img, (385, 385)), 24)
    right = rotate(resize(img, (385, 385)), -11)
    frame.paste(left, (-5, 355))
    frame.paste(right, (649, 310))
    frame.paste(rip, mask=rip)
    return to_jpg(frame)


async def throw(img: IMG) -> io.BytesIO:
    img = resize(rotate(circle(img), random.randint(1, 360), expand=False), (143, 143))
    frame = await get_resource('throw', '0.png')
    frame.paste(img, (15, 178), mask=img)
    return to_jpg(frame)


async def crawl(img: IMG) -> io.BytesIO:
    img = resize(circle(img), (100, 100))
    frame = await get_resource('crawl', '{:02d}.jpg'.format(random.randint(1, 91)))
    frame.paste(img, (0, 400), mask=img)
    return to_jpg(frame)


async def support(img: IMG) -> io.BytesIO:
    support = await get_resource('support', '0.png')
    frame = Image.new('RGBA', support.size, (255, 255, 255, 0))
    img = rotate(resize(img, (815, 815)), 23)
    frame.paste(img, (-172, -17))
    frame.paste(support, mask=support)
    return to_jpg(frame)
