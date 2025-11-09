from contextlib import contextmanager
from time import sleep
from random import randint
import sys
from typing import Callable, Optional, Tuple, Any, List


from ascript.android import action
from ascript.android.action import click
from ascript.android.screen import FindColors, Ocr, FindImages
from ascript.android.system import R

import logging


# 相似度
DIFF = 0.9

# 最大尝试次数
MAX_RETRIES = 1

# 尝试间隔
INTERVAL = 0

# 结束后等待时间
WAIT = 0.1

FULL_SRC = [0,0,1264,2780]

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



## 程序无法继续进行时调用，弹出提示框和提示内容
def err(code=1,text="错误类型缺省"):
	logger.error(text)
	p = action.catch_click(f"程序出错，点击屏幕结束\n错误代码:{code}\n{text}")
	sys.exit()

## 程序结束时调用，弹出提示框和提示内容，提示内容默认为空
def end(text = ''):
	action.catch_click(f"程序结束，请点击屏幕\n{text}")
	sys.exit()



def _find_with_retry(
	finder: Callable[[], Any],
	desc = None,
	max_retries: int = MAX_RETRIES,
	interval: float = INTERVAL,
	wait: float = WAIT,
) -> Any:
	"""
	通用重试框架：执行 finder()，直到成功或耗尽重试次数。
	- finder 应返回“真值”表示成功，None/[]/False 表示未找到。
	- 成功时立即返回结果；失败返回 None。
	"""
	for _ in range(max_retries):
		result = finder()
		if result:  # 支持 list、对象、tuple 等非空即真
			logger.info(f"寻找 成功：{result}")
			sleep(wait)
			return result
		sleep(interval)
	logger.info(f"寻找 失败")
	sleep(wait)
	return None

# --- 文本策略 ---
def _ocr_find_text(area, pattern, confidence):
	res = Ocr.paddleocr_v2(rect=area, pattern=pattern, confidence=confidence)
	if not res:
		res = Ocr.mlkitocr_v2(rect=area, pattern=pattern)
	return (res[0].center_x, res[0].center_y) if res else None

def _ocr_find_text_get(area, pattern, confidence):
	res = Ocr.paddleocr_v2(rect=area, pattern=pattern, confidence=confidence)
	if not res:
		res = Ocr.mlkitocr_v2(rect=area, pattern=pattern)
	return [item.text for item in res] if res else None

# --- 图片策略 ---
def _ocr_find_image(area, img_path, confidence):
	results = FindImages.find_all_template([img_path], rect=area, confidence=confidence)
	if results:
		first = results[0]
		return (int(first['center_x']), int(first['center_y']))
	return None

# --- 多色策略 ---
def _ocr_find_color(area, pattern, diff):
	results = FindColors.find(pattern, rect=area, diff=diff)
	if results:
		x, y = results.x, results.y
		return (int(x), int(y))
	return None


# 方法1：寻找文本_base
def find_text_base(area, pattern, desc=None,
				   confidence=DIFF, max_retries=MAX_RETRIES,
				   interval=INTERVAL, wait=WAIT):
	if desc is None:
		desc = str(pattern)
	logger.info(f"寻找 '{desc}' ...")
	return _find_with_retry(
		lambda: _ocr_find_text(area, pattern, confidence),
		desc, max_retries, interval, wait
	)

# 方法2：寻找文本_逐字（任意一字）
def find_text_any(area, pattern, desc=None,
                  confidence=DIFF, max_retries=MAX_RETRIES,
                  interval=INTERVAL, wait=WAIT):
	if desc is None:
		desc = str(pattern)
	logger.info(f"寻找 '{desc}' (逐字)...")
	if not pattern:
		return None
	for char in pattern:
		pos = find_text_base(area, char,
							 confidence=confidence, max_retries=max_retries,
							 interval=interval, wait=0)
		if pos:
			sleep(wait)
			return pos
	sleep(wait)
	return None

# 方法3：输出找到的文字
def find_text_out(area, pattern, desc=None,
					  confidence=DIFF, max_retries=MAX_RETRIES,
					  interval=INTERVAL, wait=WAIT):
	if desc is None:
		desc = str(pattern)
	logger.info(f"寻找 '{desc}' ...")
	return _find_with_retry(
		lambda: _ocr_find_text_get(area, pattern, confidence),
		desc, max_retries, interval, wait
	) or []  # 确保返回 list 而非 None

# 方法4：寻找图片
def find_img(area, pattern, desc=None,
			   confidence=DIFF, max_retries=MAX_RETRIES,
			   interval=INTERVAL, wait=WAIT):
	if desc is None:
		desc = str(pattern)
	logger.info(f"寻找 '{desc}' ...")
	img_path = R.img(f"{pattern}.png")
	return _find_with_retry(
		lambda: _ocr_find_image(area, img_path, confidence),
		desc,max_retries, interval, wait
	)

# 方法5：多色寻找
def find_color(area, pattern, desc="多色",
					confidence=DIFF, max_retries=MAX_RETRIES,
					interval=INTERVAL, wait=WAIT):
	if desc is None:
		desc = str(pattern)
	logger.info(f"寻找 '{desc}' ...")
	return _find_with_retry(
		lambda: _ocr_find_color(area, pattern, confidence),
		desc, max_retries, interval, wait
	)

print("————————————————before")
# res = find_text_content(area=FULL_SRC,pattern="天机",desc = "摩尔线程")
# res = find_text_any(area=FULL_SRC,pattern="天机")
# res2 = find_text_base(area=FULL_SRC,pattern="天机",desc = "摩尔线程")
# res = find_image(FULL_SRC,"2")
res = find_color(FULL_SRC,"982,2428,#CF6D97|1018,2428,#F9FAFE|985,2454,#213166|1015,2454,#324E87","关闭")
print("————————————————after")
print(res)
# click(res[0],res[1])
end()

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