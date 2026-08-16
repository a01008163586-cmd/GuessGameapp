from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window
import random

DATA_STORE = {
    "فواكه وخضروات": [
        {"name": "بطيخ", "tags": ["أخضر", "كبير", "بذر", "حلو", "صيفي", "دائري"]},
        {"name": "موز", "tags": ["أصفر", "صغير", "طويل", "حلو", "بدون بذر"]},
        {"name": "تفاح", "tags": ["أحمر", "أخضر", "صغير", "بذر", "حلو", "دائري"]},
        {"name": "ليمون", "tags": ["أصفر", "أخضر", "صغير", "حامض", "بذر"]},
        {"name": "جزر", "tags": ["برتقالي", "صغير", "طويل", "خضار", "مقرمش"]},
        {"name": "عنب", "tags": ["صغير", "حلو", "دائري", "أخضر", "أحمر", "بذر"]}
    ],
    "حيوانات وطيور": [
        {"name": "أسد", "tags": ["مفترس", "كبير", "ثدييات", "أصفر", "صوت قوي"]},
        {"name": "صقر", "tags": ["يطير", "مفترس", "ريش", "حجم متوسط", "سريع"]},
        {"name": "بطريق", "tags": ["طائر", "لا يطير", "سباح", "أسود وأبيض", "يعيش في الثلج"]},
        {"name": "فيل", "tags": ["ضخم", "رمادي", "خرطوم", "ثدييات", "أذنان كبيرتان"]},
        {"name": "حمامة", "tags": ["يطير", "طائر", "صغير", "أبيض", "أليف"]}
    ],
    "جماد وأدوات": [
        {"name": "هاتف", "tags": ["إلكتروني", "صغير", "شاشة", "اتصال", "مربع"]},
        {"name": "سيارة", "tags": ["وسيلة نقل", "عجلات", "محرّك", "كبير", "حديد"]},
        {"name": "ثلاجة", "tags": ["كبير", "إلكتروني", "تبريد", "حديد", "منزلي"]}
    ]
}

QUESTION_TAG_MAP = {
    "هل هو كبير الحجم؟": "كبير",
    "هل لونه أخضر؟": "أخضر",
    "هل لونه أصفر؟": "أصفر",
    "هل يطير؟": "يطير",
    "هل هو مفترس؟": "مفترس",
    "هل يحتوي على بذر؟": "بذر",
    "هل هو حلو المذاق؟": "حلو",
    "هل هو إلكتروني؟": "إلكتروني",
    "هل يعتبر ضخم؟": "ضخم",
    "هل هو طائر؟": "طائر",
    "هل هو أليف؟": "أليف"
}

class MainGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10
        self.score = 0
        self.level = 1
        self.setup_new_round()
        self.build_ui()

    def setup_new_round(self):
        self.category = random.choice(list(DATA_STORE.keys()))
        self.target_item = random.choice(DATA_STORE[self.category])
        self.attempts = max(4, 8 - (self.level // 2))

    def build_ui(self):
        self.clear_widgets()
        stats_box = BoxLayout(size_hint_y=0.1)
        self.score_label = Label(text=f"⭐ النقاط: {self.score}", font_size='16sp', bold=True)
        self.level_label = Label(text=f"🏆 المستوى: {self.level}", font_size='16sp', bold=True)
        self.attempts_label = Label(text=f"⏳ المحاولات: {self.attempts}", font_size='16sp', bold=True)
        stats_box.add_widget(self.score_label)
        stats_box.add_widget(self.level_label)
        stats_box.add_widget(self.attempts_label)
        self.add_widget(stats_box)

        self.cat_label = Label(
            text=f"القسم المطلوب: [color=00ffff]{self.category}[/color]",
            markup=True, font_size='20sp', size_hint_y=0.08
        )
        self.add_widget(self.cat_label)

        self.scroll = ScrollView(size_hint_y=0.42)
        self.log_label = Label(
            text="[color=888888]اختر سؤالاً لتحليل خصائص الكلمة السرية...[/color]\n",
            markup=True, font_size='15sp', size_hint_y=None, halign='center'
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        self.scroll.add_widget(self.log_label)
        self.add_widget(self.scroll)

        q_grid = GridLayout(cols=2, spacing=5, size_hint_y=0.28)
        for q_text in QUESTION_TAG_MAP.keys():
            btn = Button(text=q_text, font_size='12sp', background_color=(0.2, 0.5, 0.8, 1))
            btn.bind(on_press=lambda b, q=q_text: self.analyze_question(q, b))
            q_grid.add_widget(btn)
        self.add_widget(q_grid)

        guess_box = BoxLayout(size_hint_y=0.12, spacing=5)
        self.input_guess = TextInput(
            hint_text="اكتب تخمينك هنا...",
            multiline=False, font_size='16sp', halign='center'
        )
        submit_btn = Button(
            text="تأكيد التخمين", size_hint_x=0.35,
            background_color=(0.1, 0.8, 0.3, 1), bold=True
        )
        submit_btn.bind(on_press=self.verify_user_guess)
        
        guess_box.add_widget(self.input_guess)
        guess_box.add_widget(submit_btn)
        self.add_widget(guess_box)

    def analyze_question(self, question_text, btn_obj):
        if self.attempts <= 0:
            return
        tag = QUESTION_TAG_MAP.get(question_text)
        is_match = tag in self.target_item["tags"]
        self.attempts -= 1
        btn_obj.disabled = True
        result_text = "نعم! ✅" if is_match else "لا! ❌"
        color = "00ff00" if is_match else "ff3333"
        self.log_label.text += f"\n• {question_text} -> [{color}]{result_text}[/{color}]"
        self.attempts_label.text = f"⏳ المحاولات: {self.attempts}"
        if self.attempts == 0:
            self.show_popup("انتهاء المحاولات!", f"للأسف انتهت المحاولات!\nالكلمة كانت: {self.target_item['name']}", False)

    def verify_user_guess(self, instance):
        user_input = self.input_guess.text.strip()
        if not user_input:
            return
        if user_input == self.target_item["name"]:
            earned_points = self.attempts * 10 + 50
            self.score += earned_points
            self.level += 1
            self.show_popup("إجابة صحيحة! 🎉", f"ممتاز! التخمين صحيح.\nحصلت على {earned_points} نقطة!", True)
        else:
            self.show_popup("تخمين خاطئ! ❌", f"الإجابة ليست '{user_input}'.\nالكلمة الصحيحة هي: {self.target_item['name']}", False)

    def show_popup(self, title, message, is_win):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message, font_size='16sp', halign='center'))
        btn_text = "المستوى التالي ➔" if is_win else "محاولة جديدة 🔄"
        next_btn = Button(text=btn_text, size_hint_y=0.3, background_color=(0.2, 0.6, 1, 1))
        content.add_widget(next_btn)
        popup = Popup(title=title, content=content, size_hint=(0.85, 0.4), auto_dismiss=False)
        next_btn.bind(on_press=lambda x: self.restart_game(popup))
        popup.open()

    def restart_game(self, popup):
        popup.dismiss()
        self.setup_new_round()
        self.build_ui()

class SmartGuessGameApp(App):
    def build(self):
        Window.softinput_mode = 'below_target'
        return MainGame()

if __name__ == '__main__':
    SmartGuessGameApp().run()
