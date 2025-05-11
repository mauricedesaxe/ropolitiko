from openai import OpenAI
import logging
from app.scraper.protv import ArticleData
from app.env import OPENAI_API_KEY

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=OPENAI_API_KEY)
LLM_MODEL = "gpt-4o" 

def clean_article_content(raw_content: str, metadata: ArticleData = None) -> str:
    """
    Clean raw scraped article content and convert to markdown using LLM.
    
    Args:
        raw_content (str): Raw scraped content from the article
        metadata (ArticleData): Article metadata (title, url, source, etc.)
        
    Returns:
        str: Cleaned markdown content
    """
    try:
        metadata_prompt = ""
        if metadata:
            metadata_prompt = "Article metadata (use this to improve cleaning):\n"
            for key, value in metadata.items():
                if value:
                    metadata_prompt += f"- {key}: {value}\n"
        
        prompt = f"""
        Convert this raw scraped news article into clean markdown.
        ONLY include the main article content - remove all:
        - Navigation elements
        - Timestamps (like "18:35")
        - Related article sections
        - "VEZI MAI MULTE ȘTIRI" sections
        - Social media links
        - Tags and metadata
        - Advertisements
        - Footer information

        Format as markdown with:
        - EXACTLY preserve the original paragraph structure without reorganizing
        - Keep paragraphs in their original order
        - Maintain any lists or quotes exactly as they appear
        - Format subheadings appropriately

        The content shall remain in the same language as the original content.

        IMPORTANT RULES:
        - Do NOT add ANY information that is not present in the original content
        - Do NOT reorganize paragraphs or sections
        - Do NOT alter the original flow of content
        - Do NOT expand on any topics beyond what's in the original
        - Do NOT include any preamble, introduction, or summary
        - Simply provide the cleaned content maintaining its exact structure

        {metadata_prompt}
        
        Raw content:
        {raw_content}
        """
        
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.exception(f"Error cleaning article content: {str(e)}")
        # Return original content as fallback
        return raw_content