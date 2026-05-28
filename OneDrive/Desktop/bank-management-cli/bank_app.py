import datetime
import json

class Transaction:
    """A Record Of A Transaction (date, type, amount, balance_after)"""
    def __init__(self, trans_type, amount, balance_after):
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.type = trans_type
        self.amount = amount
        self.balance_after = balance_after

    def display(self):
        return f"{self.date} | {self.type:8} | {self.amount:8.2f} | Balance: {self.balance_after:.2f}"

class BankAccount:
    """Bank Account class with encapsulation"""
    def __init__(self, account_number, holder_name, initial_balance=0):
        self.account_number = account_number
        self.holder_name = holder_name
        self.__balance = initial_balance
        self.__transactions = []

        if initial_balance > 0:
            self.__add_transaction("Deposit", initial_balance)

    def __add_transaction(self, trans_type, amount):
        """private method to add transaction record"""
        trans = Transaction(trans_type, amount, self.__balance)
        self.__transactions.append(trans)

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")  
            return False
        self.__balance += amount
        self.__add_transaction("Deposit", amount)
        print (f"Deposited Rs:{amount:.2f}.New balance: Rs:{self.__balance:.2f}")
        return True
    
    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if amount > self.__balance:
            print(f" Insufficient balance! Available: Rs:{self.__balance:.2f}")
            return False
        self.__balance -= amount
        self.__add_transaction("Withdraw", amount)
        print(f"Withdraw Rs:{amount:.2f}.New balance Rs:{self.__balance:.2f}")
        return True
    
    def check_balance(self):
        print(f" Account {self.account_number} | {self.holder_name} | Balance: Rs:{self.__balance:.2f}")
        return self.__balance
    
    def get_account_info(self):
        return {
            "account_number": self.account_number,
            "holder_name": self.holder_name,
            "balance": self.__balance

        }
    
    def show_transactions(self, limit=10):
        for t in self.__transactions[-limit:]:
            print("  " + t.display())

class Bank:
    """Bank class manages multiple accounts"""
    def __init__(self, name):
        self.name = name 
        self.__accounts = {}
        self.file_name = "bank_data.json"
        self.load_data()

    def create_account(self, holder_name, initial_deposit=0):
        """Create new account with unique account number"""
        acc_num = f"ACC{len(self.__accounts)+1:04d}"
        account = BankAccount(acc_num, holder_name, initial_deposit)
        self.__accounts[acc_num] = account
        self.save_data()
        print(f" Account created successfully!")
        print(f" Account Number: {acc_num}")
        print(f" Holder: {holder_name}")
        print(f" Initial Balance: Rs:{initial_deposit:.2f}")
        return acc_num
    
    def get_account(self, account_number):
        """Return account object if exists, else None"""
        return self.__accounts.get(account_number)
    
    def total_balance(self):
        total = sum(acc.get_account_info()['balance']
                    for acc in self.__accounts.values())
        print(f" {self.name} Total Bank Balance: Rs{total:.2f}")
        return total
    
    def list_accounts(self):
        print(f"\n All Accounts in {self.name}")
        if not self.__accounts:
            print("No Accounts Yet.")
            return
        for acc_num, acc in self.__accounts.items():
            info = acc.get_account_info()
            print(f" {acc_num} | {info['holder_name']:15} | Rs:{info['balance']:.2f}")

    def save_data(self):
        data = {}
        for acc_num, acc in self.__accounts.items():
            info = acc.get_account_info()
            data[acc_num] = {
                 "holder_name": info["holder_name"],
                 "balance": info["balance"]
            }
        with open(self.file_name, "w") as file:
             json.dump(data, file, indent=4)
    def load_data(self):

        try:
            with open(self.file_name, "r") as file:
                data = json.load(file)
            for acc_num, details in data.items():
                account = BankAccount(
                    acc_num,
                    details["holder_name"],
                    details["balance"]
                )

                self.__accounts[acc_num] = account

        except FileNotFoundError:
            pass
 
def main():
    bank = Bank("Python Bank")
    print("=" * 50)
    print(" WELCOME TO PYTHON BANK MANAGEMENT SYSTEM ")
    print("=" * 50)

    while True:
        print("\n--- MAIN MENU ---")
        print("1. Create New Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. View Transaction History")
        print("6. List All Accounts")
        print("7. Total Bank Balance")
        print("8. Exit")

        choice = input("\n Enter Your Choice (1-8): ").strip()

        if choice == "1":
            name = input("Enter account holder name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            try:
                init_bal = float(input("Initial deposit amount (Rs): "))
                if init_bal < 0:
                    print("Initial deposit cannot be negative.")
                    continue
            except ValueError:
                print("Invalid ammount. please enter a number.")
                continue
            bank.create_account(name, init_bal)

        elif choice == "2":
            acc_num = input("Enter account number: ").strip()
            account = bank.get_account(acc_num)
            if not account:
                print("Account Not Found.")
                continue
            try:
                amount = float(input("Deposit ammount (Rs): "))
            except ValueError:
                print("Invalid amount.")
                continue
            account.deposit(amount)
            bank.save_data()

        elif choice == "3":
            acc_num = input("Enter account number: ").strip()
            account = bank.get_account(acc_num)
            if not account:
                print("Account Not Found.")
                continue
            try:
                amount = float(input("Withdraw amount (Rs): "))
            except ValueError:
                print("Invalid amount.")
                continue
            account.withdraw(amount)
            bank.save_data()

        elif choice == "4":
            acc_num = input("Enter account number: ").strip()
            account = bank.get_account(acc_num)
            if not account:
                print("Account not found.")
                continue
            account.check_balance()
        
        elif choice == "5":
            acc_num = input("Enter account number: ").strip()
            account = bank.get_account(acc_num)
            if not account:
                print("Account not found.")
                continue
            account.show_transactions()
        
        elif choice == "6":
            bank.list_accounts()

        elif choice == "7":
            bank.total_balance()

        elif choice == "8":
            print("\n Thank you for using Python Bank. Have a great day!")
            break
       
        else:
            print("Invalid choice. please enter 1 to 8.")

if __name__ == "__main__":
    main()


            
        





    

            
            



    
    
