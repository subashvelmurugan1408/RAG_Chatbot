import requests
import os
from pathlib import Path
import time

# Create documents folder
Path("documents").mkdir(exist_ok=True)

# AI/ML research papers (direct arXiv PDFs)
AI_ML_PAPERS = [
    # RAG Papers (Priority 1)
    {
        "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "url": "https://arxiv.org/pdf/2005.11401.pdf",
        "category": "RAG"
    },
    {
        "title": "Dense Passage Retrieval for Open-Domain QA",
        "url": "https://arxiv.org/pdf/2004.04906.pdf",
        "category": "RAG"
    },
    
    # Transformers & Foundation Models
    {
        "title": "Attention Is All You Need",
        "url": "https://arxiv.org/pdf/1706.03762.pdf",
        "category": "Transformers"
    },
    {
        "title": "Language Models are Few-Shot Learners (GPT-3)",
        "url": "https://arxiv.org/pdf/2005.14165.pdf",
        "category": "LLM"
    },
    {
        "title": "BERT Pre-training of Deep Bidirectional Transformers",
        "url": "https://arxiv.org/pdf/1810.04805.pdf",
        "category": "NLP"
    },
    
    # NLP & Language Understanding
    {
        "title": "Language Models are Unsupervised Multitask Learners (GPT-2)",
        "url": "https://arxiv.org/pdf/1902.10673.pdf",
        "category": "LLM"
    },
    {
        "title": "Sentence-BERT Sentence Embeddings",
        "url": "https://arxiv.org/pdf/1908.10084.pdf",
        "category": "Embeddings"
    },
    
    # Vision & Multimodal
    {
        "title": "An Image is Worth 16x16 Words (Vision Transformer)",
        "url": "https://arxiv.org/pdf/2010.11929.pdf",
        "category": "Vision"
    },
    {
        "title": "DALL-E Zero-Shot Text-to-Image Generation",
        "url": "https://arxiv.org/pdf/2102.12092.pdf",
        "category": "Multimodal"
    },
    
    # Model Architecture
    {
        "title": "LLaMA Open and Efficient Foundation Language Models",
        "url": "https://arxiv.org/pdf/2302.13971.pdf",
        "category": "LLM"
    },
]

def download_paper(url, filename):
    """Download a paper from arXiv"""
    try:
        print(f"📥 Downloading: {filename}...", end="", flush=True)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        file_path = f"documents/{filename}"
        with open(file_path, "wb") as f:
            f.write(response.content)
        
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        print(f" ✓ ({file_size:.1f} MB)")
        
        return True
    except Exception as e:
        print(f" ✗ Error: {e}")
        return False

def main():
    print("🤖 AI/ML Research Paper Downloader")
    print("=" * 60)
    
    # Create category folders
    categories = set(paper["category"] for paper in AI_ML_PAPERS)
    for cat in categories:
        Path(f"documents/{cat}").mkdir(exist_ok=True)
    
    successful = 0
    failed = 0
    
    for i, paper in enumerate(AI_ML_PAPERS, 1):
        print(f"\n[{i}/{len(AI_ML_PAPERS)}] {paper['category']}")
        print(f"Title: {paper['title']}")
        
        # Create safe filename
        filename = f"{paper['category']}/{paper['title'][:50].replace('/', '_')}.pdf"
        
        if download_paper(paper["url"], filename):
            successful += 1
        else:
            failed += 1
        
        # Be respectful to arXiv servers - add delay
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print(f"✓ Downloaded: {successful}")
    print(f"✗ Failed: {failed}")
    print(f"📁 Location: documents/")
    print("\nPapers organized by category:")
    for cat in sorted(categories):
        count = len([p for p in AI_ML_PAPERS if p["category"] == cat])
        print(f"  • {cat}: {count} papers")

if __name__ == "__main__":
    print("Installing requests if needed...")
    os.system("pip install requests -q")
    
    main()