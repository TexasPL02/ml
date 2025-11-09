# __init__.py 为初始化加载文件
import sys



print("Hello AS!")

from .res.ui.test import *


from .res.ui.start import *
from .res.ui.task import *




task_start = [
	enter_game,
	wait_for_enter_game,
	start_game,
	cancel_pop,
]

task_test =[
	日常事件簿,
	代言女王,
	思绪漫步1,

	元气使用,
好友,
礼物,
协会,
福利,

收集,
盲盒,
追光,

mail,

	思绪漫步2,
	日程,
	商业街,
]
flag = 1

'''
思绪漫步1,2
元气使用,0
好友,1
礼物,3
协会,1
福利,1


收集,1
盲盒,1
追光,1


mail,3
代言女王,2
日常事件簿,2

思绪漫步2,2
日程,1
商业街,1


'''



# flag = 0

if flag:

	for task in task_start:
		task()

	for task in task_test:
		res = task()
		if res == -1:         # 如果返回 -1，立即退出循环
			logger.info(f"任务 {task.__name__} 返回 -1，停止后续任务")
			end("思绪漫步已领取，\n其他任务可能已完成")
			break

# 日常事件簿()
# click_red([50,50,1100,2500])
# to_page_main()
# for i in range(20):
# 	click_red(A_FRIEND)
# 	sleep(0.5)
# 	click_back()
# 	sleep(0.5)
# 	print(i,is_in_page_main())
# click_red()
# print(find_text_exist(GIFT_LEFT,"点击开启","点击开启（左）"))
end()

