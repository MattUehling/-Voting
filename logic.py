import csv
import os

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow
from gui import Ui_MainWindow
from logic_login import Logic_Login


class Logic(QMainWindow, Ui_MainWindow):
    additionSuccessful = pyqtSignal()

    def __init__(self, logic_login: Logic_Login) -> None:
        """Initialize the Logic instance."""
        super().__init__()
        self.setupUi(self)
        self.submit_button.clicked.connect(lambda: self.submit())
        self.exit_button.clicked.connect(lambda: self.clear())
        self.result_button.clicked.connect(lambda: self.results())
        self.logic_login = logic_login
        self.username: str = self.logic_login.getUsername()
        self.id: str = self.logic_login.getId()
        if self.username == 'Admin':
            self.submit_button.hide()
            self.result_button.show()
        else:
            self.submit_button.show()
            self.result_button.hide()

    def submit(self) -> None:
        """Submit the vote based on the selected candidate."""
        if self.candidate1_button.isChecked():
            self.writeVote('John')
        elif self.candidate2_button.isChecked():
            self.writeVote('Jane')
        elif self.candidate3_button.isChecked():
            self.writeVote(self.other_input.text().strip())
        else:
            self.result_text.setText("Please select one candidate.")
        self.clear()

    def writeVote(self, candidate_choice: str) -> None:
        """Write the vote to the CSV file."""
        temp_file = 'temp.csv'
        fieldnames = ['Username', 'Id', 'Candidate']

        with open('Output.csv', 'r', newline='') as input_file, \
                open(temp_file, 'w', newline='') as output_file:

            reader = csv.DictReader(input_file)
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            print("Username:", self.username)
            print("ID:", self.id)
            for row in reader:
                if row['Username'] == self.username and row['Id'] == self.id:
                    row['Candidate'] = f"{candidate_choice}"
                writer.writerow(row)

        try:
            os.replace(temp_file, 'Output.csv')
            self.result_text.setText("Vote recorded successfully.")
        except Exception as e:
            print(f"Error replacing file: {e}")
            self.result_text.setText("Error recording vote. Please try again.")
            self.error_message.setStyleSheet("color: red")

        self.result_text.setText("Vote recorded successfully.")

    def clear(self) -> None:
        """Clear the selected candidate and emit additionSuccessful signal."""
        self.candidate1_button.setChecked(False)
        self.candidate2_button.setChecked(False)
        self.additionSuccessful.emit()

    def results(self) -> None:
        """Show the current vote count."""
        if self.username == 'Admin':
            self.submit_button.hide()
            candidate_votes = {'John': 0, 'Jane': 0}

            with open('output.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    candidate_name = row['Candidate'].strip()
                    if candidate_name != '':
                        candidate_votes[candidate_name] = candidate_votes.get(candidate_name, 0) + 1

            result_text = 'The current votes are:\n'
            for candidate, votes in candidate_votes.items():
                result_text += f'{candidate}: {votes}\n'

            self.result_text.setText(result_text)
        else:
            self.result_text.setText("Invalid authority")
            self.result_text.setStyleSheet("color: red")
