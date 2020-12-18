#################################### Set Up ####################################
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
tod=time.strftime('%d;%m')

alph=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'z']

##################################### Main #####################################
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Ordinazioni')
sheet_instance = sheet.get_worksheet(0)

datefilter=lambda x:(x[3]==tod)
classorter=lambda x: int(x[1][0])*100+alph.index(x[1][1])

u=sheet_instance.get_all_values()
u=list(filter(datefilter,u))
u.sort(key=classorter)

def lin(x):
    a,b,c=x[:3]
    return a+' '*(10-len(a))+'; '+b+' ; '+c+' '*(20-len(c))

with open('ordinazioni_di_oggi.txt','w') as f:
    f.write('\n'.join(list(map(lin,u))))