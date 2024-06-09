import time
import random
import os
import colorama
from colorama import Fore, Back, Style
import datetime
import requests
import sys
import platform
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
import random
import pygame
colorama.init()
os.system('cls')
version = "KARDANA_PRO_3"
calculator = "Calculator"
kardana_play = "Kardana Play"
Weather = "Weather"
text = "Kardana Pro 3"
Watch = "Watch"
Secret_box = 'Secret_box'
Toss_a_Coin = "Toss a Coin"
Guess_the_number = 'Guess the number'
Password_Generator_Pro = "Password Generator Pro"
kardana_radio = 'Kardana Radio v1'
kardana_music = "Kardana Music v1"
box = ["Nothing","Junk","Key","License for the free version","Ball","Scooter","Boat","Bottle"]
colored_text = text.replace("3", f"{Fore.RED}3{Fore.RESET}")
bold_colored_text = f"{Style.BRIGHT}{colored_text}{Style.RESET_ALL}"
print(bold_colored_text)
def install_application(installed_apps):
    app_name = input("Enter the name of the application: ")
    file_name = input(f"Enter the file name for {app_name} (leave blank to use default): ")
    if not file_name:
        file_name = app_name.lower().replace(" ", "_") + ".py"

    # Сохранение имени приложения и файла в файл
    with open("installed_apps.txt", "a") as file:
        file.write(f"{app_name} = {file_name}\n")

    print(f"{app_name} has been installed as {file_name}")

    # Обновление словаря установленных приложений
    installed_apps[app_name] = file_name

# Функция для удаления приложения
def uninstall_application(installed_apps):
    app_name = input("Enter the name of the application to uninstall: ")

    if app_name in installed_apps:
        del installed_apps[app_name]
        print(f"{app_name} has been uninstalled.")

        # Обновление файла installed_apps.txt
        with open("installed_apps.txt", "w") as app_file:
            for app, file in installed_apps.items():
                app_file.write(f"{app} = {file}\n")
    else:
        print(f"{app_name} is not installed.")
# Функция для запуска приложения
def run_application(app_name):
    # Получение имени файла из файла installed_apps.txt
    with open("installed_apps.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(f"{app_name} = "):
                file_name = line.split("=")[1].strip()
                # Проверка наличия файла перед запуском
                if os.path.exists(file_name):
                    os.system(f"python {file_name}")
                else:
                    print(f"The application '{app_name}' is not found. Removing it from the list.")
                    # Удаление приложения из словаря
                    del installed_apps[app_name]
                    # Обновление файла installed_apps.txt
                    with open("installed_apps.txt", "w") as app_file:
                        for app, file in installed_apps.items():
                            app_file.write(f"{app} = {file}\n")
                return

    print(f"{app_name} is not installed.")

# Загрузка установленных приложений из файла
installed_apps = {}
if os.path.exists("installed_apps.txt"):
    with open("installed_apps.txt", "r") as app_file:
        lines = app_file.readlines()
        for line in lines:
            parts = line.split(" = ")
            if len(parts) == 2:
                app_name = parts[0].strip()
                file_name = parts[1].strip()
                installed_apps[app_name] = file_name
time.sleep(2)
os.system('clear')
print(''' 
  _  __             _                     _____             ____  
 | |/ /            | |                   |  __ \           |___ \ 
 | ' / __ _ _ __ __| | __ _ _ __   __ _  | |__) | __ ___     __) |
 |  < / _` | '__/ _` |/ _` | '_ \ / _` | |  ___/ '__/ _ \   |__ < 
 | . \ (_| | | | (_| | (_| | | | | (_| | | |   | | | (_) |  ___) |
 |_|\_\__,_|_|  \__,_|\__,_|_| |_|\__,_| |_|   |_|  \___/  |____/ 
                                                                  
                                                                  
  ''')
time.sleep(2)
os.system('clear')
print('Loading...')
time.sleep(1)
os.system('clear')
while True:
    print(bold_colored_text)
    print('Applications:\n'+calculator+'[write 1 to open]\n'+kardana_play+"[write 2 to open]")
    for index, (app_name, _) in enumerate(installed_apps.items(), start=3):
        print(f"{app_name}[write {index} to open]")
    menu = input( )
    if menu == "1":
        print('Loading...')
        time.sleep(1)
        print('''Welcome to the calculator
        Operators + - * / %
        Write your example''')
        try:
            p = input()
            result = eval(p)
            print("Solution:")
            print(result)
            time.sleep(2)
            os.system('clear')
        except Exception as e:
            print("Error:", e)
            time.sleep(1)
            print("Please enter a valid expression and try again.")
    else:
        os.system('clear')
    if menu == "2":
        print("Loading...")
        time.sleep(1)
        os.system('clear')
        print('Applications:\n'+Weather+'[write 1 to open]\n'+Watch+"[write 2 to open]\n"+Password_Generator_Pro+"[write 3 to open]\n"+kardana_radio+"[write 4 to open]")
        print('Games:\n'+Secret_box+'[write 5 to open]\n'+Guess_the_number+"[write 6 to open]\n"+Toss_a_Coin+"[write 7 to open]\n"+kardana_music+"[write 8 to open]")
        kardana_play_menu = input()
        if kardana_play_menu == '1':
            # Вставьте код для погоды здесь
            def get_weather_data(city):
                # Construct the request
                url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=en&appid=79d1ca96933b0328e1c7e3e7a26cb347'
                
                # Send the request to the server and immediately get the result
                response = requests.get(url)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return None

            def setup_city():
                settings_file = 'settings_kardana.txt'

                # Check if there's already a saved city in the file
                if os.path.exists(settings_file):
                    with open(settings_file, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            if line.startswith('City'):
                                city = line.split('=')[1].strip()
                                return city

                # If the file doesn't exist, ask the user to enter the city
                print('Enter your city:')
                city = input()

                # Save the entered city to the file
                with open(settings_file, 'w') as file:
                    file.write(f'City = {city}\n')

                return city

            def main():
                # Get the city from the file or ask the user if the file doesn't exist
                city = setup_city()

                # Get weather data
                weather_data = get_weather_data(city)

                if weather_data:
                    # Get temperature and feels-like temperature
                    temperature = round(weather_data['main']['temp'])
                    temperature_feels = round(weather_data['main']['feels_like'])

                    # Display values on the screen
                    print('Currently in', city, str(temperature), '°C')
                    print('Feels like', str(temperature_feels), '°C')
                else:
                    print('Sorry, weather information for the specified city was not found.')

            if __name__ == "__main__":
                main()
                time.sleep(2)
                os.system('clear')
        elif kardana_play_menu == '2':
            print('Loading...')
            time.sleep(1)
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current time:", current_time)
            time.sleep(2)
            os.system('clear')
        elif kardana_play_menu == '3':
            chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            while True:
                try:
                    number = int(input('Number of passwords: '))
                    if number > 0:
                        break
                    else:
                        print("Please enter a positive integer for the number of passwords.")
                except ValueError:
                    print("Invalid input. Please enter a valid integer for the number of passwords.")
            while True:
                try:
                    length = int(input('Line length: '))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid integer for line length.")
            for x in range(number):
                password = ''
                for i in range(length):
                    password += random.choice(chars)
                print(password)
            time.sleep(2)
            os.system('clear')
        elif kardana_play_menu == '4':
            class ConsoleMediaPlayer:
                def __init__(self, stream_url):
                    self.player = QMediaPlayer()
                    self.playlist = QMediaPlaylist()
                    self.playlist.addMedia(QMediaContent(QUrl(stream_url)))
                    self.player.setPlaylist(self.playlist)
                    self.player.setVolume(100)

                def play(self):
                    self.player.play()

                def pause(self):
                    self.player.pause()

                def stop(self):
                    self.player.stop()

            if __name__ == '__main__':
                stream_url = 'https://online.hitfm.ua/HitFM'
                
                console_media_player = ConsoleMediaPlayer(stream_url)
                exit_requested = False
                
                while True:
                    console_media_player.play()
                    os.system('clear')
                    print('Loading...')
                    time.sleep(3)
                    os.system('clear')
                    print('''
  _  __             _                     _____           _ _              __ 
 | |/ /            | |                   |  __ \         | (_)            /_ |
 | ' / __ _ _ __ __| | __ _ _ __   __ _  | |__) |__ _  __| |_  ___   __   _| |
 |  < / _` | '__/ _` |/ _` | '_ \ / _` | |  _  // _` |/ _` | |/ _ \  \ \ / / |
 | . \ (_| | | | (_| | (_| | | | | (_| | | | \ \ (_| | (_| | | (_) |  \ V /| |
 |_|\_\__,_|_|  \__,_|\__,_|_| |_|\__,_| |_|  \_\__,_|\__,_|_|\___/    \_/ |_|
                                                                              
                                                                              
''')
                    command = input("Enter command (stop/exit): ").lower()
                    if command == "stop":
                        console_media_player.stop()
                        while True:
                            command1 = input("Enter command (play/exit): ").lower()
                            if command1 == "play":
                                os.system('cls')
                                break
                            elif command1 == "exit":
                                console_media_player.stop()
                                exit_requested = True
                                break

                        if command == "exit" or exit_requested:
                            os.system('cls')
                            break
                        else:
                            print("Invalid command. Try again.")
                    elif command == "exit":
                        console_media_player.stop()
                        exit_requested = True
                        break
                    else:
                        print("Invalid command. Try again.")

                if exit_requested:
                    print("Exiting the program.")
        elif kardana_play_menu == '5':
            print("Loading...")
            time.sleep(1)
            print("Opening a secret box")
            print("You got:")
            print(random.choice(box))
            time.sleep(2)
            os.system('clear')
        elif kardana_play_menu == '6':
            print("Loading...")
            time.sleep(1)
            c = random.randrange(1, 10)
            print("Guess the number from 1 to 10")
            r = True
            while r:
                cv = int(input( ))
                if cv == c:
                    print("You won")
                    r = False
                    time.sleep(1)
                    os.system('cls')
                else:
                    if cv > c:
                        print("Your number is too high")
                    if cv < c:
                        print("Your number is too small")
        elif kardana_play_menu == '7':
            moneta = ["Heads","Tails"]
            print("I'm tossing a coin...")
            time.sleep(1)
            os.system('cls')
            print('You got:')
            print(random.choice(moneta))
            time.sleep(1)
            os.system('cls')
        elif kardana_play_menu == '8':
            os.system('cls')
            def play_music(music_file):
                pygame.mixer.init()
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play()

            # Функция для вывода списка музыкальных файлов
            def list_music_files(directory):
                music_files = [f for f in os.listdir(directory) if f.endswith(('.mp3', '.wav'))]
                if not music_files:
                    print("В папке нет музыкальных файлов.")
                else:
                    print("Список музыкальных файлов:")
                    for i, music_file in enumerate(music_files):
                        print(f"{i + 1}. {music_file}")
                return music_files

            # Основная часть программы
            music_folder = "kardana_music"
            while True:
                try:
                    music_files = list_music_files(music_folder)
                    print('''
              _  __             _                     __  __           _             __ 
             | |/ /            | |                   |  \/  |         (_)           /_ |
             | ' / __ _ _ __ __| | __ _ _ __   __ _  | \  / |_   _ ___ _  ___  __   _| |
             |  < / _` | '__/ _` |/ _` | '_ \ / _` | | |\/| | | | / __| |/ __| \ \ / / |
             | . \ (_| | | | (_| | (_| | | | | (_| | | |  | | |_| \__ \ | (__   \ V /| |
             |_|\_\__,_|_|  \__,_|\__,_|_| |_|\__,_| |_|  |_|\__,_|___/_|\___|   \_/ |_|
                                                                                        
                                                                                        
            ''')
                    choice = int(input("Введите номер трека для воспроизведения (0 для выхода): "))
                    if choice == 0:
                        os.system('cls')
                        break
                    elif 1 <= choice <= len(music_files):
                        chosen_music_file = os.path.join(music_folder, music_files[choice - 1])
                        play_music(chosen_music_file)
                        while True:
                            control = input("'pause' для паузы, 'resume' для продолжения, 'exit' для выбора нового трека: ")
                            if control == 'pause':
                                pygame.mixer.music.pause()
                            elif control == 'resume':
                                pygame.mixer.music.unpause()
                            elif control == 'exit':
                                pygame.mixer.music.stop()
                                os.system('cls')
                                break
                            else:
                                print("Некорректная команда. Попробуйте снова.")
                                time.sleep(1)
                                os.system('cls')
                    else:
                        print("Некорректный номер трека. Попробуйте снова.")
                        time.sleep(1)
                        os.system('cls')
                except ValueError:
                    print("Введите целое число. Попробуйте снова.")
                    time.sleep(1)
                    os.system('cls')
        else:
            os.system('cls')
    elif menu == "dota 2":
        print('''
  _____   ____ _______         ___  
 |  __ \ / __ \__   __|/\     |__ \ 
 | |  | | |  | | | |  /  \       ) |
 | |  | | |  | | | | / /\ \     / / 
 | |__| | |__| | | |/ ____ \   / /_ 
 |_____/ \____/  |_/_/    \_\ |____|
                                    
                                    
''')
        time.sleep(2)
    elif menu == "about":
        print(''' 
          _  __             _                     _____             ____  
         | |/ /            | |                   |  __ \           |___ \ 
         | ' / __ _ _ __ __| | __ _ _ __   __ _  | |__) | __ ___     __) |
         |  < / _` | '__/ _` |/ _` | '_ \ / _` | |  ___/ '__/ _ \   |__ < 
         | . \ (_| | | | (_| | (_| | | | | (_| | | |   | | | (_) |  ___) |
         |_|\_\__,_|_|  \__,_|\__,_|_| |_|\__,_| |_|   |_|  \___/  |____/ 
                                                                          
                                                                          
          ''')
        system_info = {
            "Your Version of Kardana": "KARDANA_PRO_3_BETA",
            "Your OS": platform.system(),
            "OS Version": platform.version(),
            "Processor Architecture": platform.architecture(),
            "Machine Type": platform.machine(),
            "Node Name": platform.node(),
            "Processor": platform.processor()
        }

        print("Information about your computer:")
        for key, value in system_info.items():
            print(f"{key}: {value}")
        time.sleep(5)
        os.system("cls")
    elif menu.lower().startswith("kardana_install"):
        install_application(installed_apps)
    elif menu.lower().startswith("kardana_uninstall"):
        uninstall_application(installed_apps)
    elif menu.isdigit() and 3 <= int(menu) <= len(installed_apps) + 2:
        app_index = int(menu) - 3
        app_name = list(installed_apps.keys())[app_index]
        run_application(app_name)
        time.sleep(2)
        os.system('cls')
    else:
        os.system('cls')
