from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import Clock


Window.size = (350,350)

class MainApp(MDApp):
       
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=30, padding=10)
        self.theme_cls.primary_palette='Green'

        self.balance = MDTextField(pos_hint={'center_x':0.5, 'center_y':0.5}, size_hint=(None,None), width = 100)
        self.increment = MDTextField(pos_hint={'center_x':0.5, 'center_y':0.5}, size_hint=(None,None), width = 100)        
        button = MDRectangleFlatButton(text='Submit',
                                pos_hint={'center_x':0.5, 'center_y':0.5},
                                on_release = self.release)           
        self.result = MDLabel()  

        layout.add_widget(self.balance)
        layout.add_widget(self.increment)
        layout.add_widget(button)
        layout.add_widget(self.result)

        return layout


    def release(self, obj):
        """Casts the balance to a position variable
            and calls on the calculate function every second.
            """
        self.position = self.balance.text
        Clock.schedule_interval(self.calculate, 1)
    
    
    def calculate(self, obj): 
        """Takes the position variable and increments it by the increment variable 
            and then updates the result label. 
            This function is run every second"""
        if self.position:
            self.position = str( int(self.position) + int(self.increment.text) ) 
            self.result.text = 'Result is : ' + str(self.position)


if __name__ == '__main__':
    MainApp().run()            
