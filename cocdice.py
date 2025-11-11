import tkinter as tk
from tkinter import scrolledtext, messagebox
import random
import time


class DiceRollerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("COC 通用骰子工具 (General Dice Roller)")
        self.root.geometry("450x400")  # 设置窗口初始大小
        self.root.minsize(300, 300)  # 设置窗口最小尺寸

        # --- 1. 预设骰子按钮 ---
        preset_frame = tk.Frame(root, pady=10)
        preset_frame.pack(fill='x')

        preset_label = tk.Label(preset_frame, text="常用骰子 (COC Presets):")
        preset_label.pack(side=tk.LEFT, padx=5)

        # 预设按钮列表 (骰子面数, 按钮文本)
        # d100, d20, d10, d8, d6, d4, d3
        presets = [(100, "d100"), (20, "d20"), (10, "d10"), (8, "d8"), (6, "d6"), (4, "d4"), (3, "d3")]

        for sides, text in presets:
            # 使用 lambda 来传递参数
            button = tk.Button(preset_frame, text=text, width=5,
                               command=lambda s=sides: self.roll_preset(s))
            button.pack(side=tk.LEFT, padx=3)

        # --- 2. 自定义骰子 ---
        custom_frame = tk.Frame(root, pady=5)
        custom_frame.pack(fill='x')

        custom_label = tk.Label(custom_frame, text="自定义 (Custom Roll) 1d")
        custom_label.pack(side=tk.LEFT, padx=5)

        self.custom_entry = tk.Entry(custom_frame, width=10)
        self.custom_entry.pack(side=tk.LEFT, padx=5)
        # 绑定回车键
        self.custom_entry.bind("<Return>", self.roll_custom_event)

        custom_button = tk.Button(custom_frame, text="掷骰 (Roll)",
                                  command=self.roll_custom)
        custom_button.pack(side=tk.LEFT, padx=5)

        # --- 3. 日志窗口 ---
        log_frame = tk.Frame(root, pady=5)
        # expand=True, fill='both' 让日志窗口随窗口缩放
        log_frame.pack(fill='both', expand=True, padx=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, state='disabled', height=10, wrap=tk.WORD)
        self.log_text.pack(fill='both', expand=True)

        # --- 4. 清空按钮 ---
        clear_button = tk.Button(root, text="清空日志 (Clear Log)",
                                 command=self.clear_log)
        clear_button.pack(pady=5)

    def log_message(self, message):
        """向日志窗口添加一条消息，并自动滚动到底部。"""
        self.log_text.config(state='normal')  # 解锁

        # 添加时间戳
        timestamp = time.strftime("[%H:%M:%S] ")
        full_message = f"{timestamp}{message}\n"

        self.log_text.insert(tk.END, full_message)

        # --- d100 特殊高亮 ---
        if "(d100)" in message:
            # 查找刚刚插入的文本的起始位置
            start_index = self.log_text.index(f"{tk.END} - {len(full_message)}c")
            end_index = self.log_text.index(f"{tk.END} - 1c")  # 结束位置（-1c表示不包括换行符）

            if "大成功" in message:
                self.log_text.tag_add("crit_success", start_index, end_index)
            elif "大失败" in message:
                self.log_text.tag_add("crit_fumble", start_index, end_index)

        self.log_text.see(tk.END)  # 滚动到底部
        self.log_text.config(state='disabled')  # 重新锁定

        # 定义高亮标签的样式
        self.log_text.tag_config("crit_success", foreground="green", font=("TkDefaultFont", 9, "bold"))
        self.log_text.tag_config("crit_fumble", foreground="red", font=("TkDefaultFont", 9, "bold"))

    def roll_preset(self, sides):
        """处理预设按钮的掷骰。"""
        result = random.randint(1, sides)
        message = f"掷骰 (1d{sides}): {result}"

        # COC d100 检定规则
        if sides == 100:
            if result == 1:
                message += "  <-- 大成功! (Crit Success!)"
            elif result >= 96:
                message += "  <-- 大失败! (Crit Fumble!)"

        self.log_message(message)

    def roll_custom(self):
        """处理自定义掷骰。"""
        sides_str = self.custom_entry.get()
        try:
            sides = int(sides_str)
            if sides <= 0:
                raise ValueError("面数必须大于0")

            # 复用预设掷骰逻辑 (但d100的特殊提示不一定适用)
            result = random.randint(1, sides)
            self.log_message(f"掷骰 (1d{sides}): {result}")

        except ValueError:
            # 如果输入不是有效数字
            self.log_message(f"错误: '{sides_str}' 不是一个有效的骰子面数。")
        finally:
            # 清空输入框
            self.custom_entry.delete(0, tk.END)

    def roll_custom_event(self, event):
        """处理自定义输入框的回车事件。"""
        self.roll_custom()

    def clear_log(self):
        """清空日志窗口。"""
        # 弹窗确认
        if messagebox.askyesno("确认", "你确定要清空所有掷骰日志吗？"):
            self.log_text.config(state='normal')
            self.log_text.delete('1.0', tk.END)
            self.log_text.config(state='disabled')


# --- 启动应用 ---
if __name__ == "__main__":
    root = tk.Tk()
    app = DiceRollerApp(root)
    root.mainloop()