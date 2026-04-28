import csv
import pandas as pd


class InvalidLoanError(Exception):
    pass

def compute_emi(P, R, N):
    r = R / 1200
    return (P * r * (1 + r)**N) / ((1 + r)**N - 1)


def validate_inputs(P, R, N):
    if P <= 0:
        raise InvalidLoanError("Loan amount must be positive")
    if R <= 0:
        raise InvalidLoanError("Interest rate must be positive")
    if N <= 0:
        raise InvalidLoanError("Tenure must be positive")

class Loan:
    def __init__(self, principal, rate, tenure):
        validate_inputs(principal, rate, tenure)

        self.principal = principal
        self.rate = rate
        self.tenure = tenure
        self.emi = compute_emi(principal, rate, tenure)

    def summary(self):
        return (self.principal, self.rate, self.tenure, self.emi)

    def display(self):
        print(f"\nLoan: {self.principal}")
        print(f"Rate: {self.rate}%")
        print(f"Tenure: {self.tenure} months")
        print(f"EMI: {self.emi:.2f}")

class Prepayment(Loan):
    def apply_prepayment(self, amount):
        if amount > self.principal:
            raise InvalidLoanError("Prepayment exceeds loan")

        self.principal -= amount
        self.emi = compute_emi(self.principal, self.rate, self.tenure)
def save_loan_to_csv(loan):
    with open("loans.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(loan.summary())


def load_loans_from_csv():
    try:
        with open("loans.csv", "r") as f:
            reader = csv.reader(f)
            print("\nSaved Loans:")
            for row in reader:
                print(row)
    except FileNotFoundError:
        print("No saved data found.")

def generate_amortization(loan):
    data = []
    balance = loan.principal
    r = loan.rate / 1200
    emi = loan.emi

    for month in range(1, loan.tenure + 1):
        interest = balance * r
        principal = emi - interest
        balance -= principal

        data.append([month, principal, interest, max(balance, 0)])

    df = pd.DataFrame(data, columns=["Month", "Principal", "Interest", "Balance"])
    return df

loans = []
unique_rates = set()
def main():
    while True:
        print("\n====== EMI MASTER ======")
        print("1. Add Loan")
        print("2. View Loans")
        print("3. Save Loans")
        print("4. Load Loans")
        print("5. Amortization Table")
        print("6. Apply Prepayment")
        print("7. Exit")

        choice = input("Enter choice: ")
        try:

            if choice == "1":
                P = float(input("Loan Amount: "))
                R = float(input("Interest Rate (%): "))
                N = int(input("Tenure (months): "))
loan = Loan(P, R, N)
                loans.append(loan)
                unique_rates.add(R)

                print("Loan added successfully!")

            elif choice == "2":
                if not loans:
                    print("No loans available.")
                for loan in loans:
                    loan.display()
                print("Unique Rates:", unique_rates)

            elif choice == "3":
                for loan in loans:
                    save_loan_to_csv(loan)
                print("Saved to CSV.")

            elif choice == "4":
                load_loans_from_csv()

            elif choice == "5":
                if not loans:
                    print("No loans to analyze.")
                    continue

                index = int(input("Select loan index (0-based): "))
                df = generate_amortization(loans[index])
                print(df.head(12))  # show first year

            elif choice == "6":
                index = int(input("Select loan index: "))
                amount = float(input("Prepayment amount: "))

                prepay = Prepayment(
                    loans[index].principal,
                    loans[index].rate,
                    loans[index].tenure
                )

                prepay.apply_prepayment(amount)
                prepay.display()
elif choice == "7":
                print("Exiting EMI MASTER...")
                break

            else:
                print("Invalid choice.")

        except Exception as e:
            print("Error:", e)
if __name__ == "__main__":
    main()
