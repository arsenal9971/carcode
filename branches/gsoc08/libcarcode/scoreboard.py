import widgets

class Scoreboard(widgets.Window):
    def __init__(self,  exitcb = None):
        widgets.Window.__init__(self, "Scoreboard",  pos=(0, 0),  size=(240, 320),  backcolor=(0.2,0.2,0.2, 0.5))
        self.centered = True
        
        self.layout = widgets.Pack(orientation=widgets.VERTICAL,  margin=5,  pos=(0, 0),  size=(240,  320))
        self.scorelayout = widgets.Pack(orientation=widgets.VERTICAL,  margin=5,  pos=(0, 0),  size=(0,  0))
        
        self.btnOk = widgets.Button(widgets.Label("Ok"),  pos=(0, 0),  size=(10,  32))
        self.btnOk.onClick.subscribe(self.exit)
        
        self.layout.add_entity(self.scorelayout)
        self.layout.add_entity(self.btnOk,  expand = False)
        
        self.add_entity(self.layout)
        self.visible = False
        self.scoring = ['D','C',  'B',  'A',  'S',  'Out of rank']
        self.exitcb = exitcb
    
    def exit(self,  btn):
        self.visible = False
        if self.exitcb:
            self.exitcb()
        
    def show_scoring(self,  score_list):
        p = 0.0
        for score in score_list:
            p += score.score()
            lblstr = "%s : %s" % (score.name,   self.scoring[score.score()])
            self.scorelayout.add_entity(widgets.Label(lblstr,  pos=(0, 0),  size=(0, 0)),  expand = False)
        self.visible = True
        p = p / len(score_list)
        lblstr = "Total : %s" % self.scoring[int(p)]
        self.scorelayout.add_entity(widgets.Label(lblstr,  pos=(0, 0),  size=(0, 0)),  expand = True)
