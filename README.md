# 📁 Submission Sorter

Automatically sorts folders of photo and video submissions into organized categories based on content and resolution.

---

## 🚀 What This Does

This script scans a folder of submissions (each in its own folder) and moves each entire folder into one of the following:

```
Videos/
Landscape/
Portrait/
```

Each category is further split into:

```
Hi Res/
Low Res/
```

---

## 🧠 How It Works

### Folder-Level Sorting (Important)

* The script **moves entire folders**, not individual files
* Folder names and file names remain unchanged

---

### 📂 Category Rules

For each submission folder:

1. **If ANY video exists**
   → Folder goes to `Videos`

2. **If NO video, but ANY image is wider than tall**
   → Folder goes to `Landscape`

3. **Otherwise**
   → Folder goes to `Portrait`

---

### 📏 Resolution Rules

* **Hi Res** = width ≥ 1920 AND height ≥ 1080
* **Low Res** = anything below that

If **any file in the folder** meets Hi Res:
→ whole folder is marked **Hi Res**

---

## 🗂 Output Structure

```
Output Folder/
├── Videos/
│   ├── Hi Res/
│   └── Low Res/
├── Landscape/
│   ├── Hi Res/
│   └── Low Res/
├── Portrait/
│   ├── Hi Res/
│   └── Low Res/
```

---

## 🧾 Logging

* A log file is created **outside the output folder**
* Includes:

  * Folder name
  * Category
  * Resolution
  * Destination path
  * Errors (if any)

Example:

```
sort_log_2026-04-13_09-42-10.txt
```

---

## ⚙️ Setup

### 1. Create virtual environment (recommended)

```
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```
pip install pillow opencv-python
```

---

## ▶️ Usage

```
python sort_submissions.py "INPUT_FOLDER" "OUTPUT_FOLDER"
```

### Example

```
python sort_submissions.py "Y:\Submissions" "Y:\Sorted"
```

---

## ⚠️ Important Notes

* This script uses **MOVE**, not copy
  → Your input folder will be emptied as files are sorted

* If duplicate folder names exist:
  → Script appends `_2`, `_3`, etc. to prevent overwrite

* Works recursively
  → Files inside subfolders are included in detection

* Video resolution detection requires OpenCV
  → If unavailable, videos default to Low Res

---

## ✅ Recommended Workflow

1. Test with a small batch first
2. Check output folders
3. Review log file
4. Run on full dataset

---

## 🔧 Future Improvements (Optional)

* Dry run mode (preview without moving)
* CSV log output
* UI for non-technical users
* Auto-trigger via Discord bot or server watcher

---

## 🙌 Why This Exists

Because manually sorting hundreds of submissions is a terrible use of time.

---

Enjoy not dragging folders around like it's 2006.
