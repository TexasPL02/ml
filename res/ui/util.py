import logging
from time import sleep
from random import randint

from ascript.android.action import click
from ascript.android.screen import FindColors, Ocr, FindImages
from ascript.android.system import R


from contextlib import contextmanager
# 相似度
DIFF = 0.9

# 最大尝试次数
MAX_RETRIES = 3

# 尝试间隔
INTERVAL = 0.3

# 结束后等待时间
WAIT = 0.2

# 打印日志
ISPRINT = 0

# 配置日志
logging.basicConfig(
	level=logging.INFO,
    format='(%(lineno)d行) %(funcName)s() : %(message)s'  # ← 关键：只保留消息
    )
logger = logging.getLogger(__name__)



@contextmanager
def temp_log_level(logger_obj, temp_level):
	"""
	临时修改 logger 级别，退出时自动恢复
	"""
	original_level = logger_obj.level  # 保存原始级别
	logger_obj.setLevel(temp_level)  # 设置临时级别
	try:
		yield logger_obj
	finally:
		logger_obj.setLevel(original_level)  # 恢复原始级别




def err(code=1,text="错误类型缺省"):
	logger.error(text)
	p = action.catch_click(f"程序出错，点击屏幕结束\n错误代码:{code}\n{text}")
	quit()

def end(text = ''):
	action.catch_click(f"程序结束，请点击屏幕\n{text}")
	quit()


p = (0,0)
# 寻找元素坐标_寻找类型（ 寻找区域， 寻找参数, 文本，打印日志）
# 文字检测
def find_text(area, pattern, name,
              confidence=DIFF, max_retries=MAX_RETRIES, interval=INTERVAL, wait=WAIT,
              isprint = ISPRINT):
	res = []
	isprint and logging.info(f"[文本]寻找'{name}'中……")
	for i in range(max_retries):
		res = (Ocr.paddleocr_v2(rect=area, pattern=pattern,confidence = confidence)
		       or Ocr.mlkitocr_v2(rect=area, pattern=pattern))
		if res is None:
			sleep(interval)
		else:
			isprint and logging.info(f"[文本]寻找 成功'{name}':{res}")
			res = (res[0].center_x, res[0].center_y)
			break
	if not res:
		isprint and logging.warning(f"[文本]寻找 失败'{name}'（{max_retries}次）")
	sleep(wait)
	return res if res is not None else 0

# 文字遍历检测
def find_text_exist(area, pattern, name, confidence=DIFF,
                    max_retries=MAX_RETRIES, interval=INTERVAL, wait=WAIT,
                    isprint = ISPRINT):
	isprint and logging.warning(f"[文本]寻找'{name}'中……")
	for (i,s) in enumerate(pattern):
		res = find_text(area, s, s,
		                confidence, max_retries, interval, wait,
		                isprint = 0)
		if res:
			isprint and logging.warning(f"[文本]寻找 成功'{name}'")
			return res
	else:
		isprint and logging.warning(f"[文本]寻找 失败'{name}'")
		return 0



# 输出识别文字
def find_text_out(area, pattern, name,
                  confidence=DIFF, max_retries=MAX_RETRIES, interval=INTERVAL, wait=WAIT,
                  isprint = ISPRINT):
	res = []
	isprint and logging.info(f"[文本]寻找'{name}'中……")
	for i in range(max_retries):
		res = (Ocr.paddleocr_v2(rect=area, pattern=pattern,confidence = confidence)
		       or Ocr.mlkitocr_v2(rect=area, pattern=pattern))
		if res is None:
			# logging.info(f"第({i + 1})次未找到'{name}'")
			sleep(interval)
		else:
			isprint and logging.info(f"[文本]寻找 成功'{name}':{res}")
			# res = (res[0].center_x, res[0].center_y)
			break
	if not res :
		isprint and logging.warning(f"[文本]寻找 失败'{name}'（{max_retries}次）")
	sleep(wait)
	return res if res is not None else 0


def find_img(area, pattern, name,
             confidence=DIFF, max_retries=MAX_RETRIES, interval=INTERVAL, wait=WAIT,
              isprint = ISPRINT):
	res = []
	isprint and logging.info(f"[图片]寻找'{name}'中……")
	for i in range(max_retries):
		res = FindImages.find_template([R.img(f"{pattern}.png")], rect=area,
		                               confidence=confidence)
		if res is None:
			# logging.info(f"第({i + 1})次未找到'{name}'")
			sleep(interval)
		else:
			isprint and logging.info(f"[图片]寻找 成功'{name}':{res}")
			res = (res['result'][0], res['result'][1])
			break

	if not res:
		isprint and logging.warning(f"[图片]寻找 失败'{name}'（{max_retries}次）")
	sleep(wait)
	return res if res is not None else 0


def find_color(area, pattern, name,
               confidence=DIFF, max_retries=MAX_RETRIES, interval=INTERVAL, wait=WAIT,
              isprint = ISPRINT):
	res = []
	isprint and logging.info(f"[图色]寻找'{name}'中……")
	for i in range(max_retries):
		res = FindColors.find(pattern, rect=area, diff=confidence)
		if res is None:
			# logging.info(f"第({i + 1})次未找到'{name}'")
			sleep(interval)
		else:
			isprint and logging.info(f"[图色]寻找 成功'{name}':{res}")
			res = (res.x, res.y)
			break
	if not res:
		isprint and logging.warning(f"[图色]寻找 失败'{name}'（{max_retries}次）")
	sleep(wait)
	return res if res else 0


# 点击坐标

def click_p(p,x=0,y=0,r_x=10,r_y=10, wait=WAIT):
	if p:
		p_x = p[0]
		p_y = p[1]
		r_x = randint(-r_x, r_x)
		r_y = randint(-r_y, r_y)
		c_x = p_x+x+r_x
		c_y = p_y+y+r_y
		logging.info(f"点击:({c_x},{c_y})")
		click(c_x, c_y)
		sleep(wait)
		return 1
	return 0


# 点击区域
def click_a(a,wait=WAIT):
	r_x = randint(a[0], a[2])
	r_y = randint(a[1], a[3])
	logging.info(f"点击:({r_x},{r_y})")
	click(r_x, r_y)
	sleep(wait)
	return 1

def moveUp(a1,a2,b1,b2,d1=700,d2=700):
	print(f"按下({a1},{a2})，耗时{d1}ms")
	action.Touch.down(a1, a2)
	action.Touch.move(b1, b2,d1)
	action.Touch.up(b1, b2,d2)
	print(f"抬起({b1},{b2})，耗时{d2}ms)")

def moveUP_desktop(a1,a2,b1,b2,d1=700):
	print(f"按下({a1},{a2})")
	action.slide(a1, a2, b1, b2, d1)
	print(f"抬起({b1},{b2})，耗时{d1}ms)")

# find_element(1,[1,1,500,500],"直播","测试")
# p = find_element("text",[1,1,1200,1200],"直播","测试2")

# 【】        [<airscript.screen.OcrText 'OcrText{text='直播 推荐 热门',confidence=1.0, center_x=316, center_y=190, rect=[104,164,529,217], text_box_position=[]}'>,
# <airscript.screen.OcrText 'OcrText{text='【直播】JDG vs VWBG 异哩哔哩英雄联盟赛事',confidence=1.0, center_x=357, center_y=340, rect=[148,292,566,388], text_box_position=[]}'>]
# 【0】       OcrText{text='直播 推荐 热门',confidence=1.0, center_x=317, center_y=357, rect=[105,331,529,384], text_box_position=[]}
# 【err】     None
# 【err 0】   TypeError: 'NoneType' object is not subscriptable



# test = "259,612,#9398BE|295,610,#849EC1|355,609,#FFEFE7|243,660,#717670"
# ------------------------------------------------------------p = find_element("color",[1,1,500,500],RED_Detail ,"小红点测试")
# p = find_element("color", [1,1,1200,1200], test, "图色测试")

# 【】        jarray('Landroid/graphics/Point;')
#   ([<android.graphics.Point 'Point(269, 253)'>, <android.graphics.Point 'Point(471, 581)'>,
#   <android.graphics.Point 'Point(256, 600)'>, <android.graphics.Point 'Point(252, 605)'>, <android.graphics.Point 'Point(257, 605)'>,
#   <android.graphics.Point 'Point(262, 608)'>, <android.graphics.Point 'Point(256, 610)'>, <android.graphics.Point 'Point(267, 612)'>,
#   <android.graphics.Point 'Point(261, 613)'>, <android.graphics.Point 'Point(266, 617)'>, <android.graphics.Point 'Point(271, 617)'>,
#   <android.graphics.Point 'Point(260, 618)'>, <android.graphics.Point 'Point(265, 622)'>])
# 【0】       Point(269, 253)
# 【err】     jarray('Landroid/graphics/Point;')([])
# 【err 0】   IndexError: array index out of range



# p = find_element("img",[1,1,1200,1200],"red","小红点测试")

# 【】        [{'result': (169.0, 174.0), 'rectangle': ([160, 167], (160, 181), (178, 167), (178, 181)), 'rect': [160, 167, 178, 181], 'center_x': 169, 'center_y': 174, 'confidence': 0.9955822229385376},
#   {'result': (134.0, 550.0), 'rectangle': ([125, 543], (125, 557), (143, 543), (143, 557)), 'rect': [125, 543, 143, 557], 'center_x': 134, 'center_y': 550, 'confidence': 0.9702301621437073},
#   {'result': (134.0, 737.0), 'rectangle': ([125, 730], (125, 744), (143, 730), (143, 744)), 'rect': [125, 730, 143, 744], 'center_x': 134, 'center_y': 737, 'confidence': 0.9514971375465393}]
# 【0】       {'result': (169.0, 174.0), 'rectangle': ([160, 167], (160, 181), (178, 167), (178, 181)), 'rect': [160, 167, 178, 181], 'center_x': 169, 'center_y': 174, 'confidence': 0.9955822229385376}
# 【err】     []
# 【err 0】   IndexError: list index out of range

# print(p)
# print(p[0])


# 区域识别
from ascript.android import action
def scr_area():

	p1 = action.catch_click("请点击任意位置1",False)
	p2 = action.catch_click("请点击任意位置2",False)
	area = [p1.x,p1.y,p2.x,p2.y]
	# print(p1,p2)
	print(area)
	return area