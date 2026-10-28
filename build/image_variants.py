"""Deterministic image treatments for the artist photo publishing pipeline."""
import io
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps
import images

FONTS = Path(images.HERE) / 'fonts'


def fit_font(draw, text, width, start):
    for size in range(start, 17, -2):
        font = ImageFont.truetype(str(FONTS / 'Anton-Regular.ttf'), size)
        if draw.textbbox((0,0),text,font=font)[2] <= width:
            return font
    return font


def treatments(source, name, island):
    """Original, branded landscape, square crop, and a mirrored color variant."""
    original = Image.open(io.BytesIO(source)).convert('RGB')
    banner = original.copy()
    overlay = Image.new('RGBA',banner.size,(0,0,0,0))
    pen = ImageDraw.Draw(overlay)
    for y in range(banner.height):
        alpha = int(230*max(0,(y/banner.height-.20)/.80))
        pen.line((0,y,banner.width,y), fill=(3,12,11,alpha))
    banner = Image.alpha_composite(banner.convert('RGBA'),overlay).convert('RGB')
    pen=ImageDraw.Draw(banner)
    font=fit_font(pen,name.upper(),1160,100)
    pen.text((54,446),name.upper(),font=font,fill='#ffffff')
    sub=ImageFont.truetype(str(FONTS/'Montserrat-800.ttf'),30)
    pen.text((58,580),'BOUYON'+(' · '+island.upper() if island else ''),font=sub,fill='#27d8c8')
    pen.text((58,646),'BOUYON MUSIQUE',font=ImageFont.truetype(str(FONTS/'Montserrat-800.ttf'),18),fill='#ffffff')
    square=ImageOps.fit(original,(1080,1080),method=Image.Resampling.LANCZOS)
    strip=Image.new('RGBA',square.size,(0,0,0,0))
    draw=ImageDraw.Draw(strip)
    draw.rectangle((0,790,1080,1080),fill=(4,18,16,225))
    square=Image.alpha_composite(square.convert('RGBA'),strip).convert('RGB')
    draw=ImageDraw.Draw(square)
    draw.text((42,826),name.upper(),font=fit_font(draw,name.upper(),996,90),fill='#ffffff')
    draw.text((46,978),'BOUYON · BOUYON MUSIQUE',font=sub,fill='#27d8c8')
    mirror=ImageEnhance.Color(ImageOps.mirror(original)).enhance(.78)
    return {'banner':banner,'square':square,'mirror':mirror}


def encode(im, width, fmt, metadata):
    frame=im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS)
    out=io.BytesIO()
    options={'quality':86,'optimize':True} if fmt=='jpg' else {'quality':84,'method':6}
    frame.save(out,format='JPEG' if fmt=='jpg' else 'WEBP',exif=images.exif_bytes(metadata),
               xmp=images.xmp_packet(metadata),**options)
    return out.getvalue()
