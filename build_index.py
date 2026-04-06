import os
import json
import re

def extract_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    # Basic text extraction from HTML
    # 1. Remove script and style
    html = re.sub(r'<(script|style).*?>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    # 2. Extract content from specific tags or just all text
    tags_to_extract = re.findall(r'<(h[1-6]|p|li|td|strong|em|span|b|i|code).*?>(.*?)</\1>', html, flags=re.DOTALL | re.IGNORECASE)
    
    text_content = []
    for tag, content in tags_to_extract:
        # Clean tags inside content
        clean_text = re.sub(r'<.*?>', '', content)
        clean_text = clean_text.strip().replace('\n', ' ')
        if clean_text:
            text_content.append(clean_text)
            
    return " ".join(text_content)

def build_index():
    chapters = [
        {"id": "1", "title": "Pengenalan Basis Data", "file": "Slide 1 - Introduction to Databases_.pptx.html"},
        {"id": "2", "title": "Konsep & Arsitektur", "file": "Slide-02_Database-Concept-and-Architecture.html"},
        {"id": "3", "title": "Pemodelan ER", "file": "Slide_3_-_Pemodelan_Basis_Data_dengan_ER.html"},
        {"id": "4A", "title": "Pemodelan EER Part 1", "file": "Slide_4_-_Pemodelan_Basis_Data_dengan_EER_Part_1.html"},
        {"id": "4B", "title": "Pemodelan EER Part 2", "file": "Slide_4_-_Pemodelan_Basis_Data_dengan_EER_Part_2(1).html"},
        {"id": "5", "title": "Model Relasional", "file": "Slide_5_-_The_Relational_Data_Model_and_Relational_Database_Constraints.html"},
        {"id": "6", "title": "Pemetaan (E)ER", "file": "Slide_6_-_Pemetaan_Diagram__E_ER_ke_Skema_Relasional_-_updated-by-sby.html"},
        {"id": "7", "title": "SQL Definition", "file": "Slide_7_-_SQL_-_Data_Definition.html"},
        {"id": "8", "title": "Basic SQL Query", "file": "Slide_8_-_Basic_SQL_Query.html"},
        {"id": "CS", "title": "Cheatsheet", "file": "cheatsheet.html"}
    ]
    
    search_index = []
    for chapter in chapters:
        file_path = chapter['file']
        if os.path.exists(file_path):
            print(f"Indexing {file_path}...")
            content = extract_content(file_path)
            # Normalize and remove excessive spaces
            content = re.sub(r'\s+', ' ', content).strip()
            
            # Extract keywords (simple: alphanumeric or common DB terms)
            keywords = list(set(re.findall(r'\b\w{3,}\b', content.lower())))
            
            search_index.append({
                "title": chapter['title'],
                "file": chapter['file'],
                # We store a truncated content or just keywords to save space
                "keywords": keywords,
                # Store some preview text (first 200 chars)
                "preview": content[:200] + "..."
            })
            
    with open('search_index.json', 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    build_index()
