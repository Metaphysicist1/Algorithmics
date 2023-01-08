###################################################################

#სტეკის შესახებ:
    # მონაცემთა სტრუქტურა, რომელშიც ბოლოს შენახული ელემენტი პირველი გამოიტანება
    # ჩვენს კოდში ცალკე სტეკი არ შეგვიქმნია, არამედ გამოვიყენეთ სია - list და ვიმუშავეთ მის ბოლო ელემენტზე 
    # ვისაც არ ახსოვს [-1] არის უარყოფით ინდექსაცია და იღებს სიის ბოლო ელემენტს

#lambda შესახებ:
    # ფუნქციონალური დაპროგრამების ელემენტი
    # ლამბდა-ს მეშვეობით ვქმნით და ვიყენებთ ანონიმურ ფუნქციებს რომლებიც 
    # ანონიმურია ფუნქცია რომელიც იქვე გამოიყენება და არ ინახება მეხსიერებაში 
    
    
###################################################################
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui_calc_2023 import Ui_MainWindow
import operator # ამ ბიბლიოთეკაში გვაქვს მათემატიკური ოპერაციები 
                # ეს ოპერაციები +-/* add,sub,mul,truediv სიტყვიერი ოპერატორების სახით


READY = 0
INPUT = 1

class MyWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setupUi(self)
        
        for number in range(0, 10): # ბევრი რომ არ ვწეროთ დავატრიალოთ ციკლი
            # ქვემოთ მოცემული ბრძანებით ვააქტიურებთ მოვლენებს events
            # რიცხვი ღილაკზე დაჭერისას ეკრანზე გამოიტანება რიცხვი
            # lambda შესახებ  წაიკითხე ზემოთ
            getattr(self, 'num%s' % number).pressed.connect(lambda v=number:self.input_num(v))
            # ამ შემთხვევაში ვიყენებთ ლამბდას რომ გადავცეთ რიცხვი პარამეტრად connect ფუნქციას

        self.add.clicked.connect(lambda:self.operation(operator.add))
        self.subst.clicked.connect(lambda:self.operation(operator.sub))
        self.mult.clicked.connect(lambda:self.operation(operator.mul))
        self.divide.clicked.connect(lambda:self.operation(operator.truediv))
        
        self.equal.clicked.connect(self.equals)
        self.clear.clicked.connect(self.reset)
        
        self.reset() # დეფაულტად პარამეტრების მინიჭება 
        self.show() # ეკრანის ჩვენება
        
        
    def display(self): # პასუხის ფანჯარა
        # stack შესახებ წაიკითხე სულ სულ ზემოთ 
        self.lcd.display(self.stack[-1]) # პასუხის ფანჯარაზე გაჩნდეს ბოლო დამატებული რიცხვი
    
    def reset(self): # პროგრამის გამშვები საწყისი ფუნქცია
        self.state=READY #
        self.stack = [0] # სტეკის შექმნა და დეფაულტად ნულის შეყვანა 
        self.last_operation = None
        self.current_operation = None
        self.display()
        
    
    def input_num(self,num):  # რიცხვის  შეყვანის ფუნქცია
        if self.state == READY:
            self.state = INPUT
            self.stack[-1] = num #  სიაში [სტეკში] ვამატებთ შეყვანილ რიცხვს
        else:
            # ქვემოთ: ციფრების მიწებებება -  შეგყავს 4 მერე 9, გამოდის 49 იგივე 4 * 10 + 9
            self.stack[-1] = self.stack[-1] * 10 + num #  სიაში [სტეკში] ვამატებთ იმას რაც მივიღეთ
        
        # ქვედა გამოიძახება მიუხედავად იმისა if შესრულდება თუ else
        self.display() #იძახებს ფუნქციას რომ გაანახლოს ეკრანი და გვაჩვენოს ბოლო შეყვანილი რიცხვი
    
    def operation(self,op):
        print("-------- operation")
        # ქვემოთ if სრულდება ყველა შემთხვევაში როცა არ არის false და None 
        # if self.current_operation: #  # current_operation ის შემოწმება, მნიშვნელობის ქონაზე
        #     self.equals() # სრულდება გამოთვლა თუ current_operation არ არის ცარიელი
        
        self.stack.append(0) 
        self.state=INPUT
        self.current_operation = op
        
    def equals(self):
        
        # ქვედა IF ში სრულდება ოპერაცია თუ რაიმეს გამოვთვლით 
        # და მეორეჯერ დავაწკაპუნეთ ტოლობის ნიშანს ოპერაცია გამეორდება
        if self.state==READY and self.last_operation: # თუ უკვე მინიმუმ ერთხელ შესრულდა ტოლობა
            #ქვემოთ:  წინა ოპერაცია ხდება ახლად შესრულებელი ბრძანება
            s,self.current_operation = self.last_operation # ზედმეტად დავაჭერთ ტოლობას ზედმეტად შესრულდება წინა მოქმედება
            self.stack.append(s) # 
           
            
        if self.current_operation: 
            self.last_operation = self.stack[-1], self.current_operation # ბოლო ოპერაცია ხ
            try:
                #ქვემოთ გამოთვლას ასრულებს operator მოდულის ფუნქციები და რასააც პარამეტრად ჩავუსვამთ იმას ითვლის
                self.stack = [self.current_operation(*self.stack)] #ბოლო ელემენტი ხდება გამოთვლის შედეგი
                
            except Exception: #გამონაკლისები
                self.lcd.display("Error") # შეცდომას დაგვიწერს მაგ: ნულზე გაყოფა
                self.stack=[0] # ნულდება ეკრანი
            else: # წინააღმდეგ შემთხვევაში
                self.current_operation =None # ოპერაცია ამჟამად არ გვაქვს რადგან შევასრულეთ ტოლობა
                self.state=READY # ავღნიშნეთ რომ ტოლობა შესრულდა
                self.display() # გამოტანა
            
            
app = QApplication([])
window = MyWindow()

app.exec_()