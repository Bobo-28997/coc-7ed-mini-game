import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import random
import math

# --- 职业定义 (来自用户的脚本) ---
# 结构: "职业名称": {
# "skill_points_logic": 计算逻辑 (列表),
# "skills": [技能列表],
# "credit_rating": (最小值, 最大值)
# }
OCCUPATIONS = {
    "古文物学家/古董收藏家（教育）": {
        "skill_points_logic": [("EDU", 4)],
        "skills": ["估价", "艺术与手艺（任一）", "历史", "图书馆使用", "其他语言", "一种社交技能（魅惑、话术、恐吓或说服）",
                   "侦查", "自选一技能"],
        "credit_rating": (30, 70)
    },
    "艺术家（教育，意志，敏捷）": {
        "skill_points_logic": [("EDU", 2), [("POW", 2), ("DEX", 2)]],
        "skills": ["艺术与手艺（任一）", "历史或博物学", "一种社交技能（魅惑、话术、恐吓或说服）", "其他语言", "心理学",
                   "侦查", "自选二技能"],
        "credit_rating": (9, 50)
    },
    "运动员（教育，敏捷，力量）": {
        "skill_points_logic": [("EDU", 2), [("DEX", 2), ("STR", 2)]],
        "skills": ["攀爬", "跳跃", "格斗（斗殴）", "骑术", "一种社交技能（魅惑、话术、恐吓或说服）", "游泳", "投掷",
                   "自选一技能"],
        "credit_rating": (9, 70)
    },
    "作家（教育）": {
        "skill_points_logic": [("EDU", 4)],
        "skills": ["艺术（文学）", "历史", "图书馆使用", "博物学或神秘学", "其他语言", "母语", "心理学", "自选一技能"],
        "credit_rating": (9, 30)
    },
    "神职人员（教育）": {
        "skill_points_logic": [("EDU", 4)],
        "skills": ["会计学", "历史", "图书馆使用", "聆听", "其他语言", "一种社交技能（魅惑、话术、恐吓或说服）", "心理学",
                   "自选一技能"],
        "credit_rating": (9, 60)
    },
    "罪犯（教育，敏捷，力量）": {
        "skill_points_logic": [("EDU", 2), [("DEX", 2), ("STR", 2)]],
        "skills": ["一种社交技能（魅惑、话术、恐吓或说服）", "心理学", "侦查", "潜行",
                   "下列选四：估价、易容、格斗、射击、锁匠、机械维修、妙手"],
        "credit_rating": (5, 65)
    },
    "业余艺术爱好者（教育，外貌）": {
        "skill_points_logic": [("EDU", 2), ("APP", 2)],
        "skills": ["艺术与手艺（任一）", "射击", "其他语言", "骑术", "一种社交技能（魅惑、话术、恐吓或说服）", "自选三技能"],
        "credit_rating": (50, 99)
    },
    "医生（教育）": {
        "skill_points_logic": [("EDU", 4)],
        "skills": ["急救", "其他语言（拉丁文）", "医学", "心理学", "科学（生物学）", "科学（药学）",
                   "任两种有关学术或个人专业的技能"],
        "credit_rating": (30, 80)
    },
    "流浪者（教育，外貌，敏捷，力量四选三）": {
        "skill_points_logic": [("EDU", 2), [("APP", 2), ("DEX", 2), ("STR", 2)]],  # 规则是三选一，这里简化为取三者最高
        "skills": ["攀爬", "跳跃", "聆听", "领航", "一种社交技能（魅惑、话术、恐吓或说服）", "潜行", "自选二技能"],
        "credit_rating": (0, 5)
    },
    "工程师（教育）": {
        "skill_points_logic": [("EDU", 4)],
        "skills": ["艺术与手艺（设计图纸）", "电气维修", "图书馆使用", "机械维修", "操作重型机械", "科学（工程学）",
                   "科学（物理学）", "自选一技能"],
        "credit_rating": (30, 60)
    },
    "艺人/演艺人员（教育，外貌）": {
        "skill_points_logic": [("EDU", 2), ("APP", 2)],
        "skills": ["艺术与手艺（表演）", "乔装", "两种社交技能（魅惑、话术、恐吓或说服）", "聆听", "心理学", "自选二技能"],
        "credit_rating": (9, 70)
    },
    "农民（教育，敏捷，力量）": {
        "skill_points_logic": [("EDU", 2), [("DEX", 2), ("STR", 2)]],
        "skills": ["艺术与手艺（农事）", "汽车（或畜车）驾驶", "一种社交技能（魅惑、话术、恐吓或说服）", "机械维修", "博物学",
                   "操作重型机械", "追踪", "自选一技能"],
        "credit_rating": (9, 30)
    },
    "黑客（教育）": {  # 适用于现代背景
        "skill_points_logic": [("EDU", 4)],
        "skills": ["计算机使用", "电气维修", "电子学", "图书馆使用", "侦查", "一种社交技能（魅惑、话术、恐吓或说服）",
                   "自选二技能"],
        "credit_rating": (10, 70)
    },
    "记者（教育）": {
        "skill_points_logic": [("EDU", 4)],
        "skills": ["艺术与手艺（摄影）", "历史", "图书馆使用", "其他语言", "一种社交技能（魅惑、话术、恐吓或说服）", "心理学",
                   "自选二技能"],
        "credit_rating": (9, 30)
    },
    "律师（教育）": {
        "skill_points_logic": [("EDU", 4)],
        "skills": ["会计学", "法律", "图书馆使用", "二种社交技能（魅惑、话术、恐吓或说服）", "心理学", "自选二技能"],
        "credit_rating": (30, 80)
    },
    "图书馆管理员（教育）": {
        "skill_points_logic": [("EDU", 4)],
        "skills": ["会计学", "图书馆使用", "其他语言", "母语", "任意四个与个人特质和阅读专业有关的技能"],
        "credit_rating": (9, 35)
    },
    "军官（教育，敏捷，力量）": {
        "skill_points_logic": [("EDU", 2), [("DEX", 2), ("STR", 2)]],
        "skills": ["会计学", "射击", "领航", "二种社交技能（魅惑、话术、恐吓或说服）", "心理学", "生存", "自选一技能"],
        "credit_rating": (20, 70)
    },
    "传教士（教育）": {
        "skill_points_logic": [("EDU", 4)],
        "skills": ["艺术与手艺（任一）", "机械维修", "医学", "博物学", "一种社交技能（魅惑、话术、恐吓或说服）",
                   "自选二技能"],
        "credit_rating": (0, 30)
    },
    "音乐家（教育，敏捷，意志）": {
        "skill_points_logic": [("EDU", 2), [("DEX", 2), ("POW", 2)]],
        "skills": ["艺术与手艺（乐器）", "一种社交技能（魅惑、话术、恐吓或说服）", "聆听", "心理学", "自选四技能"],
        "credit_rating": (9, 30)
    },
    "人类学家（教育）": {  # 应该是“人类学家”或“超心理学家”？按原文翻译
        "skill_points_logic": [("EDU", 4)],
        "skills": ["人类学", "艺术与手艺（摄影）", "历史", "图书馆使用", "神秘学", "其他语言", "心理学", "自选一技能"],
        "credit_rating": (9, 30)
    },
    "飞行员（教育，敏捷）": {
        "skill_points_logic": [("EDU", 2), ("DEX", 2)],
        "skills": ["电气维修", "机械维修", "领航", "操作重型机械", "驾驶（飞行器）", "科学（天文学）", "自选二技能"],
        "credit_rating": (20, 70)
    },
    "警探【原作向】（教育，敏捷，力量）": {
        "skill_points_logic": [("EDU", 2), [("DEX", 2), ("STR", 2)]],
        "skills": ["艺术与手艺（表演）或乔装", "射击", "法律", "聆听", "一种社交技能（魅惑、话术、恐吓或说服）", "心理学",
                   "侦查", "自选一技能"],
        "credit_rating": (20, 50)
    },
    "警察（教育，敏捷，力量）": {
        "skill_points_logic": [("EDU", 2), [("DEX", 2), ("STR", 2)]],
        "skills": ["格斗（拳击）", "射击", "急救", "一种社交技能（魅惑、话术、恐吓或说服）", "法律", "心理学", "侦查",
                   "选一：汽车驾驶或骑术"],
        "credit_rating": (9, 30)
    },
    "私家侦探（教育，敏捷，力量）": {
        "skill_points_logic": [("EDU", 2), [("DEX", 2), ("STR", 2)]],
        "skills": ["艺术与手艺（摄影）", "乔装", "法律", "图书馆使用", "一种社交技能（魅惑、话术、恐吓或说服）", "心理学",
                   "侦查", "自选一技能（例如锁匠、射击）"],
        "credit_rating": (9, 30)
    },
    "教授（教育）": {
        "skill_points_logic": [("EDU", 4)],
        "skills": ["图书馆使用", "其他语言", "母语", "心理学", "自选四种与学术或个人专业有关的技能"],
        "credit_rating": (20, 70)
    },
    "士兵（教育，敏捷，力量）": {
        "skill_points_logic": [("EDU", 2), [("DEX", 2), ("STR", 2)]],
        "skills": ["攀爬或游泳", "闪避", "格斗", "射击", "潜行", "生存", "下列选二：急救、机械维修、其他语言"],
        "credit_rating": (9, 30)
    },
    "部落成员（教育，敏捷，力量）": {
        "skill_points_logic": [("EDU", 2), [("DEX", 2), ("STR", 2)]],
        "skills": ["攀爬", "格斗或投掷", "博物学", "聆听", "神秘学", "侦查", "游泳", "生存（任一）"],
        "credit_rating": (0, 15)
    },
    "狂热者（教育，外貌，意志）": {
        "skill_points_logic": [("EDU", 2), [("APP", 2), ("POW", 2)]],
        "skills": ["历史", "二种社交技能（魅惑、话术、恐吓或说服）", "心理学", "潜行", "自选三技能"],
        "credit_rating": (0, 30)
    },
}


# --- 所有来自用户脚本的辅助函数 ---

def roll_dice(num, sides):
    """掷 num 个 sides 面的骰子，返回总和。"""
    return sum(random.randint(1, sides) for _ in range(num))


def generate_base_characteristics():
    """生成 8 项基础属性。"""
    chars = {
        "STR": roll_dice(3, 6) * 5,
        "CON": roll_dice(3, 6) * 5,
        "POW": roll_dice(3, 6) * 5,
        "DEX": roll_dice(3, 6) * 5,
        "APP": roll_dice(3, 6) * 5,
        "SIZ": (roll_dice(2, 6) + 6) * 5,
        "INT": (roll_dice(2, 6) + 6) * 5,
        "EDU": (roll_dice(2, 6) + 6) * 5,
    }
    total_sum = sum(chars.values())
    chars["TotalSum"] = total_sum
    return chars


def calculate_derived_attributes(characteristics):
    """根据基础属性计算衍生属性 (HP, MP, Luck, SAN, MOV)。"""
    c = characteristics
    hp = (c["CON"] + c["SIZ"]) // 10
    mp = c["POW"] // 5
    san = c["POW"]
    luck = roll_dice(3, 6) * 5

    mov = 8
    if c["STR"] < c["SIZ"] and c["DEX"] < c["SIZ"]:
        mov = 7
    elif c["STR"] > c["SIZ"] and c["DEX"] > c["SIZ"]:
        mov = 9

    return {"HP": hp, "MP": mp, "Luck": luck, "SAN": san, "MOV": mov}


def calculate_combat_attributes(characteristics):
    """计算伤害加值 (DB) 和体格 (Build)。"""
    c = characteristics
    str_siz_total = c["STR"] + c["SIZ"]

    if str_siz_total <= 64:
        db, build = "-2", -2
    elif str_siz_total <= 84:
        db, build = "-1", -1
    elif str_siz_total <= 124:
        db, build = "0", 0
    elif str_siz_total <= 164:
        db, build = "+1d4", 1
    elif str_siz_total <= 204:
        db, build = "+1d6", 2
    elif str_siz_total <= 244:
        db, build = "+2d6", 3
    elif str_siz_total <= 284:
        db, build = "+3d6", 4
    else:
        db, build = f"+{math.floor(str_siz_total / 80) + 1}d6", math.floor(str_siz_total / 80)

    return {"DB": db, "Build": build}


def get_characteristic_description(attr, value):
    """根据属性值返回对应的中文描述。"""
    match attr:
        case "STR":
            if value <= 15: return ":(手无缚鸡之力。。。"
            if value <= 40: return "力量虚弱"
            if value <= 60: return "普通力量"
            if value <= 80: return "力量强大"
            return ":)力能扛鼎的人形起重机！"
        case "CON":
            if value <= 15: return ":(一点小伤病就卧床不起。。。"
            if value <= 40: return "健康堪忧"
            if value <= 60: return "普通体质"
            if value <= 80: return "体魄强健"
            return ":)钢铁般的体魄和免疫力！"
        case "SIZ":
            if value <= 15: return "孩童或侏儒"
            if value <= 45: return "瘦小或少年"
            if value <= 80: return "普通人类体型"
            return "高大威猛或重度肥胖"
        case "DEX":
            if value <= 15: return ":(极度缓慢笨拙。。。"
            if value <= 40: return "不太灵活"
            if value <= 60: return "正常敏捷"
            if value <= 80: return "身段轻盈"
            return ":)运动员或舞者般的灵巧！"  # > 80
        case "APP":
            if value <= 15: return ":(让人感到恐惧、厌恶和怜悯。。。"
            if value <= 40: return "逊色或丑陋"
            if value <= 60: return "普通的外貌"
            if value <= 80: return "引人回首"
            return ":)足以让所有人为你倾倒的魅力！"  # > 80
        case "INT":
            if value <= 15: return ":(数到10都得学很久。。。"
            if value <= 40: return "学得比较慢"
            if value <= 60: return "普通人水平"
            if value <= 80: return "思维很敏捷"
            return ":)福尔摩斯般的超凡之脑！"  # > 80
        case "POW":
            if value <= 15: return ":(崩溃边缘。。。"
            if value <= 40: return "信念薄弱"
            if value <= 60: return "意志力普通"
            if value <= 80: return "意志坚定"
            return ":)永不动摇的无畏灵魂！"  # > 80
        case "EDU":
            if value <= 15: return ":(新生儿或野人。。。"
            if value <= 49: return "文盲到初中肄业"
            if value <= 59: return "初中毕业或以上"
            if value <= 69: return "高中毕业或以上"
            if value <= 79: return "大学毕业或以上"
            if value <= 89: return "硕士毕业或以上"
            return ":)博士后或教授级别的教育！"  # >= 90
        case _:
            return ""


def generate_characteristic_summary(characteristics):
    """生成一句话的属性综述。"""
    attr_map = {
        "STR": "力量", "CON": "体质", "SIZ": "体型",
        "DEX": "敏捷", "APP": "外貌", "INT": "智力",
        "POW": "意志", "EDU": "教育"
    }

    summary_parts = []
    first = True
    for attr_key, attr_name in attr_map.items():
        description = get_characteristic_description(attr_key, characteristics[attr_key])
        if first:
            summary_parts.append(f"你的{attr_name}是{description}")
            first = False
        else:
            summary_parts.append(f"{attr_name}是{description}")

    return "；".join(summary_parts) + "。"


def get_luck_assessment(total_sum):
    """根据基础属性总和评估运气 (平均值 457.5)。"""
    if total_sum < 400:
        return "你的基础属性综合评分为： 天谴之人(平均值 457.5)"
    elif total_sum <= 439:
        return "你的基础属性综合评分为： 略逊常人(平均值 457.5)"
    elif total_sum <= 475:
        return "你的基础属性综合评分为： 不强不弱(平均值 457.5)"
    elif total_sum <= 510:
        return "你的基础属性综合评分为： 强于常人(平均值 457.5)"
    else:  # > 510
        return "你的基础属性综合评分为： 天命化身(平均值 457.5)"


def calculate_occupation_skill_points(c, logic):
    """根据新的 'OR' 逻辑计算职业技能点。"""
    points = 0
    for item in logic:
        if isinstance(item, tuple):
            attr, multiplier = item
            points += c[attr] * multiplier
        elif isinstance(item, list):
            max_or_points = 0
            for or_item in item:
                attr, multiplier = or_item
                if attr in c:
                    max_or_points = max(max_or_points, c[attr] * multiplier)
                else:
                    print(f"警告: 在 'OR' 逻辑中找不到属性 {attr}")
            points += max_or_points
    return points


# --- Tkinter GUI 应用 ---

class CharacterCreatorApp(tk.Tk):
    def __init__(self, occupations):
        super().__init__()
        self.title("COC 7版 - 调查员生成器 (GUI版)")
        self.geometry("650x700")

        self.occupations = occupations
        self.character = {}  # Store generated character data

        self.create_widgets()

    def create_widgets(self):
        # Set a slightly more modern theme
        style = ttk.Style(self)
        style.theme_use("clam")  # 'clam', 'alt', 'default', 'classic'

        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- 1. Generation Button ---
        gen_button = ttk.Button(main_frame, text="1. 生成/重置 调查员属性", command=self.generate_character)
        gen_button.pack(fill=tk.X, pady=5)

        # --- 2. Attributes Display ---
        attr_frame = ttk.LabelFrame(main_frame, text="属性 & 综述", padding="10")
        attr_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.attr_display = ScrolledText(attr_frame, height=18, width=70, wrap=tk.WORD, state="disabled")
        self.attr_display.pack(fill=tk.BOTH, expand=True)

        # --- 3. Occupation Selection ---
        occ_frame = ttk.LabelFrame(main_frame, text="职业选择 & 技能点", padding="10")
        occ_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        ttk.Label(occ_frame, text="2. 选择职业:").pack(side=tk.LEFT, padx=5)

        self.occupation_var = tk.StringVar()
        self.occupation_combo = ttk.Combobox(occ_frame,
                                             textvariable=self.occupation_var,
                                             values=list(self.occupations.keys()),
                                             state="disabled",  # Start disabled
                                             width=30)
        self.occupation_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Bind selection event
        self.occupation_combo.bind("<<ComboboxSelected>>", self.on_occupation_select)

        # --- 4. Occupation Details Display ---
        self.occ_display = ScrolledText(occ_frame, height=10, width=70, wrap=tk.WORD, state="disabled")
        self.occ_display.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    def _update_text_widget(self, widget, content):
        """Helper function to update a text widget."""
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", content)
        widget.config(state="disabled")

    def generate_character(self):
        """Generates all base stats and updates the GUI."""
        # 1. 基础属性
        self.character = generate_base_characteristics()

        # 2. 衍生属性
        derived = calculate_derived_attributes(self.character)
        self.character.update(derived)

        # 3. 战斗属性
        combat = calculate_combat_attributes(self.character)
        self.character.update(combat)

        # 4. 属性综述
        summary = {"CharacteristicSummary": generate_characteristic_summary(self.character)}
        self.character.update(summary)

        # 5. 运气评估
        luck_assessment = {"LuckAssessment": get_luck_assessment(self.character["TotalSum"])}
        self.character.update(luck_assessment)

        # 6. 个人兴趣点
        personal_points = self.character["INT"] * 2
        self.character["Personal Interest Points"] = personal_points

        # --- Format display text for attributes ---
        sheet = self.character
        display_text = "====== 调查员属性 ======\n\n"
        display_text += "--- 基础属性 ---\n"
        display_text += f" STR (力量): {sheet['STR']:<5} CON (体质): {sheet['CON']:<5} SIZ (体型): {sheet['SIZ']:<5}\n"
        display_text += f" DEX (敏捷): {sheet['DEX']:<5} APP (外貌): {sheet['APP']:<5} INT (智力): {sheet['INT']:<5}\n"
        display_text += f" POW (意志): {sheet['POW']:<5} EDU (教育): {sheet['EDU']:<5}\n"
        display_text += f" 基础总和: {sheet['TotalSum']} ({sheet['LuckAssessment']})\n\n"

        display_text += "--- 属性综述 ---\n"
        display_text += f"{sheet['CharacteristicSummary']}\n\n"

        display_text += "--- 衍生属性 ---\n"
        display_text += f" HP (耐久): {sheet['HP']:<4} MP (魔法): {sheet['MP']:<4}\n"
        display_text += f" SAN (理智): {sheet['SAN']:<4} Luck (幸运): {sheet['Luck']:<4}\n"
        display_text += f" MOV (移动力): {sheet['MOV']}\n\n"

        display_text += "--- 战斗属性 ---\n"
        display_text += f" 伤害加值 (DB): {sheet['DB']}\n"
        display_text += f" 体格 (Build): {sheet['Build']}\n\n"

        display_text += "--- 个人兴趣 ---\n"
        display_text += f" 个人兴趣点: {sheet['Personal Interest Points']} (智力 INT * 2)\n"

        # Update attribute display
        self._update_text_widget(self.attr_display, display_text)

        # Enable occupation dropdown
        self.occupation_combo.config(state="readonly")

        # Clear occupation selection and display
        self.occupation_var.set("")
        self._update_text_widget(self.occ_display, "请从上方下拉菜单中选择一个职业...")

    def on_occupation_select(self, event=None):
        """Called when a user selects an occupation from the combobox."""
        occ_name = self.occupation_var.get()
        if not occ_name or not self.character:
            return

        occ_details = self.occupations.get(occ_name)
        if not occ_details:
            self._update_text_widget(self.occ_display, f"错误: 找不到职业 '{occ_name}' 的详细信息。")
            return

        # 1. 计算职业技能点
        occupation_skill_points = calculate_occupation_skill_points(self.character, occ_details["skill_points_logic"])

        # 2. 获取信用评级范围 (不再随机生成)
        cr_min, cr_max = occ_details["credit_rating"]
        # credit_rating = random.randint(cr_min, cr_max) # <--- 已移除
        # if cr_min == 0 and cr_max == 0: # Handle special cases # <--- 已移除
        #     credit_rating = 0 # <--- 已移除

        # --- Format display text for occupation ---
        occ_text = f"--- 职业: {occ_name} ---\n\n"
        # 原来的行: occ_text += f"信用评级 (CR): {credit_rating}  (范围: {cr_min}-{cr_max})\n\n"
        occ_text += f"信用评级 (CR) 范围: {cr_min}-{cr_max} (在此范围内自选一个数目，从技能点中扣除)\n\n"  # <--- 修改后的行

        # Format the skill point logic for display
        logic_str_parts = []
        for item in occ_details['skill_points_logic']:
            if isinstance(item, tuple):
                logic_str_parts.append(f"{item[0]} * {item[1]}")
            elif isinstance(item, list):
                or_parts = [f"{or_item[0]} * {or_item[1]}" for or_item in item]
                logic_str_parts.append(f"max({', '.join(or_parts)})")
        logic_str = " + ".join(logic_str_parts)

        occ_text += f"职业技能点: {occupation_skill_points}\n"
        occ_text += f"  (计算方式: {logic_str})\n\n"

        occ_text += "--- 本职技能列表 ---\n"
        for i, skill in enumerate(occ_details["skills"]):
            occ_text += f" {i + 1}. {skill}\n"

        # Update occupation display
        self._update_text_widget(self.occ_display, occ_text)


if __name__ == "__main__":
    app = CharacterCreatorApp(OCCUPATIONS)
    app.mainloop()