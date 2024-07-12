
from pypdf import PdfReader
import re

reader = PdfReader("/Users/GiulioSalaorni/OneDrive - ITS Angelo Rizzoli/Desktop/PROJECT WORK/ascorbic_acid.pdf")
print(len(reader.pages)) 
count = 0

for i in range(len(reader.pages)):
    page = reader.pages[i]
    text = page.extract_text().lower()

    if "ld50" in text:
        count+=1
        match = re.findall(r"ld50\s*(.+?)\s*mg/kg\s*bw", text,flags=re.IGNORECASE)
        print(match)
    if "ld 50" in text:
        count+=1
        match = re.findall(r"ld\s*50\s*(.+?)\s*mg/kg\s*bw", text,flags=re.IGNORECASE)
        print(match)
    if "ld 50s" in text:
        count+=1
        match = re.findall(r"ld\s*50s\s*(.+?)\s*mg/kg\s*bw", text,flags=re.IGNORECASE)
        print(match)




print(count)

