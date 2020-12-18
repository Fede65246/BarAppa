#################################### Set Up ####################################
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem

with open('cred.txt','r') as f:
    classe,nome=f.read().split('\n')


##################################### Main #####################################
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Ordinazioni')
sheet_instance = sheet.get_worksheet(0)


n= sheet_instance.row_values(len(list(filter(None, sheet_instance.col_values(1)))))
   

prices=dict([(n[i],n[i+1]) for i in range(0,len(n),2)])
menu=prices.keys()
def hook(ordi):
    print(ordi)
    sheet_instance.insert_rows([[ordi,classe,nome,time.strftime('%d;%m')]])

KV = '''
BoxLayout:
    orientation: "vertical"
    MDToolbar:
        title: "Menu'"
    BoxLayout:
        ScrollView:
            MDList:
                id: container
        MDLabel:
            id: ordlab
    MDRectangleFlatButton:
        id: ordbut
        text: "          Ordina (0E)          "
        on_release:app.order()
        pos_hint: {"center_x": .5, "center_y": .5}
        text_color: 1, 1, 1, 1
        md_bg_color: 0, 0, 0, 1
'''


class Test(MDApp):
    por=True
    od=[]
    def calbar(self,x):
        if self.por:
            self.root.ids.ordlab.text=x
            self.por=False
        else:
            self.root.ids.ordlab.text+=',\n'+x
        self.od.append(x)
        self.root.ids.ordbut.text="          Ordina ("+str(sum(list(map(lambda x: int(prices[x]),self.od))))+"E)          "
    calba=lambda x,y:lambda z:x.calbar(y)
    
    
    def order(self):
        for i in self.od:
            hook(i)
        self.od=[]
        self.root.ids.ordlab.text='Ordinato'
        
    
    def det(self,n):
        if len(self.od)>0:
            self.od=self.od[:-1]
            self.root.ids.ordlab.text=','.join(self.root.ids.ordlab.text.split(',')[:-1])
            if len(self.od)==0:
                self.por=True
        self.root.ids.ordbut.text="          Ordina ("+str(sum(list(map(lambda x: int(prices[x]),self.od))))+"E)          "
        
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        for i in menu:
            self.root.ids.container.add_widget(OneLineListItem(text=i+' - '+prices[i]+'E',on_release=self.calba(i)))
        self.root.ids.container.add_widget(OneLineListItem(text="Cancella l'ultimo",on_release=self.det))

Test().run()
