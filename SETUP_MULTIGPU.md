# 🖥️ คู่มือติดตั้ง VibeVoice บนเครื่อง multi-GPU (Windows)

คู่มือนี้สำหรับรันโมเดล **7B** บนเครื่องที่มี NVIDIA GPU หลายใบ (เช่น 4x RTX 3060 Ti)

**ต้องการ:** VRAM รวม >= 18GB (4x 8GB = 32GB ✅)

---

## 🟢 ระยะที่ 1: ตรวจสอบเครื่อง

### Step 1.1 — เปิด PowerShell
กด `Win + X` → เลือก **"Windows PowerShell"**

### Step 1.2 — ตรวจ GPU
```powershell
nvidia-smi
```
**ต้องเห็น:** 4x NVIDIA GeForce RTX 3060 Ti + CUDA Version

**ถ้าไม่เห็น** → ติดตั้ง NVIDIA Driver จาก https://www.nvidia.com/drivers แล้วรีสตาร์ท

### Step 1.3 — ตรวจ Python
```powershell
python --version
```

> ⚠️ **สำคัญ:** ถ้าเป็น **Python 3.13/3.14 → อย่าใช้** (ใหม่เกินไป, torch/numba/llvmlite ยังไม่รองรับ)
> ต้องใช้ **Python 3.11** (เสถียรสุด รองรับทุก package)

---

## 🟢 ระยะที่ 2: ติดตั้ง Python 3.11 (ถ้ายังไม่มี)

1. ไปที่ https://www.python.org/downloads/windows/
2. ดาวน์โหลด **Python 3.11.x** → ติดตั้ง (⚠️ ติ๊ก "Add Python to PATH")
3. ตรวจว่ามี 2 version:
```powershell
py -0
```
ควรเห็น:
```
-V:3.14
-V:3.11
```

---

## 🟢 ระยะที่ 3: Clone โปรเจกต์

### Step 3.1 — ไปที่โฟลเดอร์ที่ต้องการ
```powershell
cd D:\
```

### Step 3.2 — Clone fork ของคุณ
```powershell
git clone https://github.com/yourname/VibeVoice.git
cd VibeVoice
```
> ⚠️ เปลี่ยน `yourname` เป็นชื่อ GitHub จริงของคุณ

---

## 🟢 ระยะที่ 4: สร้าง Environment (ด้วย Python 3.11)

### Step 4.1 — สร้าง venv ด้วย Python 3.11
```powershell
py -3.11 -m venv venv
```

### Step 4.2 — เปิด venv
```powershell
venv\Scripts\activate
```
**ควรเห็น** `(venv)` ขึ้นหน้าบรรทัด

### Step 4.3 — ตรวจ Python version
```powershell
python --version
```
**ต้องเป็น 3.11.x**

### Step 4.4 — อัปเดต pip
```powershell
python -m pip install --upgrade pip
```

---

## 🟢 ระยะที่ 5: ติดตั้ง PyTorch (CUDA version) ⭐สำคัญ

### Step 5.1 — ติดตั้ง PyTorch
```powershell
pip install torch
```
(ถ้าไม่ได้ ใช้ CUDA version ชัดเจน: `pip install torch --index-url https://download.pytorch.org/whl/cu124`)

### Step 5.2 — ตรวจว่า CUDA ใช้ได้
```powershell
python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPUs:', torch.cuda.device_count())"
```
**ต้องเห็น:**
```
CUDA: True
GPUs: 4
```

**ถ้าเห็น `CUDA: False`** → torch เป็น CPU version → ติดตั้งใหม่:
```powershell
pip uninstall torch -y
pip install torch --index-url https://download.pytorch.org/whl/cu124
```

---

## 🟢 ระยะที่ 6: ติดตั้ง VibeVoice dependencies

### Step 6.1 — ติดตั้ง dependencies
```powershell
pip install -e .
```

### Step 6.2 — แก้ version conflict (huggingface-hub)
```powershell
pip install "huggingface-hub>=0.30.0,<1.0"
```

> ⚠️ ถ้าเห็น warning เรื่อง dependency conflict (hf-gradio, gcsfs ฯลฯ) → **ไม่ต้องกังวล** เป็นแค่ warning ไม่ใช่ error

---

## 🟢 ระยะที่ 7: ดาวน์โหลดโมเดล 7B

### Step 7.1 — ดาวน์โหลดโมเดล (~18GB, ใช้เวลา 10-30 นาที)
```powershell
python -c "from huggingface_hub import snapshot_download; snapshot_download('vibevoice/VibeVoice-7B', local_dir='models/VibeVoice-7B')"
```

### Step 7.2 — ตรวจว่าโมเดลครบ
```powershell
dir models\VibeVoice-7B\config.json
```
**ควรเห็น** ไฟล์ `config.json` อยู่

---

## 🟢 ระยะที่ 8: รัน TTS

### Step 8.1 — รัน multi-GPU script
```powershell
python demo\inference_from_file_multigpu.py `
    --model_path models\VibeVoice-7B `
    --txt_path demo\text_examples\2p_music.txt `
    --speaker_names Alice Frank
```

### Step 8.2 — ตรวจผลลัพธ์
- ควรเห็นข้อความ `Detected 4 GPU(s)` + `Total VRAM: 32.0 GB`
- ไฟล์เสียงจะอยู่ที่ `outputs\2p_music_generated.wav`

---

## 🟢 ระยะที่ 9: ฟังเสียง

```powershell
Start-Process outputs\2p_music_generated.wav
```

---

# 🛠️ ตารางแก้ปัญหา

| อาการ | สาเหตุ | วิธีแก้ |
|-------|--------|--------|
| `Could not find a version... torch` | Python 3.14 ใหม่เกินไป | ติดตั้ง Python 3.11 + สร้าง venv ใหม่ |
| `CUDA: False` | PyTorch เป็น CPU version | `pip install torch --index-url .../cu124` |
| `Repo id must be...` | โมเดลไม่ครบ | รัน Step 7.1 ใหม่ (snapshot_download) |
| `huggingface-hub` error | เวอร์ชันขัดกัน | รัน Step 6.2 |
| VRAM ไม่พอ | ใช้ไฟล์ผิด (ไม่ใช่ multigpu) | ใช้ `inference_from_file_multigpu.py` |
| `git` ไม่รู้จัก | ยังไม่ติดตั้ง Git | ติดตั้งจาก https://git-scm.com |
| ติดตั้ง numba/llvmlite ล้ม | Python 3.14 | ใช้ Python 3.11 |

---

## 📌 ข้อควรจำ

- **Python 3.11** เท่านั้น (ไม่ใช่ 3.14)
- ใช้ **`inference_from_file_multigpu.py`** (มี `device_map="auto"`)
- โมเดล 7B ~18GB ต้องมีดิสก์ว่าง ~25GB
- ความเร็วถูกจำกัดด้วย PCIe ระหว่าง GPU (ช้ากว่า A100 ตัวเดียว แต่รันได้)
