import sys
import uuid
import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QMessageBox, QComboBox,
    QTabWidget, QFormLayout, QHBoxLayout, QFrame
)
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Qt

# Unique and modern UI for the banking system
class BankAccount:
    def __init__(self, account_holder_name, initial_balance=0.0, account_type="Savings"):
        self.account_number = str(uuid.uuid4())[:8]
        self.account_holder_name = account_holder_name
        self.balance = initial_balance
        self.account_type = account_type
        self.transactions = []
        self.creation_date = datetime.date.today()

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(("Deposit", amount, datetime.datetime.now()))
        return f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}"

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds."
        self.balance -= amount
        self.transactions.append(("Withdraw", -amount, datetime.datetime.now()))
        return f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}"

    def get_details(self):
        return f"Account: {self.account_number}\nHolder: {self.account_holder_name}\nType: {self.account_type}\nBalance: ${self.balance:.2f}\nCreated: {self.creation_date}"

    def transaction_history(self):
        if not self.transactions:
            return "No transactions yet."
        return "\n".join([f"{t[2]} - {t[0]}: ${t[1]:.2f}" for t in self.transactions])


class BankingSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self, name, balance, account_type):
        acc = BankAccount(name, balance, account_type)
        self.accounts[acc.account_number] = acc
        return acc.account_number

    def get_account(self, acc_number):
        return self.accounts.get(acc_number)

    def delete_account(self, acc_number):
        return self.accounts.pop(acc_number, None)


class BankingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Banking System")
        self.setGeometry(200, 200, 600, 400)
        self.bank = BankingSystem()
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create Tabs
        self.create_account_tab = QWidget()
        self.manage_account_tab = QWidget()
        self.transaction_tab = QWidget()

        self.tabs.addTab(self.create_account_tab, "Create Account")
        self.tabs.addTab(self.manage_account_tab, "Account Details")
        self.tabs.addTab(self.transaction_tab, "Transactions")

        self.setup_create_account_tab()
        self.setup_manage_account_tab()
        self.setup_transaction_tab()

    def setup_create_account_tab(self):
        layout = QVBoxLayout()
        form = QFormLayout()
        
        self.name_input = QLineEdit()
        self.balance_input = QLineEdit()
        self.account_type = QComboBox()
        self.account_type.addItems(["Savings", "Checking"])
        
        form.addRow("Name:", self.name_input)
        form.addRow("Initial Balance:", self.balance_input)
        form.addRow("Account Type:", self.account_type)
        
        self.create_btn = QPushButton("Create Account")
        self.create_btn.clicked.connect(self.create_account)
        
        layout.addLayout(form)
        layout.addWidget(self.create_btn)
        self.create_account_tab.setLayout(layout)

    def setup_manage_account_tab(self):
        layout = QVBoxLayout()
        
        self.account_number_input = QLineEdit()
        self.account_number_input.setPlaceholderText("Enter Account Number")
        self.fetch_details_btn = QPushButton("Get Details")
        self.fetch_details_btn.clicked.connect(self.show_account_details)
        self.account_details_display = QTextEdit()
        self.account_details_display.setReadOnly(True)
        
        layout.addWidget(QLabel("Account Number:"))
        layout.addWidget(self.account_number_input)
        layout.addWidget(self.fetch_details_btn)
        layout.addWidget(self.account_details_display)
        self.manage_account_tab.setLayout(layout)

    def setup_transaction_tab(self):
        layout = QVBoxLayout()
        
        self.account_number_txn_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.deposit_btn = QPushButton("Deposit")
        self.withdraw_btn = QPushButton("Withdraw")
        self.txn_display = QTextEdit()
        self.txn_display.setReadOnly(True)
        
        self.deposit_btn.clicked.connect(self.deposit)
        self.withdraw_btn.clicked.connect(self.withdraw)
        
        layout.addWidget(QLabel("Account Number:"))
        layout.addWidget(self.account_number_txn_input)
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.amount_input)
        layout.addWidget(self.deposit_btn)
        layout.addWidget(self.withdraw_btn)
        layout.addWidget(self.txn_display)
        
        self.transaction_tab.setLayout(layout)

    def create_account(self):
        name = self.name_input.text()
        balance = self.balance_input.text()
        acc_type = self.account_type.currentText()
        
        if not name or not balance.isdigit():
            QMessageBox.warning(self, "Input Error", "Invalid input!")
            return
        
        acc_number = self.bank.create_account(name, float(balance), acc_type)
        QMessageBox.information(self, "Success", f"Account Created! Account Number: {acc_number}")
        self.name_input.clear()
        self.balance_input.clear()

    def show_account_details(self):
        acc_number = self.account_number_input.text()
        account = self.bank.get_account(acc_number)
        
        if account:
            self.account_details_display.setText(account.get_details())
        else:
            QMessageBox.warning(self, "Not Found", "Account not found!")

    def deposit(self):
        self.process_transaction("Deposit")

    def withdraw(self):
        self.process_transaction("Withdraw")

    def process_transaction(self, txn_type):
        acc_number = self.account_number_txn_input.text()
        amount_text = self.amount_input.text()
        
        if not amount_text.isdigit():
            QMessageBox.warning(self, "Input Error", "Invalid amount!")
            return
        
        account = self.bank.get_account(acc_number)
        if account:
            amount = float(amount_text)
            message = account.deposit(amount) if txn_type == "Deposit" else account.withdraw(amount)
            self.txn_display.setText(message)
        else:
            QMessageBox.warning(self, "Not Found", "Account not found!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BankingApp()
    window.show()
    sys.exit(app.exec())