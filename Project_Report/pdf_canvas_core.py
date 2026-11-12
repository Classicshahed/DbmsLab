import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = r"C:\Users\USER\.gemini\antigravity\scratch\dbms_Lab_project"
REPORT_DIR = os.path.join(BASE_DIR, "Project_Report")
DIAGRAMS_DIR = os.path.join(REPORT_DIR, "Project_Diagrams")
SCREENSHOTS_DIR = os.path.join(REPORT_DIR, "Project_Screenshots")

# Professional Color Palette
C_PRIMARY = colors.HexColor("#1A365D")   # Deep Navy
C_SECONDARY = colors.HexColor("#2B6CB0") # Slate Blue
C_DARK = colors.HexColor("#2D3748")      # Charcoal Body Text
C_MUTED = colors.HexColor("#718096")     # Muted Gray
C_LIGHT_BG = colors.HexColor("#F7FAFC")  # Alternate Row Light
C_BORDER = colors.HexColor("#CBD5E0")    # Border Gray
C_SUCCESS = colors.HexColor("#276749")   # Dark Green

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1: # Suppress on Cover Page
            self.saveState()
            self.setFont("Times-Roman", 8.5)
            self.setFillColor(colors.HexColor("#718096"))
            
            # Running Header
            self.drawRightString(7.5 * inch, 10.45 * inch, "Blood Bank Management System | Academic Project Report")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(1.0 * inch, 10.35 * inch, 7.5 * inch, 10.35 * inch)
            
            # Running Footer
            self.line(1.0 * inch, 0.75 * inch, 7.5 * inch, 0.75 * inch)
            self.drawString(1.0 * inch, 0.60 * inch, "Department of Computer Science & Engineering • DBMS Laboratory")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(7.5 * inch, 0.60 * inch, page_text)
            self.restoreState()

print("NumberedCanvas ready.")
