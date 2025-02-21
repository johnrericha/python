# client.py
import socket
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class ChatApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Create a ScrollView to hold the chat messages
        self.scroll_view = ScrollView(size_hint=(1, 0.9))
        self.chat_layout = GridLayout(cols=1, size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.scroll_view.add_widget(self.chat_layout)

        # Create a TextInput for message input
        self.message_input = TextInput(size_hint=(0.8, 0.1), multiline=False)
        
        # Create a Button to send messages
        send_button = Button(text='Send', size_hint=(0.2, 0.1))
        send_button.bind(on_press=self.send_message)

        # Add widgets to the main layout
        self.layout.add_widget(self.scroll_view)
        self.layout.add_widget(self.message_input)
        self.layout.add_widget(send_button)

        # Connect to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 5555))  # Change to server IP if needed

        # Start a thread to listen for incoming messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

        return self.layout

    def send_message(self, instance):
        message = self.message_input.text.strip()
        if message:  # Only send if the message is not empty
            self.client_socket.send(message.encode('utf-8'))
            self.add_message(f'You: {message}')
            self.message_input.text = ''  # Clear the input field

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.add_message(message)
            except:
                break

    def add_message(self, message):
        message_label = Label(text=message, size_hint_y=None, height=40)
        self.chat_layout.add_widget(message_label)
        self.scroll_view.scroll_to(message_label)  # Scroll to the latest message

if __name__ == '__main__':
    ChatApp().run()