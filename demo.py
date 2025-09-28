# Step 1
class Employee:
    def determine_weekly_salary(self, weekly_hours, wage):
        salary = 40 * wage
        print("\nThis Employee worked {} hrs. Paid for 40 hrs (no overtime) at ${}/hr = ${}".format(weekly_hours, wage, salary))
        print("========================================\n")

# Step 2
class Contractor(Employee):
    def determine_weekly_salary(self, weekly_hours, wage):
        salary = weekly_hours * wage
        print("\nThis Contractor worked {} hrs. Paid for {} hrs at ${}/hr = ${}".format(weekly_hours, weekly_hours, wage, salary))
        print("========================================\n")

# Step 3
def main():
    hours, wage = 50, 70
    person = Employee()
    person.determine_weekly_salary(hours, wage)

if __name__ == "__main__":
    main()
