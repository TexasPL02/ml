
from .utils import *


import functools



def start_main(func_name):
	print(f"函数 {func_name} 开始执行")
	to_page_main()

def start_task(func_name):
	print(f"函数 {func_name} 开始执行")
	to_page_task()

def end_fun(func_name):
	print(f"函数 {func_name} 执行结束")

def wrap_with_page_main(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		start_main(func.__name__)
		result = func(*args, **kwargs)
		end_fun(func.__name__)
		return result
	return wrapper

def wrap_with_page_task(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		start_task(func.__name__)
		result = func(*args, **kwargs)
		end_fun(func.__name__)
		return result
	return wrapper




@wrap_with_page_task
def 思绪漫步1():
	click_a(A_D,1)
	res = find_text_exist(meirilianxi,"练习","每日练习")
	if res:
		click_p(res)
	if find_text(meirilianxi_lingqu,"已","已领取"):
		logger.info("思绪漫步已领取")
		return -1
	to_page_main()

@wrap_with_page_task
def 思绪漫步2():
	click_a(A_D, 1)
	click_p(find_text_exist(meirilianxi_lingqu,"领取奖励","领取奖励"),wait=0.5) and click_get(0.5)
	click_back()
	# 闪亮之旅层

@wrap_with_page_main
def 元气使用():
	click_a(A_ICON)
	res = find_text(yuanqishiyong,"使用","元气使用")
	if res:
		click_p(res)
		yuanqizhi_be = find_text_out(yuanqishibie, "", "元气值")
		yuanqizhi =yuanqizhi_be[0].text.split("/")[0]
		print("元气值",yuanqizhi)
		if yuanqizhi == '0' or yuanqizhi == 'o' or yuanqizhi == 'O':
			logger.info("元气次数使用完")
		else:
			for _ in range(20):
				click_a(yuanqiduihuan)
				click_a(yuanqiduihuan)

		sleep(0.2)
		click_a(yuanqiduihuan)
		sleep(1)
		click_close()
		sleep(0.5)
		click_back()

@wrap_with_page_main
def 好友():
	if click_red(A_FRIEND):
		summer = find_text(MSG_SUMMER,"时尚顾问","时尚顾问")
		if summer:
			click_p(summer)
			click_p(find_text(MSG_SUMMER_LQ,"领取","领取返利"))and click_get() and click_back()
		if click_red(TXL):
			click_a(TXL_yijianzengsong) and click_a(TXL_LQtili) and click_a(TXL_YJLQ) and click_get() and click_close()
		if click_red(wannashequ):
			click_p(find_img(wannashequ_JB,"金币","金币——玩呐")) and click_get()
			if click_red(huati):
				for i in range(3):
					click_red(huati) and click_p(find_img(A_COLLECT_JB,"金币","金币——话题")) and click_back()
					if not find_red(huati):
						moveUp(1050,2400,1080,320,700)
				to_page_main()



		to_page_main()

@wrap_with_page_main
def 礼物():
	if find_img(A_GIFT, "gift", "礼物") and click_red(A_GIFT):
		sleep(0.5)
		click_a(GIFT_LEFT) and click_get(0.1) and click_p(find_text_exist(GIFT_CANLE,"取消","取消")) and sleep(0.5)
		click_a(GIFT_RIGHT) and click_get(0.1) and click_p(find_text_exist(GIFT_CANLE,"取消","取消")) and sleep(0.5)
		click_a(GIFT_LEFT) and click_get(0.1) and click_p(find_text_exist(GIFT_CANLE,"取消","取消")) and sleep(0.5)

		to_page_main()

@wrap_with_page_main
def 协会():
	if click_red(A_UNION):
		if click_red(lingganpengzhuang):
			for i in range(5):
				click_a(TJ_1_SY) and click_get()
			click_back()

		if click_red(yingyuan):
			for i in range(3):
				click_a(likeyingyuan) and click_get()
			click_back()


		to_page_main()

@wrap_with_page_main
def 福利():
	if click_red(A_BENEFITS):

		# 每日签到
		click_red(A_fuli_qiandao) and click_get()
		click_red(A_fuli_qiandaolibao)and click_get()

		# 每日体力
		if click_p(find_img(A_BENEFITS_TILI,"每日体力","每日体力")):
			click_a(A_TILI_1) and click_get()
			click_a(A_TILI_2) and click_get()

		# 每日分享
		for i in range(5):
			moveUp(1123,445,64,451,700)
			if click_p(find_img(A_BENEFITS_SHARE,"每日分享","每日分享")):
				if not Shared():
					break
				click_p(find_img(A_BENEFITS_SHARE_Goto,"前往分享","前往分享"),wait=1)
				click_p(find_text(A_paizhao,"拍照","拍照"),wait=1) and click_a(A_paizhao_qiezi,wait=1) and click_a(A_paizhao_SHare,wait=3)
				click_p(find_img(A_paizhao_SHare_QQShare,"QQ", "前往QQ分享"),wait=2) and click_p(find_text(A_paizhao_SHare_QQShare_close,"关闭","关闭QQ分享"),wait=2) and click_get(0.5)
				click_back()
				break

		to_page_main()

# 已被分享
def Shared():
		return find_img(A_Shared,"Shared","Shared")

@wrap_with_page_main
def 商业街():
	if click_red(A_SHOP):
		for i in range(5):
			click_red(A_SHOP_Gift) and click_get()
			if click_p(find_img(A_SHOP_Gift,"每日福利礼盒","每日福利礼盒")):
				click_p(find_text(A_buy,"购买","购买")) and click_get()
				if not find_red(A_SHOP_A):
					break
			moveUp(1072,2077,993,557)

		if click_red(A_SHOP_B):
			for i in range(5):
				click_red(A_SHOP_Gift) and click_get()
				if not find_red(A_SHOP_A):
					break
				moveUp(1072,2077,993,557)

		if click_red(A_SHOP_huiyr):
			click_red(A_SHOP_zx) and click_get()
			click_red(A_SHOP_zz) and click_get()
			click_red(A_SHOP_qd7) and click_get()

		for i in range(4):
			moveUp(1146,330,151,320,700)
			click_red(A_SHOP_SIDE)


		to_page_main()

@wrap_with_page_main
def 收集():
	if click_red(A_COLLECT):
		click_p(find_img(A_COLLECT_JB,"金币","金币——收集")) and click_get()
		to_page_main()

@wrap_with_page_main
def 盲盒():
	if click_red(A_BLINDBOX):
		click_red(BLINDBOX2) and click_red([]) and click_get()
		if find_red([]):
			click_red([])and click_get() and to_page_main()
		to_page_main()

@wrap_with_page_main
def 追光():
	if click_red(A_Other5):
		# if
		click_red(A_Other5_QD) and click_red(A_Other5_QD_JB) and click_get() and to_page_main()



		to_page_main()

@wrap_with_page_main
def mail():
	if is_in_page_main() and click_red(A_MAIL):

		to_page_main()

@wrap_with_page_main
def 日程():
	if click_red(A_SCHEDULE):
		click_p(find_text_exist(rich_yijianlq,"一键领取","一键领取"))
		sleep(1)

		for i in range(6):
			if click_red(rich_HUOYUEDU):
				click_get()
			else:
				break
			sleep(1)

		click_red(rich_ZHOUHUOYUE) and click_red(rich_ZHOUHUOYUE_A) and click_get()

		to_page_main()


# @wrap_with_page_main
# def 闪亮():
# 	to_page_main()
# 	click_p(find_img(A_LIGHT,"light","闪亮之旅"),wait=1)
#
# # def 心意之期():
#
@wrap_with_page_task
def 代言女王():
	if click_red(A_C):
		click_red(meirixuanchuan) and click_p(find_text(kashixuanchuan,"宣传","开始宣传")) and click_get()

		c = [SNE_1,WST_2,YNS_3,BBL_4]
		for f in c:
			click_a(f)
			if click_p(find_text(yijianshiqu, "拾取","一键拾取")):
				click_blank(0.3)
				click_blank(0.3)
				click_blank(0.3)
				click_blank(0.3)

			sleep(0.5)
			for i in range(5):
				if find_text_exist(meirixuanchuan, "每日宣传", "每日宣传"):
					break
				click_back()

		click_back()

#
@wrap_with_page_task
def 日常事件簿():
	click_a(A_E)
	click_JB(A_richangshijianbu_JB) and click_get()
	click_red(richangshijianbu_rect) and click_a(richangshijianbu_LQ) and click_get(0.3)

	for i in range(5):
		res1 = find_text_exist(richangshijianbu_range,"罕见","罕见")
		# res2 = find_text_exist(richangshijianbu_range,"难得","难得")
		# res3 = find_text_exist(richangshijianbu_range,"日常","日常")
		if res1:
			break
		elif (int(find_text_out(free_re_count,"免费","免费刷新次数")[0].text[-1]) >0
			or find_text_exist(free_re_count,"钻石","钻石") is False
			):
			click_p(find_text(richangshijianbu_re,"刷新","刷新"))
		sleep(0.5)

	for i in range(4):

		print("step0")
		if click_p(find_img(PQ_rect,"派遣","派遣"),wait=0.5):
			click_a(YJPQ,0.5)
			print("一键派遣")
			click_a(QRPQ)
			print("确认派遣")
		sleep(0.5)
	click_back()
#
#
# def 时尚对决():




# 好友()
# 礼物()
# 协会()
# 福利()
# 商业街()
# 收集()
# 盲盒()
# 追光()
# mail()
# 日程()