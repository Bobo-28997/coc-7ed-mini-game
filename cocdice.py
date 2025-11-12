import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import math
import time

# --- 战斗对抗模块的常量 ---
# (从 combat_resolver.py 移到这里)
LEVELS_NUM = {
    "Fumble": 0,  # 大失败
    "Fail": 1,  # 失败
    "Regular": 2,  # 普通成功
    "Hard": 3,  # 困难成功
    "Extreme": 4,  # 极难成功
    "Critical": 5  # 大成功
}

LEVELS_NAME = {
    0: "大失败 (Fumble)",
    1: "失败 (Fail)",
    2: "普通成功 (Regular)",
    3:"困难成功 (Hard)",
4: "极难成功 (Extreme)",
5: "大成功 (Critical)"
}

# ----------------------------------------------------------------------
# 模块 1: 通用骰子 (来自你的 DiceRollerApp)
# ----------------------------------------------------------------------
class DiceRollerTab:
    """
    这个类现在填充一个父 Frame (parent_tab)，
    而不是创建一个新的 root 窗口。
    """

    def __init__(self, parent_tab):
        # --- 1. 预设骰子按钮 ---
        preset_frame = tk.Frame(parent_tab, pady=10)
        preset_frame.pack(fill='x')

        preset_label = tk.Label(preset_frame, text="常用骰子 (COC Presets):")
        preset_label.pack(side=tk.LEFT, padx=5)

        presets = [(100, "d100"), (20, "d20"), (10, "d10"), (8, "d8"), (6, "d6"), (4, "d4"), (3, "d3")]

        for sides, text in presets:
            button = tk.Button(preset_frame, text=text, width=5,
                               command=lambda s=sides: self.roll_preset(s))
            button.pack(side=tk.LEFT, padx=3)

        # --- 2. 自定义骰子 ---
        custom_frame = tk.Frame(parent_tab, pady=5)
        custom_frame.pack(fill='x')

        custom_label = tk.Label(custom_frame, text="自定义 (Custom Roll) 1d")
        custom_label.pack(side=tk.LEFT, padx=5)

        self.custom_entry = tk.Entry(custom_frame, width=10)
        self.custom_entry.pack(side=tk.LEFT, padx=5)
        self.custom_entry.bind("<Return>", self.roll_custom_event)

        custom_button = tk.Button(custom_frame, text="掷骰 (Roll)",
                                  command=self.roll_custom)
        custom_button.pack(side=tk.LEFT, padx=5)

        # --- 3. 日志窗口 ---
        log_frame = tk.Frame(parent_tab, pady=5)
        log_frame.pack(fill='both', expand=True, padx=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, state='disabled', height=10, wrap=tk.WORD)
        self.log_text.pack(fill='both', expand=True)

        # 定义高亮标签的样式
        self.log_text.tag_config("crit_success", foreground="green", font=("TkDefaultFont", 9, "bold"))
        self.log_text.tag_config("crit_fumble", foreground="red", font=("TkDefaultFont", 9, "bold"))

        # --- 4. 清空按钮 ---
        clear_button = tk.Button(parent_tab, text="清空日志 (Clear Log)",
                                 command=self.clear_log)
        clear_button.pack(pady=5)

    def log_message(self, message):
        """向日志窗口添加一条消息，并自动滚动到底部。"""
        self.log_text.config(state='normal')  # 解锁

        timestamp = time.strftime("[%H:%M:%S] ")
        full_message = f"{timestamp}{message}\n"
        self.log_text.insert(tk.END, full_message)

        if "(1d100)" in message:  # 稍微修改了匹配逻辑
            start_index = self.log_text.index(f"{tk.END} - {len(full_message)}c")
            end_index = self.log_text.index(f"{tk.END} - 1c")

            if "大成功" in message:
                self.log_text.tag_add("crit_success", start_index, end_index)
            elif "大失败" in message:
                self.log_text.tag_add("crit_fumble", start_index, end_index)

        self.log_text.see(tk.END)  # 滚动到底部
        self.log_text.config(state='disabled')  # 重新锁定

    def roll_preset(self, sides):
        """处理预设按钮的掷骰。"""
        result = random.randint(1, sides)
        message = f"掷骰 (1d{sides}): {result}"

        if sides == 100:
            if result == 1:
                message += "  <-- 大成功! (Crit Success!)"
            elif result >= 96:
                message += "  <-- 大失败! (Crit Fumble!)"

        # 传递 (1d100) 标记用于高亮
        self.log_message(message if sides != 100 else f"掷骰 (1d100): {result}")

    def roll_custom(self):
        """处理自定义掷骰。"""
        sides_str = self.custom_entry.get()
        try:
            sides = int(sides_str)
            if sides <= 0:
                raise ValueError("面数必须大于0")

            result = random.randint(1, sides)
            log_msg = f"掷骰 (1d{sides}): {result}"

            # 如果自定义掷d100，也应用规则
            if sides == 100:
                if result == 1:
                    log_msg += "  <-- 大成功! (Crit Success!)"
                elif result >= 96:
                    log_msg += "  <-- 大失败! (Crit Fumble!)"
                self.log_message(f"掷骰 (1d100): {result}")
            else:
                self.log_message(log_msg)

        except ValueError:
            self.log_message(f"错误: '{sides_str}' 不是一个有效的骰子面数。")
        finally:
            self.custom_entry.delete(0, tk.END)

    def roll_custom_event(self, event):
        self.roll_custom()

    def clear_log(self):
        if messagebox.askyesno("确认", "你确定要清空所有掷骰日志吗？"):
            self.log_text.config(state='normal')
            self.log_text.delete('1.0', tk.END)
            self.log_text.config(state='disabled')


# ----------------------------------------------------------------------
# 模块 2: 战斗对抗 (来自 CombatResolverApp)
# ----------------------------------------------------------------------
class CombatResolverTab:
    """
    这个类现在填充一个父 Frame (parent_tab)，
    而不是创建一个新的 root 窗口。
    """

    def __init__(self, parent_tab):
        # --- 数据变量 ---
        self.atk_skill_var = tk.IntVar(value=50)
        self.def_brawl_var = tk.IntVar(value=50)
        self.def_dodge_var = tk.IntVar(value=30)
        self.atk_bonus_var = tk.BooleanVar(value=False)
        self.def_bonus_var = tk.BooleanVar(value=False)

        # 使用 parent_tab 作为所有控件的父级
        main_frame = ttk.Frame(parent_tab, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- 1. 输入区域 ---
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)

        # 攻击方
        ttk.Label(input_frame, text="攻击方技能:", font=("", 10, "bold")).grid(row=0, column=0, padx=5, sticky="w")
        atk_spin = ttk.Spinbox(input_frame, from_=0, to=100, textvariable=self.atk_skill_var, width=5)
        atk_spin.grid(row=0, column=1, padx=5, sticky="ew")
        atk_bonus_check = ttk.Checkbutton(input_frame, text="奖励骰", variable=self.atk_bonus_var)
        atk_bonus_check.grid(row=1, column=1, padx=5, sticky="w")

        ttk.Separator(input_frame, orient="vertical").grid(row=0, column=2, rowspan=3, sticky="ns", padx=15)

        # 防御方
        ttk.Label(input_frame, text="防御方 [格斗] 技能:", font=("", 10, "bold")).grid(row=0, column=2, padx=5,
                                                                                       sticky="w")
        def_brawl_spin = ttk.Spinbox(input_frame, from_=0, to=100, textvariable=self.def_brawl_var, width=5)
        def_brawl_spin.grid(row=0, column=3, padx=5, sticky="ew")
        ttk.Label(input_frame, text="防御方 [闪避] 技能:", font=("", 10, "bold")).grid(row=1, column=2, padx=5,
                                                                                       sticky="w")
        def_dodge_spin = ttk.Spinbox(input_frame, from_=0, to=100, textvariable=self.def_dodge_var, width=5)
        def_dodge_spin.grid(row=1, column=3, padx=5, sticky="ew")
        def_bonus_check = ttk.Checkbutton(input_frame, text="奖励骰", variable=self.def_bonus_var)
        def_bonus_check.grid(row=2, column=3, padx=5, sticky="w")

        # --- 2. 按钮区域 ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        style = ttk.Style()
        style.configure("FightBack.TButton", foreground="red", font=("", 10, "bold"))
        style.configure("Dodge.TButton", foreground="blue", font=("", 10, "bold"))

        fight_back_button = ttk.Button(button_frame,
                                       text="执行对抗 (防御方 [反击])",
                                       style="FightBack.TButton",
                                       command=lambda: self.resolve_combat("Fight Back"))
        fight_back_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        dodge_button = ttk.Button(button_frame,
                                  text="执行对抗 (防御方 [闪避])",
                                  style="Dodge.TButton",
                                  command=lambda: self.resolve_combat("Dodge"))
        dodge_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # --- 3. 结果显示区域 ---
        result_frame = ttk.LabelFrame(main_frame, text="检定结果报告", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.result_display = scrolledtext.ScrolledText(result_frame, height=15, width=70, wrap=tk.WORD,
                                                        state="disabled", font=("", 9))
        self.result_display.pack(fill=tk.BOTH, expand=True)

    # --- 战斗对抗模块的辅助函数 ---
    def roll_d100_with_bonus(self, has_bonus):
        """
        投掷d100，处理奖励骰逻辑（掷两个十位，取低）。
        返回 (最终骰值, "投掷过程描述字符串")
        """
        units_val = random.randint(0, 9)
        tens_val_1 = random.randint(0, 9)  # 0-9

        if not has_bonus:
            roll = tens_val_1 * 10 + units_val
            if roll == 0: roll = 100
            return roll, ""
        else:
            tens_val_2 = random.randint(0, 9)

            roll_1 = tens_val_1 * 10 + units_val
            if roll_1 == 0: roll_1 = 100

            roll_2 = tens_val_2 * 10 + units_val
            if roll_2 == 0: roll_2 = 100

            if roll_1 == 100 and roll_2 != 100:
                roll = roll_2
            elif roll_2 == 100 and roll_1 != 100:
                roll = roll_1
            elif roll_1 == 100 and roll_2 == 100:
                roll = 100
            else:
                roll = min(roll_1, roll_2)

            desc = f"(奖励骰: {roll_1} vs {roll_2}, 取 {roll})"
            return roll, desc

    def get_success_level(self, skill_value, roll):
        if roll == 1: return LEVELS_NUM["Critical"]
        if roll == 100: return LEVELS_NUM["Fumble"]
        if roll > skill_value:
            return LEVELS_NUM["Fumble"] if roll >= 96 else LEVELS_NUM["Fail"]
        if roll <= (skill_value // 5): return LEVELS_NUM["Extreme"]
        if roll <= (skill_value // 2): return LEVELS_NUM["Hard"]
        return LEVELS_NUM["Regular"]

    def resolve_combat(self, defender_choice):
        try:
            atk_skill = self.atk_skill_var.get()

            if defender_choice == "Fight Back":
                def_skill = self.def_brawl_var.get()
                rule_desc = "规则: 防御方 [反击] 必须获得 *高于* 攻击方的成功等级。"
                def_action_name = "反击 (格斗)"
            else:  # "Dodge"
                def_skill = self.def_dodge_var.get()
                rule_desc = "规则: 防御方 [闪避] 必须获得 *等于或高于* 攻击方的成功等级。"
                def_action_name = "闪避"

            atk_has_bonus = self.atk_bonus_var.get()
            def_has_bonus = self.def_bonus_var.get()

            atk_roll, atk_roll_desc = self.roll_d100_with_bonus(atk_has_bonus)
            def_roll, def_roll_desc = self.roll_d100_with_bonus(def_has_bonus)

            atk_level_num = self.get_success_level(atk_skill, atk_roll)
            def_level_num = self.get_success_level(def_skill, def_roll)

            atk_level_name = LEVELS_NAME[atk_level_num]
            def_level_name = LEVELS_NAME[def_level_num]

            final_result = ""
            if defender_choice == "Fight Back":
                if def_level_num > atk_level_num:
                    final_result = "--- 结果: 防御方 [反击] 成功！ ---"
                    if def_level_num >= LEVELS_NUM["Regular"]:
                        final_result += "\n(防御方对攻击方造成伤害)"
                else:
                    final_result = "--- 结果: 防御方 [反击] 失败，攻击方命中！ ---"
                    if atk_level_num >= LEVELS_NUM["Regular"]:
                        final_result += "\n(攻击方对防御方造成伤害)"
            else:  # "Dodge"
                if def_level_num >= atk_level_num:
                    final_result = "--- 结果: 防御方 [闪避] 成功！ ---"
                    final_result += "\n(双方均未造成伤害)"
                else:
                    final_result = "--- 结果: 防御方 [闪避] 失败，攻击方命中！ ---"
                    if atk_level_num >= LEVELS_NUM["Regular"]:
                        final_result += "\n(攻击方对防御方造成伤害)"

            report = (
                f"====== 对抗检定开始 ======\n\n"
                f"【攻击方】 (技能: {atk_skill})\n"
                f"  投掷: {atk_roll} {atk_roll_desc}\n"
                f"  成功等级: {atk_level_name}\n\n"
                f"【防御方】 (使用 {def_action_name}: {def_skill})\n"
                f"  投掷: {def_roll} {def_roll_desc}\n"
                f"  成功等级: {def_level_name}\n\n"
                f"【判定】\n"
                f"  {rule_desc}\n\n"
                f"{final_result}\n"
                f"===========================\n\n"
            )

            self._update_result_text(report)
            self.atk_bonus_var.set(False)
            self.def_bonus_var.set(False)

        except Exception as e:
            self._update_result_text(f"发生错误: {e}\n请确保所有技能值都是有效的数字。")

    def _update_result_text(self, content):
        self.result_display.config(state="normal")
        self.result_display.insert("1.0", content)
        self.result_display.config(state="disabled")


# ----------------------------------------------------------------------
# 主应用: COC 工具箱
# ----------------------------------------------------------------------
class CoCToolkit:
    """
    主应用，使用 ttk.Notebook 来组织两个模块。
    """

    def __init__(self, root):
        self.root = root
        self.root.title("COC 模块化工具箱 (CoC Toolkit)")
        self.root.geometry("620x500")  # 调整窗口大小以适应内容
        self.root.minsize(500, 400)

        # 创建 Notebook 控件
        self.notebook = ttk.Notebook(root)

        # 创建两个 Frame 作为选项卡
        self.tab1_dice = ttk.Frame(self.notebook)
        self.tab2_combat = ttk.Frame(self.notebook)

        # 将选项卡添加到 Notebook
        self.notebook.add(self.tab1_dice, text="通用骰子 (Dice Roller)")
        self.notebook.add(self.tab2_combat, text="战斗对抗 (Combat Resolver)")

        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        # --- 实例化两个应用，将它们填充到各自的选项卡 Frame 中 ---
        self.dice_roller_app = DiceRollerTab(self.tab1_dice)
        self.combat_resolver_app = CombatResolverTab(self.tab2_combat)


# --- 启动应用 ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CoCToolkit(root)
    root.mainloop()