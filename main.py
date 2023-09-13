import csv
import json
import random
import os

class Quiz:
    def __init__(self):
    # reads preferences from config.json
        with open ("config.json", "r") as file:
            settings = json.load(file)

            self.quiz_mode = settings["quiz_mode"]
            self.vocab_list = settings["vocab_list"]
            self.shuffle = settings["shuffle"]
            self.record_incorrect_answers = settings["record_incorrect_answers"]
            self.overwrite_old_answersheet_on_new_quiz = settings["overwrite_old_answersheet_on_new_quiz"]
            self.show_final_report = settings["show_final_report"]
            self.create_new_quiz_with_incorrect_answers = settings["create_new_quiz_with_incorrect_answers"]
            self.new_csv_file_name = settings["new_csv_file_name"]

            # checks config file for errors
            self.validate_config()

            file.close()

        terms = []

        # adds questions to terms
        with open(self.vocab_list, "r") as file:
            reader = csv.DictReader(file, delimiter=":")
            for row in reader:
                terms.append(row)

        self.terms = terms

        self.term_count = len(self.terms)

        self.incorrect_answers = []

        # creates a tuple used by quiz 
        if self.quiz_mode == "terms":
            self.quiz_settings = ("term", "definition")
        else:
            self.quiz_settings = ("definition", "term")

        # shuffles terms
        if self.shuffle == True:
            random.shuffle(self.terms)

        # number of questions that the user got incorrect
        self.incorrect_count = 0

        self.show_settings()

    def quiz(self):
        self.clear_console()

        if (self.overwrite_old_answersheet_on_new_quiz == True):
            with open ("incorrect answers.txt", "w") as file:
                file.truncate(0)

        while len(self.terms):
            term = self.terms[0]
            answer = input(term[self.quiz_settings[0]] + "\n")

            if (answer.replace(" ", "").lower() != term[self.quiz_settings[1]].replace(" ", "").lower()): # incorrect answer
                
                if (self.record_incorrect_answers == True):
                    self.save_answer(term[self.quiz_settings[0]], answer, term[self.quiz_settings[1]])

                    self.incorrect_count += 1

                if (self.create_new_quiz_with_incorrect_answers == True):
                    self.incorrect_answers.append(term)

                print("correct answer:" + term[self.quiz_settings[1]] + "\n")
            else: # correct answer (simply just clears the line)
                self.clear_console()

            self.terms.remove(term)

        # on quiz end
        if (self.record_incorrect_answers == True):
            print("accuracy:" + str(self.term_count - self.incorrect_count) + "/" + str(self.term_count))
            print("percentage:" + str(((self.term_count - self.incorrect_count) / self.term_count) * 100)[:-2])

        if (self.create_new_quiz_with_incorrect_answers == True):
            self.generate_new_vocab_list()

        user_input = input('hit "enter" to exit \n')
        exit()

    def generate_new_vocab_list(self):
        with open (self.new_csv_file_name, "a") as file:
            file.truncate(0)

            file.write("term:definition\n")

            for answer in self.incorrect_answers:
                row = answer["term"] + ":" + answer["definition"] + "\n"
                file.write(row)

        file.close()


    def show_settings(self):
        print("quiz_mode: " + self.quiz_mode)
        print("vocab_list: " + self.vocab_list)
        print("shuffle: " + str(self.shuffle))  
        print("record_incorrect_answers: " + str(self.record_incorrect_answers)) 
        print("overwrite_old_answersheet_on_new_quiz: " + str(self.overwrite_old_answersheet_on_new_quiz))
        print("show_final_report: " + str(self.show_final_report))
        print("create_new_quiz_with_incorrect_answers: " + str(self.create_new_quiz_with_incorrect_answers))

        user_input = input('if settings are incorrect, type "quit". Otherwise hit "enter" \n')

        if (user_input.replace(" ", "").lower() == "quit"):
            exit()

    def save_answer(self, term, recordedAnswer, correctAnswer):
        with open("incorrect answers.txt", "a+") as file:
            file.write("Question:" + term + "\n" + "your answer:" + recordedAnswer + "\n" + "correct answer:" + correctAnswer + "\n \n")
            file.close()

    def validate_config(self):
        # error checking
        if (self.quiz_mode != "terms" and self.quiz_mode != "definitions"):
            self.write_error('quiz_mode can only be "terms" or "definitions" \n \n')
            exit()

        if (self.shuffle != True and self.shuffle != False):
            self.write_error('shuffle can only be "true" or "false" \n \n')
            exit()

        if (self.record_incorrect_answers != True and self.record_incorrect_answers != False):
            self.write_error('record_incorrect_answers can only be "true" or "false" \n \n')
            exit()
        
        if (self.overwrite_old_answersheet_on_new_quiz != True and self.overwrite_old_answersheet_on_new_quiz != False):
            self.write_error('overwrite_old_answersheet_on_new_quiz can only be "true" or "false" \n \n')
            exit()

        if (self.show_final_report != True and self.show_final_report != False):
            self.write_error('show_final_report can only be "true" or "false" \n \n')
            exit()

        if (self.create_new_quiz_with_incorrect_answers != True and self.create_new_quiz_with_incorrect_answers != False):
            self.write_error('create_new_quiz_with_incorrect_answers can only be "true" or "false" \n \n')
            exit()

        if (os.path.isfile(self.vocab_list) != True):
            self.write_error("vocab list must be an existing csv file \n \n")
            exit()

    def write_error(self, error):
        with open ("error_log.txt", "a") as file:
            file.write(error)

    def clear_console(self):
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

quiz = Quiz()
quiz.quiz()