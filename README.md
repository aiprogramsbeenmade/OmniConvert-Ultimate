# 🚀 OmniConvert Ultimate

**OmniConvert Ultimate** è una potente applicazione desktop per macOS (e non solo) che permette di convertire file in modo massivo con un semplice **Drag & Drop**. Dimentica i convertitori online lenti e poco sicuri: OmniConvert processa tutto localmente, garantendo privacy totale e velocità fulminea.

## ✨ Caratteristiche principali

* **Drag & Drop Intelligente**: Trascina i file direttamente nell'app. Il sistema riconosce automaticamente la categoria (Immagini, Documenti, Video, Dati).
* **Conversione Batch**: Gestisci decine di file contemporaneamente con impostazioni specifiche per ogni formato.
* **Motori di Conversione Avanzati**:
  * **Documenti**: Basato su LibreOffice per la massima fedeltà, con integrazione di `pdf2docx` per ricostruire file Word e `PyMuPDF` per estrazioni di testo istantanee.
  * **Multimedia**: Potenziato da `FFmpeg` per conversioni audio/video di alta qualità.
  * **Immagini**: Gestione professionale tramite `Pillow`, incluso il supporto per file `.webp`, `.heic` e creazione di icone `.ico`.
* **Interfaccia Moderna**: UI dinamica costruita in PySide6 con barra di progresso in tempo reale e gestione intelligente della coda.
* **Privacy Totale**: Nessun dato lascia mai il tuo computer.

## 📂 Formati Supportati

| Categoria | Input | Output Supportati |
| :--- | :--- | :--- |
| **Documenti** | PDF, DOCX, DOC, ODT, RTF, EPUB, TXT | **PDF, DOCX, TXT, EPUB** |
| **Immagini** | JPG, PNG, WEBP, HEIC, TIFF, BMP, ICO, GIF | **PNG, JPG, WEBP, ICO, BMP** |
| **Video/Audio** | MP4, MKV, MOV, AVI, WEBM, MP3, WAV, FLAC, OGG | **MP4, MP3, WAV, WEBM** |
| **Dati** | CSV, XLSX, JSON, XLS | **CSV, JSON, XLSX** |

## 🛠️ Requisiti di Sistema

Per il corretto funzionamento, assicurati di avere:

1. **Python 3.9+**
2. **LibreOffice**
3. **FFmpeg**

## 📦 Installazione e Avvio

1. **Clona il repository**:
   ```bash
   git clone [https://github.com/tuo-username/OmniConverter.git](https://github.com/tuo-username/OmniConverter.git)
   cd OmniConverter
   ```
2. **Crea e attiva un ambiente virtuale:**
    ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Installa le dipendenze:**
    ```bash
   pip3 install -r requirements.txt
   ```
4. **Avvia l'applicazione:**
    ```bash
   python3 main.py
   ```
   
## 🚀 Come si usa

1.  **Carica**: Trascina i file nella lista superiore.
2.  **Gestisci la coda**: Clicca su un file per far apparire il tasto **Elimina selezionato** o usa **Svuota tutto** per pulire la lista.
3.  **Configura**: L'area "Impostazioni Conversione" raggrupperà i file per estensione. Scegli il formato desiderato dal menu a tendina.
4.  **Converti**: Clicca su **Avvia Conversione**.
5.  **Risultato**: I file convertiti appariranno nella cartella `OmniConvert_Output` sul tuo Desktop.

## 📄 Licenza

Questo progetto è distribuito sotto licenza **MIT**. Consulta il file `LICENSE` per ulteriori dettagli.
