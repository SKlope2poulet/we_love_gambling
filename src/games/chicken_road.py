import tkinter as tk
import random

# === Thème ===
BG_TOP = "#0b1220"
BG_BOTTOM = "#101a33"
GLASS_A = "#1f2a44"
GLASS_B = "#263352"
GLASS_BRD = "#131b2f"
NEON = "#7cf77c"
NEON_ALT = "#9cc6ff"
DANGER = "#ff5c5c"
GOLD = "#f7d774"
TEXT = "#e8eefb"

def lerp(a,b,t): return a+(b-a)*t
def gradient_background(canvas,w,h,top=BG_TOP,bottom=BG_BOTTOM,steps=60):
    canvas.delete("bggrad")
    rt,gt,bt = canvas.winfo_rgb(top)
    rb,gb,bb = canvas.winfo_rgb(bottom)
    for i in range(steps):
        t=i/(steps-1)
        r=int(lerp(rt,rb,t))>>8; g=int(lerp(gt,gb,t))>>8; b=int(lerp(bt,bb,t))>>8
        color=f"#{r:02x}{g:02x}{b:02x}"
        y1=int(lerp(0,h,t)); y2=int(lerp(0,h,(i+1)/steps))
        canvas.create_rectangle(0,y1,w,y2,outline="",fill=color,tags="bggrad")

def draw_tile(canvas,x1,y1,x2,y2,on=False):
    base=GLASS_B if on else GLASS_A
    canvas.create_rectangle(x1,y1,x2,y2,outline=GLASS_BRD,fill=base,width=2,tags="board")
    if on: canvas.create_rectangle(x1+1,y1+1,x2-1,y2-1,outline=NEON,width=2,tags="board")

def glow_text(canvas,x,y,text,color,size):
    canvas.create_text(x,y,text=text,fill=color,font=("Segoe UI",size,"bold"))

class NeonButton(tk.Canvas):
    def __init__(self,master,text,cmd,w=120,color=NEON):
        super().__init__(master,width=w,height=34,bg=master["bg"],highlightthickness=0)
        self.cmd=cmd; self.color=color
        self.rect=self.create_rectangle(2,2,w-2,32,outline=color,fill="#1a233b",width=2)
        self.txt=self.create_text(w//2,17,text=text,fill=TEXT,font=("Segoe UI",10,"bold"))
        self.bind("<Button-1>",lambda e:self.fire())
        self.bind("<Enter>",lambda e:self.itemconfigure(self.rect,fill="#1f2a44"))
        self.bind("<Leave>",lambda e:self.itemconfigure(self.rect,fill="#1a233b"))
    def fire(self):
        self.itemconfigure(self.rect,fill="#253151")
        self.after(120,lambda:self.itemconfigure(self.rect,fill="#1a233b"))
        if callable(self.cmd): self.cmd()

class ChickenRoad:
    # ⬇️ petit ajout: portfolio optionnel
    def __init__(self, root, portfolio=None):
        self.cols=11; self.visible_cols=self.cols
        self.tile=110; self.padding=14
        self.board_w=self.visible_cols*self.tile; self.board_h=self.tile
        # ⬇️ si un portefeuille est fourni, on initialise avec son solde
        self.portfolio = portfolio
        self.balance = (portfolio.balance if portfolio and hasattr(portfolio, "balance") else 100.0)
        self.bet=0.0
        self.player_col=0; self.playing=False; self.win=False; self.lose=False
        self.difficulty="Facile"; self.multipliers=self._generate_mults()
        self.losing_cell=None
        self.last_win=None

        root.title("🐔 Chicken Road — Realistic Casino Probabilities")
        root.configure(bg=BG_BOTTOM)
        self.canvas=tk.Canvas(root,width=self.board_w+self.padding*2,height=self.board_h+self.padding*2,
                              bg=BG_BOTTOM,highlightthickness=0)
        self.canvas.pack(padx=10,pady=10)
        self.info=tk.Label(root,text="",fg=NEON_ALT,bg=BG_BOTTOM,font=("Segoe UI",11))
        self.info.pack(pady=(0,4))
        self.last_lbl=tk.Label(root,text="Dernier gain : —",fg=GOLD,bg=BG_BOTTOM,font=("Segoe UI",10))
        self.last_lbl.pack(pady=(0,8))
        ctrl=tk.Frame(root,bg=BG_BOTTOM); ctrl.pack(pady=5)
        self.bet_entry=tk.Entry(ctrl,width=8,font=("Segoe UI",12),bg="#18223b",fg=TEXT,insertbackground=TEXT)
        self.bet_entry.insert(0,"10"); self.bet_entry.grid(row=0,column=0,padx=5)
        NeonButton(ctrl,"Miser",self.place_bet).grid(row=0,column=1,padx=4)
        NeonButton(ctrl,"➡ Avancer",self.advance).grid(row=0,column=2,padx=4)
        NeonButton(ctrl,"🔥 Difficulté",self.toggle_difficulty,color=NEON_ALT).grid(row=0,column=3,padx=4)
        NeonButton(ctrl,"💸 Cash-Out",self.cash_out,color=GOLD).grid(row=0,column=4,padx=4)
        NeonButton(ctrl,"🔁 Rejouer",self.reset_game,color=DANGER).grid(row=0,column=5,padx=4)
        self.update_info(); self.redraw_all()

    # ⬇️ synchro portefeuille, appelée dans update_info()
    def sync_portfolio(self):
        if self.portfolio and hasattr(self.portfolio, "balance"):
            self.portfolio.balance = self.balance
            if hasattr(self.portfolio, "update_display"):
                self.portfolio.update_display()

    # === logique ===
    def _risk_fixed(self): return 0.4 if self.difficulty=="Facile" else 0.6
    def _realistic_loss_chance(self):
        base=self._risk_fixed()
        progress=self.player_col/(self.cols-2)
        curve=base*0.5 + base*progress
        return min(0.95,max(0.05,curve+random.uniform(-0.08,0.08)))

    def _generate_mults(self):
        m=[]
        for c in range(self.cols):
            if c==0: m.append(1.00)
            else:
                base=1.1+(c/(self.cols-1))*(4.0-1.1)
                if self.difficulty=="Difficile": base*=1.35
                m.append(round(base+random.uniform(-0.08,0.08),2))
        return m

    def update_info(self):
        cur=self.multipliers[self.player_col]; risk=int(self._risk_fixed()*100)
        self.info.config(text=f"Mode: {self.difficulty} • Risque moyen: {risk}% • Solde: {self.balance:.2f}€ • Mise: {self.bet:.2f}€ • x{cur}")
        # ⬇️ pousse la valeur vers l'UI principale
        self.sync_portfolio()

    def reset_game(self):
        self.player_col=0; self.playing=False; self.win=self.lose=False
        self.losing_cell=None; self.multipliers=self._generate_mults()
        self.update_info(); self.redraw_all()

    def place_bet(self):
        self.reset_game()
        try:
            a=float(self.bet_entry.get())
            if a<=0 or a>self.balance: raise ValueError
            self.bet=a; self.balance-=a; self.playing=True
            self.update_info(); self.flash("💰 Mise placée",NEON_ALT)
        except: self.flash("⚠ Mise invalide",DANGER)

    def toggle_difficulty(self):
        self.difficulty="Difficile" if self.difficulty=="Facile" else "Facile"
        self.multipliers=self._generate_mults()
        self.update_info(); self.flash(f"Mode {self.difficulty}",NEON_ALT)
        self.redraw_all()

    def advance(self):
        if not self.playing or self.lose or self.win: return
        self.player_col+=1
        if self.player_col>=self.cols-2: self.victory(); return
        if random.random()<self._realistic_loss_chance(): self.defeat(); return
        self.update_info(); self.redraw_all()

    def cash_out(self):
        if not self.playing or self.lose or self.win or self.bet<=0: return
        cur=self.multipliers[self.player_col]; gain=round(self.bet*cur,2)
        self.balance+=gain; self.bet=0.0; self.playing=False
        self.last_win=f"+{gain:.2f}€ (x{cur}) — {self.difficulty}"
        self.last_lbl.config(text=f"Dernier gain : {self.last_win}")
        self.update_info(); self.animate_cash(gain,cur)
        self.losing_cell=self._predict_loss_cell()
        self.redraw_all(); self.canvas.after(1200,self.hide_loss)

    def _predict_loss_cell(self):
        for c in range(self.player_col+1,self.cols-1):
            if random.random()<self._realistic_loss_chance():
                return c
        return None

    def hide_loss(self): self.losing_cell=None; self.redraw_all()

    def victory(self):
        cur=self.multipliers[self.player_col]; gain=round(self.bet*cur,2)
        self.balance+=gain; self.bet=0.0; self.playing=False
        self.last_win=f"+{gain:.2f}€ (x{cur}) — {self.difficulty}"
        self.last_lbl.config(text=f"Dernier gain : {self.last_win}")
        self.update_info(); self.animate_banner("🎉 VICTOIRE 🎉",NEON)

    def defeat(self):
        self.lose=True; self.bet=0.0; self.playing=False
        self.last_lbl.config(text="Dernier gain : PERDU 💀")
        self.update_info(); self.animate_defeat()

    # === animations ===
    def animate_cash(self,gain,mult):
        x=self.padding+self.board_w//2; y=self.padding+self.board_h//2
        tid=self.canvas.create_text(x,y,text=f"💸 +{gain:.2f}€ (x{mult})",fill=GOLD,font=("Segoe UI",20,"bold"))
        def step(i=0):
            if i>=20: self.canvas.delete(tid); return
            self.canvas.move(tid,0,-5)
            self.canvas.after(30,lambda:step(i+1))
        step()

    def animate_banner(self,text,color):
        x=self.padding+self.board_w//2; y=self.padding+self.board_h//2
        tid=self.canvas.create_text(x,y,text=text,fill=color,font=("Segoe UI",26,"bold"))
        def blink(i=0):
            if i>=6: self.canvas.delete(tid); return
            self.canvas.itemconfigure(tid,state="hidden" if i%2 else "normal")
            self.canvas.after(180,lambda:blink(i+1))
        blink()

    def animate_defeat(self):
        x=self.padding+self.board_w//2; y=self.padding+self.board_h//2
        tid=self.canvas.create_text(x,y,text="💀",fill=DANGER,font=("Segoe UI",42,"bold"))
        def pulse(i=0):
            if i>=10: self.canvas.delete(tid); return
            self.canvas.scale(tid,x,y,1.15,1.15)
            self.canvas.after(100,lambda:pulse(i+1))
        pulse()

    def flash(self,text,color):
        tid=self.canvas.create_text(self.padding+self.board_w//2,self.padding-15,
                                    text=text,fill=color,font=("Segoe UI",11,"bold"))
        self.canvas.after(1000,lambda:self.canvas.delete(tid))

    # === dessin ===
    def redraw_all(self):
        self.canvas.delete("all")
        w=self.board_w+self.padding*2; h=self.board_h+self.padding*2
        gradient_background(self.canvas,w,h)
        bx1,by1=self.padding,self.padding; bx2,by2=bx1+self.board_w,by1+self.board_h
        self.canvas.create_rectangle(bx1,by1,bx2,by2,outline="#0f1528",fill="#0f162b")
        for c in range(self.visible_cols):
            x1=self.padding+c*self.tile; x2=x1+self.tile; y1=self.padding; y2=y1+self.tile
            draw_tile(self.canvas,x1,y1,x2,y2,on=(c==self.player_col))
            val=self.multipliers[c]; col=NEON_ALT if c==self.player_col else TEXT
            glow_text(self.canvas,(x1+x2)//2,(y1+y2)//2,f"x{val}",col,13)
            if self.losing_cell==c:
                glow_text(self.canvas,(x1+x2)//2,(y1+y2)//2,"💀",DANGER,22)
        self.draw_chicken()

    def draw_chicken(self):
        c=self.player_col; x=self.padding+c*self.tile+self.tile//2; y=self.padding+self.tile//2; r=self.tile//3
        self.canvas.create_oval(x-r,y-r,x+r,y+r,fill=GOLD if not self.lose else "#777777",outline="#000")
        self.canvas.create_oval(x-8,y-r-6,x-2,y-r,fill=DANGER,outline="")
        self.canvas.create_oval(x+2,y-r-6,x+8,y-r,fill=DANGER,outline="")
        self.canvas.create_polygon(x+r-4,y,x+r+6,y+2,x+r-4,y+4,fill="#ffae42",outline="#000")

# === Helper pour l’intégration à l’UI principale ===
def launch_chicken_road(parent, portfolio):
    """Ouvre Chicken Road dans une fenêtre enfant, avec synchro de solde."""
    top = tk.Toplevel(parent)
    ChickenRoad(top, portfolio=portfolio)
    return top

# === Main standalone (dev local) ===
if __name__=="__main__":
    root=tk.Tk()
    app=ChickenRoad(root)
    root.mainloop()
