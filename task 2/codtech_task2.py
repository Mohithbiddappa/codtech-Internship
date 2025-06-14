import requests
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import random

# ------------------------------
# Fetch data from API
# ------------------------------
url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)

if response.status_code == 200:
    users = response.json()
else:
    print("Failed to fetch data from API.")
    exit()

# ------------------------------
# Load into DataFrame
# ------------------------------
df = pd.DataFrame(users)
df_cleaned = df[['name', 'username', 'email', 'address', 'company']].copy()
df_cleaned['city'] = df_cleaned['address'].apply(lambda x: x['city'])
df_cleaned['company'] = df_cleaned['company'].apply(lambda x: x['name'])
df_cleaned.drop('address', axis=1, inplace=True)

# ------------------------------
# Simulate More Users
# ------------------------------
df_expanded = pd.concat([df_cleaned]*3, ignore_index=True)
city_pool = df_cleaned['city'].tolist()
df_expanded['city'] = df_expanded['city'].apply(lambda x: random.choice(city_pool))
df_expanded = df_expanded.sample(frac=1).reset_index(drop=True)

# ------------------------------
# Create Bar Chart
# ------------------------------
city_counts = df_expanded['city'].value_counts()
plt.figure(figsize=(10, 5))
city_counts.plot(kind='bar', color='skyblue')
plt.title("Number of Users per City (Simulated)")
plt.xlabel("City")
plt.ylabel("User Count")
plt.tight_layout()
plt.savefig("bar_chart.png")
plt.close()

# ------------------------------
# Create PDF Report (Improved Table)
# ------------------------------
from fpdf import FPDF

# Use Landscape mode on A4
pdf = FPDF(orientation='L', unit='mm', format='A4')
pdf.add_page()

pdf.set_font("Arial", size=11)

# Title
pdf.set_font("Arial", 'B', 16)
pdf.cell(0, 10, "Simulated User Data Report", ln=True, align='C')
pdf.ln(10)

# Adjusted column widths for landscape
col_widths = [50, 40, 65, 35, 60]
headers = ["Name", "Username", "Email", "City", "Company"]

# Header
pdf.set_font("Arial", 'B', 11)
for i, header in enumerate(headers):
    pdf.cell(col_widths[i], 10, header, 1)
pdf.ln()

# Rows
pdf.set_font("Arial", '', 9)
for index, row in df_expanded.head(25).iterrows():
    row_data = [
        str(row['name'])[:30],
        str(row['username'])[:20],
        str(row['email'])[:35],
        str(row['city'])[:15],
        str(row['company'])[:25]
    ]
    for i in range(len(headers)):
        pdf.cell(col_widths[i], 10, row_data[i], 1)
    pdf.ln()

# Add chart image
pdf.ln(5)
pdf.image("bar_chart.png", x=10, w=270)

# Footer
pdf.set_font("Arial", 'I', 10)
pdf.ln(5)
pdf.cell(0, 10, "Generated by Mohith MB | CodTech Internship 2025", ln=True, align='C')

pdf.output("User_Report.pdf")
print("PDF generated successfully!")