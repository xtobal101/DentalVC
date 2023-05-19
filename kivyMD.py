# importing all necessary modules
# like MDApp, MDLabel Screen, MDTextField
# and MDRectangleFlatButton
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton

from kivy.network.urlrequest import UrlRequest

#Next 


# creating Demo Class(base class)
class Demo(MDApp):
    url = "https://3hr2j3gquj.execute-api.us-east-1.amazonaws.com/prod/patients"
 
    def build(self):
        screen = Screen()
                 
        # defining label with all the parameters
        l = MDLabel(text="HI PEOPLE!", halign='center',
                    theme_text_color="Custom",
                    text_color=(0.5, 0, 0.5, 1),
                    font_style='Caption')
         
        # defining Text field with all the parameters
        name = MDTextField(text="Enter name", pos_hint={
                           'center_x': 0.5, 'center_y': 0.8},
                           size_hint_x=None, width=100)
         
        # defining Button with all the parameters
        btn = MDRectangleFlatButton(text="Patients", pos_hint={
                                    'center_x': 0.5, 'center_y': 0.3},
                                    on_release=self.btnfunc)
        # adding widgets to screen
        screen.add_widget(name)
        screen.add_widget(btn)
        screen.add_widget(l)
        # returning the screen
        return screen
 
    # defining a btnfun() for the button to
    # call when clicked on it
    def btnfunc(self, obj):
        req = UrlRequest(self.url, self.got_json) #default Get
         
        print("button is pressed!!")
        #print(f"req {req}") 

    def got_json(self, req, result):
        #for key, value in req.resp_headers.items():
        #    print('{}: {}'.format(key, value))    

        for dictItem  in req.result['patients']:    
            #print(f"Hola tio !!! {item}")    
            for key, value in dictItem.items():
                print('{}: {}'.format(key, value))    


        #print(f"result {req.result}" )    
  
    
if __name__ == "__main__":
    Demo().run()