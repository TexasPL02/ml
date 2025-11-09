

from .utils import *

from .task import *
# from .utils import *
from .start import  *
def test_text():
	a = [0,329,206,530]
	a1 = [24,155,726,529]
	b = "福利"
	c = "测试——文本"
	b2 = "反向测试"
	c2 = "反向测试——文本"
	p = find_text(a,b,b)
	p2 = find_text(a,b2,b2)
	# p = find_element("color",BACK_CLOSE,BACK_CLOSE_Color,"返回")
	print("测试结果：",p)
	print("________")
	print("反向测试结果：",p2)
	# print(p[0])
	# print(len(p))
	# print(p[0].center_x)

	# t = find_back()
	# print(t)

def test_image():
	a = [20,97,1256,1461]
	b = "red"
	c = "测试——图片"
	b2 = "red"
	c2 = "反向测试——图片"
	p = find_img(a,b,c)
	p2 = find_img(a,b2,c2)
	print("测试结果：",p)
	print("________")
	print("反向测试结果：",p2)

def test_color():
	a = BACK_CLOSE
	b = BACK_CLOSE_Color
	c = "测试——图色"
	b2 = RED_Color
	c2 = "反向测试——图色"
	p = find_color(a,b,c)
	p2 = find_color(a,b2,c2)
	print("测试结果：",p)
	print("________")
	print("反向测试结果：",p2)


# test_text()
# test_image()
# test_color()



# print(back)
# print(red)
# click(back)
# click(red(center_x),red.y)

# if find_quit_cancel_btn():
# 	click_quit_cancel_btn()
# click_get()

# click_pop_an()
# print(isMain())

# print("测试结果（是否为0）：",click_back_main())
# scr_area()


# find_text([180, 2029, 689, 2189],"新","检查新字")
# res = find_text_out([180, 2029, 689, 2189],"新","检查新字")
# print(res[0].text)
# for i in enumerate("蜡笔小新"):
# 	print(i)

# def a():

# for i in range(10):
# 	res = find_pop()
# 	print(res)

# 元气使用()
# cancel_pop()
# for o in range(0,200):
# 	print(is_in_page_task())

# 思绪漫步2()
# click_get()
# 协会()
# 日程()

# 日常事件簿()