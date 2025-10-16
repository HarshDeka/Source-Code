import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import string
from datetime import datetime

LIGHT = {
    "bg": "#f5f6fb", "fg": "#24272e", "primary": "#25C684", "secondary": "#2b2e38",
    "button": "#e3e8ee", "button_hover": "#c1c7d0", "entry": "#fff", "border": "#e2e2e2",
    "card": "#fff", "review_bg": "#efefef", "review_fg": "#333"
}

DARK = {
    "bg": "#18202c", "fg": "#f7fafc", "primary": "#25C684", "secondary": "#24272e",
    "button": "#23272f", "button_hover": "#323648", "entry": "#23272f", "border": "#323648",
    "card": "#23272f", "review_bg": "#222b37", "review_fg": "#f7f7fa"
}

def star_string(rating):
    full, half = divmod(rating, 1)
    return '★' * int(full) + ('½' if half >= 0.5 else '')

class ShramikSevaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shramik Seva")
        self.geometry("1100x850")
        self.resizable(False, False)
        self.theme = DARK
        self.is_employer = False
        self.subscription_plan = None
        self.current_user = {}
        self.jobs = {}
        self.fade_job = None
        self.sun_icon = "☀"
        self.moon_icon = "🌙"

        self.workers = [
            {"name": "Amit Singh", "service": "Plumber", "phone": "9999999999", "aadhaar": "1234-5678-9012", "region": "North", "verified": True, "rating": 4.5, "reviews": []},
            {"name": "Sara Ahmed", "service": "Electrician", "phone": "8888888888", "aadhaar": "2345-6789-0123", "region": "South", "verified": True, "rating": 5, "reviews": []},
            {"name": "Ravi Kumar", "service": "Carpenter", "phone": "7777777777", "aadhaar": "3456-7890-1234", "region": "East", "verified": True, "rating": 4.2, "reviews": []},
            {"name": "Neha Sharma", "service": "Painter", "phone": "6666666666", "aadhaar": "4567-8901-2345", "region": "West", "verified": True, "rating": 3.8, "reviews": []},
        ]

        # Main containers
        self.topbar = tk.Frame(self, height=64, bg=self.theme["secondary"])
        self.topbar.pack(fill='x')
        self.body = tk.Frame(self, bg=self.theme["bg"])
        self.body.pack(fill='both', expand=True)

        self.theme_btn = tk.Button(
            self.topbar, text=self.moon_icon, font=("Arial", 19), width=2, bg=self.theme["primary"], fg="#fff",
            bd=0, cursor="hand2", command=self.toggle_theme, activebackground=self.theme["button_hover"]
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=26, pady=14)
        self.logo = tk.Label(
            self.topbar, text="Shramik Seva", bg=self.theme["secondary"], fg=self.theme["primary"],
            font=("Arial", 22, "bold")
        )
        self.logo.pack(side=tk.LEFT, padx=32)

        # Subscription status label
        self.sub_status_label = tk.Label(
            self.topbar, text="Subscription: None", bg=self.theme["secondary"], fg=self.theme["primary"], font=("Arial", 14, "bold")
        )
        self.sub_status_label.pack(side=tk.RIGHT, padx=10, pady=18)

        self.sections = {}
        self.setup_welcome_section()
        self.show_section("welcome")

    # ------- SECTIONS -------
    def setup_welcome_section(self):
        frame = tk.Frame(self.body, bg=self.theme["bg"])
        self.sections["welcome"] = frame
        title = tk.Label(
            frame, text="WELCOME TO SHRAMIK SEVA", font=("Arial", 39, "bold"),
            bg=self.theme["bg"], fg=self.theme["primary"]
        )
        title.pack(pady=220)
        press_label = tk.Label(
            frame, text="Press any button to skip", font=("Arial", 17),
            bg=self.theme["bg"], fg=self.theme["fg"]
        )
        press_label.pack(pady=12)
        press_label.place_forget()

        def start_fade():
            press_label.place(relx=0.5, y=360, anchor="center")
            self.fade_in_out(press_label, 0, 1)
        def skip(event=None):
            if self.fade_job:
                self.after_cancel(self.fade_job)
            self.show_section("login")
        frame.bind("<Key>", skip)
        frame.bind("<Button>", skip)
        frame.focus_set()
        self.after(2000, start_fade)

    def fade_in_out(self, label, step, direction):
        alpha = int(120+100*(step/12))
        color = f"#{alpha:02x}{alpha:02x}{alpha:02x}"
        label.config(fg=color)
        step = (step+1) % 12
        direction = 1-direction if step == 0 else direction
        self.fade_job = self.after(85, lambda: self.fade_in_out(label, step, direction))

    def setup_login_section(self):
        frame = tk.Frame(self.body, bg=self.theme["bg"])
        self.sections["login"] = frame
        form = tk.Frame(frame, bg=self.theme["card"], padx=72, pady=34, bd=3, relief="groove")
        form.pack(expand=True)
        tk.Label(form, text="Sign in", font=("Arial", 22, "bold"), bg=self.theme["card"], fg=self.theme["fg"]).grid(row=0, columnspan=2, pady=24)
        tk.Label(form, text="Username:", bg=self.theme["card"], fg=self.theme["fg"], font=("Arial",13)).grid(row=1, column=0, sticky="e", pady=8)
        username = tk.Entry(form, font=("Arial",13), bg=self.theme["entry"], fg=self.theme["fg"])
        username.grid(row=1, column=1, pady=8)
        tk.Label(form, text="Password:", bg=self.theme["card"], fg=self.theme["fg"], font=("Arial",13)).grid(row=2, column=0, sticky="e", pady=8)
        password = tk.Entry(form, font=("Arial",13), show="*", bg=self.theme["entry"], fg=self.theme["fg"])
        password.grid(row=2, column=1, pady=8)
        err = tk.Label(form, text="", bg=self.theme["card"], fg="red")
        err.grid(row=3, column=0, columnspan=2)

        def on_enter(e): login()
        username.bind("<Return>", on_enter)
        password.bind("<Return>", on_enter)
        def login():
            user, pw = username.get(), password.get()
            if user == "1" and pw == "1":
                self.current_user = {"role": "client", "username": "1"}
                self.is_employer = False
                self.subscription_plan = None
                self.sub_status_label.config(text="Subscription: None")
                self.show_section("main")
            else:
                err.config(text="Invalid username or password")
        loginbtn = tk.Button(
            form, text="Login", font=("Arial", 12, "bold"), width=22,
            bg=self.theme["primary"], fg="#fff", bd=0, command=login
        )
        loginbtn.grid(row=4, column=0, columnspan=2, pady=22)
        self.add_hover(loginbtn)

    def setup_main_section(self):
        frame = tk.Frame(self.body, bg=self.theme["bg"])
        self.sections["main"] = frame
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=self.theme["bg"], tabmargins=0)
        style.configure('TNotebook.Tab', background=self.theme["card"], foreground=self.theme["fg"], padding=[22, 10], font=("Arial",13,"bold"))
        style.map('TNotebook.Tab', background=[('selected', self.theme["primary"])])
        switch = ttk.Notebook(frame)
        # Hire tab
        hire_tab = self.get_hire_tab(frame)
        switch.add(hire_tab, text="Hire Worker")
        # Employer Tab
        emp_tab = self.get_employer_tab(frame)
        switch.add(emp_tab, text="Employer Plans")
        # Register Tab
        reg_tab = self.get_register_tab(frame)
        switch.add(reg_tab, text="Register Worker")
        # Track Job tab
        track_tab = self.get_track_tab(frame)
        switch.add(track_tab, text="Track Job")
        switch.pack(expand=True, fill='both', pady=42)

    def get_hire_tab(self, frame):
        tab = tk.Frame(frame, bg=self.theme["bg"])
        # Service/region filter bar
        filter_frame = tk.Frame(tab, bg=self.theme["card"])
        filter_frame.pack(fill='x', pady=16)
        tk.Label(filter_frame, text="Filter Services:", font=("Arial",14,"bold"), bg=self.theme["card"], fg=self.theme["fg"]).grid(row=0, column=0)
        service_entry = tk.Entry(filter_frame, font=("Arial",12), width=30, bg=self.theme["entry"], fg=self.theme["fg"])
        service_entry.grid(row=0, column=1, padx=10)
        tk.Label(filter_frame, text="Location:", font=("Arial",14,"bold"), bg=self.theme["card"], fg=self.theme["fg"]).grid(row=0, column=2)
        loc_entry = tk.Entry(filter_frame, font=("Arial",12), width=16, bg=self.theme["entry"], fg=self.theme["fg"])
        loc_entry.grid(row=0, column=3, padx=10)
        search_btn = tk.Button(filter_frame, text="Search", bg=self.theme["primary"], fg="#fff", font=("Arial",12,"bold"),
                               command=lambda: self.populate_workers(tab, service_entry.get(), loc_entry.get()))
        search_btn.grid(row=0, column=4, padx=18)
        self.add_hover(search_btn)

        # Scrollable worker display area
        canvas = tk.Canvas(tab, bg=self.theme["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme["bg"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.worker_display = scrollable_frame

        self.populate_workers(tab, '', '')

        # Reviews section
        review_frame = tk.Frame(tab, bg=self.theme["review_bg"], bd=1, relief="solid")
        review_frame.pack(side=tk.BOTTOM, fill='x', pady=20)
        review_title = tk.Label(review_frame, text="Worker Reviews", font=("Arial",16,"bold"), bg=self.theme["review_bg"], fg=self.theme["review_fg"])
        review_title.pack(pady=5)

        self.reviews_sec = tk.Frame(review_frame, bg=self.theme["review_bg"])
        self.reviews_sec.pack(fill='x', padx=22)
        self.populate_reviews()

        tk.Button(review_frame, text="Add a Review", font=("Arial",13,"bold"), bg=self.theme["primary"], fg="#fff", command=self.add_review_popup).pack(pady=12)
        self.add_hover(review_title)

        return tab

    def populate_reviews(self):
        for child in self.reviews_sec.winfo_children():
            child.destroy()
        for w in self.workers:
            for review in w["reviews"]:
                stars = "★" * review["stars"]
                info = f"{review['review']} ({stars})"
                meta = f"{review['date'].strftime('%d/%m/%Y %H:%M')}"
                tk.Label(self.reviews_sec,
                         text=f"{w['name']}: {info} - {meta}",
                         anchor='w', font=("Arial",12), bg=self.theme["review_bg"], fg=self.theme["review_fg"]).pack(fill='x', pady=2)

    def add_review_popup(self):
        win = tk.Toplevel(self)
        win.title('Add Review')
        win.geometry('400x350')
        win.config(bg=self.theme["card"])

        tk.Label(win, text="Worker Name:", font=("Arial",13), bg=self.theme["card"], fg=self.theme["fg"]).pack(pady=(15,5))
        worker_sel = ttk.Combobox(win, values=[w["name"] for w in self.workers], font=("Arial",13))
        worker_sel.pack(pady=5)

        tk.Label(win, text="Stars:", font=("Arial",13), bg=self.theme["card"], fg=self.theme["fg"]).pack(pady=(15,5))
        star_var = tk.IntVar()
        star_frame = tk.Frame(win, bg=self.theme["card"])
        star_frame.pack(pady=5)
        for i in range(1,6):
            rb = tk.Radiobutton(star_frame, text="★"*i, variable=star_var, value=i, bg=self.theme["card"], fg="#f1c40f", indicatoron=0,
                                font=("Arial",19,"bold"))
            rb.pack(side="left", padx=5)

        tk.Label(win, text="Your review:", font=("Arial",13), bg=self.theme["card"], fg=self.theme["fg"]).pack(pady=(15,5))
        entry = tk.Text(win, font=("Arial",12), width=35, height=5)
        entry.pack(pady=5)

        def submit():
            name = worker_sel.get().strip()
            stars = star_var.get()
            review = entry.get("1.0", tk.END).strip()
            if not name or not stars or not review:
                messagebox.showerror("Error", "Fill all fields.")
                return
            for w in self.workers:
                if w["name"] == name:
                    w["reviews"].append({
                        "stars": stars,
                        "review": review,
                        "date": datetime.now()
                    })
                    nrev = len(w["reviews"])
                    w["rating"] = round((w["rating"]*(nrev-1)+stars)/nrev, 1)
            win.destroy()
            self.populate_reviews()
            self.populate_workers(self.sections["main"].winfo_children()[0], '', '')
            messagebox.showinfo("Done", "Review added!")

        tk.Button(win, text="Submit", command=submit, font=("Arial",14,"bold"),
                  bg=self.theme["primary"], fg="#fff", bd=0).pack(pady=20)
        self.add_hover(win)

    def populate_workers(self, tab, service, region):
        for child in self.worker_display.winfo_children():
            child.destroy()
        for w in self.workers:
            if (not region or w['region'].lower() == region.lower()) and (not service or service.lower() in w['service'].lower()):
                card = tk.Frame(self.worker_display, bg=self.theme["card"], bd=1, relief="ridge", padx=30, pady=10)
                card.pack(fill='x', padx=18, pady=12)
                tk.Label(card, text=w['name'], font=("Arial",17,"bold"), bg=self.theme["card"], fg=self.theme["primary"], anchor="w").grid(row=0, column=0, sticky='w')
                stars_lbl = tk.Label(card, text=star_string(w["rating"]), font=("Arial",16), bg=self.theme["card"], fg="#f1c40f")
                stars_lbl.grid(row=0, column=1, padx=10, sticky='w')
                tk.Label(card, text=w['service'], font=("Arial",14), bg=self.theme["card"], fg=self.theme["fg"]).grid(row=1, column=0, sticky='w')
                tk.Label(card, text=f"Location: {w['region']}", font=("Arial",13), bg=self.theme["card"], fg="#b2b7c2").grid(row=1, column=1, sticky='w', padx=6)
                col = 2
                if w.get("verified"):
                    tk.Label(card, text="✔️ Verified", font=("Arial",12), bg=self.theme["card"], fg='#38e07f').grid(row=2, column=0, sticky='w')
                else:
                    tk.Label(card, text="Unverified", font=("Arial",12), bg=self.theme["card"], fg='#e67e22').grid(row=2, column=0, sticky='w')
                btn_hire = tk.Button(card, text="Hire", font=("Arial",12,"bold"),
                          bg=self.theme["primary"], fg="#fff", width=10, bd=0,
                          command=lambda w=w: self.hire_worker(w))
                btn_hire.grid(row=0, column=col, padx=6, pady=6)
                btn_msg = tk.Button(card, text="Message", font=("Arial",12),
                          bg=self.theme["button"], fg=self.theme["fg"], width=10,
                          command=lambda w=w: self.message_call_warn("Message", w))
                btn_msg.grid(row=1, column=col, padx=6, pady=6)
                btn_call = tk.Button(card, text="Call", font=("Arial",12),
                          bg=self.theme["button"], fg=self.theme["fg"], width=10,
                          command=lambda w=w: self.message_call_warn("Call", w))
                btn_call.grid(row=2, column=col, padx=6, pady=6)
                for b in [btn_hire, btn_msg, btn_call]:
                    self.add_hover(b)

    def hire_worker(self, worker):
        work_id = "SS-" + ''.join(random.choices("0123456789", k=4))
        self.jobs[work_id] = {"worker": worker, "client": self.current_user.get("username"), "status": "Pending"}
        messagebox.showinfo("Job Assigned", f"Worker assigned!\nWork ID: [{work_id}]\nUse Track Job tab to see status.")

    def message_call_warn(self, action, worker):
        if self.is_employer:
            messagebox.showinfo(action, f"{action}ing {worker['phone']}... (simulated)")
        else:
            messagebox.showwarning("Access Denied",
                f"Employer access required for this action.\nCurrent subscription: None")

    def get_employer_tab(self, frame):
        tab = tk.Frame(frame, bg=self.theme["bg"])
        c = tk.Frame(tab, bg=self.theme["bg"], pady=32)
        c.pack(pady=44)
        card_basic = tk.Frame(c, bg=self.theme["card"], width=270, bd=3, relief="groove")
        card_basic.grid(row=0, column=0, padx=28)
        tk.Label(card_basic, text="Basic Access", font=("Arial",18,"bold"), bg=self.theme["card"], fg=self.theme["fg"]).pack(pady=10)
        tk.Label(card_basic, text="₹99/month", font=("Arial",18,"bold"), bg=self.theme["card"], fg="#292929").pack(pady=2)
        features = [
            "Basic Contact Access", "Browse All Worker Profiles",
            "❌ Unverified Worker Contact", "❌ Limited Reviews & Ratings"
        ]
        for feat in features:
            tk.Label(card_basic, text=feat, font=("Arial",11), bg=self.theme["card"], fg=self.theme["fg"]).pack(anchor='w', padx=14)

        btn_basic = tk.Button(card_basic, text="Get Basic Plan", font=("Arial",13,"bold"), bg=self.theme["button"], fg="#222", width=18,
                  command=lambda: self.set_subscription("Basic"))
        btn_basic.pack(pady=20)
        self.add_hover(btn_basic)

        card_premium = tk.Frame(c, bg=self.theme["secondary"], bd=3, relief="groove", highlightbackground="#f1c40f", highlightthickness=3)
        card_premium.grid(row=0, column=1, padx=28)
        tk.Label(card_premium, text="Premium Verified", font=("Arial",18,"bold"), bg=self.theme["secondary"], fg="#25C684").pack(pady=10)
        tk.Label(card_premium, text="₹199/month", font=("Arial",18,"bold"), bg=self.theme["secondary"], fg="#fff").pack(pady=2)
        tk.Label(card_premium, text="Recommended", font=("Arial",12,"bold"), bg="#25C684", fg="#fff").pack(pady=2)
        features = [
            "✔️ Full Direct Communication", "✔️ Access to Verified Workers",
            "✔️ Detailed Ratings & History","✔️ Priority Support"
        ]
        for feat in features:
            tk.Label(card_premium, text=feat, font=("Arial",11), bg=self.theme["secondary"], fg="#eee").pack(anchor='w', padx=14)
        btn_premium = tk.Button(card_premium, text="Subscribe Now", font=("Arial",13,"bold"), bg="#25C684", fg="#fff", width=18,
                  command=lambda: self.set_subscription("Premium Verified"))
        btn_premium.pack(pady=18)
        self.add_hover(btn_premium)
        return tab

    def set_subscription(self, plan):
        self.subscription_plan = plan
        self.is_employer = True
        self.sub_status_label.config(text=f"Subscription: {plan}")
        messagebox.showinfo("Subscribed!", f"You subscribed to {plan}")

    def get_register_tab(self, frame):
        tab = tk.Frame(frame, bg=self.theme["bg"])
        form = tk.Frame(tab, bg=self.theme["card"], padx=32, pady=28, bd=2, relief="groove")
        form.pack(pady=70)
        entries = {}
        for idx, (labeltxt, key) in enumerate([
            ("Name:", "name"), ("Service:", "service"),
            ("Phone Number:", "phone"), ("Aadhaar Number:", "aadhaar"),
            ("Region:", "region")
        ]):
            tk.Label(form, text=labeltxt, font=("Arial",13), bg=self.theme["card"], fg=self.theme["fg"]).grid(row=idx, column=0, sticky='e', pady=9)
            entry = tk.Entry(form, font=("Arial",13), width=26, bg="#fff", fg="#111")
            entry.grid(row=idx, column=1, pady=9, padx=12)
            entries[key] = entry
        verify_done = tk.BooleanVar(value=False)
        def verify():
            phone = entries["phone"].get()
            otp = "1234"
            messagebox.showinfo("OTP", f"Enter OTP sent to {phone}: Use {otp}")
            get_otp = simpledialog.askstring("Phone Verification", "Enter OTP:")
            if get_otp == otp:
                verify_done.set(True)
                messagebox.showinfo("Verified", "Phone number verified!")
            else:
                messagebox.showerror("Failed", "Phone verification failed.")
                verify_done.set(False)
        verify_btn = tk.Button(form, text="Send OTP", font=("Arial",12), bg=self.theme["primary"], fg="#fff", width=14, command=verify)
        verify_btn.grid(row=2, column=2, padx=8)
        self.add_hover(verify_btn)
        def submit():
            if not all(e.get().strip() for e in entries.values()):
                messagebox.showerror("Error", "Please fill all fields.")
                return
            if not verify_done.get():
                messagebox.showerror("Error", "Please verify phone first!")
                return
            self.workers.append({
                k:v.get().strip() for k,v in entries.items()
            } | {'verified': True, "rating": 0, "reviews": []})
            messagebox.showinfo("Success", "Worker Registered!")
            for e in entries.values(): e.delete(0, tk.END)
            verify_done.set(False)
            self.populate_workers(self.sections["main"].winfo_children()[0], '', '')
        reg_btn = tk.Button(form, text="Register", font=("Arial",13,"bold"), bg="#25C684", fg="#fff", width=18, command=submit)
        reg_btn.grid(row=5, columnspan=2, pady=20)
        self.add_hover(reg_btn)
        return tab

    def get_track_tab(self, frame):
        tab = tk.Frame(frame, bg=self.theme["bg"])
        layout = tk.Frame(tab, bg=self.theme["bg"])
        layout.pack(expand=True)
        tk.Label(layout, text="Track Your Job Status", font=("Arial",18,"bold"), bg=self.theme["bg"], fg=self.theme["fg"]).pack(pady=24)
        row = tk.Frame(layout, bg=self.theme["bg"])
        row.pack(pady=8)
        job_entry = tk.Entry(row, font=("Arial",13), width=28, bg="#fff", fg="#111")
        job_entry.pack(side="left", padx=8)
        btn_track = tk.Button(row, text="Track Status", font=("Arial",13,"bold"), bg="#25C684", fg="#fff",
                  command=lambda: self.track_job(job_entry.get()))
        btn_track.pack(side="left")
        self.add_hover(btn_track)
        return tab

    def track_job(self, jobid):
        if jobid in self.jobs:
            job = self.jobs[jobid]
            msg = f"Job Status: {job['status']}\nWorker: {job['worker']['name']}\nClient: {job['client']}"
            messagebox.showinfo("Job Status", msg)
        else:
            messagebox.showerror("Error", "Invalid Job ID.")

    # --------- UTILITIES ----------
    def toggle_theme(self):
        self.theme = LIGHT if self.theme == DARK else DARK
        self.theme_btn.config(text=self.sun_icon if self.theme == LIGHT else self.moon_icon,
                             bg=self.theme["primary"], fg="#fff")
        self.logo.config(bg=self.theme["secondary"], fg=self.theme["primary"])
        self.sub_status_label.config(bg=self.theme["secondary"], fg=self.theme["primary"])
        self.configure(bg=self.theme["bg"])
        for section in self.sections.values():
            section.config(bg=self.theme["bg"])
            for widget in section.winfo_children():
                try:
                    widget.config(bg=self.theme["bg"], fg=self.theme["fg"])
                except:
                    pass
        if hasattr(self, 'sections') and "main" in self.sections and self.sections["main"].winfo_ismapped():
            self.sections["main"].destroy()
            self.setup_main_section()
            self.sections["main"].pack(fill='both', expand=True)

    def add_hover(self, widget):
        bg_normal = widget["bg"]
        def _hover(e):
            widget.config(bg=self.theme["button_hover"])
        def _leave(e):
            widget.config(bg=bg_normal)
        widget.bind("<Enter>", _hover)
        widget.bind("<Leave>", _leave)

    def show_section(self, which):
        if which == "login" and which not in self.sections:
            self.setup_login_section()
        elif which == "main" and which not in self.sections:
            self.setup_main_section()
        for frame in self.sections.values():
            frame.pack_forget()
        self.sections[which].pack(fill='both', expand=True)
        self.sections[which].focus_set()

if __name__ == "__main__":
    app = ShramikSevaApp()
    app.mainloop()
