Python version
-

To run this application and Psychopy you need Python version 3.10.

Creating a virtual environment and install packages
-
- To do this, run the command: **python3 -m venv .venv**

- Once this is done, issue this command to enter the virtual environment: **.\/.venv./Scripts/activate**
- You can now run: **pip install -r requirements.txt**

Once you've done all this, you've either encountered no problems or you've probably encountered a problem with dupky. 
To solve the problem, simply install Visual Studio Build Tools. Once this has been done on the Visual Build Tools application,
simply install Development in a desktop environment with C++.

You can then rerun the last command to install the missing packages.

Transforming the application
-

In the Python_scripts/Spec_files/ folder, there's a file called toexecute.bat, in which you'll find everything you need 
to turn all your python files into executables. To do this, however, you'll need version 6.10.0 of Pyinstaller, which 
you should have installed with requirements.txt.


In the Python_scripts/Spec_files/ folder, there's a file called toexecute.bat, in which you'll find everything you need 
to turn all your python files into executables. To do this, however, you'll need version 6.10.0 of Pyinstaller, which 
you should have installed with requirements.txt.


Open the file toexecute.bat and replace every place where it says C:\Users\coren\AppData\LocalPackages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\pyinstaller.exe
with the path to the .exe version of Pyinstaller you've just installed. You will also have to change the path of the 
spec (i.e "C:\Users\coren\Documents\Memoire\Application\Application\API Psycho\Python_scripts\Spec_files\video.spec") 
files to match the paths in your PC

Once you've done this, you can run the toexecute.bat file and a series of command prompts will open to create an executable for each paradigm.

When all the windows have finished running, you should end up with a dist folder in the Python_scripts/Spec_files/ folder.

Inside you'll find folders for each paradigm. What you're going to do is take all the executables and put them in the 
same folder. Once you've done that, you can take the _internal folder from any of the paradigm folders and put it in 
the folder where you put the executable files.  To make sure that each paradigm can run properly, take the files from
each _internal in the paradigm folders and put them in the _internal you put with the exe files (you can ignore the
common files).

once this is done, you can copy a line from the toexecute.bat file and go to the API Psycho folder via a terminal. Once
this is done, you can run the following command: Path\to\your\pyinstaller.exe app.spec replacing Path\to\your\pyinstaller.exe
with the path to your Pyinstaller exe.

You'll get a dist folder containing an application folder with an application.exe file and an _internal folder. 
All that's left to do is reorganize everything and you'll have the application in portable format.

To do this, create a folder containing application.exe and the _internal folder that went with it. Then you'll place 
the application's Input folder there and also create an Output_files folder. Then you'll create a folder called 
Python_scripts in which you'll put all the executable files for the paradigms and the _internal folder, which is made up
of the _internal folders for each paradigm. 



- Main Folder:
  - Folder: _internal
  - File: application.exe             
  - Folder: Input
  - Folder: Fichiers_output
  - Folder: Python_scripts
    - Folder: _internal
    - File: IA_audition.exe
    - File: IA_image.exe
    - File: Psychopy_Adjectifs.exe
    - File: Psychopy_Cyberball.exe
    - File: Psychopy_EMO_FACE.exe
    - File: Psychopy_EMO_VOICEs.exe
    - File: Psychopy_everything.exe
    - File: Psychopy_Image.exe
    - File: Psychopy_Localizer.exe
    - File: Psychopy_Priming.exe
    - File: Psychopy_Stroop.exe
    - File: Psychopy_Text.exe
    - File: Psychopy_Video.exe

 Input Folder
-

Be careful, there are some files in the folder that must not be deleted or moved for the application to work properly.
Here's the list of files and folders for each paradigm that must not be deleted:

- **Cyberball:**
  - Folder : Banque_personnage
  - File : Femme2.jpg
  - File : Homme1.jpg
  - File : Homme2.jpg
  
- **Positive/Negative adjectives:**
  - File : entrainement.txt (this file can be modified but not deleted)

- **Audition:**
  - Folder : images

- **Strooper (Folder "Paradigme_Couleur"):**
  - there is no file or folder but to use it u need to put the word you want to show then a virgule and the color
    in which you want the word to appear (in english)
  
- **Emo Face:**
  - Folder : EMO_faces_list (you can add images)

- **EMO Voices:**
  - Folder : emo_voices (you can add audios)
  - File : oreille.png

- **IA Audition:**
  - Folder : audios (you can add audios)

- **IA Image:**
  - Folder : images (you can add images)

- **Static Images:**
  - Folder : stim_static (you can add images)

- **Localizer:**
  - Folder : images (you can add images)

- **Repetition Priming:**
  - Folder : stim_static (you can add images)

- **Scrolling videos:**
  - Folder : new_stimuli (you can add images)

How to use the application 
-
The link of a youtube video will be put here to explain how to use the application.
But if you follow the above instructions, you shouldn't have any problems using the application.