
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

# Load the files using openpyxl engine
file1_data = pd.read_excel(file1_path, engine='openpyxl')
file2_data = pd.read_excel(file2_path, engine='openpyxl')

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
        try:
            if division_result == 1.0:
                decimal_part_str = '00'
            else:
                # Get the second and third decimal places
                decimal_part = int(str(division_result).split('.')[1][1:3])
                decimal_part_str=str(decimal_part)
        except:
            print()
        # Find the matching IBAN based on the first two digits
        for _, potential_iban_row in potential_ibans.iterrows():
            iban = potential_iban_row['IBAN']
            if iban[2:4] == decimal_part_str:
                # Add the result to the filtered list
                filtered_ibans.append({
                    'User': potential_iban_row['User'],
                    'Country': phone_number.split()[0],
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
