$pptxPath = "C:\Users\USER\.gemini\antigravity\scratch\dbms_Lab_project\Professional_Presentation\Final_Professional_Presentation.pptx"
$pdfPath  = "C:\Users\USER\.gemini\antigravity\scratch\dbms_Lab_project\Professional_Presentation\Final_Professional_Presentation.pdf"

$pptApp = New-Object -ComObject PowerPoint.Application
$presentation = $pptApp.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
$presentation.SaveAs($pdfPath, 32)  # 32 = ppSaveAsPDF
$presentation.Close()
$pptApp.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($pptApp) | Out-Null
Write-Host "PDF exported successfully: $pdfPath"

