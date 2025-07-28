# 🎵 BootBeats
Welcome to BootBeats, the place where you can relax and take a break from coding. I will guide you trough making some relaxing music so that you can take the most out of your break. The application has a clear UI and stores your song, for if you want to take a full day away from your computer. 
## 🖥️ Instructions and Preview
- To add notes write the notes in the text with a ', ' in between
- If you want to skip a note write a '-' in between the commas
- If you want to save the notes add the save notes button
- You can add or delete a new intrument and repeat this process again.
- And lastly don't forget to enjoy your music!
<img width="1904" height="890" alt="image" src="https://github.com/user-attachments/assets/c12f7980-bd36-4f22-9d36-d163b4a210ee" />

## 🚀 Quick-start
#### Install uv (If not done yet)
```bash
curl -Ls https://astral.sh/uv/install.sh | sh
# Or
pip install uv
```
#### 1. Clone repository:
Go to the folder you want the new project to be in and:
```bash 
git clone https://github.com/riessss/BootBeats.git 
cd BootBeats
```
#### 2. Create virtual environment and install dependencies:
```bash
uv .venv
source .venv/bin/activate # or .venv\Scripts\activate on Windows
uv sync
```
#### 3. Run the app
```bash
uv run main.py
```

## 🛠 Tech Stack
- **Flask** – Backend web framework  
- **SQLAlchemy** – ORM for database interaction  
- **Tailwind CSS** – Utility-first CSS framework  
- **Tone.js** – Web audio library for music synthesis
