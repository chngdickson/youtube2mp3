# youtube2mp3

1. Create Conda environment
```
conda create --name <env> --file requirements.txt
conda activate <env>
```
2. Create an executable
```
pyinstaller --onefile -w -F --add-binary "yt2mp3.png;." yt2mp3_v2.py
```
3. The executable will be in the dist folder
```
Enjoyyy! :D
```