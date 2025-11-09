import logging
from time import time, sleep

from ascript.android.node import Selector

from .utils import *


def enter_game():
    logging.info("开始启动游戏")
    action.Key.home()
    sleep(0.2)
    res = Selector().text("以闪亮之名").find()
    if res is None:
        action.Key.back()
        sleep(0.1)
        Selector().text("以闪亮之名").find()

    if res is None:
        action.Key.home()
        sleep(0.2)
        moveUP_desktop(600, 2086, 610, 400, 700)
        sleep(0.2)
        res_a = Selector(1).path(
            "/FrameLayout/LinearLayout/FrameLayout/FrameLayout/FrameLayout/RelativeLayout/RelativeLayout/FrameLayout/View/COUITouchSearchView").click().find()
        res = Selector().desc("以闪亮之名").find()
        res is not None and res.click()
    # print(res)
    res.click()
    sleep(2)

def wait_for_enter_game(timeout=30):
    logger.info("等待进入游戏主界面...")
    start_time = time()
    while time() - start_time < timeout:
        if is_in_page_main:
            logger.info("成功进入主界面")
            return True
        sleep(1)
    err(code=4, text="进入主界面超时")
    return False


def start_game():
    if find_back():
        to_page_main()
    # 处理误触退出弹窗
    click_quit_cancel_btn()
    if not cancel_pop():
        # return True
    # 点击开始按钮并等待加载
        start_time = time()
        while time() - start_time < 30:
            click_pop_an()
            start_pos = find_text(A_Click_Start, "点击开始", "点击开始")
            load_pos = find_text(A_Load, "加载", "加载",max_retries=2)

            if not load_pos and start_pos:
                logger.info("点击开始按钮")
                click_p(start_pos)
                sleep(2)
                return True
            sleep(1)
        err(1,"等待超时")
        return False

def cancel_pop():
    for i in range(7):
        res = is_in_page_main(1)
        x = find_pop()
        if x:
            click_pop()
        elif res:
            print("开始任务")
            return True
        else:
            return 0
        sleep(0.7)