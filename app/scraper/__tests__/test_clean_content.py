import pytest
import os
from app.scraper.clean_content import clean_article_content, client, LLM_MODEL

def test_clean_article_content():
    """Test that the article content cleaning function works correctly"""
    # Load the sample content file
    sample_file_path = os.path.join(
        os.path.dirname(__file__), 
        "raw_content_samples", 
        "ce-spun-ungurii.txt"
    )
    
    try:
        with open(sample_file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
    except Exception as e:
        pytest.skip(f"Skipping test: Cannot read sample file - {str(e)}")
    
    # Sample metadata matching ProTVArticleScraper.ArticleData format
    metadata = {
        "title": "Ce spun ungurii despre rezultatul alegerilor prezidențiale din România. L-au descris pe George Simion într-un singur cuvânt",
        "url": "https://stirileprotv.ro/stiri/actualitate/ce-spun-ungurii-despre-rezultatul-alegerilor-prezidentiale-din-romania-l-au-descris-pe-george-simion-intr-un-singur-cuvant.html",
        "image_url": None,
        "source": "PRO TV",
        "published_at": "05-05-2025 10:03",
        "lead": "George Simion este câștigătorul clar al primului tur al alegerilor prezidențiale"
    }
    
    # Clean the content
    cleaned_content = clean_article_content(raw_content, metadata)
    
    # Verify the cleaning worked
    assert cleaned_content, "Cleaned content should not be empty"
    assert len(cleaned_content) <= len(raw_content), "Cleaned content should be shorter or equal in length to raw content"
    
    # Check for common elements that should be removed
    assert "VEZI MAI MULTE ȘTIRI" not in cleaned_content, "Navigation element not removed"
    assert "Etichete:" not in cleaned_content, "Tags section not removed"
    assert "Dată publicare:" not in cleaned_content, "Publication date footer not removed"
    
    # Check that main content is preserved
    assert "George Simion" in cleaned_content, "Key article content should be preserved"
    
    # Print sample of cleaned content for debugging
    print(f"Cleaned content sample: \n\n{cleaned_content[:250]}...\n\n")
    
    # LLM evaluation
    criteria = """
    1. No navigation elements or website-specific content
    2. Main article substance preserved
    3. Proper paragraph structure maintained
    4. No advertisements or unrelated content
    5. Overall readability improved
    """
    
    evaluation = evaluate_content_quality(raw_content, cleaned_content, criteria)
    print(f"LLM Evaluation:\n{evaluation}")
    
    # Check for failure indicators in evaluation
    assert "FAIL" not in evaluation, f"LLM evaluation failed: {evaluation}"

def test_clean_article_content_no_metadata():
    """Test that the function works without metadata"""
    # Load the sample content file
    sample_file_path = os.path.join(
        os.path.dirname(__file__), 
        "raw_content_samples", 
        "ce-spun-ungurii.txt"
    )
    
    try:
        with open(sample_file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
    except Exception as e:
        pytest.skip(f"Skipping test: Cannot read sample file - {str(e)}")
    
    # Clean the content without metadata
    cleaned_content = clean_article_content(raw_content)
    
    # Basic verification
    assert cleaned_content, "Cleaned content should not be empty"
    assert "George Simion" in cleaned_content, "Key article content should be preserved"
    
    # LLM evaluation
    criteria = """
    1. No navigation elements or website-specific content
    2. Main article substance preserved
    3. Content is coherent without metadata context
    """
    
    evaluation = evaluate_content_quality(raw_content, cleaned_content, criteria)
    print(f"LLM Evaluation (no metadata):\n{evaluation}")
    
    # Check for failure indicators in evaluation
    assert "FAIL" not in evaluation, f"LLM evaluation failed: {evaluation}"


def evaluate_content_quality(raw_content, cleaned_content, criteria):
    """Use LLM to evaluate cleaned content quality"""
    prompt = f"""
    You are judging the quality of content cleaning for news articles.
    The content shall remain in the same language as the original content.
    
    RAW CONTENT SAMPLE:
    {raw_content[:1000]}...
    
    CLEANED CONTENT:
    {cleaned_content}
    
    Evaluate the cleaned content on these criteria:
    {criteria}
    
    For each criterion, respond with only "PASS" or "FAIL" followed by brief explanation.
    """
    
    response = client.generate(model=LLM_MODEL, prompt=prompt)
    return response['response'].strip()