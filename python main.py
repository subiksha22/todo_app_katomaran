import tkinter as tk
from tkinter import messagebox, simpledialog
import json, os
from datetime import datetime

# ------------------ STYLES ------------------
COLORS = {
    "bg_dark": "#0D3025",
    "bg_light": "#E6F0E6",
    "accent": "#C2A24B",
    "btn_gray": "#5A7261",
    "btn_green": "#455F51",
    "entry_bg": "#CBD5D8",
    "task_fill": "#DCE8DB",
    "task_bg": "#5E7766",
    "text_light": "#E6F0E6",
    "text_dark": "#0D3025"
}

FONTS = {
    "header": ("Helvetica Neue", 28, "bold"),
    "subheader": ("Helvetica Neue", 22),
    "body": ("Helvetica Neue", 14),
    "link": ("Helvetica Neue", 12, "underline"),
    "button": ("Helvetica Neue", 14, "bold")
}

# ------------------ DATA ------------------
def load_users():
    return json.load(open("users.json")) if os.path.exists("users.json") else {}

def save_users(u): json.dump(u, open("users.json", "w"))
def load_tasks(u):
    fn = f"{u}_tasks.json"
    return json.load(open(fn)) if os.path.exists(fn) else []
def save_tasks(u, t): json.dump(t, open(f"{u}_tasks.json", "w"))

current_user = None

# ------------------ BASE APP ------------------
class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("414x896")
        self.title("Todo App")
        self.users = load_users()
        self.frames = {}
        self.configure(bg=COLORS['bg_dark'])
        for F in (WelcomePage, LoginPage, SignUpPage, MenuPage,
                  CreateTaskPage, ViewTaskPage, UpdateTaskPage, DeleteTaskPage):
            frm = F(self)
            self.frames[F] = frm
            frm.place(relwidth=1, relheight=1)
        self.show(WelcomePage)

    def show(self, page):
        self.frames[page].tkraise()
        if hasattr(self.frames[page], "refresh"):
            self.frames[page].refresh()

# ------------------ HELPER WIDGETS ------------------
def styled_button(master, text, fg="white", bg=None, cmd=None, width=25, icon=""):
    b = tk.Button(master, text=f"{text}{icon}", font=FONTS['button'],
                  bg=bg or COLORS['btn_gray'], fg=fg,
                  relief="flat", command=cmd, width=width)
    return b

def task_bar(master, title, progress=0.6, status_icon="🗑️"):
    fr = tk.Frame(master, bg=COLORS['bg_dark'])
    tk.Label(fr, text=title, font=FONTS['body'],
             bg=COLORS['bg_dark'], fg=COLORS['text_light']).pack(anchor="w", padx=10)
    barframe = tk.Frame(fr, bg=COLORS['task_bg'], width=320, height=24)
    barframe.pack(padx=10, pady=5)
    barframe.pack_propagate(False)
    fill = tk.Frame(barframe, bg=COLORS['task_fill'],
                    width=int(320 * progress), height=24)
    fill.pack(side="left")
    btn = styled_button(fr, "", fg=COLORS['text_light'], bg=COLORS['bg_dark'],
                        cmd=None, width=3, icon=status_icon)
    btn.pack(side="right", padx=10, pady=2)
    return fr

# ------------------ PAGES ------------------
class WelcomePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORS['bg_dark'])
        tk.Label(self, text="🔶", font=("Helvetica Neue", 48), bg=COLORS['bg_dark'],
                 fg=COLORS['accent']).pack(pady=(100,10))
        tk.Label(self, text="Let’s Get", font=FONTS['subheader'], bg=COLORS['bg_dark'],
                 fg=COLORS['text_light']).pack()
        tk.Label(self, text="Started!", font=FONTS['header'], bg=COLORS['bg_dark'],
                 fg=COLORS['accent']).pack(pady=(0,40))
        styled_button(self, "SIGN IN", cmd=lambda: master.show(LoginPage)).pack(pady=10)
        tk.Label(self, text="OR SIGN IN WITH", font=FONTS['body'],
                 bg=COLORS['bg_dark'], fg=COLORS['text_light']).pack(pady=5)
        styled_button(self, " G", width=6).pack(pady=5)  # Google icon placeholder
        tk.Label(self, text="DIDN’T HAVE ACCOUNT?", font=FONTS['body'],
                 bg=COLORS['bg_dark'], fg=COLORS['text_light']).pack(pady=(80,0))
        styled_button(self, "SIGN UP NOW", fg="blue",
                      bg=COLORS['bg_dark'], cmd=lambda: master.show(SignUpPage)).pack()

class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORS['bg_dark'])
        tk.Label(self, text="Welcome", font=FONTS['subheader'], bg=COLORS['bg_dark'],
                 fg=COLORS['text_light']).pack(pady=(100,0))
        tk.Label(self, text="Back!", font=FONTS['header'], bg=COLORS['bg_dark'],
                 fg=COLORS['accent']).pack(pady=(0,30))
        self.email = tk.Entry(self, font=FONTS['body'], bg=COLORS['entry_bg'])
        self.email.insert(0, "Email Address"); self.email.pack(pady=5, ipadx=20, ipady=5)
        self.password = tk.Entry(self, font=FONTS['body'], show="*", bg=COLORS['entry_bg'])
        self.password.insert(0, "Password"); self.password.pack(pady=5, ipadx=20, ipady=5)
        styled_button(self, "LOG IN", cmd=self.login).pack(pady=10)
        tk.Label(self, text="Forgot Password?", font=FONTS['link'],
                 fg="blue", bg=COLORS['bg_dark']).pack()
        tk.Label(self, text="Don’t have an account?", font=FONTS['body'],
                 fg=COLORS['text_light'], bg=COLORS['bg_dark']).pack(pady=(60,0))
        styled_button(self, "Sign up", fg="blue", bg=COLORS['bg_dark'],
                      cmd=lambda: master.show(SignUpPage)).pack()

    def login(self):
        global current_user
        u = self.email.get(); p = self.password.get()
        if u in self.master.users and self.master.users[u] == p:
            current_user = u
            self.master.show(MenuPage)
        else:
            messagebox.showerror("Error", "Invalid credentials")

class SignUpPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORS['bg_dark'])
        tk.Label(self, text="Create an", font=FONTS['subheader'], bg=COLORS['bg_dark'],
                 fg=COLORS['text_light']).pack(pady=(100,0))
        tk.Label(self, text="Account!", font=FONTS['header'], bg=COLORS['bg_dark'],
                 fg=COLORS['accent']).pack(pady=(0,30))
        self.username = tk.Entry(self, font=FONTS['body'], bg=COLORS['entry_bg'])
        self.username.insert(0, "Username"); self.username.pack(pady=5, ipadx=20, ipady=5)
        self.email = tk.Entry(self, font=FONTS['body'], bg=COLORS['entry_bg'])
        self.email.insert(0, "Email Address"); self.email.pack(pady=5, ipadx=20, ipady=5)
        self.password = tk.Entry(self, font=FONTS['body'], show="*", bg=COLORS['entry_bg'])
        self.password.insert(0, "Password"); self.password.pack(pady=5, ipadx=20, ipady=5)
        self.confirm = tk.Entry(self, font=FONTS['body'], show="*", bg=COLORS['entry_bg'])
        self.confirm.insert(0, "Confirm Password"); self.confirm.pack(pady=5, ipadx=20, ipady=5)
        styled_button(self, "CREATE ACCOUNT", cmd=self.register).pack(pady=20)
        tk.Button(self, text="Already have an account? Sign in", font=FONTS['link'],
                  fg="blue", bg=COLORS['bg_dark'], relief="flat",
                  command=lambda: master.show(LoginPage)).pack()

    def register(self):
        u = self.username.get(); p = self.password.get(); cp = self.confirm.get()
        if p != cp:
            messagebox.showerror("Error", "Passwords don't match")
            return
        if u in self.master.users:
            messagebox.showerror("Error", "User exists")
        else:
            self.master.users[u] = p
            save_users(self.master.users)
            messagebox.showinfo("Success", "Account created")
            self.master.show(LoginPage)

class MenuPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORS['bg_dark'])
        tk.Label(self, text="Menu", font=FONTS['header'], bg=COLORS['bg_dark'],
                 fg=COLORS['accent']).pack(pady=40)
        for txt, page, icon in [
            ("Create Task", CreateTaskPage, " ➕"),
            ("Update Task", UpdateTaskPage, " 🔄"),
            ("Delete Task", DeleteTaskPage, " 🗑️"),
            ("View Task", ViewTaskPage, " 👁️")
        ]:
            styled_button(self, txt, cmd=lambda p=page: master.show(p), icon=icon).pack(pady=10)
        styled_button(self, "Logout", fg=COLORS['btn_green'], bg=COLORS['bg_dark'],
                      cmd=lambda: master.show(WelcomePage)).pack(pady=30)

class CreateTaskPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORS['bg_light'])
        tk.Label(self, text="Create Task", font=FONTS['header'], bg=COLORS['bg_light'],
                 fg=COLORS['text_dark']).pack(pady=20)
        self.title = tk.Entry(self, font=FONTS['body'], bg=COLORS['entry_bg'])
        self.title.insert(0, "Title"); self.title.pack(pady=5, ipadx=20, ipady=5)
        self.desc = tk.Entry(self, font=FONTS['body'], bg=COLORS['entry_bg'])
        self.desc.insert(0, "Description"); self.desc.pack(pady=5, ipadx=20, ipady=5)
        self.due = tk.Entry(self, font=FONTS['body'], bg=COLORS['entry_bg'])
        self.due.insert(0, "Due Date (YYYY-MM-DD)"); self.due.pack(pady=5, ipadx=20, ipady=5)
        styled_button(self, "Save Task", fg=COLORS['text_dark'], bg=COLORS['btn_gray'],
                      cmd=self.save_task).pack(pady=10)
        styled_button(self, "Back", fg=COLORS['text_dark'], bg=COLORS['entry_bg'],
                      cmd=lambda: master.show(MenuPage)).pack(pady=10)

    def save_task(self):
        tasks = load_tasks(current_user)
        tasks.append({"title": self.title.get(),
                      "desc": self.desc.get(),
                      "due": self.due.get(),
                      "status": "Pending"})
        save_tasks(current_user, tasks)
        messagebox.showinfo("Success", "Task created!")
        self.master.show(MenuPage)

class ViewTaskPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORS['bg_dark'])
        tk.Label(self, text="Your Tasks", font=FONTS['header'], bg=COLORS['bg_dark'],
                 fg=COLORS['accent']).pack(pady=20)
        self.container = tk.Frame(self, bg=COLORS['bg_dark'])
        self.container.pack(pady=10)
        styled_button(self, "Back", fg=COLORS['text_light'], bg=COLORS['entry_bg'],
                      cmd=lambda: master.show(MenuPage)).pack(pady=10)

    def refresh(self):
        for w in self.container.winfo_children(): w.destroy()
        for i, t in enumerate(load_tasks(current_user)):
            progress = 0.4 if t["status"]=="Pending" else 1.0
            tb = task_bar(self.container, f"{i+1}. {t['title']}", progress, status_icon="🗑️")
            tb.pack(pady=10)

class UpdateTaskPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORS['bg_dark'])
        tk.Label(self, text="Update Task", font=FONTS['header'], bg=COLORS['bg_dark'],
                 fg=COLORS['accent']).pack(pady=20)
        self.container = tk.Frame(self, bg=COLORS['bg_dark'])
        self.container.pack(pady=10)
        styled_button(self, "Back", fg=COLORS['text_light'], bg=COLORS['entry_bg'],
                      cmd=lambda: master.show(MenuPage)).pack(pady=10)

    def refresh(self):
        for w in self.container.winfo_children(): w.destroy()
        tasks = load_tasks(current_user)
        for i, t in enumerate(tasks):
            b = styled_button(self.container, f"{t['title']} (Edit)", cmd=lambda i=i: self.edit(i), bg=COLORS['btn_gray'])
            b.pack(pady=5)

    def edit(self, idx):
        task = load_tasks(current_user)[idx]
        top = simpledialog._QueryString(self, f"Edit {task['title']}", initialvalue=task['title'])
        new_title = top.result
        if new_title is None: return
        task['title'], task['desc'], task['due'] = new_title, simpledialog.askstring("Desc","New?", initialvalue=task['desc']), simpledialog.askstring("Due","New?", initialvalue=task['due'])
        tasks = load_tasks(current_user); tasks[idx] = task
        save_tasks(current_user, tasks)
        self.refresh()

class DeleteTaskPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORS['bg_dark'])
        tk.Label(self, text="Delete Task", font=FONTS['header'], bg=COLORS['bg_dark'],
                 fg=COLORS['accent']).pack(pady=20)
        self.container = tk.Frame(self, bg=COLORS['bg_dark'])
        self.container.pack(pady=10)
        styled_button(self, "Back", fg=COLORS['text_light'], bg=COLORS['entry_bg'],
                      cmd=lambda: master.show(MenuPage)).pack(pady=10)

    def refresh(self):
        for w in self.container.winfo_children(): w.destroy()
        for i, t in enumerate(load_tasks(current_user)):
            b = styled_button(self.container, f"Delete {t['title']}", fg="white", bg="red",
                              cmd=lambda i=i: self.delete(i))
            b.pack(pady=5)

    def delete(self, idx):
        tasks = load_tasks(current_user)
        del tasks[idx]
        save_tasks(current_user, tasks)
        self.refresh()

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
