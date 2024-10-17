
import pandas as pd

# Helper function to extract country code from phone number
def extract_country_code(phone_number):
    return int(phone_number.split()[0][1:])

# Helper function to extract the last two digits from the phone number
def extract_last_two_digits(phone_number):
    return int(phone_number.split()[1][-2:])

# Load the provided Excel files
file1_path = 'Foobar1.xlsx'
file2_path = 'Foobar2.xlsx'
country_code_file='ISO3166.xlsx'

# Load the files using openpyxl engine
file1_data = pd.read_excel(file1_path, engine='openpyxl')
file2_data = pd.read_excel(file2_path, engine='openpyxl')
country_code_data = pd.read_excel(country_code_file, engine='openpyxl')

# Create a dictionary for quick lookup of country names by country code
country_code_dict = {str(row['alpha-2']): row['name'] for _, row in country_code_data.iterrows()}


# Process each row from Foobar2.xlsx and find matching IBANs
filtered_ibans = []
for index, row in file2_data.iterrows():
    phone_number = row['PhoneNumber']
    last_4_digits = str(row['Last4Digits'])
    country_code = extract_country_code(phone_number)
    last_two_digits = extract_last_two_digits(phone_number)

    # Filter IBANs by the last four digits
    potential_ibans = file1_data[file1_data['IBAN'].str.endswith(last_4_digits)]
    
    # Check if there are any potential matches
    if not potential_ibans.empty:
        # Divide the last two digits by the country code
        division_result = last_two_digits / country_code

        # Handle the special case where the division result is 1.0
        if division_result == 1.0:
            decimal_part = '00'
        else:
            # Get the second and third decimal places for normal cases
            decimal_part = str(division_result).split('.')[1][1:3]

        # Find the matching IBAN based on the first two digits
        for _, potential_iban_row in potential_ibans.iterrows():
            iban = potential_iban_row['IBAN']
            if iban[2:4] == decimal_part:
                country_name = country_code_dict.get(str(iban[:2]), "Unknown Country")
                # Add the result to the filtered list
                filtered_ibans.append({
                    'User': potential_iban_row['User'],
                    'Country': country_name,
                    'PhoneNumber': phone_number,
                    'IBAN': iban
                })
                break

# Convert the result to a DataFrame
filtered_ibans_df = pd.DataFrame(filtered_ibans)

# Save the filtered IBANs to a CSV file
output_file_path = 'filtered_ibans.csv'
filtered_ibans_df.to_csv(output_file_path, index=False)

print(f'Filtered IBANs saved to {output_file_path}')
