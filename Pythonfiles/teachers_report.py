import pyodbc, sys, pygame, time
from pygame.locals import *
from random import randint
import inputbox, textrect, os, win32print, win32api

pygame.init()

#Please change the DBQ accordingly to the access file's location. [DBQ=[HDD Name]/[Folder Name]/students.accdb;]
conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:/Pythonfiles/students.accdb;")
#conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:/pythonfiles/students.accdb;")
cursor = conn.cursor()

#images
bif = "images/image.jpg"

#colors
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
black = (0,0,0)
white = (255,255,255)
grey = (192,192,192)

#Controllers
main = 0
password_prompt = 0
teachers = 0
student_id = 0
students = 0

#Setting up the screen
screen = pygame.display.set_mode((800,600),pygame.FULLSCREEN,32)
#screen = pygame.display.set_mode((800,600), 0, 32)
background = pygame.image.load(bif).convert()
###pygame.display.set_caption('Easy Mathematic Game')
pygame.display.set_caption('Juego Facil de la Matematica')
directory = r'reports'
if not os.path.exists(directory):
    os.makedirs(directory)

def clear():
    screen.blit(background, (0, 0))
    titleFont = pygame.font.Font(None, 50)
    title_str = "Teacher's Database"
    title_rect = pygame.Rect((100,30),(600,100))
    title_print = textrect.render_textrect(title_str, titleFont, title_rect, black, grey, 1)
    screen.blit(title_print, title_rect.topleft)

def win_print(filename, printer_name = None):
    if not printer_name:
        printer_name = win32print.GetDefaultPrinter()
    out = '/d:"%s"' % (printer_name)
    win32api.ShellExecute(0, "print", filename, out, ".", 0)

while True:
    if main == 0:
        if password_prompt == 0:
            clear()
            welcome_msg = "Welcome to Student's Database! Please state if you are a student or teacher [S/T]."
            welcome_font = pygame.font.Font(None, 32)
            welcome_rect = pygame.Rect((100,200),(600,400))
            welcome_print = textrect.render_textrect(welcome_msg, welcome_font, welcome_rect, black, grey, 1)
            screen.blit(welcome_print, welcome_rect.topleft)
            welcome_choice = inputbox.ask_input(screen, "[S/T]")
            if welcome_choice.upper() == 'T':
                clear()
                username_text = "Dear Teachers, Please log in.\n\nEnter your username."
                username_print = textrect.render_textrect(username_text, welcome_font, welcome_rect, black, grey, 1)
                screen.blit(username_print, welcome_rect.topleft)
                username_choice = inputbox.ask_input(screen, "Username")
                clear()
                password_text = "Please enter your password."
                password_print = textrect.render_textrect(password_text, welcome_font, welcome_rect, black, grey, 1)
                screen.blit(password_print, welcome_rect.topleft)
                password_choice = inputbox.ask_password(screen, "Password")
                if password_choice == chr(97) + chr(100) + chr(109) + chr(105) + chr(110):
                    if username_choice == chr(97) + chr(100) + chr(109) + chr(105) + chr(110):
                        teachers = 1
                    else:
                        fail_login_text = "Wrong password or username! Please try again!"
                        fail_login_print = textrect.render_textrect(fail_login_text, welcome_font, welcome_rect, black, grey, 1)
                        screen.blit(fail_login_print, welcome_rect.topleft)
                        tryagain = inputbox.ask_input(screen, "Press Enter")
                else:
                    fail_login_text = "Wrong password or username! Please try again!"
                    fail_login_print = textrect.render_textrect(fail_login_text, welcome_font, welcome_rect, black, grey, 1)
                    screen.blit(fail_login_print, welcome_rect.topleft)
                    tryagain = inputbox.ask_input(screen, "Press Enter")
            elif welcome_choice.upper() == 'S':
                student_text = "Dear Student, please enter your student ID."
                student_print = textrect.render_textrect(student_text, welcome_font, welcome_rect, black, grey, 1)
                screen.blit(student_print, welcome_rect.topleft)
                studentid_prompt = inputbox.ask_input(screen,"Student ID")
                cursor.execute("SELECT * FROM alumnos")
                for i in cursor.fetchall():
                    if studentid_prompt == str(i[0]):
                        student_id = studentid_prompt
                        students = 1

        if students == 1:
            clear()
            main_cat_font = pygame.font.Font(None, 32)
            main_cat_text = 'Please select a choice below:'
            main_cat_text_rendered = main_cat_font.render(main_cat_text, 1, black)
            screen.blit(main_cat_text_rendered, (50,150))

            main_text = '1. View your reports\n\n2. Exit'
            main_rect_font = pygame.font.Font(None, 28)
            main_rect = pygame.Rect((100,200),(600,400))
            main_print = textrect.render_textrect(main_text, main_rect_font, main_rect, black, grey, 0)
            screen.blit(main_print, main_rect.topleft)
            main_choice = inputbox.ask_input(screen, "Escoja")
            if main_choice == '1':
                cursor.execute("""SELECT a.prenombre, a.apellido, g.Student_ID, g.Num_range_A, g.Thescore, g.Thetime, g.Gametype, g.Timedate
                                    FROM alumnos AS a, game_results AS g
                                    WHERE g.Student_ID = a.Alum_ID AND g.Student_ID = """ + str(student_id) + """ ORDER BY g.Gametype, g.Timedate DESC;
                                        """)
                student_report_fetch = cursor.fetchall()
                count_entry = 0
                clear()
                print_text1 = 'Student Name\n\n'
                print_text2 = 'Game Type\n\n'
                print_text3 = 'Num Range\n\n'
                print_text4 = 'Score\n\n'
                print_text5 = 'Time\n\n'
                print_text6 = 'Date\n\n'
                print_font = pygame.font.Font(None, 20)
                print_rect1 = pygame.Rect((25,100), (175, screen.get_height() - 100))
                print_rect2 = pygame.Rect((225,100), (100, screen.get_height() - 100))
                print_rect3 = pygame.Rect((350,100), (100, screen.get_height() - 100))
                print_rect4 = pygame.Rect((475,100), (50, screen.get_height() - 100))
                print_rect5 = pygame.Rect((550,100), (50, screen.get_height() - 100))
                print_rect6 = pygame.Rect((625,100), (150, screen.get_height() - 100))
                for i in student_report_fetch:
                    name_length = str(i[0]) + ' ' + str(i[1])
                    if count_entry > 9:
                        break
                    elif len(name_length) >= 16:
                        if str(i[6]) == '+':
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Addition\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                        elif str(i[6]) == '*':
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Multiplication\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                        else:
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Subtraction\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                    else:
                        if str(i[6]) == '+':
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Addition\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                        elif str(i[6]) == '*':
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Multiplication\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                        else:
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Subtraction\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                    count_entry += 1

                print_completed1 = textrect.render_textrect(print_text1, print_font, print_rect1, black, grey, 1)
                screen.blit(print_completed1, print_rect1.topleft)

                print_completed2 = textrect.render_textrect(print_text2, print_font, print_rect2, black, grey, 1)
                screen.blit(print_completed2, print_rect2.topleft)

                print_completed3 = textrect.render_textrect(print_text3, print_font, print_rect3, black, grey, 1)
                screen.blit(print_completed3, print_rect3.topleft)

                print_completed4 = textrect.render_textrect(print_text4, print_font, print_rect4, black, grey, 1)
                screen.blit(print_completed4, print_rect4.topleft)

                print_completed5 = textrect.render_textrect(print_text5, print_font, print_rect5, black, grey, 1)
                screen.blit(print_completed5, print_rect5.topleft)

                print_completed6 = textrect.render_textrect(print_text6, print_font, print_rect6, black ,grey, 1)
                screen.blit(print_completed6, print_rect6.topleft)

                print_choice = inputbox.ask_input(screen,'Press Enter')
                break


        if teachers == 1:
            clear()
            main_cat_font = pygame.font.Font(None, 32)
            main_cat_text = 'Please select a choice below:'
            main_cat_text_rendered = main_cat_font.render(main_cat_text, 1, black)
            screen.blit(main_cat_text_rendered, (50,150))

            main_text = '1. Report of a single Student\n\n2. Report of all Students\n\n3. Report of Students based on score\n\n4. Exit'
            main_rect_font = pygame.font.Font(None, 28)
            main_rect = pygame.Rect((100,200),(600,400))
            main_print = textrect.render_textrect(main_text, main_rect_font, main_rect, black, grey, 0)
            screen.blit(main_print, main_rect.topleft)
            main_choice = inputbox.ask_input(screen, "Escoja")
            if main_choice == '1':
                clear()
                choice_one_font = pygame.font.Font(None, 30)
                choice_one_text = 'Please enter the student ID.'
                choice_one_rect = pygame.Rect((100,200), (600,400))
                choice_one_print = textrect.render_textrect(choice_one_text, choice_one_font, choice_one_rect, black, grey, 1)
                screen.blit(choice_one_print, choice_one_rect.topleft)
                choice_one_choice = inputbox.ask_input(screen, "Student ID")
                cursor.execute("""SELECT a.prenombre, a.apellido, g.Student_ID, g.Num_range_A, g.Thescore, g.Thetime, g.Gametype, g.Timedate
                                    FROM alumnos AS a, game_results AS g
                                    WHERE g.Student_ID = a.Alum_ID AND g.Student_ID = """ + str(choice_one_choice) + """ ORDER BY g.Gametype, g.Timedate DESC;
                                        """)
                student_report_fetch = cursor.fetchall()
                count_entry = 0
                clear()
                print_text1 = 'Student Name\n\n'
                print_text2 = 'Game Type\n\n'
                print_text3 = 'Num Range\n\n'
                print_text4 = 'Score\n\n'
                print_text5 = 'Time\n\n'
                print_text6 = 'Date\n\n'
                print_font = pygame.font.Font(None, 20)
                print_rect1 = pygame.Rect((25,100), (175, screen.get_height() - 100))
                print_rect2 = pygame.Rect((225,100), (100, screen.get_height() - 100))
                print_rect3 = pygame.Rect((350,100), (100, screen.get_height() - 100))
                print_rect4 = pygame.Rect((475,100), (50, screen.get_height() - 100))
                print_rect5 = pygame.Rect((550,100), (50, screen.get_height() - 100))
                print_rect6 = pygame.Rect((625,100), (150, screen.get_height() - 100))
                student_report = open('reports/student_id_' + str(choice_one_choice) + '.txt', 'w')
                for i in student_report_fetch:
                    name_length = str(i[0]) + ' ' + str(i[1])
                    if count_entry == 0:
                        student_report.write("=" * 49 + ' Student Report ' + "=" * 49 + "\n\n\n\n")
                        student_report.write("\t    Student Name\t   Game Type\t    Num Range\tScore\t    Time\t   Date\n\n")
                    if count_entry > 9:
                        break
                    if len(name_length) >= 16:
                        if str(i[6]) == '+':
                            student_report.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t   Addition\t       ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Addition\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                        elif str(i[6]) == '*':
                            student_report.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t   Multiplication      ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Multiplication\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                        else:
                            student_report.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t   Subtraction\t       ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Subtraction\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                    else:
                        if str(i[6]) == '+':
                            student_report.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t\t   Addition\t       ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Addition\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                        elif str(i[6]) == '*':
                            student_report.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t\t   Multiplication      ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Multiplication\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                        else:
                            student_report.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t\t   Subtraction\t       ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Subtraction\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                        count_entry += 1
                student_report.write('Total Reports: ' + str(count_entry))

                print_completed1 = textrect.render_textrect(print_text1, print_font, print_rect1, black, grey, 1)
                screen.blit(print_completed1, print_rect1.topleft)

                print_completed2 = textrect.render_textrect(print_text2, print_font, print_rect2, black, grey, 1)
                screen.blit(print_completed2, print_rect2.topleft)

                print_completed3 = textrect.render_textrect(print_text3, print_font, print_rect3, black, grey, 1)
                screen.blit(print_completed3, print_rect3.topleft)

                print_completed4 = textrect.render_textrect(print_text4, print_font, print_rect4, black, grey, 1)
                screen.blit(print_completed4, print_rect4.topleft)

                print_completed5 = textrect.render_textrect(print_text5, print_font, print_rect5, black, grey, 1)
                screen.blit(print_completed5, print_rect5.topleft)

                print_completed6 = textrect.render_textrect(print_text6, print_font, print_rect6, black ,grey, 1)
                screen.blit(print_completed6, print_rect6.topleft)

                print_choice = inputbox.ask_input(screen,'Exit')
                student_report.close()
                clear()
                """file_completed = 'Do you want to print the report out? [Y/N]'
                file_completed_print = textrect.render_textrect(file_completed, choice_one_font, choice_one_rect, black, grey, 1)
                screen.blit(file_completed_print, choice_one_rect.topleft)
                print_prompt = inputbox.ask_input(screen,"[Y/N]")
                if print_prompt.upper() == 'Y':
                    win_print('reports/student_id_' + str(choice_one_choice) + '.txt')"""
                break

            elif main_choice == '2':
                clear()
                choice_two_font = pygame.font.Font(None, 30)
                choice_two_text = 'An external text file will be created to store the reports of all the students.\n\nDo you want to continue?'
                choice_two_rect = pygame.Rect((100,200),(600,400))
                choice_two_print = textrect.render_textrect(choice_two_text, choice_two_font, choice_two_rect, black, grey, 1)
                screen.blit(choice_two_print, choice_two_rect.topleft)
                choice_two_choice = inputbox.ask_input(screen, "[Y/N]")
                if choice_two_choice.upper() == 'Y':
                    clear()
                    filename_prompt = 'Please enter the filename of the text file that you desires'
                    filename_print = textrect.render_textrect(filename_prompt, choice_two_font, choice_two_rect, black, grey, 1)
                    screen.blit(filename_print, choice_two_rect.topleft)
                    filename = inputbox.ask_input(screen,"Enter filename")
                    all_students_report = open('reports/' + str(filename) + '.txt', 'w')
                    cursor.execute("""SELECT a.prenombre, a.apellido, g.Student_ID, g.Num_range_A, g.Thescore, g.Thetime, g.Gametype, g.Timedate
                                        FROM alumnos AS a, game_results AS g
                                        WHERE g.Student_ID = a.Alum_ID ORDER BY g.Gametype, g.Timedate DESC;
                                        """)
                    alldata = cursor.fetchall()
                    all_students_report.write("=" * 44 + " Students Report Database " + "=" * 44 + '\n\n')
                    count_entry = 0
                    all_students_report.write("\t    Student Name\t   Game Type\t    Num Range\tScore\t    Time\t   Date\n\n")
                    clear()
                    print_text1 = 'Student Name\n\n'
                    print_text2 = 'Game Type\n\n'
                    print_text3 = 'Num Range\n\n'
                    print_text4 = 'Score\n\n'
                    print_text5 = 'Time\n\n'
                    print_text6 = 'Date\n\n'
                    print_font = pygame.font.Font(None, 20)
                    print_rect1 = pygame.Rect((25,100), (175, screen.get_height() - 100))
                    print_rect2 = pygame.Rect((225,100), (100, screen.get_height() - 100))
                    print_rect3 = pygame.Rect((350,100), (100, screen.get_height() - 100))
                    print_rect4 = pygame.Rect((475,100), (50, screen.get_height() - 100))
                    print_rect5 = pygame.Rect((550,100), (50, screen.get_height() - 100))
                    print_rect6 = pygame.Rect((625,100), (150, screen.get_height() - 100))
                    for i in alldata:
                        name_length = str(i[0]) + ' ' + str(i[1])
                        if count_entry > 9:
                            break
                        if len(name_length) >= 16:
                            if str(i[6]) == '+':
                                all_students_report.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t   Addition\t       ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                                print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                                print_text2 += 'Addition\n\n'
                                print_text3 += str(i[3]) + '\n\n'
                                print_text4 += str(i[4]) + '/20\n\n'
                                print_text5 += str(i[5]) + '\n\n'
                                print_text6 += str(i[7]) + '\n\n'
                            elif str(i[6]) == '*':
                                all_students_report.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t   Multiplication      ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                                print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                                print_text2 += 'Multiplication\n\n'
                                print_text3 += str(i[3]) + '\n\n'
                                print_text4 += str(i[4]) + '/20\n\n'
                                print_text5 += str(i[5]) + '\n\n'
                                print_text6 += str(i[7]) + '\n\n'
                            else:
                                all_students_report.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t   Subtraction\t       ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                                print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                                print_text2 += 'Subtraction\n\n'
                                print_text3 += str(i[3]) + '\n\n'
                                print_text4 += str(i[4]) + '/20\n\n'
                                print_text5 += str(i[5]) + '\n\n'
                                print_text6 += str(i[7]) + '\n\n'
                        else:
                            if str(i[6]) == '+':
                                all_students_report.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t\t   Addition\t       ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                                print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                                print_text2 += 'Addition\n\n'
                                print_text3 += str(i[3]) + '\n\n'
                                print_text4 += str(i[4]) + '/20\n\n'
                                print_text5 += str(i[5]) + '\n\n'
                                print_text6 += str(i[7]) + '\n\n'
                            elif str(i[6]) == '*':
                                all_students_report.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t\t   Multiplication      ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                                print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                                print_text2 += 'Multiplication\n\n'
                                print_text3 += str(i[3]) + '\n\n'
                                print_text4 += str(i[4]) + '/20\n\n'
                                print_text5 += str(i[5]) + '\n\n'
                                print_text6 += str(i[7]) + '\n\n'
                            else:
                                all_students_report.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t\t   Subtraction\t       ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                                print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                                print_text2 += 'Subtraction\n\n'
                                print_text3 += str(i[3]) + '\n\n'
                                print_text4 += str(i[4]) + '/20\n\n'
                                print_text5 += str(i[5]) + '\n\n'
                                print_text6 += str(i[7]) + '\n\n'
                        count_entry += 1
                    all_students_report.write('Total Number of Reports: ' + str(count_entry))
                    print_completed1 = textrect.render_textrect(print_text1, print_font, print_rect1, black, grey, 1)
                    screen.blit(print_completed1, print_rect1.topleft)

                    print_completed2 = textrect.render_textrect(print_text2, print_font, print_rect2, black, grey, 1)
                    screen.blit(print_completed2, print_rect2.topleft)

                    print_completed3 = textrect.render_textrect(print_text3, print_font, print_rect3, black, grey, 1)
                    screen.blit(print_completed3, print_rect3.topleft)

                    print_completed4 = textrect.render_textrect(print_text4, print_font, print_rect4, black, grey, 1)
                    screen.blit(print_completed4, print_rect4.topleft)

                    print_completed5 = textrect.render_textrect(print_text5, print_font, print_rect5, black, grey, 1)
                    screen.blit(print_completed5, print_rect5.topleft)

                    print_completed6 = textrect.render_textrect(print_text6, print_font, print_rect6, black ,grey, 1)
                    screen.blit(print_completed6, print_rect6.topleft)

                    print_choice = inputbox.ask_input(screen,'choice')
                    all_students_report.close()
                    clear()
                    file_completed = 'File has been created successfully. Please check it under /reports/ to view it.\n\nPress Enter to exit. Have a nice day!'
                    file_completed_print = textrect.render_textrect(file_completed, choice_two_font, choice_two_rect, black, grey, 1)
                    screen.blit(file_completed_print, choice_two_rect.topleft)
                    inputbox.ask_input(screen,"Press Enter")
                    break
            elif main_choice == '3':
                clear()
                choice_three_font = pygame.font.Font(None, 30)
                choice_three_text_score = 'Please enter the score you desires.'
                choice_three_rect = pygame.Rect((100,200), (600,400))
                choice_three_print = textrect.render_textrect(choice_three_text_score, choice_three_font, choice_three_rect, black, grey, 1)
                screen.blit(choice_three_print, choice_three_rect.topleft)
                choice_one_score = inputbox.ask_input(screen, "Score")
                clear()
                choice_three_text_operator = 'Please enter the operator you desires.\n\n[1] for [> ' + str(choice_one_score) + ']\n\n[2] for [< ' + str(choice_one_score) + ']\n\n[3] for [= ' + str(choice_one_score) + ']'
                choice_three_rect = pygame.Rect((100,200), (600,400))
                choice_three_print = textrect.render_textrect(choice_three_text_operator, choice_three_font, choice_three_rect, black, grey, 1)
                screen.blit(choice_three_print, choice_three_rect.topleft)
                choice_one_operator = inputbox.ask_input(screen, "Choice")
                if choice_one_operator == '1':
                    cursor.execute("""SELECT a.prenombre, a.apellido, g.Student_ID, g.Num_range_A, g.Thescore, g.Thetime, g.Gametype, g.Timedate
                                    FROM alumnos AS a, game_results AS g
                                    WHERE g.Student_ID = a.Alum_ID AND g.Thescore > """ + str(choice_one_score) + """ ORDER BY g.Gametype, g.Timedate DESC;
                                        """)
                    student_file = open('reports/students_score_morethan' + str(choice_one_score) + '.txt', 'w')
                    student_file.write("=" * 40 + ' Student with Score more than ' + str(choice_one_score) + ' ' + "=" * 40 + '\n\n')
                elif choice_one_operator == '2':
                    cursor.execute("""SELECT a.prenombre, a.apellido, g.Student_ID, g.Num_range_A, g.Thescore, g.Thetime, g.Gametype, g.Timedate
                                    FROM alumnos AS a, game_results AS g
                                    WHERE g.Student_ID = a.Alum_ID AND g.Thescore < """ + str(choice_one_score) + """ ORDER BY g.Gametype, g.Timedate DESC;
                                        """)
                    student_file = open('reports/students_score_lessthan' + str(choice_one_score) + '.txt', 'w')
                    student_file.write("=" * 40 + ' Student with Score less than ' + str(choice_one_score) + ' ' + "=" * 40 + '\n\n')
                else:
                    cursor.execute("""SELECT a.prenombre, a.apellido, g.Student_ID, g.Num_range_A, g.Thescore, g.Thetime, g.Gametype, g.Timedate
                                    FROM alumnos AS a, game_results AS g
                                    WHERE g.Student_ID = a.Alum_ID AND g.Thescore = """ + str(choice_one_score) + """ ORDER BY g.Gametype, g.Timedate DESC;
                                        """)
                    student_file = open('reports/students_score_equalsto' + str(choice_one_score) + '.txt', 'w')
                    student_file.write("=" * 40 + ' Student with Score equals to ' + str(choice_one_score) + ' ' + "=" * 40 + '\n\n')
                unique_student_report = cursor.fetchall()
                count_entry = 0
                student_file.write("\t    Student Name\t   Game Type\t    Num Range\tScore\t    Time\t   Date\n\n")
                clear()
                print_text1 = 'Student Name\n\n'
                print_text2 = 'Game Type\n\n'
                print_text3 = 'Num Range\n\n'
                print_text4 = 'Score\n\n'
                print_text5 = 'Time\n\n'
                print_text6 = 'Date\n\n'
                print_font = pygame.font.Font(None, 20)
                print_rect1 = pygame.Rect((25,100), (175, screen.get_height() - 100))
                print_rect2 = pygame.Rect((225,100), (100, screen.get_height() - 100))
                print_rect3 = pygame.Rect((350,100), (100, screen.get_height() - 100))
                print_rect4 = pygame.Rect((475,100), (50, screen.get_height() - 100))
                print_rect5 = pygame.Rect((550,100), (50, screen.get_height() - 100))
                print_rect6 = pygame.Rect((625,100), (150, screen.get_height() - 100))
                for i in unique_student_report:
                    name_length = str(i[0]) + ' ' + str(i[1])
                    if count_entry > 9:
                        break
                    if len(name_length) >= 16:
                        if str(i[6]) == '+':
                            student_file.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t   Addition\t       ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Addition\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                        elif str(i[6]) == '*':
                            student_file.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t   Multiplication      ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Multiplication\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                        else:
                            student_file.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t   Subtraction\t       ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Subtraction\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                    else:
                        if str(i[6]) == '+':
                            student_file.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t\t   Addition\t       ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Addition\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                        elif str(i[6]) == '*':
                            student_file.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t\t   Multiplication      ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Multiplication\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                        else:
                            student_file.write('\t' + str(i[0]) + ' ' + str(i[1]) + '\t\t   Subtraction\t       ' + str(i[3]) + '\t' + str(i[4]) + '/20\t    ' + str(i[5]) + '\t    ' + str(i[7]) + '\n\n')
                            print_text1 += str(i[0]) + ' ' + str(i[1]) + '\n\n'
                            print_text2 += 'Subtraction\n\n'
                            print_text3 += str(i[3]) + '\n\n'
                            print_text4 += str(i[4]) + '/20\n\n'
                            print_text5 += str(i[5]) + '\n\n'
                            print_text6 += str(i[7]) + '\n\n'
                    count_entry += 1
                student_file.write('Total Reports: ' + str(count_entry))
                print_completed1 = textrect.render_textrect(print_text1, print_font, print_rect1, black, grey, 1)
                screen.blit(print_completed1, print_rect1.topleft)

                print_completed2 = textrect.render_textrect(print_text2, print_font, print_rect2, black, grey, 1)
                screen.blit(print_completed2, print_rect2.topleft)

                print_completed3 = textrect.render_textrect(print_text3, print_font, print_rect3, black, grey, 1)
                screen.blit(print_completed3, print_rect3.topleft)

                print_completed4 = textrect.render_textrect(print_text4, print_font, print_rect4, black, grey, 1)
                screen.blit(print_completed4, print_rect4.topleft)

                print_completed5 = textrect.render_textrect(print_text5, print_font, print_rect5, black, grey, 1)
                screen.blit(print_completed5, print_rect5.topleft)

                print_completed6 = textrect.render_textrect(print_text6, print_font, print_rect6, black ,grey, 1)
                screen.blit(print_completed6, print_rect6.topleft)

                print_choice = inputbox.ask_input(screen,'choice')
                student_file.close()
                clear()
                file_completed = 'File has been created successfully. Please check it under /reports/ to view it.\n\nPress Enter to exit. Have a nice day!'
                file_completed_print = textrect.render_textrect(file_completed, choice_three_font, choice_three_rect, black, grey, 1)
                screen.blit(file_completed_print, choice_three_rect.topleft)
                inputbox.ask_input(screen,"Press Enter")
                break
            elif main_choice == 4:
                break

    pygame.display.update()

pygame.quit()
