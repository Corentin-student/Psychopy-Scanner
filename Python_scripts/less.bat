@echo off
echo Démarrage des compilations PyInstaller...

start "Compilation Image" cmd /c C:\Users\coren\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\pyinstaller.exe "C:\Users\coren\Documents\Memoire\Application\API Psycho\Python_scripts\Image.spec"
start "Compilation Stroop" cmd /c C:\Users\coren\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\pyinstaller.exe "C:\Users\coren\Documents\Memoire\Application\API Psycho\Python_scripts\Stroop.spec"
start "Compilation Video" cmd /c C:\Users\coren\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\pyinstaller.exe "C:\Users\coren\Documents\Memoire\Application\API Psycho\Python_scripts\video.spec"
start "Compilation Audition" cmd /c C:\Users\coren\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\pyinstaller.exe "C:\Users\coren\Documents\Memoire\Application\API Psycho\Python_scripts\Audition.spec"
start "Compilation EMO_FACE" cmd /c C:\Users\coren\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\pyinstaller.exe "C:\Users\coren\Documents\Memoire\Application\API Psycho\Python_scripts\EMO_FACE.spec"





echo Les compilations ont été lancées.
