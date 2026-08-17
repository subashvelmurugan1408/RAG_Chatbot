# create_sample_doc.py
from pathlib import Path

# Create documents folder
Path("documents").mkdir(exist_ok=True)

# Create a sample text file
sample_text = """
Artificial Intelligence (AI) is transforming industries worldwide.
Machine Learning enables computers to learn from data.
Deep Learning uses neural networks to process complex patterns.
Natural Language Processing (NLP) helps machines understand human language.
Computer Vision allows systems to interpret images and videos.
"""

with open("documents/ai_basics.txt", "w") as f:
    f.write(sample_text)

print("Sample document created!")