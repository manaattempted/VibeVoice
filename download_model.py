import argparse
import os
from huggingface_hub import snapshot_download

def main():
    parser = argparse.ArgumentParser(
        description="VibeVoice Model Downloader - เครื่องมือดาวน์โหลดโมเดล VibeVoice จาก Hugging Face"
    )

    # Parameter สำหรับเลือกขนาดโมเดลแบบเร็ว (Shortcut)
    parser.add_argument(
        "--size",
        type=str,
        choices=["small", "large"],
        help="เลือกขนาดโมเดล: 'small' สำหรับ 1.5B, 'large' สำหรับ 7B"
    )

    # Parameter สำหรับระบุ Model ID โดยตรง (ถ้าไม่อยากใช้ shortcut)
    parser.add_argument(
        "--model_id",
        type=str,
        help="ระบุ Hugging Face Model ID โดยตรง (เช่น vibevoice/VibeVoice-7B)"
    )

    # Parameter สำหรับระบุโฟลเดอร์ที่ต้องการเซฟ
    parser.add_argument(
        "--local_dir",
        type=str,
        help="ระบุโฟลเดอร์ที่ต้องการบันทึกโมเดล (ถ้าไม่ระบุ จะสร้างตามชื่อโมเดล)"
    )

    args = parser.parse_args()

    # 1. กำหนด Model ID
    if args.model_id:
        model_id = args.model_id
    elif args.size == "small":
        model_id = "vibevoice/VibeVoice-1.5B"
    elif args.size == "large":
        model_id = "vibevoice/VibeVoice-7B"
    else:
        print("❌ Error: กรุณาระบุ --size (small/large) หรือ --model_id")
        parser.print_help()
        return

    # 2. กำหนด Local Directory (ถ้าไม่ระบุ ให้สร้างตามชื่อโมเดล)
    if args.local_dir:
        local_dir = args.local_dir
    else:
        # เปลี่ยน 'vibevoice/VibeVoice-7B' -> 'models/VibeVoice-7B'
        model_name = model_id.split('/')[-1]
        local_dir = os.path.join("models", model_name)

    print("\n" + "="*50)
    print(f"🚀 Starting Download")
    print(f"📦 Model ID  : {model_id}")
    print(f"📂 Save Dir  : {local_dir}")
    print("="*50 + "\n")

    try:
        # เริ่มดาวน์โหลด
        # local_dir_use_symlinks=False สำคัญมากสำหรับ Windows เพื่อให้ได้ไฟล์จริง ไม่ใช่ symlink
        path = snapshot_download(
            repo_id=model_id,
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )
        print(f"\n✅ Download Complete!")
        print(f"📂 Model is saved at: {path}")
    except Exception as e:
        print(f"\n❌ An error occurred during download: {e}")

if __name__ == "__main__":
    main()
