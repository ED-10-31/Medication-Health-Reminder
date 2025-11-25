from fpdf import FPDF
from medication import get_medication_history


class PDFReport(FPDF):
    """
    Custom PDF class to handle Header and Footer automatically.
    """

    def header(self):

        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Medication History Report', ln=1, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')


def generate_pdf_report(user_id: int, filename: str = "Medication_Report.pdf"):
    """
    Fetches user history and compiles it into a PDF.
    Returns: True if successful, False if error.
    """
    try:
        history_data = get_medication_history(user_id)

        if not history_data:
            print("No history found for this user.")
            return False

        pdf = PDFReport()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.set_font("Times", 'B', 12)
        pdf.set_fill_color(200, 220, 255)

        pdf.cell(100, 10, "Medication Name", 1, 0, 'L', True)
        pdf.cell(90, 10, "Time Taken", 1, 1, 'L', True)

        pdf.set_font("Times", size=12)

        for record in history_data:
            name = record['medication_name']
            time = record['time_taken']

            pdf.cell(100, 10, name, 1)
            pdf.cell(90, 10, time, 1, 1)

        pdf.output(filename)
        print(f"PDF generated successfully: {filename}")
        return True

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False
