# using pymupdf4llm
# import pymupdf4llm
# import pathlib
# md_text = pymupdf4llm.to_markdown("tests/data/新西兰攻略2024.pdf")
# pathlib.Path("output.md").write_bytes(md_text.encode())

# using paddleocr
from paddleocr import PaddleOCR, draw_ocr
ocr = PaddleOCR(use_angle_cls=True, lang='en')
img_path = 'tests/data/itinerary-flight-tickets.png'
result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)

# draw result
# from PIL import Image
# result = result[0]
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# im_show = draw_ocr(image, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/fonts/simfang.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')