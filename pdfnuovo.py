from pypdf import PdfReader
import re

# Carica il file PDF
reader = PdfReader("/Users/GiulioSalaorni/OneDrive - ITS Angelo Rizzoli/Desktop/PROJECT WORK/ascorbic_acid.pdf")
print(f"Number of pages: {len(reader.pages)}")

# Inizializza il conteggio
count = 0

# Itera su ogni pagina
for i in range(len(reader.pages)):
    page = reader.pages[i]
    text = page.extract_text()
    
    # Debug: Stampa il testo estratto per la pagina corrente
    ##print(f"--- Page {i + 1} ---")
    ##print(text[:500])  # Print the first 500 characters for a quick check
    ##print("--------------------")

    # Converti il testo in minuscolo e rimuovi caratteri speciali
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Rimuovi spazi extra

    # Definisci l'espressione regolare che copre tutte le varianti
    pattern = r"ld\s*50\s*(?:s)?\s*(.+?)\s*mg/kg\s*bw"

    # Trova tutte le occorrenze che corrispondono al pattern
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    
    # Aggiorna il conteggio e stampa i match
    if matches:
        count += len(matches)
        print(f"Matches on page {i + 1}: {matches}")
        print(f"Counts on page {i + 1}: {count}")

print(f"Total count: {count}")