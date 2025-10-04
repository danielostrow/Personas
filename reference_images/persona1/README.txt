📸 PERSONA1 REFERENCE IMAGES FOLDER

🎯 WHAT TO PUT HERE:
• 20-30 high-quality photos of persona1
• Various angles: front, 3/4 view, profile
• Different expressions: smiling, serious, laughing
• Multiple lighting conditions: natural, studio, outdoor
• Mix of shots: close-up, medium, full body

📋 NAMING CONVENTION:
• persona1_001.jpg
• persona1_002.jpg
• persona1_003.jpg
• ... up to persona1_030.jpg

🔧 HOW TO ADD IMAGES:
1. Use the organize-images script:
   python scripts/organize_reference_images.py --source-dir /path/to/your/photos --persona-name persona1

2. OR manually copy images to this folder with sequential naming

⚡ TRAINING PROCESS:
1. Add 20-30 images to this folder
2. Run: ./scripts/train_lora.sh persona1 1e-4 10000
3. Load trained LoRA in ADAPTIVE_BATCH_COMMUNITY_GENERATOR workflow
4. Generate community scenes!

💡 IMAGE QUALITY TIPS:
• Use consistent lighting across the set
• Include variety in poses and expressions
• Avoid blurry or low-resolution images
• Focus on clear facial features
• Include some full-body shots for better body representation
