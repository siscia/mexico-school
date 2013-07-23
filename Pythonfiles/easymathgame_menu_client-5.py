#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------------------------------
#1 [ Easy Mathematic Games ]

#2 Created by AndrewProgramming
#3 Completed on 19 January 2013

#  Modules needed:
#  pygame
#  pyodbc
#  inputbox
#  textrect

#4 This are created based on the location which the database file is stored in my PC.
#5 Please change the 'DBQ' accordingly to where the file is.
#6 If this program is going to be used by students in schools, it is HIGHLY recommended that-
#7 -you store the MS Access Database file in a location where all the school computers are able to-
#8 access to. In that way, all results will be stored in a file instead of creating multiple files in-
#9 different computers and it makes retrieving the datas harder.

#10 Please ensure students exit the program in a proper way. If any case if the program is not able to-
#11 exit upon clicking the 'X', please open up your task manager and end the task named "pythonw.exe".
#-------------------------------------------------------------------------------------------------------

#images
bif = "images/image.jpg"
bear = "images/bear.png"
professor = "images/professor.png"

#imports
import pyodbc, sys, pygame, time, os
from pygame.locals import *
from random import randint
import inputbox, textrect, pyaudio, wave

pygame.init()
pygame.mixer.init()

#Please change the DBQ accordingly to the access file's location. [DBQ=[HDD Name]/[Folder Name]/students.accdb;]
#conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:/Pythonfiles/students.accdb;")
conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=/home/simo/Downloads/NewArchive/Pythonfiles/students.accdb;")
#conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:/Users/123660/Desktop/Elance Jobs/Easy Math Game/students.accdb;")
cursor = conn.cursor()

#lists
points1 = [(100,220),(100,150),(150,220),(150,150),(200,220),(200,150),(250,220),(250,150),(300,220),(300,150)]
points2 = [(450,220),(450,150),(500,220),(500,150),(550,220),(550,150),(600,220),(600,150),(650,220),(650,150)]

#colors
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
black = (0,0,0)
white = (255,255,255)
grey = (192,192,192)

#strings
user_info = ''
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 7
sound_controller = 1
lesson_controller = 1

#Setting up the screen
screen = pygame.display.set_mode((800,600),pygame.FULLSCREEN,32)
#screen = pygame.display.set_mode((800,600), 0, 32)
background = pygame.image.load(bif).convert()
bear_pic = pygame.image.load(bear).convert_alpha()
professor_pic = pygame.image.load(professor).convert_alpha()
###pygame.display.set_caption('Easy Mathematic Game')
pygame.display.set_caption('Juego Facil de la Matematica')

#Definitions
def menu():
    titleFont = pygame.font.Font(None, 50)
    ###title_str = "Simple Mathematic Game"
    title_str = "Juego Facil de la Matematica"
    title_rect = pygame.Rect((100,30),(600,100))
    title_print = textrect.render_textrect(title_str, titleFont, title_rect, black, grey, 1)
    screen.blit(title_print, title_rect.topleft)

def clear():
    screen.blit(background, (0,0))
    menu()

def mainmenu():
    screen.blit(background, (0,0))
    main_msg1 = u"Diviértete y Apréndete"
    mainMenuFont1 = pygame.font.Font(None, 46)
    main_rect1 = pygame.Rect((100,30),(600,400))
    main_print1 = textrect.render_textrect(main_msg1, mainMenuFont1, main_rect1, black, grey, 1)
    screen.blit(main_print1, main_rect1.topleft)

def sleep(time):
    time.sleep(time)

def lesson1():
    global english_text, lesson_controller
    english_print = textrect.render_textrect(english_text, english_font, lesson_rect, black, grey, 1)
    screen.blit(english_print, lesson_rect.topleft)
    lesson_spanish.play()
    inputbox.ask_input(screen, 'Press Enter')
    lesson_spanish.stop()
    lesson_controller += 1

def lesson2():
    global english_text, lesson_controller
    english_print = textrect.render_textrect(english_text, english_font, lesson_rect, black, grey, 1)
    screen.blit(english_print, lesson_rect.topleft)
    lesson_english.play(8)
    inputbox.ask_input(screen, 'Press Enter')
    lesson_english.stop()
    WAVE_OUTPUT_FILENAME = 'student_recordings/student_' + str(user_info) + '_' + str(sound_controller) + '.wav'
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    clear()
    #record_text = "Press Enter if you are ready.\n\nThe recording will go on for 6 seconds.\n\nOnce you pressed Enter, go ahead and talk.\n\nThe screen will stay hanged for 6 seconds."
    record_text = "Presiona Enter si estas listo.\n\nLa grabacion seguira por 6 segundos.\n\nEn cuanto presiones Enter, puedes hablar.\n\nLa pantalla se quedara sin cambiar por 6 segundos."
    record_print = textrect.render_textrect(record_text, english_font, lesson_rect, black, grey, 1)
    screen.blit(record_print, lesson_rect.topleft)
    inputbox.ask_input(screen, 'Press Enter')

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        clear()
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    lesson_controller += 1

def lesson3():
    global student_recording
    student_recording = pygame.mixer.Sound('student_recordings/student_' + str(user_info) + '_' + str(sound_controller) + '.wav')
    clear()
    #repeat_text = 'Your recording has been saved.\n\nPress [Space] to listen to your pronunciation and the correct pronunciation.\n\nPress G to repeat your recordings and Press [Backspace] to go to next lesson.'
    repeat_text = 'Tu grabacion a sido guardada.\n\n\nPresiona [Spacio]para escuchar tu pronunciacion y la pronunciacion correcta.\n\nPreciona G para repetir tu gravacion y preciona [Backspace]para ir a siguinte leccion.'
    repeat_print = textrect.render_textrect(repeat_text, english_font, lesson_rect, black, grey, 1)
    screen.blit(repeat_print, lesson_rect.topleft)

def create_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

#Controllers
main = 0
math_controller = 10
report_controller = 0
question_number = 1
correct = 0
time_controller = 0
name_controller = 0
user_name = ''
main_menu_control = -1
nameFont = pygame.font.Font(None, 40)

#sounds NEW CHANGES
correct_sound = pygame.mixer.Sound('sound/ping.wav')
wrong_sound = pygame.mixer.Sound('sound/bong.wav')

#Main Program
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                if main == 1:
                    main = 2
                    mainmenu()
                elif lesson_controller == 3:
                    student_recording.stop()
                    lesson_english.stop()
                    student_recording.play()
                    pygame.time.wait(6000)
                    lesson_english.play()
            elif event.key == K_BACKSPACE:
                if main == 1:
                    main = 0
                    name_controller = 0
                    mainmenu()
                elif lesson_controller == 3:
                    sound_controller += 1
                    lesson_controller = 1
            elif event.key == K_g:
                lesson_controller = 2

    if main == 0:
        mainmenu()
        ###main_msg2 = "Welcome to your School's Curriculum\n\n\nPlease enter your student number below."
        main_msg2 = "Bien venido al Curiculo de tu Escuela\n\n\nFavor de teclear tu numero de alumno en el espcio inidado."
        mainMenuFont2 = pygame.font.Font(None, 30)
        main_rect2 = pygame.Rect((100,200),(600,400))
        main_print2 = textrect.render_textrect(main_msg2, mainMenuFont2, main_rect2, black, grey, 1)
        screen.blit(main_print2, main_rect2.topleft)
        ###main_choice = inputbox.ask_input(screen, "Student Number")
        main_choice = inputbox.ask_input(screen, "Numero de Alumno")

        cursor.execute("SELECT * FROM alumnos")
        student_info = cursor.fetchall()
        for i in student_info:
            if main_choice == str(i[0]):
                main += 1
                user_info = i[0]
                user = i[1] + ' '
                user += i[2]
                user_name = user
                screen.blit(background, (0,0))
                name_controller = 1
                break
        if name_controller != 1:
            mainmenu()
            ###error_name = "You have entered an invalid Student number. Please try again."
            error_name = "Has puesto un numero incorrecto.  Intenta otra vez, por favor."
            errorFont = pygame.font.Font(None, 26)
            error_message = errorFont.render(error_name, 1, black)
            screen.blit(error_message, (120, 200))
            ###pausing = inputbox.ask_input(screen, "Press Enter")
            pausing = inputbox.ask_input(screen, "Oprima Enter")

    elif main == 1:
        mainmenu()
        py_rect = pygame.Rect((screen.get_width() / 4 - 50, 200),(500,500))
        ###welcome_msg = "Welcome back, " + str(user_name) + '.\n\n\nIf this is not your name, press [Backspace].\n\n\nPress [Spacebar] to continue.'
        welcome_msg = "Bien venido de regreso, " + str(user_name) + '.\n\n\nSi eso no es tu nombre, tecles [la retrocedora].\n\n\nOprima [Espaciadora] para continuar.'
        startFont = pygame.font.Font(None, 30)
        welcome = textrect.render_textrect(welcome_msg, startFont, py_rect, black, grey, 1)
        screen.blit(welcome, py_rect.topleft)

    elif main == 2:
        if main_menu_control == -1:
            mainmenu()
            main2_font = pygame.font.Font(None, 32)
            ###category_text = "Please select a category:"
            category_text = "Escoja una categoria, por favor:"
            category_text_rendered = main2_font.render(category_text, 1, black)
            screen.blit(category_text_rendered, (50,100))

            main2_rect_font = pygame.font.Font(None, 28)
            ###main_cat_text = '1. Videos about the many ways to achieve quality lives or diminish the quality of life\n\n\n\n2. Exercises for the development of essential skills'
            main_cat_text = '1. Videos de vidas de buena y mala calidad [Not Available]\n\n\n2. Exercicos para el desarrollo de habilidades basicas\n\n\n3. Change Student Player\n\n\n4. Terminar'
            main_cat_rect = pygame.Rect((100,175),(600,400))
            main_cat_print = textrect.render_textrect(main_cat_text, main2_rect_font, main_cat_rect, black, grey, 0)
            screen.blit(main_cat_print, main_cat_rect.topleft)
            ###main2_choice = inputbox.ask_input(screen, "Your Choice")
            main2_choice = inputbox.ask_input(screen, "Escoja")
            if main2_choice == '1':
                #main_menu_control = 0 Not available yet
                continue
            elif main2_choice == '2':
                main_menu_control = 3
            elif main2_choice == '3':
                main = 0
                name_controller = 0
            elif main2_choice == '4':
                pygame.quit()
                break

        elif main_menu_control == 0: #Page 1
            mainmenu()
            ###cat1_text = 'Please select a video:'
            cat1_text = 'Escoja un video, por favor:'
            main2_font = pygame.font.Font(None, 32)
            cat1_rendered = main2_font.render(cat1_text, 1, black)
            screen.blit(cat1_rendered, (50,100))
            ###cat1_vid = '1. Life in Las Trincheras\n\n2. How people can earn a living\n\n3. How people can stay healthy\n\n4. How people protect themselves from violence\n\n5. How government help and harm their citizens, past and present\n\n6. [Next Page]\n\n7. [Previous Page]'
            cat1_vid = '1. La Vida en Las Trincheras\n\n2. Como la gente gana la vida\n\n3. Como la gente mantiene la salud\n\n4. Como la gente se protegen de la violencia\n\n5. Como los gobiernos ayuda o hacen daño a sus ciudadanos, en el pasado y presente\n\n6. [Proxima pagina]\n\n7. [Pagina anterior]'
            cat1_rect = pygame.Rect((75,150),(700,400))
            main2_rect_font = pygame.font.Font(None, 28)
            cat1_print = textrect.render_textrect(cat1_vid, main2_rect_font, cat1_rect, black, grey, 0)
            screen.blit(cat1_print, cat1_rect.topleft)
            ###cat1_choice = inputbox.ask_input(screen, "Your Choice")
            cat1_choice = inputbox.ask_input(screen, "Escoja")
            if cat1_choice == '6':
                main_menu_control = 1
            elif cat1_choice == '7':
                main_menu_control = -1

        elif main_menu_control == 1: #Page 2
            ###cat1_vid_two = '1. Great industries and organizations, their work, importance and power\n\n2. The Importance and pleasure of Art and Music\n\n3. How people spend their leisure time for pleasure and personal benefit\n\n4. How to protect the world for the benefit of all people\n\n5. War: its history, causes and prevention\n\n6. The world, its form, wealth, climates and its people\n\n6. [Next Page]\n\n7. [Previous Page]'
            cat1_vid_two = '1. Grandes industrias y organizaciones, su trabajo, importancia y poderes\n\n2. La Importancia y placer del Arte y la Musica\n\n3. Como la gente emplean sus tiempos libres para su placer o beneficio\n\n4. Como proteger el ambiente para ek beneficio de todo el mundo\n\n5. La Guerra: su historia, causes y prevenciones\n\n6. El mundo, su forma, riqueza, clima y sus gentes\n\n6. [Next Page]\n\n7. [Previous Page]'
            main2_rect_font = pygame.font.Font(None, 28)
            cat1_rect = pygame.Rect((75,150),(700,400))
            cat1_print_two = textrect.render_textrect(cat1_vid_two, main2_rect_font, cat1_rect, black, grey, 0)
            screen.blit(cat1_print_two, cat1_rect.topleft)
            ###cat1_choice_two = inputbox.ask_input(screen, "Your Choice")
            cat1_choice_two = inputbox.ask_input(screen, "Escoja")
            if cat1_choice_two == '6':
                main_menu_control = 2
            elif cat1_choice_two == '7':
                main_menu_control = 0

        elif main_menu_control == 2: #Page 3
            ###cat1_vid_three = '1. The causes and prevention of unhappiness\n\n2. Important persons and events in the history of Mexico\n\n3. Important persons and events in the history of the world\n\n4. The importance of the human rights\n\n5. The importance of democracy and the dangers of autocracy\n\n6. [Previous Page]'
            cat1_vid_three = '1. Las causes y prevenciones de la infelicidad\n\n2. Importantes personas e eventos en la historia de Mexico\n\n3. Importantes personas e eventos en la historia del mundo\n\n4. La importancia de los derechos humanos\n\n5. La importancia de la democacia y los riesgos de las autocracias\n\n6. [Previous Page]'
            main2_rect_font = pygame.font.Font(None, 28)
            cat1_rect = pygame.Rect((75,150),(700,400))
            cat1_print_three = textrect.render_textrect(cat1_vid_three, main2_rect_font, cat1_rect, black, grey, 0)
            screen.blit(cat1_print_three, cat1_rect.topleft)
            ###cat1_choice_three = inputbox.ask_input(screen, "Your Choice")
            cat1_choice_three = inputbox.ask_input(screen, "Escoja")
            if cat1_choice_three == '6':
                main_menu_control = 1

            #Unfinished
        elif main_menu_control == 3:
            mainmenu()
            cat2_font = pygame.font.Font(None, 32)
            ###cat2_text = 'Exercises for the development of essential skills:'
            cat2_text = 'Ejercicios para el desarrollo de habilidades basicas:'
            cat2_rendered = cat2_font.render(cat2_text, 1, black)
            screen.blit(cat2_rendered, (50,150))

            ###cat2_exercise = '1. Math\n\n2. Spanish\n\n3. Science\n\n4. English\n\n5. Computacion'
            #cat2_exercise = '1. Matematica\n\n2. Espanol\n\n3. Ciencia\n\n4. Ingles\n\n5. Computacion'
            cat2_exercise = '1. Matematica\n\n2. English\n\n3. See Reports\n\n4. [Previous Page]'
            cat2_rect_font = pygame.font.Font(None, 28)
            cat2_rect = pygame.Rect((100,200),(600,400))
            cat2_print = textrect.render_textrect(cat2_exercise, cat2_rect_font, cat2_rect, black, grey, 0)
            screen.blit(cat2_print, cat2_rect.topleft)
            ###cat2_choice = inputbox.ask_input(screen, "Your Choice")
            cat2_choice = inputbox.ask_input(screen, "Escoja")
            if cat2_choice == '1': # Maths
                math_controller = 0
                main_menu_control = -2
            elif cat2_choice == '2': # English
                report_controller = 1
                main_menu_control = -2
            elif cat2_choice == '3':
                report_controller = 2
                main_menu_control = -2
            elif cat2_choice == '4':
                main_menu_control = -1

        if report_controller == 1:
            if not os.path.exists('student_recordings'):
                os.makedirs('student_recordings')
            english_font = pygame.font.Font(None, 30)
            lesson_english = pygame.mixer.Sound('LobowavFiles/L' + str(sound_controller) + 'e.wav')
            lesson_spanish = pygame.mixer.Sound('LobowavFiles/L' + str(sound_controller) + 's.wav')
            lesson_rect = pygame.Rect((100, 200), (600,500))
            clear()
            if sound_controller == 1:
                if lesson_controller == 1:
                    scene_text = u"Escena 1 - Jeyob, Sam, Luna, Teylor y Celeste están sentados en frente de la casa de Luna."
                    scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                    screen.blit(scene_print, lesson_rect.topleft)
                    inputbox.ask_input(screen, "Press Enter")
                    english_text = "Sam: 'Que vamos a hacer hoy?'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho." # (What are we going to do today?)
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Sam: 'What are we going to do today?'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            if sound_controller == 2:
                if lesson_controller == 1:
                    english_text = "Luna: 'Yo quiero ver las cascadas'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Luna: 'I want to see the waterfalls'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 3:
                if lesson_controller == 1:
                    english_text = "Luna: 'al otro lado del bosque.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Luna: 'on the other side of the woods.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 4:
                if lesson_controller == 1:
                    english_text = u"Celeste: 'Yo también.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Celeste: 'Me too.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 5:
                if lesson_controller == 1:
                    english_text = "Jeyob: 'Pero es peligroso en el bosque,'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Jeyob: 'But its dangerous in the woods,'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 6:
                if lesson_controller == 1:
                    english_text = "Jeyob: 'hay lobos.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Jeyob: 'there are wolves.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 7:
                if lesson_controller == 1:
                    english_text = "Teylor: 'No se preocupan,'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Teylor: 'Don´t worry,'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 8:
                if lesson_controller == 1:
                    english_text = "Teylor: 'llevo mi rifle.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Teylor: 'I have my rifle.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 9:
                if lesson_controller == 1:
                    english_text = u"Sam: 'Que bueno, vámonos.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Sam: 'Great, lets go.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 10:
                if lesson_controller == 1:
                    scene_text = "Escena 2 -  Todos están en frente del bosque, listos a entrar."
                    scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                    screen.blit(scene_print, lesson_rect.topleft)
                    inputbox.ask_input(screen, "Press Enter")
                    english_text = "Teylor: 'Listos, todos?'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Teylor: 'Everyone ready?'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 11:
                if lesson_controller == 1:
                    english_text = "Teylor: 'Vamos a cruzar el bosque.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Teylor: 'We´re going to go through the woods.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 12:
                if lesson_controller == 1:
                    english_text = "Jeyoh: 'Pero esta lleno de lobos!'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Jeyoh: 'But its full of wolves!'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 13:
                if lesson_controller == 1:
                    english_text = "Luna: 'Parece que tenemos que atravesar el bosque.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Luna: 'But it looks like we have to go through the woods.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 14:
                if lesson_controller == 1:
                    english_text = "Celeste: 'Ya vamos a entrar.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Celeste: 'Now we are going to enter.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 15:
                if lesson_controller == 1:
                    english_text = "Teylor: 'Ay, a poco le tienes miedo'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Teylor: 'Aye, don´t tell me you are afraid'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 16:
                if lesson_controller == 1:
                    english_text = "Teylor: 'a unos perritos'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Teylor: 'of some little dogs.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 17:
                if lesson_controller == 1:
                    scene_text = u"Ellos no tenían así que entrar en el camino.\n\n Los chicos fueron a vre si no había peligro, y las chicas siguieron.\n\nPronto las chicas tuvieron otro sendero.\n\nCuando las chicas se dieron cuenta de que estaban perdidas se refugiaron en una cabaña abandonada.  "
                    scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                    screen.blit(scene_print, lesson_rect.topleft)
                    inputbox.ask_input(screen, "Press Enter")
                    scene_text = u"Luna llamo a Teylor y le dijo que estaban en la cabaña.\n\nLos chicos fueron pero cuando casi llegaron, escucharon un aullido, voltearon e era un lobo."
                    scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                    screen.blit(scene_print, lesson_rect.topleft)
                    inputbox.ask_input(screen, "Press Enter")
                    english_text = "Celeste: 'No veo los chicos.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Celeste: 'I don´t see the boys.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 18:
                if lesson_controller == 1:
                    english_text = u"Celeste: 'Allí hay una cabaña.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Celeste: 'There is a cabin over there.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 19:
                if lesson_controller == 1:
                    english_text = "Celeste: 'Entramos'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Celeste: 'Lets go in'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 20:
                if lesson_controller == 1:
                    english_text = "Celeste: 'para esperarlos.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Celeste: 'and wait for them.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 21:
                if lesson_controller == 1:
                    scene_text = u"Escena 3 - Se encuentra los chicos en el bosque a la vista de la cabaña."
                    scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                    screen.blit(scene_print, lesson_rect.topleft)
                    inputbox.ask_input(screen, "Press Enter")
                    english_text = u"Sam: 'Oigan, donde están las chicas?'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Sam: 'Hey, where are the girls?'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 22:
                if lesson_controller == 1:
                    english_text = u"Teylor: 'No lo sé.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Teylor: 'I don´t know.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 23:
                if lesson_controller == 1:
                    english_text = u"Sam: 'Vamos a aquella cabaña.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Sam: 'Let´s go to that cabin.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 24:
                if lesson_controller == 1:
                    scene_text = u"Aparece un lobo atrás de un árbol."
                    scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                    screen.blit(scene_print, lesson_rect.topleft)
                    inputbox.ask_input(screen, "Press Enter")
                    english_text = u"Sam: 'Aauuuuu!'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Sam: 'Aauuuuu!'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 25:
                if lesson_controller == 1:
                    scene_text = u"Luna aparece en la puerta de la cabaña y grita."
                    scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                    screen.blit(scene_print, lesson_rect.topleft)
                    inputbox.ask_input(screen, "Press Enter")
                    english_text = u"Luna: 'Teylor, estamos en una cabaña,'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Luna: 'Taylor, we´re in a cabin,'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 26:
                if lesson_controller == 1:
                    english_text = u"Luna: 'rápido escucho lobos.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Luna: 'hurry I hear wolves.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 27:
                if lesson_controller == 1:
                    english_text = u"Teylor: 'Voy para allá.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Teylor: 'I´m coming.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 28:
                if lesson_controller == 1:
                    scene_text = u"Los chicos entraron rápido la cabaña así que le lobo se fue."
                    scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                    screen.blit(scene_print, lesson_rect.topleft)
                    inputbox.ask_input(screen, "Press Enter")
                    english_text = u"Jeyob: 'Ya se fue.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Jeyob: 'He´s gone.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 29:
                if lesson_controller == 1:
                    english_text = u"Sam: 'Seguro?'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Sam: 'Are you sure?'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 30:
                if lesson_controller == 1:
                    english_text = u"Luna: 'Si, miren!'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Luna: 'Yes, look!'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 31:
                if lesson_controller == 1:
                    english_text = u"Luna: 'Se me cayó la bolsa.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Luna: 'I dropped my purse.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 32:
                if lesson_controller == 1:
                    english_text = u"Luna: 'Iré por ella.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Luna: 'I am going to get it.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 33:
                if lesson_controller == 1:
                    english_text = u"Celeste: 'Te acompañamos.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Celeste: 'We´ll go with you.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 34:
                if lesson_controller == 1:
                    scene_text = u"Luna vio que se cayó una bolsa con dinero.\n\nElla, San y Celeste salieron por la bolsa."
                    scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                    screen.blit(scene_print, lesson_rect.topleft)
                    inputbox.ask_input(screen, "Press Enter")
                    english_text = u"Sam: 'Perfecto. Vámonos.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Sam: 'Perfect, Let´s go.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 35:
                if lesson_controller == 1:
                    english_text = u"Luna: 'La tengo!'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Luna: 'I have it!'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 36:
                if lesson_controller == 1:
                    scene_text = u"Mientras muestra la bolsa a todos, regresa el lobo. Sam lo vea."
                    scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                    screen.blit(scene_print, lesson_rect.topleft)
                    inputbox.ask_input(screen, "Press Enter")
                    english_text = u"Sam: 'El lobo, corren, corren!'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Sam: 'The wolf, run, run!'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 37:
                if lesson_controller == 1:
                    scene_text = u"Ellas corrieron pero se traspasaron el lobo Sam se caya.\n\nEl lobo mordió en el pie a Sam."
                    scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                    screen.blit(scene_print, lesson_rect.topleft)
                    inputbox.ask_input(screen, "Press Enter")
                    english_text = u"Sam: 'Se me cayó, socorro!'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Sam: 'I fell down, help!'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 38:
                if lesson_controller == 1:
                    scene_text = u"El lobo alcanza a Sam y le muerde en la pierna."
                    scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                    screen.blit(scene_print, lesson_rect.topleft)
                    inputbox.ask_input(screen, "Press Enter")
                    english_text = u"Lobo: 'Aauuuuu!'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Lobo: 'Aauuuuu!'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 39:
                if lesson_controller == 1:
                    english_text = u"Sam: 'Oooooo, el lobo me mordió!'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Sam: 'Ohhh, the wolf bit me!'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 40:
                if lesson_controller == 1:
                    scene_text = u"Pero Teylor salió y les disparó al lobo."
                    scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                    screen.blit(scene_print, lesson_rect.topleft)
                    inputbox.ask_input(screen, "Press Enter")
                    english_text = u"Sam: 'Muere, maldito! Pas! Pas!'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Sam: 'Die, cursed beast! Bang! Bang!'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 41:
                if lesson_controller == 1:
                    scene_text = u"El lobo corre, cojeando hacia el bosque y desaparece."
                    scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                    screen.blit(scene_print, lesson_rect.topleft)
                    inputbox.ask_input(screen, "Press Enter")
                    english_text = u"Lobo: 'Aauuuuu, aauuuuu, aauuuu!'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Lobo: 'Aauuuuu, aauuuuu, aauuuu!'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 42:
                if lesson_controller == 1:
                    scene_text = u"Jeyob cargó a Sam hasta la cabaña y como Teylor sabia cazar, cargó el rifle y Luna le preguntó,"
                    scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                    screen.blit(scene_print, lesson_rect.topleft)
                    inputbox.ask_input(screen, "Press Enter")
                    english_text = u"Luna: 'A dónde vas,'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Luna: 'Where are you going,'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 43:
                if lesson_controller == 1:
                    english_text = u"Luna: 'no irás a matar al lobo o si?'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Luna: 'are you going kill the wolf or not?'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 44:
                if lesson_controller == 1:
                    english_text = u"Teylor: 'Si voy a matarlo.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Teylor: Yes, I´m going to kill him.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 45:
                if lesson_controller == 1:
                    english_text = u"Teylor: 'No es peligroso.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Teylor: 'He´s not dangerous.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 46:
                if lesson_controller == 1:
                    english_text = u"Luna: 'Mejor vámonos ahora a la cascada.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Luna: 'Good, lets go now to the waterfall.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 47:
                if lesson_controller == 1:
                    english_text = u"Todos juntos: 'Si, si si si.'\n\nOprima enter para ver estas palabras en Ingles y oirlas dicho."
                    lesson1()
                if lesson_controller == 2:
                    english_text = "Todos juntos: 'Yes, yes, yes, yes.'\n\nEscucha el Ingles varias veces hasta que piensas que puedes decirlas mas o menos correctamente.\n\nEntonces opima enter y grabar tu propia voz diciendo las."
                    lesson2()
                if lesson_controller == 3:
                    lesson3()
            elif sound_controller == 48:
                scene_text = u"Todos salen y caminen en le bosque, el lobo les esta viendo de atrás de un árbol."
                scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                screen.blit(scene_print, lesson_rect.topleft)
                inputbox.ask_input(screen, "Press Enter")
                scene_text = u"EL FIN"
                scene_print = textrect.render_textrect(scene_text, english_font, lesson_rect, black, grey, 1)
                screen.blit(scene_print, lesson_rect.topleft)
                inputbox.ask_input(screen, "Press Enter")
                break

        if report_controller == 2:
            clear()
            report_rect = pygame.Rect((100, 125), (600, 500))
            ###five_report = 'Past Five Records\n\n\n'
            five_report = 'Los ultimos cinco intentos\n\n\n'
            number_controller = 1
            cursor.execute("SELECT * FROM game_results ORDER BY Timedate DESC")
            report = cursor.fetchall()
            for i in report:
                if i[1] == user_info and number_controller != 6:
                    ###five_report += str(number_controller) + '. Score: ' + str(i[6]) + '/20  Time: ' + str(i[7]) + ' sec\n\n'
                    if i[8] == '+':
                        five_report += str(number_controller) + '. Game: Addition  Resultado: ' + str(i[6]) + '/20  Tiempo: ' + str(i[7]) + ' sec\n\n'
                    elif i[8] == '-':
                        five_report += str(number_controller) + '. Game: Subtraction  Resultado: ' + str(i[6]) + '/20  Tiempo: ' + str(i[7]) + ' sec\n\n'
                    elif i[8] == '*':
                        five_report += str(number_controller) + '. Game: Multiplication  Resultado: ' + str(i[6]) + '/20  Tiempo: ' + str(i[7]) + ' sec\n\n'
                    number_controller += 1
            number_controller = 1
            finalFont = pygame.font.Font(None, 30)
            report_look = textrect.render_textrect(five_report, finalFont, report_rect, black, grey, 1)
            screen.blit(report_look, report_rect.topleft)
            ###prompt_answer = inputbox.ask_input(screen, "Play Again? [Y/N]")
            prompt_answer = inputbox.ask_input(screen, "Press Enter")
            main_menu_control = 3
            report_controller = 0

    #Math
        if math_controller == 0:
            clear()
            ###title_msg1 = "Hi, I am Professor Computer. Welcome to my Easy Math Game.\n\n\nPress [Enter] to continue."
            #title_msg1 = "Hola, soy el profesor Computo. Bien venido a mi juego de la matematia facil.\n\n\nOprima [Enter] para continuar."
            #msgFont = pygame.font.Font(None, 26)
            #message1_rect = pygame.Rect((100,300),(600,400))
            #message1_print = textrect.render_textrect(title_msg1, msgFont, message1_rect, black, grey, 1)
            #screen.blit(message1_print, message1_rect.topleft)
            #screen.blit(professor_pic,(350, 150))
            ###inputbox.ask_input(screen, "Press Enter")
            #inputbox.ask_input(screen, "Oprima Enter")
            #clear()
            py_rect1 = pygame.Rect((100, 100),(600,400))
            py_rect2 = pygame.Rect((75, 200),(600,400))
            ###welcome_msg = "Welcome back, " + str(user_name) + '.'
            welcome_msg = "Bien venido de regreso, " + str(user_name) + '.\n\nEscoje el juego que quiere.'
            math_choice = "1. Adicion\n\n2. Sustraccion\n\n3. Multiplicacion\n\n4. Division"
            startFont = pygame.font.Font(None, 28)
            startFont2 = pygame.font.Font(None, 26)
            math_append = textrect.render_textrect(math_choice, startFont, py_rect2, black, grey, 0)
            welcome = textrect.render_textrect(welcome_msg, startFont2, py_rect1, black, grey, 1)
            screen.blit(welcome, py_rect1.topleft)
            screen.blit(math_append, py_rect2.topleft)
            ###mathgame_choice = inputbox.ask_input(screen, 'Your Choice')
            mathgame_choice = inputbox.ask_input(screen, 'Escoja')
            if mathgame_choice == '1':
                math_controller = 2
            elif mathgame_choice == '2':
                math_controller = 3
            elif mathgame_choice == '3':
                math_controller = 4
            elif mathgame_choice == '4':
                math_controller = 5

    #Addition
        elif math_controller == 2:
            if time_controller != 1:
                start = time.time()
            time_controller = 1
            clear()
            if question_number > 20:
                end = time.time()
                not_converted = end - start
                elapsed = str(not_converted).split(".")
                final_rect = pygame.Rect((100, 200), (600, 400))
                ### correct_ans = "Your results: " + str(correct) + "/" + str(question_number - 1) + " correct\n\nYour time was " + str(elapsed[0]) + " seconds.\n\nA good time is less than a minute.\n\n"
                correct_ans = "Tus resultados: " + str(correct) + "/" + str(question_number - 1) + " correcto\n\nTu tiempo fue " + str(elapsed[0]) + " segundos.\n\nUn buen tiempo es menos de un minuto.\n\n"
                infoFont = pygame.font.Font(None, 30)
                final_look = textrect.render_textrect(correct_ans, infoFont, final_rect, black, grey, 1)
                screen.blit(final_look, final_rect.topleft)
                now = time.strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""INSERT INTO game_results (Student_ID, Timedate, Game_ID, Gametype, Num_Range_A, Num_Range_B, Thescore, Thetime)
                                VALUES
                                (""" + str(user_info) + """, '""" + str(now) + """', 1, '+', '""" + str(range_a) + """', '""" + str(range_b) + """', """ + str(correct) + """, """ + str(elapsed[0]) + """);""")
                ###inputbox.ask_input(screen, "Press Enter to Continue")
                inputbox.ask_input(screen, "Oprima Enter para Continuar")
                clear()
                report_rect = pygame.Rect((100, 125), (600, 500))
                ###five_report = 'Past Five Records\n\n\n'
                five_report = 'Los ultimos cinco intentos\n\n\n'
                number_controller = 1
                cursor.execute("SELECT * FROM game_results ORDER BY Timedate DESC")
                report = cursor.fetchall()
                for i in report:
                    if i[1] == user_info and number_controller != 6:
                        ###five_report += str(number_controller) + '. Score: ' + str(i[6]) + '/20  Time: ' + str(i[7]) + ' sec\n\n'
                        if i[8] == '+':
                            five_report += str(number_controller) + '. Game: Addition  Resultado: ' + str(i[6]) + '/20  Tiempo: ' + str(i[7]) + ' sec\n\n'
                        elif i[8] == '-':
                            five_report += str(number_controller) + '. Game: Subtraction  Resultado: ' + str(i[6]) + '/20  Tiempo: ' + str(i[7]) + ' sec\n\n'
                        elif i[8] == '*':
                            five_report += str(number_controller) + '. Game: Multiplication  Resultado: ' + str(i[6]) + '/20  Tiempo: ' + str(i[7]) + ' sec\n\n'
                        number_controller += 1
                number_controller = 1
                finalFont = pygame.font.Font(None, 30)
                report_look = textrect.render_textrect(five_report, finalFont, report_rect, black, grey, 1)
                screen.blit(report_look, report_rect.topleft)
                ###prompt_answer = inputbox.ask_input(screen, "Play Again? [Y/N]")
                prompt_answer = inputbox.ask_input(screen, "Jueges otra vez? [S/N]")
                ###if prompt_answer.upper() == 'Y':
                if prompt_answer.upper() == 'S':
                    math_controller = 0
                else:
                    main_menu_control = -1
                    math_controller = -1
                question_number = 1
                correct = 0
                time_controller = 0
            else:
                cursor.execute('SELECT * FROM game_results')
                stats = cursor.fetchall()
                num_range = ''
                the_score = 0
                the_time = 0
                for i in stats:
                    if str(user_info) == str(i[1]) and i[6] > 18 and i[7] < 61 and i[8] == '+':
                        num_range = i[4]
                        the_score = i[6]
                        the_time = i[7]
                new_range_num = num_range.split('-')
                if the_score == 19 and the_time <= 60:
                    numberone = int(new_range_num[0]) + 1
                    numbertwo = int(new_range_num[1]) + 1
                    a = randint(numberone, numbertwo)
                    b = randint(numberone, numbertwo)
                    c = a + b
                    if numbertwo <= 10:
                        bear_controller = 9
                        for i in range(0,a):
                            screen.blit(bear_pic, points1[bear_controller])
                            bear_controller -= 1
                        bear_controller = 0
                        for i in range(0,b):
                            screen.blit(bear_pic, points2[bear_controller])
                            bear_controller += 1
                    range_a = str(numberone) + '-' + str(numbertwo)
                    range_b = str(numberone) + '-' + str(numbertwo)
                elif the_score == 20 and the_time <= 60:
                    numberone = int(new_range_num[0]) + 2
                    numbertwo = int(new_range_num[1]) + 2
                    a = randint(numberone, numbertwo)
                    b = randint(numberone, numbertwo)
                    c = a + b
                    if numbertwo <= 10:
                        bear_controller = 9
                        for i in range(0,a):
                            screen.blit(bear_pic, points1[bear_controller])
                            bear_controller -= 1
                        bear_controller = 0
                        for i in range(0,b):
                            screen.blit(bear_pic, points2[bear_controller])
                            bear_controller += 1
                    range_a = str(numberone) + '-' + str(numbertwo)
                    range_b = str(numberone) + '-' + str(numbertwo)
                else:
                    a = randint(1, 5)
                    b = randint(1, 5)
                    numberone = 0
                    numbertwo = 0
                    c = a + b
                    bear_controller = 9
                    for i in range(0,a):
                        screen.blit(bear_pic, points1[bear_controller])
                        bear_controller -= 1
                    bear_controller = 0
                    for i in range(0,b):
                        screen.blit(bear_pic, points2[bear_controller])
                        bear_controller += 1
                    range_a = "1-5"
                    range_b = "1-5"
                questionFont = pygame.font.Font(None, 72)
                infoFont = pygame.font.Font(None, 30)
                plus = "+"
                question_no = "Q" + str(question_number) + "."
                question_statement = str(a) + ' + ' + str(b) + ' = ? '
                correct_statement = str(correct) + '/' + str(question_number - 1) + ' Correcto'
                name_unrender = "Student's Name: " + str(user_name)
                plus_message = questionFont.render(plus, 1, black)
                message5 = questionFont.render(question_no, 1, black)
                message6 = questionFont.render(question_statement, 1, black)
                message7 = infoFont.render(correct_statement, 1, black)
                name_display = nameFont.render(name_unrender, 1, black)
                screen.blit(name_display, (100,500))
                screen.blit(message5, (30,100))
                screen.blit(message7, (650,100))
                if numbertwo <= 10:
                    screen.blit(message6, (325,300))
                    screen.blit(plus_message, (375,185))
                else:
                    screen.blit(message6, (325,250))
                ###answer = inputbox.ask_input(screen, "Answer")
                answer = inputbox.ask_input(screen, "Respuesta")
                if answer == str(c):
                    correct_sound.play()
                    correct += 1
                    question_number += 1
                else:
                    wrong_sound.play()
                    question_number += 1
                    correctFont = pygame.font.Font(None, 45)
                    ###correct_answer = "No, the correct answer is " + str(c)
                    correct_answer = "No, la respuesta correct es " + str(c)
                    correctMessage = correctFont.render(correct_answer, 1, red)
                    screen.blit(correctMessage, (100, 360))
                    ###pause = inputbox.ask_input(screen, "Please Enter to continue")
                    pause = inputbox.ask_input(screen, "Oprima Enter para continuar")
                screen.blit(background, (0,0))


    #Subtraction

        elif math_controller == 3:
            if time_controller != 1:
                start = time.time()
                time_controller = 1
            mainmenu()
            if question_number > 20:
                end = time.time()
                not_converted = end - start
                elapsed = str(not_converted).split(".")
                final_rect = pygame.Rect((100, 200), (600, 400))
                ###correct_ans = "Your results: " + str(correct) + "/" + str(question_number - 1) + " correct\n\nYour time was " + str(elapsed[0]) + " seconds.\n\nA good time is less than a minute.\n\n"
                correct_ans = "Tus resultados: " + str(correct) + "/" + str(question_number - 1) + " correcto\n\nTu tiempo fue " + str(elapsed[0]) + " segundos.\n\nUn buen tiempo es menos de un minuto.\n\n"
                infoFont = pygame.font.Font(None, 30)
                final_look = textrect.render_textrect(correct_ans, infoFont, final_rect, black, grey, 1)
                screen.blit(final_look, final_rect.topleft)
                now = time.strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""INSERT INTO game_results (Student_ID, Timedate, Game_ID, Gametype, Num_Range_A, Num_Range_B, Thescore, Thetime)
                                VALUES
                                (""" + str(user_info) + """, '""" + str(now) + """', 1, '-', '""" + str(range_a) + """', '""" + str(range_b) + """', """ + str(correct) + """, """ + str(elapsed[0]) + """);""")
                ###inputbox.ask_input(screen, "Press Enter to Continue")
                inputbox.ask_input(screen, "Oprima Enter para Continuar")
                clear()
                report_rect = pygame.Rect((100, 125), (600, 500))
                ###five_report = 'Past Five Records\n\n\n'
                five_report = 'Ultimos cinco resultados\n\n\n'
                number_controller = 1
                cursor.execute("SELECT * FROM game_results ORDER BY Timedate DESC")
                report = cursor.fetchall()
                for i in report:
                    if i[1] == user_info and number_controller != 6:
                        ###five_report += str(number_controller) + '. Score: ' + str(i[6]) + '/20  Time: ' + str(i[7]) + ' sec\n\n'
                        if i[8] == '+':
                            five_report += str(number_controller) + '. Game: Addition  Resultado: ' + str(i[6]) + '/20  Tiempo: ' + str(i[7]) + ' sec\n\n'
                        elif i[8] == '-':
                            five_report += str(number_controller) + '. Game: Subtraction  Resultado: ' + str(i[6]) + '/20  Tiempo: ' + str(i[7]) + ' sec\n\n'
                        elif i[8] == '*':
                            five_report += str(number_controller) + '. Game: Multiplication  Resultado: ' + str(i[6]) + '/20  Tiempo: ' + str(i[7]) + ' sec\n\n'
                        number_controller += 1
                number_controller = 1
                finalFont = pygame.font.Font(None, 30)
                report_look = textrect.render_textrect(five_report, finalFont, report_rect, black, grey, 1)
                screen.blit(report_look, report_rect.topleft)
                ###prompt_answer = inputbox.ask_input(screen, "Play Again? [Y/N]")
                prompt_answer = inputbox.ask_input(screen, "Juegues otra vez? [S/N]")
                ###if prompt_answer.upper() == 'Y':
                if prompt_answer.upper() == 'S':
                    math_controller = 0
                else:
                    main_menu_control = -1
                    math_controller = -1
                question_number = 1
                correct = 0
                time_controller = 0
            else:
                cursor.execute('SELECT * FROM game_results')
                stats = cursor.fetchall()
                num_range = ''
                the_score = 0
                the_time = 0
                for i in stats:
                    if str(user_info) == str(i[1]) and i[6] > 18 and i[7] < 61 and i[8] == "-":
                        num_range = i[4]
                        the_score = i[6]
                        the_time = i[7]
                new_range_num = num_range.split('-')
                if the_score == 19 and the_time <= 60:
                    numberone = int(new_range_num[0]) + 1
                    numbertwo = int(new_range_num[1]) + 1
                    a = randint(numberone, numbertwo)
                    b = randint(numberone, numbertwo)
                    if a > b:
                        c = a - b
                        if numbertwo <= 10:
                            bear_controller = 9
                            for i in range(0,a):
                                screen.blit(bear_pic, points1[bear_controller])
                                bear_controller -= 1
                            bear_controller = 0
                            for i in range(0,b):
                                screen.blit(bear_pic, points2[bear_controller])
                                bear_controller += 1
                        question_statement = str(a) + ' - ' + str(b) + ' = ? '
                    else:
                        c = b - a
                        if numbertwo <= 10:
                            bear_controller = 0
                            for i in range(0,a):
                                screen.blit(bear_pic, points2[bear_controller])
                                bear_controller += 1
                            bear_controller = 9
                            for i in range(0,b):
                                screen.blit(bear_pic, points1[bear_controller])
                                bear_controller -= 1
                        question_statement = str(b) + ' - ' + str(a) + ' = ? '
                    range_a = str(numberone) + '-' + str(numbertwo)
                    range_b = str(numberone) + '-' + str(numbertwo)

                elif the_score == 20 and the_time <= 60:
                    numberone = int(new_range_num[0]) + 2
                    numbertwo = int(new_range_num[1]) + 2
                    a = randint(numberone, numbertwo)
                    b = randint(numberone, numbertwo)
                    if a > b:
                        c = a - b
                        if numbertwo <= 10:
                            bear_controller = 9
                            for i in range(0,a):
                                screen.blit(bear_pic, points1[bear_controller])
                                bear_controller -= 1
                            bear_controller = 0
                            for i in range(0,b):
                                screen.blit(bear_pic, points2[bear_controller])
                                bear_controller += 1
                        question_statement = str(a) + ' - ' + str(b) + ' = ? '
                    else:
                        c = b - a
                        if numbertwo <= 10:
                            bear_controller = 0
                            for i in range(0,a):
                                screen.blit(bear_pic, points2[bear_controller])
                                bear_controller += 1
                            bear_controller = 9
                            for i in range(0,b):
                                screen.blit(bear_pic, points1[bear_controller])
                                bear_controller -= 1
                        question_statement = str(b) + ' - ' + str(a) + ' = ? '
                    range_a = str(numberone) + '-' + str(numbertwo)
                    range_b = str(numberone) + '-' + str(numbertwo)
                else:
                    a = randint(1, 5)
                    b = randint(1, 5)
                    numberone = 0
                    numbertwo = 0
                    if a > b:
                        c = a - b
                        bear_controller = 9
                        for i in range(0,a):
                            screen.blit(bear_pic, points1[bear_controller])
                            bear_controller -= 1
                        bear_controller = 0
                        for i in range(0,b):
                            screen.blit(bear_pic, points2[bear_controller])
                            bear_controller += 1
                        question_statement = str(a) + ' - ' + str(b) + ' = ? '
                    else:
                        c = b - a
                        bear_controller = 0
                        for i in range(0,a):
                            screen.blit(bear_pic, points2[bear_controller])
                            bear_controller += 1
                        bear_controller = 9
                        for i in range(0,b):
                            screen.blit(bear_pic, points1[bear_controller])
                            bear_controller -= 1
                        question_statement = str(b) + ' - ' + str(a) + ' = ? '
                    range_a = "1-5"
                    range_b = "1-5"
                questionFont = pygame.font.Font(None, 72)
                infoFont = pygame.font.Font(None, 30)
                plus = "-"
                question_no = "Q" + str(question_number) + "."
                correct_statement = str(correct) + '/' + str(question_number - 1) + ' Correcto'
                name_unrender = "Nombre del Alumno: " + str(user_name)
                plus_message = questionFont.render(plus, 1, black)
                message5 = questionFont.render(question_no, 1, black)
                message6 = questionFont.render(question_statement, 1, black)
                message7 = infoFont.render(correct_statement, 1, black)
                name_display = nameFont.render(name_unrender, 1, black)
                screen.blit(name_display, (10,10))
                screen.blit(message5, (30,100))
                screen.blit(message7, (650,100))
                if numbertwo <= 10:
                    screen.blit(message6, (325,300))
                    screen.blit(plus_message, (375,185))
                else:
                    screen.blit(message6, (325,250))
                ###answer = inputbox.ask_input(screen, "Answer")
                answer = inputbox.ask_input(screen, "Respuesta")
                if answer == str(c):
                    correct_sound.play()
                    correct += 1
                    question_number += 1
                else:
                    wrong_sound.play()
                    question_number += 1
                    correctFont = pygame.font.Font(None, 35)
                    ###correct_answer = "No, the correct answer is " + str(c)
                    correct_answer = "No, la respuesta correcta es " + str(c)
                    correctMessage = correctFont.render(correct_answer, 1, red)
                    screen.blit(correctMessage, (250, 550))
                    ###pause = inputbox.ask_input(screen, "Please Enter to continue")
                    pause = inputbox.ask_input(screen, "Oprima Enter para continuar")
                screen.blit(background, (0,0))



    #Multiplication


        elif math_controller == 4:
            if time_controller != 1:
                start = time.time()
                time_controller = 1
            mainmenu()
            if question_number > 20:
                end = time.time()
                not_converted = end - start
                elapsed = str(not_converted).split(".")
                final_rect = pygame.Rect((100, 200), (600, 400))
                ###correct_ans = "Your results: " + str(correct) + "/" + str(question_number - 1) + " correct\n\nYour time was " + str(elapsed[0]) + " seconds.\n\nA good time is less than a minute.\n\n"
                correct_ans = "Tus resultados: " + str(correct) + "/" + str(question_number - 1) + " correcto\n\nTu tiempo fue " + str(elapsed[0]) + " segundos.\n\nUn buen tiempo es menos de un minuto.\n\n"
                infoFont = pygame.font.Font(None, 30)
                final_look = textrect.render_textrect(correct_ans, infoFont, final_rect, black, grey, 1)
                screen.blit(final_look, final_rect.topleft)
                now = time.strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""INSERT INTO game_results (Student_ID, Timedate, Game_ID, Gametype, Num_Range_A, Num_Range_B, Thescore, Thetime)
                                VALUES
                                (""" + str(user_info) + """, '""" + str(now) + """', 1, '*', '""" + str(range_a) + """', '""" + str(range_b) + """', """ + str(correct) + """, """ + str(elapsed[0]) + """);""")
                ###inputbox.ask_input(screen, "Press Enter to Continue")
                inputbox.ask_input(screen, "Oprima Enter para continuar")
                clear()
                report_rect = pygame.Rect((100, 125), (600, 500))
                ###five_report = 'Past Five Records\n\n\n'
                five_report = 'Los ultimos cinco resultados\n\n\n'
                number_controller = 1
                cursor.execute("SELECT * FROM game_results ORDER BY Timedate DESC")
                report = cursor.fetchall()
                for i in report:
                    if i[1] == user_info and number_controller != 6:
                        ###five_report += str(number_controller) + '. Score: ' + str(i[6]) + '/20  Time: ' + str(i[7]) + ' sec\n\n'
                        if i[8] == '+':
                            five_report += str(number_controller) + '. Game: Addition  Resultado: ' + str(i[6]) + '/20  Tiempo: ' + str(i[7]) + ' sec\n\n'
                        elif i[8] == '-':
                            five_report += str(number_controller) + '. Game: Subtraction  Resultado: ' + str(i[6]) + '/20  Tiempo: ' + str(i[7]) + ' sec\n\n'
                        elif i[8] == '*':
                            five_report += str(number_controller) + '. Game: Multiplication  Resultado: ' + str(i[6]) + '/20  Tiempo: ' + str(i[7]) + ' sec\n\n'
                        number_controller += 1
                number_controller = 1
                finalFont = pygame.font.Font(None, 30)
                report_look = textrect.render_textrect(five_report, finalFont, report_rect, black, grey, 0)
                screen.blit(report_look, report_rect.topleft)
                ###prompt_answer = inputbox.ask_input(screen, "Play Again? [Y/N]")
                prompt_answer = inputbox.ask_input(screen, "Juega otra vez? [S/N]")
                ###if prompt_answer.upper() == 'Y':
                if prompt_answer.upper() == 'S':
                    math_controller = 0
                else:
                    main_menu_control = -1
                    math_controller = -1
                question_number = 1
                correct = 0
                time_controller = 0
            else:
                cursor.execute('SELECT * FROM game_results')
                stats = cursor.fetchall()
                num_range = ''
                the_score = 0
                the_time = 0
                for i in stats:
                    if str(user_info) == str(i[1]) and i[6] > 18 and i[7] < 61 and i[8] == '*':
                        num_range = i[4]
                        the_score = i[6]
                        the_time = i[7]
                new_range_num = num_range.split('-')
                if the_score == 19 and the_time <= 60:
                    numberone = int(new_range_num[0]) + 1
                    numbertwo = int(new_range_num[1]) + 1
                    a = randint(numberone, numbertwo)
                    b = randint(numberone, numbertwo)
                    c = a * b
                    if numbertwo <= 10:
                        bear_controller = 9
                        for i in range(0,a):
                            screen.blit(bear_pic, points1[bear_controller])
                            bear_controller -= 1
                        bear_controller = 0
                        for i in range(0,b):
                            screen.blit(bear_pic, points2[bear_controller])
                            bear_controller += 1
                    range_a = str(numberone) + '-' + str(numbertwo)
                    range_b = str(numberone) + '-' + str(numbertwo)
                elif the_score == 20 and the_time <= 60:
                    numberone = int(new_range_num[0]) + 2
                    numbertwo = int(new_range_num[1]) + 2
                    a = randint(numberone, numbertwo)
                    b = randint(numberone, numbertwo)
                    c = a * b
                    if numbertwo <= 10:
                        bear_controller = 9
                        for i in range(0,a):
                            screen.blit(bear_pic, points1[bear_controller])
                            bear_controller -= 1
                        bear_controller = 0
                        for i in range(0,b):
                            screen.blit(bear_pic, points2[bear_controller])
                            bear_controller += 1
                    range_a = str(numberone) + '-' + str(numbertwo)
                    range_b = str(numberone) + '-' + str(numbertwo)
                else:
                    a = randint(1, 5)
                    b = randint(1, 5)
                    numberone = 0
                    numbertwo = 0
                    c = a * b
                    bear_controller = 9
                    for i in range(0,a):
                        screen.blit(bear_pic, points1[bear_controller])
                        bear_controller -= 1
                    bear_controller = 0
                    for i in range(0,b):
                        screen.blit(bear_pic, points2[bear_controller])
                        bear_controller += 1
                    range_a = "1-5"
                    range_b = "1-5"
                questionFont = pygame.font.Font(None, 72)
                infoFont = pygame.font.Font(None, 30)
                plus = "X"
                question_no = "Q" + str(question_number) + "."
                question_statement = str(a) + ' X ' + str(b) + ' = ? '
                correct_statement = str(correct) + '/' + str(question_number - 1) + ' Correct'
                name_unrender = "Student's Name: " + str(user_name)
                plus_message = questionFont.render(plus, 1, black)
                message5 = questionFont.render(question_no, 1, black)
                message6 = questionFont.render(question_statement, 1, black)
                message7 = infoFont.render(correct_statement, 1, black)
                name_display = nameFont.render(name_unrender, 1, black)
                screen.blit(name_display, (10,10))
                screen.blit(message5, (30,100))
                screen.blit(message7, (650,100))
                if numbertwo <= 10:
                    screen.blit(message6, (325,300))
                    screen.blit(plus_message, (375,185))
                else:
                    screen.blit(message6, (325,250))
                ###answer = inputbox.ask_input(screen, "Answer")
                answer = inputbox.ask_input(screen, "respuesta")
                if answer == str(c):
                    correct_sound.play()
                    correct += 1
                    question_number += 1
                else:
                    wrong_sound.play()
                    question_number += 1
                    #Changes
                    correctFont = pygame.font.Font(None, 35)
                    ###correct_answer = "No, the correct answer is " + str(c)
                    correct_answer = "No, la respuest correcta es " + str(c)
                    correctMessage = correctFont.render(correct_answer, 1, red)
                    screen.blit(correctMessage, (250, 550))
                    ###pause = inputbox.ask_input(screen, "Please Enter to continue")
                    pause = inputbox.ask_input(screen, "Tecla Enter para continuar")
                screen.blit(background, (0,0))

    #Division
        elif math_controller == 5:
            if time_controller != 1:
                start = time.time()
            time_controller = 1
            clear()
            if question_number > 20:
                end = time.time()
                not_converted = end - start
                elapsed = str(not_converted).split(".")
                final_rect = pygame.Rect((100, 200), (600, 400))
                ### correct_ans = "Your results: " + str(correct) + "/" + str(question_number - 1) + " correct\n\nYour time was " + str(elapsed[0]) + " seconds.\n\nA good time is less than a minute.\n\n"
                correct_ans = "Tus resultados: " + str(correct) + "/" + str(question_number - 1) + " correcto\n\nTu tiempo fue " + str(elapsed[0]) + " segundos.\n\nUn buen tiempo es menos de un minuto.\n\n"
                infoFont = pygame.font.Font(None, 30)
                final_look = textrect.render_textrect(correct_ans, infoFont, final_rect, black, grey, 1)
                screen.blit(final_look, final_rect.topleft)
                now = time.strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""INSERT INTO game_results (Student_ID, Timedate, Game_ID, Gametype, Num_Range_A, Num_Range_B, Thescore, Thetime)
                                VALUES
                                (""" + str(user_info) + """, '""" + str(now) + """', 1, '/', '""" + str(range_a) + """', '""" + str(range_b) + """', """ + str(correct) + """, """ + str(elapsed[0]) + """);""")
                ###inputbox.ask_input(screen, "Press Enter to Continue")
                inputbox.ask_input(screen, "Oprima Enter para Continuar")
                clear()
                report_rect = pygame.Rect((100, 125), (600, 500))
                ###five_report = 'Past Five Records\n\n\n'
                five_report = 'Los ultimos cinco intentos\n\n\n'
                number_controller = 1
                cursor.execute("SELECT * FROM game_results ORDER BY Timedate DESC")
                report = cursor.fetchall()
                for i in report:
                    if i[1] == user_info and number_controller != 6:
                        ###five_report += str(number_controller) + '. Score: ' + str(i[6]) + '/20  Time: ' + str(i[7]) + ' sec\n\n'
                        if i[8] == '+':
                            five_report += str(number_controller) + '. Game: Addition  Resultado: ' + str(i[6]) + '/20  Tiempo: ' + str(i[7]) + ' sec\n\n'
                        elif i[8] == '-':
                            five_report += str(number_controller) + '. Game: Subtraction  Resultado: ' + str(i[6]) + '/20  Tiempo: ' + str(i[7]) + ' sec\n\n'
                        elif i[8] == '*':
                            five_report += str(number_controller) + '. Game: Multiplication  Resultado: ' + str(i[6]) + '/20  Tiempo: ' + str(i[7]) + ' sec\n\n'
                        number_controller += 1
                number_controller = 1
                finalFont = pygame.font.Font(None, 30)
                report_look = textrect.render_textrect(five_report, finalFont, report_rect, black, grey, 1)
                screen.blit(report_look, report_rect.topleft)
                ###prompt_answer = inputbox.ask_input(screen, "Play Again? [Y/N]")
                prompt_answer = inputbox.ask_input(screen, "Jueges otra vez? [S/N]")
                ###if prompt_answer.upper() == 'Y':
                if prompt_answer.upper() == 'S':
                    math_controller = 0
                else:
                    main_menu_control = -1
                    math_controller = -1
                question_number = 1
                correct = 0
                time_controller = 0
            else:
                cursor.execute('SELECT * FROM game_results')
                stats = cursor.fetchall()
                num_range = ''
                the_score = 0
                the_time = 0
                for i in stats:
                    if str(user_info) == str(i[1]) and i[6] > 18 and i[7] < 61 and i[8] == '+':
                        num_range = i[4]
                        the_score = i[6]
                        the_time = i[7]
                    while True:
                        a = randint(1,100)
                        b = randint(1,100)
                        if a >= b:
                            if a % b == 0:
                                c = a / b
                                question_statement = str(a) + ' / ' + str(b) + ' = ? '
                                break
                        else:
                            if b % a == 0:
                                c = b / a
                                question_statement = str(b) + ' / ' + str(a) + ' = ? '
                                break
                    range_a = "1-100"
                    range_b = "1-100"
                questionFont = pygame.font.Font(None, 72)
                infoFont = pygame.font.Font(None, 30)
                question_no = "Q" + str(question_number) + "."
                correct_statement = str(correct) + '/' + str(question_number - 1) + ' Correcto'
                name_unrender = "Student's Name: " + str(user_name)
                message5 = questionFont.render(question_no, 1, black)
                message6 = questionFont.render(question_statement, 1, black)
                message7 = infoFont.render(correct_statement, 1, black)
                name_display = nameFont.render(name_unrender, 1, black)
                screen.blit(name_display, (100,500))
                screen.blit(message5, (30,100))
                screen.blit(message7, (650,100))
                screen.blit(message6, (325,250))
                ###answer = inputbox.ask_input(screen, "Answer")
                answer = inputbox.ask_input(screen, "Respuesta")
                if answer == str(c):
                    correct_sound.play()
                    correct += 1
                    question_number += 1
                else:
                    wrong_sound.play()
                    question_number += 1
                    correctFont = pygame.font.Font(None, 45)
                    ###correct_answer = "No, the correct answer is " + str(c)
                    correct_answer = "No, la respuesta correct es " + str(c)
                    correctMessage = correctFont.render(correct_answer, 1, red)
                    screen.blit(correctMessage, (100, 360))
                    ###pause = inputbox.ask_input(screen, "Please Enter to continue")
                    pause = inputbox.ask_input(screen, "Oprima Enter para continuar")
                screen.blit(background, (0,0))

    pygame.display.update()

cursor.close()
conn.commit()
conn.close()
pygame.quit()
