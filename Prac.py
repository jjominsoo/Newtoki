import matplotlib.pyplot as plt
import pyautogui
import threading


# 그래프 표시 함수
def show_plot():
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]

    plt.plot(x, y)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Sample Plot')
    plt.subplots_adjust(right=10)

    plt.show()


# 입력 받고 확인하는 함수
def input_confirmation():
    # 그래프가 보이는 곳에서 멀리 떨어진 위치에 GUI 생성
    # pyautogui.alert(text='Enter a number:', title='Input', button='OK')
    pyautogui.moveTo(800, 400)

    # 값을 입력 받음
    value = pyautogui.prompt(text='Enter a number:', title='Input', default='')

    if value is not None:  # 취소 버튼이 아닌 경우
        plt.close()


# 그래프 표시
show_plot_thread = threading.Thread(target=show_plot)
show_plot_thread.start()

# 입력 받고 확인
input_confirmation_thread = threading.Thread(target=input_confirmation)
input_confirmation_thread.start()

# 두 쓰레드가 모두 종료될 때까지 대기
show_plot_thread.join()
input_confirmation_thread.join()

print("Plot closed.")
