$python = "C:\Users\Ortiz Alejandro\AppData\Local\Programs\Python\Python314\python.exe"
$dir    = "C:\Users\Ortiz Alejandro\O-IAxis\frontend"
Start-Process -FilePath $python -ArgumentList "-m","http.server","3001","--bind","0.0.0.0","--directory",$dir -WindowStyle Minimized
Start-Sleep 2
Start-Process "http://127.0.0.1:3001"
