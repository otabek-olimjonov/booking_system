import random
import pandas as pd

def generate_monthly_income_distribution(total_annual_salary, company_name, year):
    # Total annual salary to monthly salary
    monthly_salary = total_annual_salary / 12
    # Generate random monthly salaries while ensuring total equals annual salary
    monthly_salaries = [round(random.uniform(monthly_salary * 0.8, monthly_salary * 1.2), -3) for _ in range(12)]
    
    # Adjust the total to equal the annual salary
    total_generated = sum(monthly_salaries)
    difference = total_annual_salary - total_generated
    
    # Adjust the first month to balance the total
    monthly_salaries[0] += difference
    
    # Prepare the data
    data = {
        "Year": [year] * 12,
        "Month": [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ],
        "Enterprise (Organization)": [company_name] * 12,
        "Accrued wage (UZS)": [round(salary, -3) for salary in monthly_salaries],
        "Personal Income Tax (PIT)": [round(salary * 0.12, -3) for salary in monthly_salaries],
        "INPS": [0] * 12
    }
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    total_pit = df["Personal Income Tax (PIT)"].sum()
    
    return df, total_annual_salary, total_pit

# Example usage
total_annual_salary = 165000000  # Example total annual salary in UZS
company_name = "Example Company"
year = 2024

monthly_income_distribution, total_salary, total_pit = generate_monthly_income_distribution(total_annual_salary, company_name, year)
print(monthly_income_distribution, total_salary, total_pit)
