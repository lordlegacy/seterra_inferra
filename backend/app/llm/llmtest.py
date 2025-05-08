from google import genai
from google.genai import types

"""
client = genai.Client(api_key="AIzaSyCAevq7ISQK2LoiUn5jO653t4HbssBrTXE")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)
"""


response = {'summary': 'The user is unable to print PDF documents.', 'diagnosis': ['Printer is not properly connected or configured.', 'Incorrect printer selected.', 'Printer driver issues.', 'PDF document is corrupted.', 'PDF reader software (e.g., Adobe Acrobat Reader) is outdated or has issues.', 'PDF document has printing restrictions or security settings enabled.', 'Insufficient system resources (memory, disk space).', 'Operating system issues.'], 'solutions': ['Verify that the printer is properly connected to the computer (USB, network) and powered on.', 'Ensure the correct printer is selected in the print dialog box.', 'Restart the printer and the computer.', 'Update or reinstall the printer driver.', 'Try printing a different PDF document to rule out a corrupted file.', 'Try printing the PDF document from a different PDF reader software (e.g., Chrome, Edge, Foxit Reader).', 'Update the PDF reader software to the latest version.', "Check the PDF document's security settings to ensure printing is allowed. If restricted, contact the document creator to remove the restrictions.", 'Ensure sufficient disk space is available on the system drive.', 'Run a system file check to identify and repair corrupted system files.', 'Test printing other types of documents (e.g., Word, text) to isolate the problem to PDFs.', "Contact the printer manufacturer's support or a qualified technician if the problem persists."], 'confidence': 0.9}

var1 = response['solutions']
print(var1)