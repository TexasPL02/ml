import logging

from .util import *
from .data import *


logger = logging.getLogger(__name__)


# ----------------------------
# 通用辅助函数（可选，提升一致性）
# ----------------------------

def _safe_click(find_func, click_func, name: str, *click_args, **click_kwargs) -> bool:
	"""安全点击：先查找，成功再点击并记录日志"""
	elem = find_func()
	if elem != 0:
		if click_func(elem, *click_args, **click_kwargs) != 0:
			logger.info(f"✅ 点击：{name}")
			return True
	logger.debug(f"❌ 未点击：{name}（未找到或点击失败）")
	return False

# ----------------------------
# 具体功能函数
# ----------------------------

def find_back():
	logger.info("寻找：返回")
	return find_color(BACK_CLOSE, BACK_CLOSE_Color, "返回", 0.85)

def click_back() -> bool:
	if not is_in_page_main():
		sleep(0.1)
		return _safe_click(find_back, click_p, "返回",r_x =0, r_y = 0)
	else:
		logger.info("已经在主界面，无法继续返回")
		return True


def find_red(area):
	logger.info("寻找：红点")
	return find_img(area, "red", "红点")

def click_red(area, x=-50, y=50, r_x=5, r_y=5) -> bool:
	return _safe_click(lambda: find_red(area), click_p, "红点", x, y, r_x, r_y)


def find_close():
	logger.info("寻找：关闭")
	return find_color(X_CLOSE, X_CLOSE_Color, "领取关闭")

def click_close() -> bool:
	return _safe_click(find_close, click_p, "关闭")


def find_pop():
	logger.info("寻找：弹窗关闭")
	return find_color(X_POP, X_POP_Color, "弹窗关闭", 0.95)

def click_pop() -> bool:
	return _safe_click(find_pop, click_p, "弹窗关闭")


def find_pop_an():
	logger.info("寻找：公告关闭")
	return find_color(X_POP_AN, X_POP_AN_Color, "公告关闭")

def click_pop_an() -> bool:
	return _safe_click(find_pop_an, click_p, "公告关闭")


def find_get():
	logger.info("寻找：恭喜获得")
	return find_text_any(A_GET, "恭喜获得", "恭喜获得", max_retries=1, interval=0.1, wait=0.1)

def click_get(wait=0.1) -> bool:
	logging.info("点击：恭喜获得")
	sleep(0.3)
	count = 0
	success_count = 0
	for i in range(7):
		if click_p(find_get(), wait=wait) != 0:
			logger.debug(f"第 {i + 1} 次点击恭喜获得成功")
			success_count += 1
		elif count == 0:
			count += 1
		elif success_count != 0:
			return True
		else:
			logger.debug("❌ 未找到：恭喜获得")
			return False

def click_blank(wait = WAIT) -> bool:
	if click_a(A_BLANK, wait=wait) != 0:
		logger.info("✅ 点击：空白区域")
		return True
	logger.debug("❌ 点击空白区域失败")
	return False


# 退出选项框——取消
def find_quit_cancel_btn():
	logging.info("寻找：退出选项")
	return find_text_base(A_CLOSEGAME,"确定退出","确定退出?")

def click_quit_cancel_btn() -> bool:
	elem = find_img(A_CANCEL, "cancel", "取消退出", 0.7)
	if elem != 0 and click_p(elem) != 0:
		logger.info("✅ 点击：退出选项")
		return True
	logger.debug("❌ 未点击：退出选项")
	return False

def is_in_page_main(c=2) -> bool:
	res = (find_text_base(A_BENEFITS,"福利","福利", max_retries=c, interval=0.1, wait=0.1)
		   or find_text_base(A_UNION,"协会","协会", max_retries=c, interval=0.1, wait=0.1))
	if res:
		logger.info("正在主界面")
		return True
	else:
		return False

def to_page_main() -> bool:
	for i in range(5):
		if is_in_page_main(1):
			logger.info("返回主界面 成功")
			return True
		click_back()

	err(text = "返回主界面 失败")
	return False


def	is_in_page_task(c=2) -> bool:
	return find_text_base(A_LIGHT_IN_RICHENG,"日程","闪亮之旅界面",max_retries=c) != 0

def	to_page_task() -> bool:
	for i in range(5):
		if is_in_page_task(1):
			logger.info("返回闪亮之旅界面 成功")
			return 1
		if is_in_page_main():
				elem = find_img(A_LIGHT, "light", "闪亮之旅")
				if elem != 0 and click_p(elem, wait=1) != 0:
					logger.info("已点击进入闪亮之旅")
					return True
		click_back()
	err(text="返回闪亮之旅界面 失败")
	return False



def click_JB(a) -> bool:
	elem = find_img(a, "金币", "金币")
	if elem != 0 and click_p(elem) != 0:
		logger.info("✅ 点击：金币")
		return True
	logger.debug("❌ 未点击：金币")
	return False
# def isLight():
# 	res find_text(A_LIGHT,)

def check_page():
	start_pos = find_text_base(A_Click_Start, "点击开始", "点击开始")
	load_pos = find_text_base(A_Load, "加载", "加载中")
	quit_btn = click_quit_cancel_btn()




