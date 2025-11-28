#!/usr/bin/env python3
"""
Medication Health Reminder - Main Application
A beautiful, modern GUI to track medications and refill alerts.
Supports English and Chinese languages.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

import customtkinter as ctk
from datetime import datetime
import tkinter.messagebox as messagebox

# Import backend modules
import database
from database import init_db, save_data, get_next_id

# Helper to get current data store (always fresh reference)
def get_data_store():
    return database.DATA_STORE

# Set appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Custom Colors - Themes
DARK_THEME = {
    "bg_dark": "#0f0f1a",
    "bg_card": "#1a1a2e",
    "bg_input": "#252540",
    "accent": "#0f3460",
    "primary": "#e94560",
    "primary_hover": "#d13a54",
    "success": "#10b981",
    "success_hover": "#059669",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "text": "#f1f5f9",
    "text_secondary": "#94a3b8",
    "border": "#334155",
}
LIGHT_THEME = {
    "bg_dark": "#eef1f6",
    "bg_card": "#ffffff",
    "bg_input": "#dfe5f1",
    "accent": "#c5d1e7",
    "primary": "#e94560",
    "primary_hover": "#d13a54",
    "success": "#14833d",
    "success_hover": "#0f6e33",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "text": "#0f172a",
    "text_secondary": "#334155",
    "border": "#c1cad9",
}

COLORS = dict(DARK_THEME)


class FontManager:
    """Central font registry to scale text without resizing widgets"""
    def __init__(self):
        self.scale = 1.0
        self.fonts = {}
    
    def _key(self, size, weight):
        return f"{size}:{weight}"
    
    def get(self, size, weight="normal"):
        key = self._key(size, weight)
        if key not in self.fonts:
            self.fonts[key] = {
                "base": size,
                "weight": weight,
                "font": ctk.CTkFont(size=int(round(size * self.scale)), weight=weight),
            }
        return self.fonts[key]["font"]
    
    def set_scale(self, scale):
        self.scale = scale
        for info in self.fonts.values():
            new_size = max(8, int(round(info["base"] * self.scale)))
            info["font"].configure(size=new_size, weight=info["weight"])


FONT_MANAGER = FontManager()


def font(size, weight="normal"):
    return FONT_MANAGER.get(size, weight)


def scale(value):
    """Scale numeric sizes (heights/padding) with current font scale"""
    return max(1, int(round(value * FONT_MANAGER.scale)))

# ============================================
# LANGUAGE TRANSLATIONS
# ============================================
TRANSLATIONS = {
    "en": {
        # App
        "app_title": "Medication Health Reminder",
        "version": "v1.0.0",
        
        # Login
        "welcome_back": "Welcome Back!",
        "sign_in_subtitle": "Sign in to your account",
        "username": "Username",
        "password": "Password",
        "enter_username": "Enter your username",
        "enter_password": "Enter your password",
        "sign_in": "Sign In",
        "new_here": "New here?",
        "create_account_btn": "Create an Account",
        
        # Register
        "create_account": "Create Account",
        "join_subtitle": "Join us and start tracking your medications",
        "choose_username": "Choose a unique username",
        "password_hint": "At least 3 characters",
        "confirm_password": "Confirm Password",
        "reenter_password": "Re-enter your password",
        "already_have_account": "Already have an account?",
        "sign_in_instead": "Sign In",
        
        # Dashboard
        "welcome_user": "Welcome",
        "my_medications": "📋  My Medications",
        "add_medication": "➕  Add Medication",
        "history": "📜  History",
        "sign_out": "🚪  Sign Out",
        
        # Medications
        "my_medications_title": "My Medications",
        "refresh": "🔄  Refresh",
        "no_medications": "No medications yet",
        "click_add": "Click 'Add Medication' to get started",
        "in_stock": "in stock",
        "per_day": "per day",
        "days_left": "days left",
        "low_stock": "⚠️ Low Stock",
        "in_stock_status": "✓ In Stock",
        "todays_progress": "Today's Progress",
        "done_today": "✅ Done for today!",
        "taken_today": "taken today",
        "more_to_go": "more to go",
        "completed_today": "✓ Completed Today",
        "take_dose": "💊 Take Dose",
        "delete": "Delete",
        "delete_confirm": "Delete this medication?",
        "delete_success": "Medication deleted.",
        
        # Add Medication
        "add_new_medication": "Add New Medication",
        "add_subtitle": "Enter the details of your medication below",
        "medication_name": "Medication Name",
        "medication_placeholder": "e.g., Lisinopril, Metformin, Aspirin",
        "total_pills": "Total Pills in Stock",
        "pills_placeholder": "e.g., 30",
        "pills_per_day": "Pills Per Day",
        "per_day_placeholder": "e.g., 2",
        "smart_alerts": "💡 Smart Alerts",
        "smart_alerts_desc": "The app will automatically calculate how many days of medication you\nhave left and alert you when stock is running low (less than 3 days).",
        "add_medication_btn": "Add Medication",
        
        # History
        "medication_history": "Medication History",
        "export_pdf": "📄  Export PDF",
        "no_history": "No history yet",
        "take_some_meds": "Take some medication to see your history here",
        
        # Dialogs
        "ok": "OK",
        "input_required": "Input Required",
        "enter_username_msg": "Please enter your username.",
        "enter_password_msg": "Please enter your password.",
        "login_failed": "Login Failed",
        "invalid_credentials": "Invalid username or password.\nPlease check your credentials.",
        "invalid_username": "Invalid Username",
        "username_min": "Username must be at least 3 characters.",
        "weak_password": "Weak Password",
        "password_min": "Password must be at least 3 characters.",
        "password_mismatch": "Password Mismatch",
        "passwords_not_match": "Passwords do not match.\nPlease try again.",
        "username_taken": "Username Taken",
        "username_exists": "is already registered.\nPlease choose another.",
        "account_created": "Account Created!",
        "welcome_new_user": "Your account has been created successfully.",
        "missing_info": "Missing Info",
        "enter_med_name": "Please enter the medication name.",
        "enter_total_pills": "Please enter the total pills in stock.",
        "enter_pills_per_day": "Please enter the pills per day.",
        "invalid_input": "Invalid Input",
        "positive_numbers": "Stock and daily dose must be positive whole numbers.",
        "success": "Success",
        "med_added": "has been added to your medications.",
        "dose_recorded": "Dose Recorded",
        "took_dose": "Took 1 dose of",
        "remaining": "Remaining:",
        "pills": "pills",
        "error": "Error",
        "record_failed": "Could not record medication intake.",
        "export_complete": "Export Complete",
        "pdf_saved": "PDF Report saved to:",
        "export_failed": "Export Failed",
        "export_error": "Could not generate PDF.\nMake sure you have medication history first.",
        
        # Language
        "language": "🌐 Language",
        "light_mode": "☀ Light",
        "dark_mode": "🌙 Dark",
    },
    "zh": {
        # App
        "app_title": "药物健康提醒",
        "version": "v1.0.0",
        
        # Login
        "welcome_back": "欢迎回来！",
        "sign_in_subtitle": "登录您的账户",
        "username": "用户名",
        "password": "密码",
        "enter_username": "请输入用户名",
        "enter_password": "请输入密码",
        "sign_in": "登录",
        "new_here": "新用户？",
        "create_account_btn": "创建账户",
        
        # Register
        "create_account": "创建账户",
        "join_subtitle": "加入我们，开始管理您的药物",
        "choose_username": "选择一个用户名",
        "password_hint": "至少3个字符",
        "confirm_password": "确认密码",
        "reenter_password": "再次输入密码",
        "already_have_account": "已有账户？",
        "sign_in_instead": "登录",
        
        # Dashboard
        "welcome_user": "欢迎",
        "my_medications": "📋  我的药物",
        "add_medication": "➕  添加药物",
        "history": "📜  历史记录",
        "sign_out": "🚪  退出登录",
        
        # Medications
        "my_medications_title": "我的药物",
        "refresh": "🔄  刷新",
        "no_medications": "暂无药物",
        "click_add": "点击「添加药物」开始",
        "in_stock": "库存",
        "per_day": "每天",
        "days_left": "天剩余",
        "low_stock": "⚠️ 库存不足",
        "in_stock_status": "✓ 库存充足",
        "todays_progress": "今日进度",
        "done_today": "✅ 今日已完成！",
        "taken_today": "今日已服用",
        "more_to_go": "还需服用",
        "completed_today": "✓ 今日已完成",
        "take_dose": "💊 服用",
        "delete": "删除",
        "delete_confirm": "确定删除该药物？",
        "delete_success": "药物已删除。",
        
        # Add Medication
        "add_new_medication": "添加新药物",
        "add_subtitle": "请输入药物详细信息",
        "medication_name": "药物名称",
        "medication_placeholder": "例如：降压药、二甲双胍、阿司匹林",
        "total_pills": "库存数量",
        "pills_placeholder": "例如：30",
        "pills_per_day": "每日用量",
        "per_day_placeholder": "例如：2",
        "smart_alerts": "💡 智能提醒",
        "smart_alerts_desc": "应用会自动计算药物剩余天数，\n当库存不足3天时会发出提醒。",
        "add_medication_btn": "添加药物",
        
        # History
        "medication_history": "用药历史",
        "export_pdf": "📄  导出PDF",
        "no_history": "暂无记录",
        "take_some_meds": "服用药物后会在这里显示记录",
        
        # Dialogs
        "ok": "确定",
        "input_required": "请输入",
        "enter_username_msg": "请输入用户名。",
        "enter_password_msg": "请输入密码。",
        "login_failed": "登录失败",
        "invalid_credentials": "用户名或密码错误。\n请重试。",
        "invalid_username": "用户名无效",
        "username_min": "用户名至少需要3个字符。",
        "weak_password": "密码太弱",
        "password_min": "密码至少需要3个字符。",
        "password_mismatch": "密码不匹配",
        "passwords_not_match": "两次输入的密码不一致。\n请重试。",
        "username_taken": "用户名已存在",
        "username_exists": "已被注册。\n请选择其他用户名。",
        "account_created": "账户创建成功！",
        "welcome_new_user": "您的账户已成功创建。",
        "missing_info": "信息不完整",
        "enter_med_name": "请输入药物名称。",
        "enter_total_pills": "请输入库存数量。",
        "enter_pills_per_day": "请输入每日用量。",
        "invalid_input": "输入无效",
        "positive_numbers": "库存和每日用量必须是正整数。",
        "success": "成功",
        "med_added": "已添加到您的药物列表。",
        "dose_recorded": "服药记录",
        "took_dose": "已服用1剂",
        "remaining": "剩余：",
        "pills": "粒",
        "error": "错误",
        "record_failed": "无法记录服药信息。",
        "export_complete": "导出完成",
        "pdf_saved": "PDF报告已保存至：",
        "export_failed": "导出失败",
        "export_error": "无法生成PDF。\n请确保您有用药记录。",
        
        # Language
        "language": "🌐 语言",
        "light_mode": "☀ 亮色",
        "dark_mode": "🌙 暗色",
    }
}


class CustomDialog(ctk.CTkToplevel):
    """Custom dialog for alerts"""
    def __init__(self, parent, title, message, dialog_type="info", btn_text="OK"):
        super().__init__(parent)
        
        self.title(title)
        self.geometry("420x240")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 210
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 120
        self.geometry(f"+{x}+{y}")
        
        # Icon based on type
        icons = {"info": "ℹ", "success": "✓", "warning": "⚠", "error": "✗"}
        colors = {"info": COLORS["primary"], "success": COLORS["success"], 
                  "warning": COLORS["warning"], "error": COLORS["error"]}
        
        icon = icons.get(dialog_type, "ℹ")
        color = colors.get(dialog_type, COLORS["primary"])
        
        # Main frame
        self.configure(fg_color=COLORS["bg_dark"])
        
        frame = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], corner_radius=10)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Icon
        ctk.CTkLabel(frame, text=icon, font=font(50), 
                     text_color=color).pack(pady=(25, 15))
        
        # Message
        ctk.CTkLabel(frame, text=message, font=font(14),
                     wraplength=360, justify="center").pack(pady=(0, 20))
        
        # Button frame to ensure proper display
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=40, pady=(0, 25))
        
        ok_btn = ctk.CTkButton(btn_frame, text=btn_text, width=140, height=scale(42),
                               font=font(14, "bold"),
                               fg_color=color, hover_color=COLORS["accent"],
                               corner_radius=10, command=self.destroy)
        ok_btn.pack(expand=True)
        
        # Focus and wait
        self.focus_set()
        ok_btn.focus_set()
        self.wait_window()


class MedicationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Current language
        self.current_lang = "en"
        self.font_scale = 1.0
        self.font_labels = []
        self.theme_mode = "dark"
        
        self.title(self.t("app_title"))
        self.geometry("1050x700")
        self.minsize(900, 600)
        
        # Configure window
        self.configure(fg_color=COLORS["bg_dark"])
        
        # Current logged in user
        self.current_user_id = None
        self.current_username = None
        
        # Initialize database
        init_db()
        
        # Show login screen first
        self.show_login()
    
    def t(self, key):
        """Get translation for current language"""
        return TRANSLATIONS.get(self.current_lang, TRANSLATIONS["en"]).get(key, key)
    
    def toggle_language(self):
        """Toggle between English and Chinese"""
        self.current_lang = "zh" if self.current_lang == "en" else "en"
        self.title(self.t("app_title"))
        self.refresh_current_view()
    
    def toggle_theme(self):
        """Switch between dark and light themes"""
        self.theme_mode = "light" if self.theme_mode == "dark" else "dark"
        new_palette = LIGHT_THEME if self.theme_mode == "light" else DARK_THEME
        COLORS.clear()
        COLORS.update(new_palette)
        ctk.set_appearance_mode(self.theme_mode)
        self.refresh_current_view()
    
    def refresh_current_view(self):
        """Reload UI based on current auth state"""
        self.configure(fg_color=COLORS["bg_dark"])
        if self.current_user_id:
            self.show_dashboard()
        else:
            self.show_login()
    
    def adjust_font_scale(self, delta):
        """Increase/decrease text size without changing layout dimensions"""
        new_scale = max(0.85, min(1.6, self.font_scale + delta))
        if abs(new_scale - self.font_scale) < 0.01:
            return
        self.font_scale = new_scale
        FONT_MANAGER.set_scale(self.font_scale)
        self.update_font_labels()
    
    def increase_font_size(self):
        self.adjust_font_scale(0.05)
    
    def decrease_font_size(self):
        self.adjust_font_scale(-0.05)
    
    def font_percent_text(self):
        return f"{int(round(self.font_scale * 100))}%"
    
    def theme_button_text(self):
        return self.t("light_mode") if self.theme_mode == "dark" else self.t("dark_mode")
    
    def register_font_label(self, label):
        """Track font-scale labels so they stay in sync"""
        self.font_labels.append(label)
        label.configure(text=self.font_percent_text())
    
    def update_font_labels(self):
        text = self.font_percent_text()
        alive_labels = []
        for lbl in self.font_labels:
            if lbl.winfo_exists():
                lbl.configure(text=text, font=font(12, "bold"))
                alive_labels.append(lbl)
        self.font_labels = alive_labels
    
    def confirm_delete(self, med_name):
        return messagebox.askyesno(self.t("delete"), f"{self.t('delete_confirm')}\n\n{med_name}")
    
    def show_dialog(self, title, message, dialog_type="info"):
        """Show a custom dialog"""
        CustomDialog(self, title, message, dialog_type, self.t("ok"))
    
    def clear_window(self):
        """Remove all widgets and reset grid"""
        for widget in self.winfo_children():
            widget.destroy()
        
        # Reset all grid configurations
        for i in range(10):
            self.grid_rowconfigure(i, weight=0)
            self.grid_columnconfigure(i, weight=0)
    
    # ============================================
    # LOGIN SCREEN
    # ============================================
    def show_login(self):
        self.clear_window()
        
        # Configure grid for split screen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Left side - Branding
        left_frame = ctk.CTkFrame(self, fg_color=COLORS["primary"], corner_radius=0)
        left_frame.grid(row=0, column=0, sticky="nsew")
        
        brand_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        brand_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(brand_frame, text="💊", font=font(80)).pack(pady=(0, 20))
        ctk.CTkLabel(brand_frame, text="Medication", font=font(38, "bold")).pack()
        ctk.CTkLabel(brand_frame, text="Health Reminder", font=font(38, "bold")).pack()
        ctk.CTkLabel(brand_frame, text="Track • Remind • Stay Healthy", 
                     font=font(16), text_color=COLORS["text"]).pack(pady=(25, 0))
        
        # Right side - Login Form
        right_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_dark"], corner_radius=0)
        right_frame.grid(row=0, column=1, sticky="nsew")
        
        # Language toggle at top right
        lang_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        lang_frame.pack(anchor="ne", padx=20, pady=15)
        
        ctk.CTkButton(lang_frame, text="A-", width=60, height=scale(32),
                      font=font(13, "bold"),
                      fg_color=COLORS["bg_input"], hover_color=COLORS["accent"],
                      corner_radius=8, border_width=1, border_color=COLORS["border"],
                      command=self.decrease_font_size,
                      text_color=COLORS["text"]).pack(side="left", padx=(0, 8))
        login_font_label = ctk.CTkLabel(lang_frame, text=self.font_percent_text(),
                                        font=font(12, "bold"), text_color=COLORS["text_secondary"])
        login_font_label.pack(side="left", padx=(0, 8))
        self.register_font_label(login_font_label)
        ctk.CTkButton(lang_frame, text="A+", width=60, height=scale(32),
                      font=font(13, "bold"),
                      fg_color=COLORS["bg_input"], hover_color=COLORS["accent"],
                      corner_radius=8, border_width=1, border_color=COLORS["border"],
                      command=self.increase_font_size,
                      text_color=COLORS["text"]).pack(side="left", padx=(0, 12))
        
        ctk.CTkButton(lang_frame, text=self.theme_button_text(), width=100, height=scale(32),
                      font=font(12, "bold"),
                      fg_color=COLORS["bg_input"], hover_color=COLORS["accent"],
                      text_color=COLORS["text"],
                      corner_radius=8, command=self.toggle_theme).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(lang_frame, text=self.t("language"), width=100, height=scale(32),
                      font=font(12),
                      fg_color=COLORS["bg_card"], hover_color=COLORS["accent"],
                      text_color=COLORS["text"],
                      corner_radius=8, command=self.toggle_language).pack(side="left")
        
        form_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(form_frame, text=self.t("welcome_back"), 
                     font=font(32, "bold")).pack(pady=(0, 8))
        ctk.CTkLabel(form_frame, text=self.t("sign_in_subtitle"), 
                     font=font(14), text_color=COLORS["text_secondary"]).pack(pady=(0, 35))
        
        # Username field
        ctk.CTkLabel(form_frame, text=self.t("username"), font=font(13, "bold")).pack(anchor="w", padx=5)
        self.login_username = ctk.CTkEntry(form_frame, width=320, height=scale(48), 
                                           placeholder_text=self.t("enter_username"),
                                           fg_color=COLORS["bg_input"],
                                           border_color=COLORS["border"],
                                           corner_radius=10)
        self.login_username.pack(pady=(5, 18))
        
        # Password field
        ctk.CTkLabel(form_frame, text=self.t("password"), font=font(13, "bold")).pack(anchor="w", padx=5)
        self.login_password = ctk.CTkEntry(form_frame, width=320, height=scale(48), 
                                           placeholder_text=self.t("enter_password"),
                                           show="●",
                                           fg_color=COLORS["bg_input"],
                                           border_color=COLORS["border"],
                                           corner_radius=10)
        self.login_password.pack(pady=(5, 30))
        
        # Login button
        ctk.CTkButton(form_frame, text=self.t("sign_in"), width=320, height=scale(50),
                      font=font(16, "bold"),
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                      corner_radius=10, command=self.handle_login).pack(pady=(0, 20))
        
        # Divider
        divider_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        divider_frame.pack(fill="x", pady=5)
        ctk.CTkFrame(divider_frame, height=1, fg_color=COLORS["border"]).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(divider_frame, text=f"  {self.t('new_here')}  ", text_color=COLORS["text_secondary"]).pack(side="left")
        ctk.CTkFrame(divider_frame, height=1, fg_color=COLORS["border"]).pack(side="left", fill="x", expand=True)
        
        # Go to Register button
        ctk.CTkButton(form_frame, text=self.t("create_account_btn"), width=320, height=scale(50),
                      font=font(16),
                      fg_color="transparent", hover_color=COLORS["bg_input"],
                      text_color=COLORS["text"],
                      border_width=2, border_color=COLORS["border"],
                      corner_radius=10, command=self.show_register).pack(pady=(15, 0))
        
        # Bind Enter key
        self.login_username.bind("<Return>", lambda e: self.login_password.focus())
        self.login_password.bind("<Return>", lambda e: self.handle_login())
        
        # Focus username
        self.after(100, self.login_username.focus)
    
    def handle_login(self):
        """Handle login"""
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        
        if not username:
            self.show_dialog(self.t("input_required"), self.t("enter_username_msg"), "warning")
            self.login_username.focus()
            return
        
        if not password:
            self.show_dialog(self.t("input_required"), self.t("enter_password_msg"), "warning")
            self.login_password.focus()
            return
        
        # Check credentials
        user_id = None
        for user in get_data_store()["users"]:
            if user["username"] == username and user["password"] == password:
                user_id = user["id"]
                break
        
        if user_id:
            self.current_user_id = user_id
            self.current_username = username
            self.show_dashboard()
        else:
            self.show_dialog(self.t("login_failed"), self.t("invalid_credentials"), "error")
            self.login_password.delete(0, "end")
            self.login_password.focus()
    
    # ============================================
    # REGISTER SCREEN
    # ============================================
    def show_register(self):
        self.clear_window()
        
        # Configure grid - single column centered layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Main scrollable container
        main_container = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg_dark"])
        main_container.grid(row=0, column=0, sticky="nsew")
        
        # Language toggle at top
        lang_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        lang_frame.pack(anchor="ne", padx=20, pady=10)
        
        ctk.CTkButton(lang_frame, text="A-", width=60, height=scale(32),
                      font=font(13, "bold"),
                      fg_color=COLORS["bg_input"], hover_color=COLORS["accent"],
                      corner_radius=8, border_width=1, border_color=COLORS["border"],
                      command=self.decrease_font_size,
                      text_color=COLORS["text"]).pack(side="left", padx=(0, 8))
        register_font_label = ctk.CTkLabel(lang_frame, text=self.font_percent_text(),
                                           font=font(12, "bold"), text_color=COLORS["text_secondary"])
        register_font_label.pack(side="left", padx=(0, 8))
        self.register_font_label(register_font_label)
        ctk.CTkButton(lang_frame, text="A+", width=60, height=scale(32),
                      font=font(13, "bold"),
                      fg_color=COLORS["bg_input"], hover_color=COLORS["accent"],
                      corner_radius=8, border_width=1, border_color=COLORS["border"],
                      command=self.increase_font_size,
                      text_color=COLORS["text"]).pack(side="left", padx=(0, 12))
        
        ctk.CTkButton(lang_frame, text=self.theme_button_text(), width=100, height=scale(32),
                      font=font(12, "bold"),
                      fg_color=COLORS["bg_input"], hover_color=COLORS["accent"],
                      text_color=COLORS["text"],
                      corner_radius=8, command=self.toggle_theme).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(lang_frame, text=self.t("language"), width=100, height=scale(32),
                      font=font(12),
                      fg_color=COLORS["bg_card"], hover_color=COLORS["accent"],
                      text_color=COLORS["text"],
                      corner_radius=8, command=self.toggle_language).pack(side="left")
        
        # Center wrapper
        center_wrapper = ctk.CTkFrame(main_container, fg_color="transparent")
        center_wrapper.pack(expand=True, pady=20)
        
        # Header with icon
        ctk.CTkLabel(center_wrapper, text="🎉", font=font(60)).pack(pady=(0, 10))
        ctk.CTkLabel(center_wrapper, text=self.t("create_account"), 
                     font=font(32, "bold")).pack(pady=(0, 8))
        ctk.CTkLabel(center_wrapper, text=self.t("join_subtitle"), 
                     font=font(14), text_color=COLORS["text_secondary"]).pack(pady=(0, 30))
        
        # Form card
        form_card = ctk.CTkFrame(center_wrapper, fg_color=COLORS["bg_card"], corner_radius=15)
        form_card.pack(padx=20)
        
        form_inner = ctk.CTkFrame(form_card, fg_color="transparent")
        form_inner.pack(padx=40, pady=35)
        
        # Username field
        ctk.CTkLabel(form_inner, text=self.t("username"), font=font(13, "bold")).pack(anchor="w")
        self.register_username = ctk.CTkEntry(form_inner, width=300, height=scale(45), 
                                              placeholder_text=self.t("choose_username"),
                                              fg_color=COLORS["bg_input"],
                                              border_color=COLORS["border"],
                                              corner_radius=10)
        self.register_username.pack(pady=(5, 15))
        
        # Password field
        ctk.CTkLabel(form_inner, text=self.t("password"), font=font(13, "bold")).pack(anchor="w")
        self.register_password = ctk.CTkEntry(form_inner, width=300, height=scale(45), 
                                              placeholder_text=self.t("password_hint"),
                                              show="●",
                                              fg_color=COLORS["bg_input"],
                                              border_color=COLORS["border"],
                                              corner_radius=10)
        self.register_password.pack(pady=(5, 15))
        
        # Confirm Password field
        ctk.CTkLabel(form_inner, text=self.t("confirm_password"), font=font(13, "bold")).pack(anchor="w")
        self.register_confirm = ctk.CTkEntry(form_inner, width=300, height=scale(45), 
                                             placeholder_text=self.t("reenter_password"),
                                             show="●",
                                             fg_color=COLORS["bg_input"],
                                             border_color=COLORS["border"],
                                             corner_radius=10)
        self.register_confirm.pack(pady=(5, 25))
        
        # Register button
        ctk.CTkButton(form_inner, text=self.t("create_account"), width=300, height=scale(48),
                      font=font(15, "bold"),
                      fg_color=COLORS["success"], hover_color=COLORS["success_hover"],
                      corner_radius=10, command=self.handle_register).pack()
        
        # Back to login section
        back_frame = ctk.CTkFrame(center_wrapper, fg_color="transparent")
        back_frame.pack(pady=(25, 0))
        
        ctk.CTkLabel(back_frame, text=self.t("already_have_account"), 
                     text_color=COLORS["text_secondary"]).pack(side="left", padx=(0, 10))
        ctk.CTkButton(back_frame, text=self.t("sign_in_instead"), width=80, height=scale(32),
                      font=font(13, "bold"),
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                      text_color="#ffffff",
                      corner_radius=8, command=self.show_login).pack(side="left")
        
        # Bind Enter key
        self.register_username.bind("<Return>", lambda e: self.register_password.focus())
        self.register_password.bind("<Return>", lambda e: self.register_confirm.focus())
        self.register_confirm.bind("<Return>", lambda e: self.handle_register())
        
        # Focus username
        self.after(100, self.register_username.focus)
    
    def handle_register(self):
        """Handle registration"""
        username = self.register_username.get().strip()
        password = self.register_password.get().strip()
        confirm = self.register_confirm.get().strip()
        
        if not username:
            self.show_dialog(self.t("input_required"), self.t("enter_username_msg"), "warning")
            self.register_username.focus()
            return
        
        if len(username) < 3:
            self.show_dialog(self.t("invalid_username"), self.t("username_min"), "warning")
            self.register_username.focus()
            return
        
        if not password:
            self.show_dialog(self.t("input_required"), self.t("enter_password_msg"), "warning")
            self.register_password.focus()
            return
        
        if len(password) < 3:
            self.show_dialog(self.t("weak_password"), self.t("password_min"), "warning")
            self.register_password.focus()
            return
        
        if password != confirm:
            self.show_dialog(self.t("password_mismatch"), self.t("passwords_not_match"), "error")
            self.register_confirm.delete(0, "end")
            self.register_confirm.focus()
            return
        
        # Check if username exists
        for user in get_data_store()["users"]:
            if user["username"].lower() == username.lower():
                self.show_dialog(self.t("username_taken"), f"'{username}' {self.t('username_exists')}", "error")
                self.register_username.focus()
                return
        
        # Create new user
        new_id = get_next_id("users")
        new_user = {
            "id": new_id,
            "username": username,
            "password": password
        }
        get_data_store()["users"].append(new_user)
        save_data()
        
        self.show_dialog(self.t("account_created"), f"{self.t('welcome_user')}, {username}!\n\n{self.t('welcome_new_user')}", "success")
        self.show_login()
    
    # ============================================
    # DASHBOARD
    # ============================================
    def show_dashboard(self):
        self.clear_window()
        
        # Configure grid for sidebar layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        self.create_sidebar()
        
        # Main content area
        self.content_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_dark"], corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Show medications by default
        self.show_medications_view()
    
    def create_sidebar(self):
        """Create the sidebar navigation"""
        sidebar_container = ctk.CTkFrame(self, width=260, fg_color=COLORS["bg_card"], corner_radius=0)
        sidebar_container.grid(row=0, column=0, sticky="nsew")
        sidebar_container.grid_propagate(False)
        
        sidebar = ctk.CTkScrollableFrame(sidebar_container, width=260, fg_color=COLORS["bg_card"], corner_radius=0, label_text="")
        sidebar.pack(fill="both", expand=True)
        sidebar.grid_columnconfigure(0, weight=1)
        
        # Logo section
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=25, pady=(35, 25))
        
        ctk.CTkLabel(logo_frame, text="💊", font=font(45)).pack()
        ctk.CTkLabel(logo_frame, text="Med Reminder", 
                     font=font(22, "bold")).pack(pady=(8, 0))
        
        # Divider
        ctk.CTkFrame(sidebar, height=1, fg_color=COLORS["border"]).pack(fill="x", padx=25, pady=(0, 20))
        
        # User info card
        user_frame = ctk.CTkFrame(sidebar, fg_color=COLORS["accent"], corner_radius=12)
        user_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        user_inner = ctk.CTkFrame(user_frame, fg_color="transparent")
        user_inner.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(user_inner, text="👤", font=font(24), text_color=COLORS["text"]).pack(side="left")
        ctk.CTkLabel(user_inner, text=self.current_username, 
                     font=font(15, "bold"), text_color=COLORS["text"]).pack(side="left", padx=(10, 0))
        
        # Navigation buttons
        self.nav_buttons = {}
        
        nav_items = [
            ("medications", self.t("my_medications"), self.show_medications_view),
            ("add", self.t("add_medication"), self.show_add_view),
            ("history", self.t("history"), self.show_history_view),
        ]
        
        for key, text, command in nav_items:
            btn = ctk.CTkButton(sidebar, text=text, width=220, height=scale(48),
                               font=font(14),
                               fg_color="transparent", 
                               hover_color=COLORS["accent"],
                               anchor="w", corner_radius=10,
                               text_color=COLORS["text"],
                               command=command)
            btn.pack(pady=4, padx=20)
            self.nav_buttons[key] = btn
        
        # Set initial active
        self.set_active_nav("medications")
        
        # Spacer
        ctk.CTkLabel(sidebar, text="").pack(fill="both", expand=True)
        
        # Extra gap before controls
        ctk.CTkFrame(sidebar, fg_color="transparent", height=scale(60)).pack(fill="x")
        
        # Font size controls
        font_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        font_frame.pack(pady=(0, scale(12)))
        
        ctk.CTkButton(font_frame, text="A-", width=60, height=scale(32),
                      font=font(13, "bold"),
                      fg_color=COLORS["bg_input"], hover_color=COLORS["accent"],
                      corner_radius=8, border_width=1, border_color=COLORS["border"],
                      text_color=COLORS["text"],
                      command=self.decrease_font_size).pack(side="left", padx=6)
        sidebar_font_label = ctk.CTkLabel(font_frame, text=self.font_percent_text(),
                                          font=font(12, "bold"), text_color=COLORS["text_secondary"])
        sidebar_font_label.pack(side="left", padx=4)
        self.register_font_label(sidebar_font_label)
        ctk.CTkButton(font_frame, text="A+", width=60, height=scale(32),
                      font=font(13, "bold"),
                      fg_color=COLORS["bg_input"], hover_color=COLORS["accent"],
                      corner_radius=8, border_width=1, border_color=COLORS["border"],
                      text_color=COLORS["text"],
                      command=self.increase_font_size).pack(side="left", padx=6)
        
        # Theme toggle
        ctk.CTkButton(sidebar, text=self.theme_button_text(), width=220, height=scale(40),
                      font=font(13, "bold"),
                      fg_color=COLORS["bg_input"], hover_color=COLORS["accent"],
                      corner_radius=10, text_color=COLORS["text"],
                      command=self.toggle_theme).pack(pady=(0, 10), padx=20)
        
        # Language toggle
        ctk.CTkButton(sidebar, text=self.t("language"), width=220, height=scale(40),
                      font=font(13),
                      fg_color=COLORS["bg_input"], hover_color=COLORS["accent"],
                      text_color=COLORS["text"],
                      corner_radius=10, command=self.toggle_language).pack(pady=(0, 10), padx=20)
        
        # Version info
        ctk.CTkLabel(sidebar, text=self.t("version"), font=font(11),
                     text_color=COLORS["text_secondary"]).pack(pady=(0, 10))
        
        # Logout button
        ctk.CTkButton(sidebar, text=self.t("sign_out"), width=220, height=scale(48),
                      font=font(14),
                      fg_color=COLORS["error"], hover_color="#dc2626",
                      corner_radius=10, command=self.logout).pack(pady=(0, 25), padx=20)
    
    def set_active_nav(self, active_key):
        """Update navigation button styles"""
        for key, btn in self.nav_buttons.items():
            if key == active_key:
                btn.configure(fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                              text_color="#ffffff")
            else:
                btn.configure(fg_color="transparent", hover_color=COLORS["accent"],
                              text_color=COLORS["text"])
    
    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def logout(self):
        """Sign out and return to login"""
        self.current_user_id = None
        self.current_username = None
        self.show_login()
    
    # ============================================
    # MEDICATIONS VIEW
    # ============================================
    def show_medications_view(self):
        self.set_active_nav("medications")
        self.clear_content()
        
        # Header
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=35, pady=(35, 25))
        
        ctk.CTkLabel(header, text=self.t("my_medications_title"), 
                     font=font(28, "bold")).pack(side="left")
        
        ctk.CTkButton(header, text=self.t("refresh"), width=120, height=scale(42),
                      fg_color=COLORS["bg_card"], hover_color=COLORS["accent"],
                      border_width=1, border_color=COLORS["border"],
                      text_color=COLORS["text"],
                      corner_radius=10, command=self.refresh_medications).pack(side="right")
        
        # Medications container
        meds_container = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        meds_container.grid(row=1, column=0, sticky="nsew", padx=35, pady=(0, 35))
        
        self.meds_container = meds_container
        self.refresh_medications()
    
    def refresh_medications(self):
        """Refresh the medications list"""
        for widget in self.meds_container.winfo_children():
            widget.destroy()
        
        # Get today's date string for comparison
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Get medications for current user
        meds = []
        for med in get_data_store()["medications"]:
            if med["user_id"] == self.current_user_id:
                current_stock = med["total_pills"]
                daily_dose = med["pills_per_day"]
                
                if daily_dose > 0:
                    days_remaining = int(current_stock / daily_dose)
                else:
                    days_remaining = 999
                
                is_low_stock = days_remaining < 3
                
                # Count pills taken today for this medication
                taken_today = 0
                for h in get_data_store()["history"]:
                    if h["med_id"] == med["id"] and h["taken_at"].startswith(today):
                        taken_today += 1
                
                med_data = med.copy()
                med_data["days_remaining"] = days_remaining
                med_data["alert"] = is_low_stock
                med_data["taken_today"] = taken_today
                meds.append(med_data)
        
        if not meds:
            empty_frame = ctk.CTkFrame(self.meds_container, fg_color=COLORS["bg_card"], corner_radius=15)
            empty_frame.pack(fill="x", pady=10)
            
            ctk.CTkLabel(empty_frame, text="📭", font=font(50)).pack(pady=(40, 15))
            ctk.CTkLabel(empty_frame, text=self.t("no_medications"), 
                         font=font(20, "bold")).pack()
            ctk.CTkLabel(empty_frame, text=self.t("click_add"),
                         text_color=COLORS["text_secondary"]).pack(pady=(8, 40))
            return
        
        for med in meds:
            self.create_medication_card(med)
    
    def create_medication_card(self, med):
        """Create a card for each medication"""
        card = ctk.CTkFrame(self.meds_container, fg_color=COLORS["bg_card"], corner_radius=15)
        card.pack(fill="x", pady=8)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Top row - name and status
        top_row = ctk.CTkFrame(inner, fg_color="transparent")
        top_row.pack(fill="x")
        
        ctk.CTkLabel(top_row, text=med['name'], 
                     font=font(20, "bold")).pack(side="left")
        
        # Status badge
        if med['alert']:
            status_color = COLORS["warning"]
            status_text = self.t("low_stock")
        else:
            status_color = COLORS["success"]
            status_text = self.t("in_stock_status")
        
        status_badge = ctk.CTkFrame(top_row, fg_color=status_color, corner_radius=8)
        
        actions = ctk.CTkFrame(top_row, fg_color="transparent")
        actions.pack(side="right", padx=(10, 0))
        
        delete_btn = ctk.CTkButton(actions, text=self.t("delete"), width=80, height=scale(32),
                                   fg_color=COLORS["error"], hover_color="#dc2626",
                                   corner_radius=8, font=font(12, "bold"),
                                   text_color="#ffffff",
                                   command=lambda m=med: self.delete_medication(m))
        delete_btn.pack(side="right")
        
        status_badge.pack(side="right", padx=(0, 10))
        ctk.CTkLabel(status_badge, text=status_text, 
                     font=font(12, "bold"), text_color="#ffffff").pack(padx=14, pady=6)
        
        # Info row
        info_frame = ctk.CTkFrame(inner, fg_color="transparent")
        info_frame.pack(fill="x", pady=(12, 15))
        
        info_items = [
            (f"💊 {med['total_pills']}", self.t("in_stock")),
            (f"📅 {med['pills_per_day']}", self.t("per_day")),
            (f"⏳ {med['days_remaining']}", self.t("days_left")),
        ]
        
        for value, label in info_items:
            item_frame = ctk.CTkFrame(info_frame, fg_color=COLORS["bg_input"], corner_radius=8)
            item_frame.pack(side="left", padx=(0, 10))
            
            ctk.CTkLabel(item_frame, text=value, font=font(14, "bold")).pack(padx=15, pady=(10, 2))
            ctk.CTkLabel(item_frame, text=label, font=font(11),
                         text_color=COLORS["text_secondary"]).pack(padx=15, pady=(0, 10))
        
        # Today's progress section
        progress_frame = ctk.CTkFrame(inner, fg_color="transparent")
        progress_frame.pack(fill="x", pady=(0, 15))
        
        taken_today = med.get('taken_today', 0)
        daily_dose = med['pills_per_day']
        remaining_today = max(0, daily_dose - taken_today)
        
        # Progress indicator
        if taken_today >= daily_dose:
            progress_color = COLORS["success"]
            progress_text = f"{self.t('done_today')} ({taken_today}/{daily_dose})"
        elif taken_today > 0:
            progress_color = COLORS["warning"]
            progress_text = f"⏰ {taken_today}/{daily_dose} {self.t('taken_today')} ({remaining_today} {self.t('more_to_go')})"
        else:
            progress_color = COLORS["text_secondary"]
            progress_text = f"📋 0/{daily_dose} {self.t('taken_today')}"
        
        # Today's progress card
        today_card = ctk.CTkFrame(progress_frame, fg_color=COLORS["bg_input"], corner_radius=8)
        today_card.pack(fill="x")
        
        today_inner = ctk.CTkFrame(today_card, fg_color="transparent")
        today_inner.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(today_inner, text=self.t("todays_progress"), 
                     font=font(12, "bold"),
                     text_color=COLORS["text_secondary"]).pack(side="left")
        
        ctk.CTkLabel(today_inner, text=progress_text, 
                     font=font(13, "bold"),
                     text_color=progress_color).pack(side="right")
        
        # Take button - disabled if already completed for today
        btn_frame = ctk.CTkFrame(inner, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        if taken_today >= daily_dose:
            # Already completed - show disabled-style button
            ctk.CTkButton(btn_frame, text=self.t("completed_today"), width=160, height=scale(42),
                          fg_color=COLORS["success"], hover_color=COLORS["success"],
                          corner_radius=10, font=font(14, "bold"),
                          state="disabled").pack(side="right")
        else:
            ctk.CTkButton(btn_frame, text=self.t("take_dose"), width=140, height=scale(42),
                          fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                          corner_radius=10, font=font(14, "bold"),
                          command=lambda m=med: self.take_medication(m)).pack(side="right")
    
    def take_medication(self, med):
        """Record taking a medication"""
        for m in get_data_store()["medications"]:
            if m["id"] == med["id"]:
                m["total_pills"] = max(0, m["total_pills"] - 1)
                new_stock = m["total_pills"]
                
                # Add history entry
                history_entry = {
                    "med_id": med["id"],
                    "medication_name": med["name"],
                    "taken_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                get_data_store()["history"].append(history_entry)
                save_data()
                
                self.refresh_medications()
                self.show_dialog(self.t("dose_recorded"), 
                               f"{self.t('took_dose')} '{med['name']}'.\n\n{self.t('remaining')} {new_stock} {self.t('pills')}", 
                               "success")
                return
        
        self.show_dialog(self.t("error"), self.t("record_failed"), "error")
    
    def delete_medication(self, med):
        """Remove a medication and related history"""
        if not self.confirm_delete(med["name"]):
            return
        
        data = get_data_store()
        data["medications"] = [m for m in data["medications"] if m["id"] != med["id"]]
        data["history"] = [h for h in data["history"] if h.get("med_id") != med["id"]]
        save_data()
        self.refresh_medications()
        self.show_dialog(self.t("success"), self.t("delete_success"), "success")
    
    # ============================================
    # ADD MEDICATION VIEW
    # ============================================
    def show_add_view(self):
        self.set_active_nav("add")
        self.clear_content()
        
        # Header
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=35, pady=(35, 25))
        
        ctk.CTkLabel(header, text=self.t("add_new_medication"), 
                     font=font(28, "bold")).pack(anchor="w")
        ctk.CTkLabel(header, text=self.t("add_subtitle"),
                     font=font(14), text_color=COLORS["text_secondary"]).pack(anchor="w", pady=(5, 0))
        
        # Form container
        form_container = ctk.CTkFrame(self.content_frame, fg_color=COLORS["bg_card"], corner_radius=15)
        form_container.grid(row=1, column=0, sticky="new", padx=35, pady=(0, 35))
        
        form = ctk.CTkFrame(form_container, fg_color="transparent")
        form.pack(padx=40, pady=40)
        
        # Medication name
        ctk.CTkLabel(form, text=self.t("medication_name"), font=font(14, "bold")).pack(anchor="w")
        self.add_name_entry = ctk.CTkEntry(form, width=450, height=scale(48), 
                                           placeholder_text=self.t("medication_placeholder"),
                                           fg_color=COLORS["bg_input"],
                                           border_color=COLORS["border"],
                                           corner_radius=10)
        self.add_name_entry.pack(pady=(8, 25))
        
        # Two column layout
        num_frame = ctk.CTkFrame(form, fg_color="transparent")
        num_frame.pack(fill="x", pady=(0, 25))
        
        # Total pills
        left_col = ctk.CTkFrame(num_frame, fg_color="transparent")
        left_col.pack(side="left", padx=(0, 25))
        ctk.CTkLabel(left_col, text=self.t("total_pills"), font=font(14, "bold")).pack(anchor="w")
        self.add_stock_entry = ctk.CTkEntry(left_col, width=212, height=scale(48),
                                            placeholder_text=self.t("pills_placeholder"),
                                            fg_color=COLORS["bg_input"],
                                            border_color=COLORS["border"],
                                            corner_radius=10)
        self.add_stock_entry.pack(pady=(8, 0))
        
        # Pills per day
        right_col = ctk.CTkFrame(num_frame, fg_color="transparent")
        right_col.pack(side="left")
        ctk.CTkLabel(right_col, text=self.t("pills_per_day"), font=font(14, "bold")).pack(anchor="w")
        self.add_daily_entry = ctk.CTkEntry(right_col, width=212, height=scale(48),
                                            placeholder_text=self.t("per_day_placeholder"),
                                            fg_color=COLORS["bg_input"],
                                            border_color=COLORS["border"],
                                            corner_radius=10)
        self.add_daily_entry.pack(pady=(8, 0))
        
        # Info box
        info_frame = ctk.CTkFrame(form, fg_color=COLORS["bg_input"], corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(info_frame, text=self.t("smart_alerts"), font=font(13, "bold")).pack(anchor="w", padx=20, pady=(15, 5))
        ctk.CTkLabel(info_frame, text=self.t("smart_alerts_desc"),
                     font=font(12), text_color=COLORS["text_secondary"],
                     justify="left").pack(anchor="w", padx=20, pady=(0, 15))
        
        # Submit button
        ctk.CTkButton(form, text=self.t("add_medication_btn"), width=450, height=scale(52),
                      font=font(16, "bold"),
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                      corner_radius=10,
                      command=self.add_new_medication).pack()
        
        # Focus first field
        self.after(100, self.add_name_entry.focus)
    
    def add_new_medication(self):
        """Add a new medication"""
        name = self.add_name_entry.get().strip()
        stock = self.add_stock_entry.get().strip()
        daily = self.add_daily_entry.get().strip()
        
        if not name:
            self.show_dialog(self.t("missing_info"), self.t("enter_med_name"), "warning")
            self.add_name_entry.focus()
            return
        
        if not stock:
            self.show_dialog(self.t("missing_info"), self.t("enter_total_pills"), "warning")
            self.add_stock_entry.focus()
            return
        
        if not daily:
            self.show_dialog(self.t("missing_info"), self.t("enter_pills_per_day"), "warning")
            self.add_daily_entry.focus()
            return
        
        try:
            stock = int(stock)
            daily = int(daily)
            if stock <= 0 or daily <= 0:
                raise ValueError()
        except ValueError:
            self.show_dialog(self.t("invalid_input"), self.t("positive_numbers"), "error")
            return
        
        # Add medication
        new_id = get_next_id("medications")
        new_med = {
            "id": new_id,
            "user_id": self.current_user_id,
            "name": name,
            "total_pills": stock,
            "pills_per_day": daily
        }
        get_data_store()["medications"].append(new_med)
        save_data()
        
        # Clear form
        self.add_name_entry.delete(0, "end")
        self.add_stock_entry.delete(0, "end")
        self.add_daily_entry.delete(0, "end")
        
        self.show_dialog(self.t("success"), f"'{name}' {self.t('med_added')}", "success")
        self.show_medications_view()
    
    # ============================================
    # HISTORY VIEW
    # ============================================
    def show_history_view(self):
        self.set_active_nav("history")
        self.clear_content()
        
        # Header
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=35, pady=(35, 25))
        
        ctk.CTkLabel(header, text=self.t("medication_history"), 
                     font=font(28, "bold")).pack(side="left")
        
        ctk.CTkButton(header, text=self.t("export_pdf"), width=140, height=scale(42),
                      fg_color=COLORS["success"], hover_color=COLORS["success_hover"],
                      corner_radius=10, command=self.export_pdf).pack(side="right")
        
        # History container
        history_container = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        history_container.grid(row=1, column=0, sticky="nsew", padx=35, pady=(0, 35))
        
        self.history_container = history_container
        self.refresh_history()
    
    def refresh_history(self):
        """Refresh the history list"""
        for widget in self.history_container.winfo_children():
            widget.destroy()
        
        # Get user's medication IDs
        user_med_ids = [m["id"] for m in get_data_store()["medications"] if m["user_id"] == self.current_user_id]
        
        # Filter history
        history = [h for h in get_data_store()["history"] if h["med_id"] in user_med_ids]
        history.sort(key=lambda x: x["taken_at"], reverse=True)
        
        if not history:
            empty_frame = ctk.CTkFrame(self.history_container, fg_color=COLORS["bg_card"], corner_radius=15)
            empty_frame.pack(fill="x", pady=10)
            
            ctk.CTkLabel(empty_frame, text="📭", font=font(50)).pack(pady=(40, 15))
            ctk.CTkLabel(empty_frame, text=self.t("no_history"), 
                         font=font(20, "bold")).pack()
            ctk.CTkLabel(empty_frame, text=self.t("take_some_meds"),
                         text_color=COLORS["text_secondary"]).pack(pady=(8, 40))
            return
        
        for log in history:
            self.create_history_card(log)
    
    def create_history_card(self, log):
        """Create a card for each history entry"""
        card = ctk.CTkFrame(self.history_container, fg_color=COLORS["bg_card"], corner_radius=12)
        card.pack(fill="x", pady=5)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=25, pady=18)
        
        ctk.CTkLabel(inner, text=f"💊  {log['medication_name']}", 
                     font=font(16, "bold")).pack(side="left")
        
        ctk.CTkLabel(inner, text=log['taken_at'], 
                     font=font(13), text_color=COLORS["text_secondary"]).pack(side="right")
    
    def export_pdf(self):
        """Export history to PDF"""
        from exporter import generate_pdf_report
        
        folder = "Reports"
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        filename = os.path.join(folder, f"Report_User_{self.current_user_id}.pdf")
        
        if generate_pdf_report(self.current_user_id, filename):
            full_path = os.path.abspath(filename)
            self.show_dialog(self.t("export_complete"), f"{self.t('pdf_saved')}\n\n{full_path}", "success")
        else:
            self.show_dialog(self.t("export_failed"), self.t("export_error"), "error")


if __name__ == "__main__":
    app = MedicationApp()
    app.mainloop()
