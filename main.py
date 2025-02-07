import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from datetime import datetime
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.lang import Builder
import random
import smtplib
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from kivy.graphics import Color, Rectangle, RoundedRectangle
import os
from kivy.properties import StringProperty

# ✅ Get the correct path for assets
def get_asset_path(filename):
    return os.path.join(os.path.dirname(__file__), 'assests', 'Images', filename)


class BreedingPigCardMenu(BoxLayout):
    def __init__(self, pig_data, **kwargs):
        super().__init__(orientation='horizontal', padding=10, spacing=10, size_hint_y=None, height=100, **kwargs)

        if not isinstance(pig_data, dict):
            raise ValueError(f"Expected dictionary, got {type(pig_data)}")

        # Extracting values safely
        male_pig_id = pig_data.get('Male_Pig_ID', "Unknown")
        female_pig_id = pig_data.get('Female_Pig_ID', "Unknown")
        cage_desc = pig_data.get('Cage_Desc', "Not available")
        status = pig_data.get('Status', "Unknown")

        # Card background styling
        with self.canvas.before:
            Color(0.85, 0.85, 0.85, 1)
            self.shadow_rect = RoundedRectangle(radius=[20], pos=(self.pos[0] + 5, self.pos[1] - 5), size=self.size)
            
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Pig image and status layout
        pig_image_layout = BoxLayout(orientation='vertical', size_hint_x=None, width=90)

    
       # Use a relative image path for the pig image
        pig_image_path = get_asset_path('lists.jpg')

        # Check if the image exists
        if not os.path.exists(pig_image_path):
            print(f"Warning: Image '{pig_image_path}' not found!")  # Debugging message

        # Create the image widget with the relative path
        pig_image = Image(source=pig_image_path, size_hint=(None, None), size=(60, 60))
        pig_image_layout.add_widget(pig_image)
        pig_status = Label(text=f"Status: {pig_data.get('Breeding_Status', 'Unknown')}", color=(0, 0, 0, 1), font_size=14)
        pig_image_layout.add_widget(pig_status)

        self.add_widget(pig_image_layout)

        # Details layout
        details_layout = BoxLayout(orientation='vertical')
        details_layout.add_widget(Label(text=f"[b]Male Pig ID:[/b] {male_pig_id}", markup=True, color=(0, 0, 0, 1), font_size=16))
        details_layout.add_widget(Label(text=f"[b]Female Pig ID:[/b] {female_pig_id}", markup=True, color=(0, 0, 0, 1), font_size=16))

        self.add_widget(details_layout)

        # Cage information layout
        cage_layout = BoxLayout(orientation='vertical', size_hint_x=None, width=120)
        cage_label = Label(text=f"[color=ff0000]{cage_desc}[/color]", markup=True, font_size=16)
        cage_layout.add_widget(cage_label)

        self.add_widget(cage_layout)

        # Button for more information (action to be added)
        more_info_button = Button(text=">", size_hint_x=0.2, background_normal='', background_down='', color=(0, 0, 0, 1))
        self.add_widget(more_info_button)

    def update_rect(self, *args):
        self.shadow_rect.pos = (self.pos[0] + 5, self.pos[1] - 5)
        self.shadow_rect.size = self.size
        self.rect.pos = self.pos
        self.rect.size = self.size

class PigCard(BoxLayout):
    def __init__(self, pig_data, **kwargs):
        super().__init__(orientation='horizontal', padding=10, spacing=10, size_hint_y=None, height=100, **kwargs)

        if not isinstance(pig_data, dict):
            raise ValueError(f"Expected dictionary, got {type(pig_data)}")

        age = pig_data.get('Age', "Age not available")
        weight = pig_data.get('Weight', "Weight not available")
        vaccination_status = pig_data.get('VaccinationStatus', "Vaccination status unknown")
        birthdate = pig_data.get('Birthdate', "Not available")
        gender = pig_data.get('Gender', "Unknown")
        classification = pig_data.get('Classification', "Unknown")
        cage_no = pig_data.get('CageNo', "Not available")
        pig_id = pig_data.get('Pig_ID', "Unknown")

        age_text = f"{age} months old" if age is not None else "0 months old"
        weight_text = f"{weight} kg" if weight is not None else "Weight not available"

        with self.canvas.before:
            Color(0.85, 0.85, 0.85, 1)
            self.shadow_rect = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

        pig_image_layout = BoxLayout(orientation='vertical', size_hint_x=None, width=90)
        # Use a relative image path for the pig image
        pig_image_path = get_asset_path('lists.jpg')

        # Check if the image exists
        if not os.path.exists(pig_image_path):
            print(f"Warning: Image '{pig_image_path}' not found!")  # Debugging message

        # Create the image widget with the relative path
        pig_image = Image(source=pig_image_path, size_hint=(None, None), size=(60, 60))
        pig_image_layout.add_widget(pig_image)
        pig_status = Label(text=f"Status: {pig_data.get('Status', 'Unknown')}", color=(0, 0, 0, 1), font_size=14)
        pig_image_layout.add_widget(pig_status)

        self.add_widget(pig_image_layout)

        details_layout = BoxLayout(orientation='vertical')
        details_layout.add_widget(Label(text=f"[b]Pig ID:[/b] {pig_id}", markup=True, color=(0, 0, 0, 1), font_size=16))
        details_layout.add_widget(Label(text=f"{gender} - {classification}", color=(0, 0, 0, 1), font_size=16))
        details_layout.add_widget(Label(text=f"{birthdate} | {weight_text}", color=(0, 0, 0, 1), font_size=16))

        self.add_widget(details_layout)

        cage_vaccination_layout = BoxLayout(orientation='vertical', size_hint_x=None, width=85, padding=[-10, 0, 0, 0])
        badge = Label(text=f"[color=ff0000]CAGE {cage_no}[/color]", halign="left", markup=True, font_size=16)
        cage_vaccination_layout.add_widget(badge)

        vaccination_status_label = Label(text=f"{vaccination_status}", markup=True, color=(0, 0, 0, 1), font_size=16, halign="left", valign="top", size_hint_x=None, width=120)
        vaccination_status_label.bind(texture_size=vaccination_status_label.setter('size'))
        cage_vaccination_layout.add_widget(vaccination_status_label)

        age_label = Label(text=f"{age_text}", markup=True, color=(0, 0, 0, 1), font_size=16, halign="left")
        cage_vaccination_layout.add_widget(age_label)

        self.add_widget(cage_vaccination_layout)

        more_info_button = Button(text=">", size_hint_x=0.2, background_normal='', background_down='', color=(0, 0, 0, 1))
        more_info_button.bind(on_release=self.open_addpig)
        self.add_widget(more_info_button)

    def update_rect(self, *args):
        self.shadow_rect.pos = self.pos
        self.shadow_rect.size = self.size
        self.rect.pos = self.pos
        self.rect.size = self.size

    def open_addpig(self, instance):
        app = App.get_running_app()
        app.root.current = "addpig"

class PigCardMonitoringMenu(BoxLayout):
    def __init__(self, pig_data, **kwargs):
        super().__init__(orientation='horizontal', padding=10, spacing=10, size_hint_y=None, height=100, **kwargs)

        # Add shadow effect
        with self.canvas.before:
            Color(0, 0, 0, 0.2)  # Shadow color (black with some transparency)
            self.shadow_rect = RoundedRectangle(pos=(self.x + 2, self.y - 5), size=(self.width - 4, self.height / 6))

        self.bind(pos=self.update_shadow, size=self.update_shadow)

        # Card background color
        with self.canvas.before:
            Color(0.917, 0.553, 0.561, 1)  # Card color
            self.rect = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

        # Add image to the card
        pig_image_layout = BoxLayout(orientation='vertical', size_hint_x=None, width=90)
        pig_image = Image(source=pig_data['image'], size_hint=(None, None), size=(70, 70), pos_hint={"center_y": 0.7})
        pig_image_layout.add_widget(pig_image)
        self.add_widget(pig_image_layout)

        # Button for displaying the pig's label
        pig_button = Button(
            text=pig_data.get('label', 'Lists of Pigs'),
            size_hint=(None, None),
            size=(250, 40),
            pos_hint={"right": 1.1, "center_y": 0.5},
            halign="center",
            bold=True,
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )

        pig_button.bind(on_press=self.on_button_press)
        self.add_widget(pig_button)

        # Add a more info button as well
        more_info_button = Button(
            text="",
            size_hint_x=0.2,
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
            bold=True
        )
        self.add_widget(more_info_button)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_shadow(self, *args):
        self.shadow_rect.pos = (self.x + 2, self.y - 5)
        self.shadow_rect.size = (self.width - 4, self.height / 6)

    def on_button_press(self, instance):
        app = App.get_running_app()
        if instance.text == "Lists of Pigs":
            app.root.current = 'monitoring'  # Switch to the monitoring screen
        elif instance.text == "Breeding":
            app.root.current = 'breedingmenu'  # Switch to the breeding screen

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(size=self.layout.size, pos=self.layout.pos)
            Color(1, 0.9, 0.9, 1)
            self.circle1 = Ellipse(pos=(-50, self.layout.height - 150), size=(150, 150))
            self.circle2 = Ellipse(pos=(50, self.layout.height - 100), size=(150, 150))

        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        # Create a centered box for the login form
        box_container = BoxLayout(orientation='vertical', padding=20, spacing=20,
                                  size_hint=(None, None), size=(350, 300),
                                  pos_hint={'center_x': 0.5, 'center_y': 0.35})

       # Use a relative image path for logo
        image_path = get_asset_path('LOGOcolored.png')
        if not os.path.exists(image_path):
            print(f"Warning: Image '{image_path}' not found!")  # Debugging message
        image = Image(source=image_path, size_hint=(0.5, 0.3), pos_hint={'center_x': 0.5, 'top': 0.95})
        self.layout.add_widget(image)


        with box_container.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.rect_box = RoundedRectangle(size=box_container.size, pos=box_container.pos, radius=[20])
        box_container.bind(size=self.update_box_rect, pos=self.update_box_rect)

        self.username_input = TextInput(hint_text="Username", multiline=False, size_hint_y=None, height=50,
                                        foreground_color=(0, 0, 0, 1), background_color=(1, 1, 1, 1))
        box_container.add_widget(self.username_input)

        self.password_input = TextInput(hint_text="Password", password=True, multiline=False,
                                        size_hint_y=None, height=50,
                                        foreground_color=(0, 0, 0, 1), background_color=(1, 1, 1, 1))
        box_container.add_widget(self.password_input)

        forgot_password_button = Button(
            text="Forgot Password?",
            size_hint=(None, None),
            size=(150, 30),
            color=(0, 0, 0, 1),
            bold=False,
            background_normal='',
            background_down='',
            border=[0, 0, 0, 0],
            background_color=(0.9, 0.9, 0.9, 1),
            pos_hint={'x': 0.05, 'top': 0.88}
        )
        forgot_password_button.bind(on_press=self.forgot_password)
        box_container.add_widget(forgot_password_button)

        login_button = Button(text="Login", size_hint_y=None, height=50, color=(1, 1, 1, 1))
        login_button.background_normal = ''
        login_button.background_color = (0, 0, 0, 0)

        with login_button.canvas.before:
            Color(234 / 255, 141 / 255, 143 / 255, 1)
            self.rect_button = RoundedRectangle(size=login_button.size, pos=login_button.pos, radius=[25])
        login_button.bind(size=self.update_button_rect, pos=self.update_button_rect)

        login_button.bind(on_press=self.login)
        box_container.add_widget(login_button)
        self.layout.add_widget(box_container)
        self.add_widget(self.layout)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        self.circle1.pos = (-50, instance.height - 150)
        self.circle2.pos = (50, instance.height - 100)

    def update_box_rect(self, instance, value):
        self.rect_box.pos = instance.pos
        self.rect_box.size = instance.size

    def update_button_rect(self, instance, value):
        self.rect_button.pos = instance.pos
        self.rect_button.size = instance.size

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

         # Temporary bypass for admin login
        if username == "admin" and password == "admin123":
            self.show_popup("Login successful", "Welcome, Admin!")
            self.manager.current = 'monitoringmenu'
            return  # Skip the API request

        url = "http://127.0.0.1:5000/login"
        payload = {"username": username, "password": password}

        # url = "http://127.0.0.1:5000/login"
        # payload = {"username": username, "password": password}
        # try:
        #     response = requests.post(url, json=payload)
        #     if response.status_code == 200:
        #         self.show_popup("Login successful", "Welcome to the system!")
        #         self.manager.current = 'monitoringmenu'
        #     else:
        #         self.show_popup("Login failed", response.json().get('error', 'Unknown error'))
        # except requests.exceptions.RequestException as e:
        #     self.show_popup("Error", f"Failed to connect to the server: {str(e)}")

    def forgot_password(self, instance):
            self.manager.current = 'forgotpass'  # Switch to the ForgotPassword screen

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10)
        label = Label(text=message, color=(0, 0, 0, 1))
        content.add_widget(label)
        button = Button(text="Close", size_hint_y=None, height=50)
        button.bind(on_press=lambda x: self.close_popup())
        content.add_widget(button)
        self.popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))
        self.popup.open()

    def close_popup(self):
        self.popup.dismiss()

class MonitoringMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root_layout = BoxLayout(orientation='vertical', padding=[10, 20, 10, 10])

        header = BoxLayout(size_hint_y=None, height=60, padding=10)
        # Use a relative image path for the back button
        back_button = Image(source=get_asset_path('BACKK.png'), size_hint=(None, None), size=(30, 30))
        back_button.bind(on_touch_down=self.on_back_button_press)
        header.add_widget(back_button)

        header.add_widget(Label(text="[b]Monitoring[/b]", font_size=24, color=(0, 0, 0, 1), markup=True))

       # Use a relative image path for the search button
        search_button = Image(source=get_asset_path('search.png'), size_hint=(None, None), size=(60, 60))
        search_button.bind(on_touch_down=self.on_search_button_press)
        header.add_widget(search_button)

        self.root_layout.add_widget(header)

        with self.root_layout.canvas.before:
            Color(0.933, 0.933, 0.933, 1)
            self.root_layout.rect = RoundedRectangle(pos=self.root_layout.pos, size=self.root_layout.size)
        self.root_layout.bind(pos=lambda _, pos: setattr(self.root_layout.rect, 'pos', pos),
                              size=lambda _, size: setattr(self.root_layout.rect, 'size', size))

        scroll = ScrollView()
        pig_list = GridLayout(cols=1, size_hint_y=None, spacing=15, padding=[15, 15])
        pig_list.bind(minimum_height=pig_list.setter('height'))

       # Sample data with relative image paths
        sample_data = [
            {'id': '001', 'image': get_asset_path('lists.jpg'), 'label': 'Lists of Pigs'},
            {'id': '002', 'image': get_asset_path('breeding.jpg'), 'label': 'Breeding'},
        ]
        for pig in sample_data:
            pig_list.add_widget(PigCardMonitoringMenu(pig))

        scroll.add_widget(pig_list)
        self.root_layout.add_widget(scroll)
        self.add_widget(self.root_layout)

    def on_back_button_press(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.manager.current = 'login'

    def on_search_button_press(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print("Search button pressed.")

class BreedingMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 

        root_layout = BoxLayout(orientation='vertical', padding=[10, 20, 10, 10])

        header = BoxLayout(size_hint_y=None, height=60, padding=10)
       
        # Use a relative image path for the back button
        back_button = Image(source=get_asset_path('BACKK.png'), size_hint=(None, None), size=(30, 30))
        back_button.bind(on_touch_down=self.on_back_button_press)
        header.add_widget(back_button)

        header.add_widget(Label(text="[b]Monitoring[/b]", font_size=24, color=(0, 0, 0, 1), markup=True))
        search_button = Image(source=get_asset_path('search.png'), size_hint=(None, None), size=(60, 60))
        search_button.bind(on_touch_down=self.on_search_button_press)
        header.add_widget(search_button)

        root_layout.add_widget(header)

        pig_list_label = Label(text="[b]     Breeding:[/b]", font_size=25, color=(0.502, 0.502, 0.502, 1), size_hint_y=None, height=30, halign="left", markup=True)
        pig_list_label.bind(size=pig_list_label.setter('text_size'))

        pig_list_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        pig_list_layout.add_widget(pig_list_label)

       # Use a relative image path for sorting button
        sort_button_for_list = Image(source=get_asset_path('sorting.png'), size_hint=(None, None), size=(50, 50))
        sort_button_for_list.bind(on_touch_down=self.on_sort_button_press)
        pig_list_layout.add_widget(sort_button_for_list)

        root_layout.add_widget(pig_list_layout)

        with root_layout.canvas.before:
            Color(0.933, 0.933, 0.933, 1)
            root_layout.rect = RoundedRectangle(pos=root_layout.pos, size=root_layout.size)
        root_layout.bind(pos=lambda _, pos: setattr(root_layout.rect, 'pos', pos),
                         size=lambda _, size: setattr(root_layout.rect, 'size', size))

        scroll = ScrollView()
        pig_list = GridLayout(cols=1, size_hint_y=None, spacing=15, padding=[15, 15])
        pig_list.bind(minimum_height=pig_list.setter('height'))

        # Fetch pig data from Flask server
        try:
            response = requests.get("http://localhost:5000/breeding_process")  # Ensure correct endpoint
            response.raise_for_status()  # Raise error if status code is not 200
            data = response.json()  # Get JSON response

            breeding_records = data.get('breeding_process', [])  # Extract breeding records

            if breeding_records:
                for record in breeding_records:
                    if isinstance(record, dict):
                        pig_list.add_widget(BreedingPigCardMenu(record))  # Display breeding details
                    else:
                        print(f"Invalid breeding data format: {record}")
            else:
                print("No breeding records found in the response.")

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        except ValueError as e:
            print(f"Error parsing JSON: {e}")

        scroll.add_widget(pig_list)
        root_layout.add_widget(scroll)

       # Floating Action Button (FAB)
        fab_layout = FloatLayout()
        fab_button = Button(
            text="+",
            size_hint=(None, None),
            size=(80, 80),
            pos_hint={"right": 1, "bottom": 1},
            background_normal='',
            background_color=(1, 0.4, 0.4, 1)
        )
        fab_button.bind(on_release=self.open_addbreed)
        fab_layout.add_widget(fab_button)
        root_layout.add_widget(fab_layout)

        self.add_widget(root_layout)

    def open_addbreed(self, instance):
        app = App.get_running_app()
        app.root.current = "breeding"

    def on_back_button_press(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.manager.current = 'breedingmenu'  # Change to the appropriate screen

    def on_back_button_press(self, instance, touch):
        # Handle back button press (perhaps navigate to the previous screen)
        pass

    def on_search_button_press(self, instance, touch):
        # Handle search button press (implement search functionality)
        pass

    def on_sort_button_press(self, instance, touch):
        # Handle sort button press (implement sorting functionality)
        pass

class MonitoringScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root_layout = BoxLayout(orientation='vertical', padding=[10, 20, 10, 10])

        header = BoxLayout(size_hint_y=None, height=60, padding=10)

        # Use a relative image path for the back button
        back_button = Image(source=get_asset_path('BACKK.png'), size_hint=(None, None), size=(30, 30))
        back_button.bind(on_touch_down=self.on_back_button_press)
        header.add_widget(back_button)

        header.add_widget(Label(text="[b]Monitoring[/b]", font_size=24, color=(0, 0, 0, 1), markup=True))

        # Use a relative image path for the search button
        search_button = Image(source=get_asset_path('search.png'), size_hint=(None, None), size=(60, 60))
        search_button.bind(on_touch_down=self.on_search_button_press)
        header.add_widget(search_button)

        root_layout.add_widget(header)

        pig_list_label = Label(text="[b]     Lists of Pigs:[/b]", font_size=25, color=(0.502, 0.502, 0.502, 1), size_hint_y=None, height=30, halign="left", markup=True)
        pig_list_label.bind(size=pig_list_label.setter('text_size'))

        pig_list_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        pig_list_layout.add_widget(pig_list_label)

        # Use a relative image path for sorting button
        sort_button_for_list = Image(source=get_asset_path('sorting.png'), size_hint=(None, None), size=(50, 50))
        sort_button_for_list.bind(on_touch_down=self.on_sort_button_press)
        pig_list_layout.add_widget(sort_button_for_list)

        root_layout.add_widget(pig_list_layout)

        with root_layout.canvas.before:
            Color(0.933, 0.933, 0.933, 1)
            root_layout.rect = RoundedRectangle(pos=root_layout.pos, size=root_layout.size)
        root_layout.bind(pos=lambda _, pos: setattr(root_layout.rect, 'pos', pos),
                         size=lambda _, size: setattr(root_layout.rect, 'size', size))

        scroll = ScrollView()
        pig_list = GridLayout(cols=1, size_hint_y=None, spacing=15, padding=[15, 15])
        pig_list.bind(minimum_height=pig_list.setter('height'))

        try:
            response = requests.get("http://localhost:5000/monitoring")
            response.raise_for_status()
            pig_data_list = response.json().get('pigs', [])

            if pig_data_list:
                for pig in pig_data_list:
                    if isinstance(pig, dict):
                        pig_list.add_widget(PigCard(pig))
            else:
                print("No pigs found in the response.")

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")

        scroll.add_widget(pig_list)
        root_layout.add_widget(scroll)

        fab_layout = FloatLayout()
        fab_button = Button(
            text="+",
            size_hint=(None, None),
            size=(80, 80),
            pos_hint={"right": 1, "bottom": 1},
            background_normal='',
            background_color=(1, 0.4, 0.4, 1)
        )
        fab_button.bind(on_release=self.open_addpig)
        fab_layout.add_widget(fab_button)
        root_layout.add_widget(fab_layout)

        self.add_widget(root_layout)

    def open_addpig(self, instance):
        app = App.get_running_app()
        app.root.current = "addpig"

    def on_back_button_press(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.manager.current = 'monitoringmenu'  # Change to the appropriate screen

    def on_search_button_press(self, instance, touch):
        # Handle search button press (implement search functionality)
        pass

    def on_sort_button_press(self, instance, touch):
        # Handle sort button press (implement sorting functionality)
        pass
    
class AddPigScreen(Screen):  # Renamed to AddPigScreen
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.root_layout = BoxLayout(orientation='vertical', padding=[10, 20, 10, 10])

        # Header with Back Button
        header = BoxLayout(size_hint_y=None, height=10, padding=3)
        back_button = Button(text="<", size_hint=(None, None), size=(30, 30), font_size=20)
        back_button.bind(on_press=self.on_back_button_press)  # Bind back button event
        header.add_widget(back_button)

        self.root_layout.add_widget(header)
        
        self.cage_data = self.fetch_dropdown_data('cages')
        self.status_data = self.fetch_dropdown_data('statuses')
        self.classification_data = self.fetch_dropdown_data('classifications')
        self.vaccine_data = self.fetch_dropdown_data('vacnames')
        self.gender_data = self.fetch_dropdown_data('genders')

        self.build()  # Call the build method to set up the UI
        self.add_widget(self.root_layout)

    def on_back_button_press(self, instance):
        self.manager.current = 'monitoringmenu'  # Replace 'previous_screen' with the actual screen name

    def fetch_dropdown_data(self, dropdown_type):
        try:
            response = requests.get(
                f"http://localhost:5000/get_dropdown_data",
                params={'type': dropdown_type}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {dropdown_type}: {e}")
            return []

    def build(self):
        layout = FloatLayout()

        with layout.canvas.before:
            Color(238 / 255, 238 / 255, 238 / 255, 1)
            self.rect = RoundedRectangle(size=layout.size, pos=layout.pos)

        layout.bind(size=self.update_rect, pos=self.update_rect)

        addpig_label = Label(
            text="Pig Details",
            font_size=30,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5, 'top': 0.98},
            color=(0, 0, 0, 1)
        )
        layout.add_widget(addpig_label)

        box_container = BoxLayout(
            orientation='vertical',
            padding=10,
            spacing=10,
            size_hint=(None, None),
            size=(450, 650),
            pos_hint={'center_x': 0.5, 'top': 0.98}
        )
        with box_container.canvas.before:
            Color(1, 1, 1, 1)
            self.rect_box = RoundedRectangle(size=box_container.size, pos=box_container.pos, radius=[20])

        box_container.bind(size=self.update_box_rect, pos=self.update_box_rect)

        pigs_info_label = Label(
            text="Pig's Information",
            font_size=24,
            color=(128 / 255, 128 / 255, 128 / 255, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.92},
            bold=True
        )
        box_container.add_widget(pigs_info_label)

        # Birthdate input
        self.birthdate_input = TextInput(
            hint_text="Birthdate (YYYY-MM-DD)", multiline=False, size_hint_y=None, height=40
        )
        box_container.add_widget(self.birthdate_input)

        # Age and Weight input
        age_weight_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        self.age_input = TextInput(hint_text="Age (Months)", multiline=False, size_hint_y=None, height=40)
        age_weight_box.add_widget(self.age_input)
        self.weight_input = TextInput(hint_text="Weight (kg)", multiline=False, size_hint_y=None, height=40)
        age_weight_box.add_widget(self.weight_input)
        box_container.add_widget(age_weight_box)

        # Piglet Count input
        self.piglet_input = TextInput(hint_text="Piglet Count", multiline=False, size_hint_y=None, height=40)
        self.piglet_input.disabled = True  # Disabled by default
        box_container.add_widget(self.piglet_input)

        # Boar Used input
        self.boar_used_input = TextInput(hint_text="Boar Used", multiline=False, size_hint_y=None, height=40)
        self.boar_used_input.disabled = True  # Disabled by default
        box_container.add_widget(self.boar_used_input)

        # Status dropdown
        status_values = [status.get('description', 'Unknown Status') for status in self.status_data] or ['No statuses available']
        self.status_spinner = Spinner(
            text="Status",
            values=status_values,
            size_hint=(None, None),
            size=(200, 40)
        )
        box_container.add_widget(self.status_spinner)

        # Gender selection (ToggleButton)
        gender_label = Label(text="Select Gender", font_size=18, size_hint_y=None, height=30)
        box_container.add_widget(gender_label)

        gender_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        self.male_toggle = ToggleButton(text="Male", group='gender')
        gender_box.add_widget(self.male_toggle)
        self.female_toggle = ToggleButton(text="Female", group='gender')
        gender_box.add_widget(self.female_toggle)
        box_container.add_widget(gender_box)

        # Classification dropdown
        classification_values = [classification.get('name', 'Unknown Classification') for classification in self.classification_data] or ['No classifications available']
        self.classification_spinner = Spinner(
            text="Select Classification",
            values=classification_values,
            size_hint=(None, None),
            size=(200, 40)
        )
        box_container.add_widget(self.classification_spinner)

        # Cage dropdown
        cage_values = [cage.get('description', 'Unknown Cage') for cage in self.cage_data] or ['No cages available']
        self.cage_spinner = Spinner(
            text="Select Cage",
            values=cage_values,
            size_hint=(None, None),
            size=(200, 40)
        )
        box_container.add_widget(self.cage_spinner)

        # Vaccine dropdown
        vaccine_values = [vaccine.get('name', 'Unknown Vaccine') for vaccine in self.vaccine_data] or ['No vaccines available']
        self.vaccine_spinner = Spinner(
            text="Select Vaccine",
            values=vaccine_values,
            size_hint=(None, None),
            size=(200, 40)
        )
        box_container.add_widget(self.vaccine_spinner)

        # Submit button
        submit_button = Button(
            text="Submit",
            size_hint_y=None,
            height=40,
            background_color=(234 / 255, 141 / 255, 143 / 255, 1),
            color=(1, 1, 1, 1)
        )
        submit_button.bind(on_press=self.submit_form)
        box_container.add_widget(submit_button)

        layout.add_widget(box_container)
        self.root_layout.add_widget(layout)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_box_rect(self, instance, value):
        self.rect_box.pos = instance.pos
        self.rect_box.size = instance.size

    def submit_form(self, instance):
        birthdate = self.birthdate_input.text
        weight = self.weight_input.text

        # Validate birthdate format
        try:
            datetime.strptime(birthdate, "%Y-%m-%d")
        except ValueError:
            self.show_popup("Error", "Invalid birthdate format. Please use YYYY-MM-DD.")
            return

        gender = "Male" if self.male_toggle.state == 'down' else "Female"
        cage_description = self.cage_spinner.text
        status = "Alive"  # Default status
        piglet_count = self.piglet_input.text if self.piglet_input.text else None
        boar_used = self.boar_used_input.text if self.boar_used_input.text else None
        vaccine_name = self.vaccine_spinner.text

        cage_id = next((item['id'] for item in self.cage_data if item['description'] == cage_description), None)
        gender_id = next((item['id'] for item in self.gender_data if item['name'] == gender), None)
        vaccine_id = next((item['id'] for item in self.vaccine_data if item['name'] == vaccine_name), None)

        form_data = {
            "birthdate": birthdate,
            "weight": weight,
            "cage_id": cage_id,
            "status": status,
            "gender_id": gender_id,
            "piglet_count": piglet_count,
            "boar_used": boar_used,
            "vacname_id": vaccine_id,
        }

        try:
            response = requests.post('http://localhost:5000/add_pig', json=form_data)

            if response.status_code == 201:
                self.show_popup("Success", "Pig added successfully!")
            else:
                self.show_popup("Error", "Failed to add pig. Please try again.")
        except requests.exceptions.RequestException as e:
            self.show_popup("Error", f"An error occurred: {e}")

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        popup_message = Label(text=message, size_hint_y=None, height=40)
        popup_close = Button(text="Close", size_hint_y=None, height=40)
        popup_layout.add_widget(popup_message)
        popup_layout.add_widget(popup_close)

        popup = Popup(title=title, content=popup_layout, size_hint=(None, None), size=(300, 200))
        popup_close.bind(on_press=popup.dismiss)
        popup.open()
        
# Define the KV language string for BreedingScreen
kv = '''
<BreedingScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        canvas.before:
            Color:
                rgba: (0.933, 0.933, 0.933, 1)  # #EEEEEE
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint_y: None
            height: '40dp'
            spacing: 10

            Button:
                size_hint_x: None  
                width: '40dp'
                background_normal: root.back_image
                background_down: root.back_image
                on_press: root.manager.current = 'monitoringmenu'

            Label:
                text: 'Breeding'
                color: (0, 0, 0, 1)
                bold: True
                size_hint_y: None
                height: '30dp'
                halign: 'center'
                width: '100dp'
                text_size: self.size

        BoxLayout:
            orientation: 'vertical'
            padding: 20
            spacing: 15
            size_hint: 0.9, 0.9 
            size: '300dp', '400dp'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            canvas.before:
                Color:
                    rgba: (1, 1, 1, 1)  # #FFFFFF
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [10]

            Label:
                text: 'Breed'
                color: (0, 0, 0, 1)
                size_hint_y: None
                height: '30dp'
                halign: 'center'
                text_size: self.size

            BoxLayout:
                orientation: 'vertical'
                spacing: 5

                Label:
                    text: 'Female Pig'
                    bold: True
                    color: (0, 0, 0, 1)
                    halign: 'left'
                    text_size: self.size
                    size_hint_y: None
                    height: '30dp'

                Spinner:
                    id: female_pig_spinner
                    text: 'Select Female Pig'
                    values: ['']  
                    size_hint_y: None
                    height: '40dp'
                    background_normal: ''
                    background_color: (1, 1, 1, 1)
                    color: (0, 0, 0, 1)

            BoxLayout:
                orientation: 'vertical'
                spacing: 5

                Label:
                    text: 'Male Pig'
                    bold: True
                    color: (0, 0, 0, 1)
                    halign: 'left'
                    text_size: self.size
                    size_hint_y: None
                    height: '30dp'

                Spinner:
                    id: male_pig_spinner
                    text: 'Select Male Pig'
                    values: ['']  
                    size_hint_y: None
                    height: '40dp'
                    background_normal: ''
                    background_color: (1, 1, 1, 1)
                    color: (0, 0, 0, 1)

            BoxLayout:
                orientation: 'vertical'
                spacing: 5

                Label:
                    text: 'Cage No.'
                    bold: True
                    color: (0, 0, 0, 1)
                    halign: 'left'
                    text_size: self.size
                    size_hint_y: None
                    height: '30dp'

                Spinner:
                    id: cage_no_spinner
                    text: 'Select Cage'
                    values: ['']  
                    size_hint_y: None
                    height: '40dp'
                    background_normal: ''
                    background_color: (1, 1, 1, 1)
                    color: (0, 0, 0, 1)

            Widget:
                size_hint_y: 0.4

            Button:
                text: 'Confirm'
                bold: True
                size_hint: None, None
                size: '150dp', '50dp'
                pos_hint: {'center_x': 0.5}
                background_normal: ''
                background_color: (0.92, 0.45, 0.45, 1)
                color: (1, 1, 1, 1)
                on_press: root.on_breeding_confirm()  # Bind the button to the function
'''

Builder.load_string(kv)

class BreedingScreen(Screen):
    back_image = StringProperty('')  # Property to hold the image path

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.back_image = get_asset_path('BACKK.png')  # Set the image path   

    def on_enter(self):
        self.update_pig_spinners()
        self.update_cage_spinner()

    def update_pig_spinners(self):
        try:
            response = requests.get("http://localhost:5000/get_breeding_pigs")
            if response.status_code == 200:
                data = response.json()

                female_pigs = [f"ID: {p['Pig_ID']} - {p['Classification']}" for p in data.get('female_pigs', [])]
                male_pigs = [f"ID: {p['Pig_ID']} - {p['Classification']}" for p in data.get('male_pigs', [])]

                female_spinner = self.ids.get('female_pig_spinner')
                male_spinner = self.ids.get('male_pig_spinner')

                if female_spinner:
                    female_spinner.values = female_pigs if female_pigs else ['No female pigs available']
                    female_spinner.text = female_spinner.values[0]

                if male_spinner:
                    male_spinner.values = male_pigs if male_pigs else ['No male pigs available']
                    male_spinner.text = male_spinner.values[0]

            else:
                print(f"Failed to fetch pig data. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error in update_pig_spinners: {e}")

    def update_cage_spinner(self):
        try:
            response = requests.get("http://localhost:5000/get_dropdown_data?type=cages")
            if response.status_code == 200:
                data = response.json()

                cages = [f"Cage ID: {c['id']} - {c['description']}" for c in data if 'id' in c and 'description' in c]

                cage_spinner = self.ids.get('cage_no_spinner')
                if cage_spinner:
                    cage_spinner.values = cages if cages else ['No cages available']
                    cage_spinner.text = cage_spinner.values[0]

            else:
                print(f"Failed to fetch cage data. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error in update_cage_spinner: {e}")

    def on_breeding_confirm(self):
        female_pig = self.ids.female_pig_spinner.text
        male_pig = self.ids.male_pig_spinner.text
        cage = self.ids.cage_no_spinner.text

        # Debugging prints to check the selected values
        print(f"Female Pig: {female_pig}, Male Pig: {male_pig}, Cage: {cage}")

        if "ID: " not in female_pig or "ID: " not in male_pig or "Cage ID: " not in cage:
            self.show_popup("Error", "Please select valid female pig, male pig, and cage.")
            return

        female_pig_id = female_pig.split("ID: ")[1].split(" -")[0]  # Extract the ID from the text
        male_pig_id = male_pig.split("ID: ")[1].split(" -")[0]      # Extract the ID from the text
        cage_id = cage.split("Cage ID: ")[1].split(" -")[0]          # Extract the Cage ID

        data = {
            'Female_Pig_ID': female_pig_id,
            'Male_Pig_ID': male_pig_id,
            'Cage_ID': cage_id
        }

        # Print the data being sent to the backend
        print(f"Sending data: {data}")

        try:
            response = requests.post("http://localhost:5000/breeding_process", json=data)
            print(f"API Response: {response.status_code}, {response.text}")  # Log the response for debugging
            if response.status_code == 200:
                result = response.json()
                self.show_popup("Success", result["message"])
            else:
                result = response.json()
                self.show_popup("Error", result["message"])
        except Exception as e:
            self.show_popup("Error", f"An error occurred: {str(e)}")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=("400dp", "200dp"))
        popup.open()

class ForgotPassword(Screen):
    def __init__(self, **kwargs):
        super(ForgotPassword, self).__init__(**kwargs)
        self.generated_otp = None  
        self.user_email = None  

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Set background color
        with layout.canvas.before:
            Color(0.97, 0.97, 0.99, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.update_rect, pos=self.update_rect)

       # Image
        img = Image(source=get_asset_path('P-ForgotPass1.jpg'), 
                    size_hint=(0.6, 0.3), pos_hint={'center_x': 0.5})

        # Back button
        back_button = Button(size_hint=(None, None), size=(60, 60), pos_hint={'top': 1, 'left': 1},
                            background_normal=get_asset_path('backk.png'))
        back_button.bind(on_press=self.go_back)
                # Labels
        label = Label(text="FORGOT PASSWORD?", size_hint=(1, None), height=40, bold=True, color=(0, 0, 0, 1),
                      halign='left', valign='middle', padding=[10, 0])
        label.bind(size=label.setter('text_size'))

        message_label = Label(text="Don't worry, it happens. Please enter your email address, and we will send an OTP.",
                              size_hint=(1, None), height=60, color=(0, 0, 0, 0.7),
                              halign='left', valign='middle', padding=[10, 0])
        message_label.bind(size=message_label.setter('text_size'))

        # Email Input
        self.text_input = TextInput(hint_text="Enter your email address", multiline=False, size_hint=(0.6, None),
                                    height=40, background_normal='', background_color=(1, 1, 1, 1))
        self.text_input.halign = 'center'

        # Continue Button
        button = Button(text="Continue", size_hint=(0.5, None), height=50, pos_hint={'center_x': 0.5},
                        background_normal='', background_color=(0, 0, 0, 0))
        button.bind(on_press=self.send_otp)

        with button.canvas.before:
            Color(234 / 255, 141 / 255, 143 / 255, 1)
            self.rounded_rect = RoundedRectangle(pos=button.pos, size=button.size, radius=[130])
        button.bind(pos=self.update_rounded_rect, size=self.update_rounded_rect)

        # Add widgets to layout
        layout.add_widget(back_button)
        layout.add_widget(img)
        layout.add_widget(label)
        layout.add_widget(message_label)
        layout.add_widget(self.text_input)
        layout.add_widget(button)

        self.add_widget(layout)

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def update_rounded_rect(self, instance, *args):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(234 / 255, 141 / 255, 143 / 255, 1)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[20])

    def go_back(self, instance):
        self.manager.current = 'login'  # Go back to login screen

    def send_otp(self, instance):
        email = self.text_input.text
        if not email or '@' not in email:
            self.show_popup("Invalid Email", "Please enter a valid email address.")
            return

        # Check if email exists in the database
        if not self.check_email_exists(email):
            self.show_popup("Error", "This email is not registered.")
            return

        self.generated_otp = random.randint(100000, 999999)
        self.user_email = email

        try:
            # Sending the OTP
            self.send_email_otp(email, self.generated_otp)
            self.show_popup("Success", f"An OTP has been sent to {email}.")
        except Exception as e:
            self.show_popup("Error", f"Failed to send OTP: {str(e)}")

    def check_email_exists(self, email):
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="127.0.0.1",       # MySQL host, assuming it's running locally
            user="root",            # MySQL username (replace with your username)
            password="",            # MySQL password (leave empty if none is set)
            database="sample_dbpiggery"  # Name of the database
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        # If result is None, email does not exist
        return result is not None

    def send_email_otp(self, email, otp):
        # Configure SMTP server
        sender_email = "player24688642@gmail.com"  # Your Gmail address
        sender_password = "ceec irhh pexb iuny"  # Your Gmail app password (if 2FA is enabled)
        subject = "Your OTP Code"
        body = f"Your OTP code is {otp}. Please use this to reset your password."

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            print(f"OTP sent to {email}")
        except Exception as e:
            print(f"Failed to send OTP: {str(e)}")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()

class App(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MonitoringMenu(name='monitoringmenu'))
        sm.add_widget(MonitoringScreen(name='monitoring'))
        sm.add_widget(AddPigScreen(name='addpig'))  # Updated to AddPigScreen
        sm.add_widget(BreedingScreen(name='breeding')) 
        sm.add_widget(BreedingMenu(name='breedingmenu')) 
        sm.add_widget(ForgotPassword(name='forgotpass')) 
        return sm

if __name__ == "__main__":
    App().run()