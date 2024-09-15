import pdfkit
import streamlit as st

# Path to wkhtmltopdf
path_wkhtmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Sample URL or HTML content to be converted to PDF
html_content = "<h1>Test PDF</h1><p>This is a test PDF generated from HTML content.</p>"

# Generate PDF from HTML
pdf_output = pdfkit.from_string(html_content, False, configuration=config)

# Streamlit button to download the PDF
st.download_button(
    label="Download PDF",
    data=pdf_output,
    file_name="output.pdf",
    mime="application/octet-stream",
)
