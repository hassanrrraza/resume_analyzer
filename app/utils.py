import os
import re
import json
from PyPDF2 import PdfReader
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download necessary NLTK resources
try:
    # Create a directory for NLTK data if it doesn't exist
    nltk_data_dir = os.path.join(os.path.expanduser('~'), 'nltk_data')
    os.makedirs(nltk_data_dir, exist_ok=True)
    
    # Download all required NLTK resources
    required_resources = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
    for resource in required_resources:
        try:
            nltk.download(resource, quiet=True, raise_on_error=True)
        except Exception as e:
            print(f"Warning: Could not download NLTK resource {resource}: {e}")
            # Try downloading to the specific directory
            nltk.download(resource, download_dir=nltk_data_dir, quiet=True)
except Exception as e:
    print(f"Warning: Issue with NLTK resource download: {e}")
    print("Attempting to continue with limited functionality...")

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_md")  # Use "en_core_web_md" for embeddings
except Exception as e:
    print(f"Error loading spaCy model: {e}")
    # Fall back to small model if medium isn't available
    try:
        print("Trying to load smaller model...")
        nlp = spacy.load("en_core_web_sm")
    except:
        print("Could not load any spaCy model. NLP functionality will be limited.")
        # Create a minimal spaCy instance as fallback
        nlp = spacy.blank("en")

# Load skills database
try:
    with open('skills_db.json', 'r') as f:
        SKILLS_DB = json.load(f)
except Exception as e:
    print(f"Could not load skills database: {e}")
    SKILLS_DB = {"skills": ["python", "flask", "nlp", "data analysis", "sql", "javascript"]}

# Define skill categories
SKILL_CATEGORIES = {
    "programming": ["python", "java", "javascript", "c++", "c#", "ruby", "php", "swift", "kotlin", "sql"],
    "web": ["html", "css", "react", "angular", "vue", "flask", "django", "node.js", "express", "bootstrap"],
    "database": ["sql", "mysql", "postgresql", "mongodb", "oracle", "sqlite", "nosql", "firebase", "redis"],
    "cloud": ["aws", "azure", "gcp", "cloud", "docker", "kubernetes", "terraform", "devops", "ci/cd"],
    "data_science": ["machine learning", "data analysis", "statistics", "python", "r", "pandas", "numpy", "tensorflow", "pytorch", "nlp"],
    "soft_skills": ["communication", "teamwork", "leadership", "problem solving", "critical thinking", "time management", "creativity"]
}

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:  # Only add if text was successfully extracted
                text += page_text + "\n"
        
        if not text.strip():
            return "No text could be extracted from this PDF. It may be scanned or contain only images."
        
        return text
    except Exception as e:
        return f"Error processing file: {e}"

def normalize_text(text):
    """Advanced text normalization beyond lowercasing.
    - Converts to lowercase
    - Removes special characters
    - Removes stopwords
    - Performs lemmatization
    """
    try:
        # Lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        try:
            # Tokenize
            tokens = word_tokenize(text)
            
            # Remove stopwords
            try:
                stop_words = set(stopwords.words('english'))
                filtered_tokens = [word for word in tokens if word not in stop_words]
            except Exception as e:
                print(f"Warning: Stopwords not available: {e}")
                filtered_tokens = tokens
            
            # Lemmatization
            try:
                lemmatizer = WordNetLemmatizer()
                lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
            except Exception as e:
                print(f"Warning: Lemmatization not available: {e}")
                lemmatized_tokens = filtered_tokens
            
            # Rejoin into string
            return ' '.join(lemmatized_tokens)
            
        except Exception as e:
            print(f"Warning: Advanced text processing failed: {e}")
            # Fallback to basic word splitting
            return ' '.join(text.split())
            
    except Exception as e:
        print(f"Error in text normalization: {e}")
        # Fallback to basic normalization
        return text.lower()

def extract_sections(text):
    """Extract resume sections like education, work experience."""
    # Create section dictionary
    sections = {
        'education': '',
        'experience': '',
        'skills': '',
        'summary': '',
        'other': ''
    }
    
    try:
        # Define section markers (common headings in resumes)
        section_patterns = {
            'education': r'(?i)education|academic|qualification|degree',
            'experience': r'(?i)experience|employment|work history|professional background',
            'skills': r'(?i)skills|technical skills|competencies|proficiencies',
            'summary': r'(?i)summary|profile|objective|professional summary'
        }
        
        # Find potential section headings
        lines = text.split('\n')
        current_section = 'other'
        
        for i, line in enumerate(lines):
            # Identify section headings
            for section, pattern in section_patterns.items():
                if re.search(pattern, line):
                    current_section = section
                    break
            
            # Add content to current section
            if i < len(lines) - 1:  # Skip adding the heading itself
                sections[current_section] += lines[i+1] + '\n'
    except Exception as e:
        print(f"Error in section extraction: {e}")
        # If section extraction fails, put all text in 'other'
        sections['other'] = text
    
    return sections

def identify_education(education_text):
    """Extract education details from the education section."""
    education_info = []
    
    try:
        # Use NLP to extract education entities
        doc = nlp(education_text)
        
        # Use pattern matching for degree detection
        degree_patterns = [
            r'(?i)bachelor|b\.?a\.?|b\.?s\.?|b\.?e\.?',
            r'(?i)master|m\.?a\.?|m\.?s\.?|m\.?b\.?a\.?',
            r'(?i)ph\.?d|doctor|doctorate'
        ]
        
        # Extract sentences that likely contain education info
        for sent in doc.sents:
            sent_text = sent.text.strip()
            
            # Skip if too short
            if len(sent_text) < 10:
                continue
                
            # Check for degree patterns
            is_education = False
            for pattern in degree_patterns:
                if re.search(pattern, sent_text):
                    is_education = True
                    break
                    
            # Check for educational institution entities
            for ent in sent.ents:
                if ent.label_ == "ORG":
                    is_education = True
                    break
            
            if is_education:
                education_info.append(sent_text)
    except Exception as e:
        print(f"Error in education identification: {e}")
    
    return education_info

def identify_experience(experience_text):
    """Extract work experience details from the experience section."""
    experience_info = []
    
    try:
        # Use NLP to extract experience entities
        doc = nlp(experience_text)
        
        # Extract sentences that likely contain work details
        current_job = {"title": "", "company": "", "duration": "", "description": []}
        
        for sent in doc.sents:
            sent_text = sent.text.strip()
            
            # Skip if too short
            if len(sent_text) < 5:
                continue
                
            # Try to identify job title and company
            title_pattern = r'(?i)(senior|junior|lead|principal|staff)?\s*(developer|engineer|analyst|manager|director|consultant)'
            company_pattern = r'(?i)(at|with|for)\s+([A-Z][A-Za-z]+)'
            date_pattern = r'(?i)(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\s*-\s*((jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}|present)'
            
            # Check for new job patterns (indicating a new entry)
            title_match = re.search(title_pattern, sent_text)
            company_match = re.search(company_pattern, sent_text)
            date_match = re.search(date_pattern, sent_text)
            
            if (title_match or company_match or date_match) and current_job["description"]:
                # Save current job before starting a new one
                experience_info.append(current_job)
                current_job = {"title": "", "company": "", "duration": "", "description": []}
            
            if title_match:
                current_job["title"] = title_match.group(0)
            
            if company_match:
                current_job["company"] = company_match.group(2)
                
            if date_match:
                current_job["duration"] = date_match.group(0)
                
            # Add to description
            current_job["description"].append(sent_text)
        
        # Add the last job if it has a description
        if current_job["description"]:
            experience_info.append(current_job)
    except Exception as e:
        print(f"Error in experience identification: {e}")
    
    return experience_info

def extract_skills(text, skills_db=None):
    """Extract skills from the text and categorize them."""
    if skills_db is None:
        skills_db = SKILLS_DB['skills']
    
    try:
        # Normalize text for skill matching
        normalized_text = normalize_text(text)
        
        # Extract skills
        found_skills = {}
        for skill in skills_db:
            skill_pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(skill_pattern, normalized_text):
                # Categorize the skill
                category = "other"
                for cat, skills in SKILL_CATEGORIES.items():
                    if skill.lower() in skills:
                        category = cat
                        break
                
                if category not in found_skills:
                    found_skills[category] = []
                found_skills[category].append(skill)
    except Exception as e:
        print(f"Error in skill extraction: {e}")
        found_skills = {"other": ["error_processing_skills"]}
    
    return found_skills

def analyze_job_description(job_description):
    """Analyze job description to extract requirements and categorize them as required or preferred."""
    try:
        # Normalize text
        normalized_text = normalize_text(job_description)
        
        # Identify required vs preferred skills
        required_skills = []
        preferred_skills = []
        
        # Pattern matching for required skills
        required_pattern = r'(?i)(required|must have|essential)(.+?)(preferred|nice to have|desirable|\.|$)'
        preferred_pattern = r'(?i)(preferred|nice to have|desirable)(.+?)(required|must have|essential|\.|$)'
        
        # Extract required skills
        req_matches = re.findall(required_pattern, job_description)
        for match in req_matches:
            if match and len(match) > 1:
                skills = extract_skills(match[1])
                for category, skill_list in skills.items():
                    for skill in skill_list:
                        if skill not in required_skills:
                            required_skills.append(skill)
        
        # Extract preferred skills
        pref_matches = re.findall(preferred_pattern, job_description)
        for match in pref_matches:
            if match and len(match) > 1:
                skills = extract_skills(match[1])
                for category, skill_list in skills.items():
                    for skill in skill_list:
                        if skill not in preferred_skills and skill not in required_skills:
                            preferred_skills.append(skill)
        
        # If no explicit required/preferred sections, intelligently distribute skills
        if not required_skills and not preferred_skills:
            all_skills = extract_skills(job_description)
            all_skills_flat = []
            for category, skill_list in all_skills.items():
                all_skills_flat.extend(skill_list)
            
            # Distribute skills: 70% required, 30% preferred
            if all_skills_flat:
                required_count = max(1, int(len(all_skills_flat) * 0.7))
                required_skills = all_skills_flat[:required_count]
                preferred_skills = all_skills_flat[required_count:]
    except Exception as e:
        print(f"Error in job description analysis: {e}")
        # Fallback to empty lists
        required_skills = []
        preferred_skills = []
    
    return {
        'required': required_skills,
        'preferred': preferred_skills
    }

def calculate_skill_match(resume_skills, job_skills):
    """Calculate skill match score based on required and preferred skills."""
    try:
        required = set(job_skills.get('required', []))
        preferred = set(job_skills.get('preferred', []))
        
        # Flatten the categorized resume skills
        all_resume_skills = []
        for category, skills in resume_skills.items():
            all_resume_skills.extend(skills)
        resume_skill_set = set(all_resume_skills)
        
        # Calculate matches
        required_matches = resume_skill_set.intersection(required)
        preferred_matches = resume_skill_set.intersection(preferred)
        
        # Calculate scores
        required_score = len(required_matches) / len(required) if required else 0
        preferred_score = len(preferred_matches) / len(preferred) if preferred else 0
        
        # Calculate skill gaps
        skill_gaps = {
            'required': list(required - required_matches),
            'preferred': list(preferred - preferred_matches)
        }
    except Exception as e:
        print(f"Error in skill matching: {e}")
        # Fallback to zero scores
        required_score = 0
        preferred_score = 0
        required_matches = []
        preferred_matches = []
        skill_gaps = {'required': [], 'preferred': []}
    
    return {
        'required_score': required_score,
        'preferred_score': preferred_score,
        'required_matched': list(required_matches),
        'preferred_matched': list(preferred_matches),
        'skill_gaps': skill_gaps
    }

def calculate_weighted_score(match_scores, weights=None):
    """Calculate weighted total score based on different match criteria."""
    if weights is None:
        weights = {
            'required_skills': 0.6,
            'preferred_skills': 0.2,
            'semantic_similarity': 0.2
        }
    
    try:
        # Calculate weighted score
        total_score = (
            match_scores['required_score'] * weights['required_skills'] +
            match_scores['preferred_score'] * weights['preferred_skills'] +
            match_scores['semantic_similarity'] * weights['semantic_similarity']
        )
    except Exception as e:
        print(f"Error in weighted score calculation: {e}")
        # Fallback to simple average
        total_score = sum(match_scores.values()) / len(match_scores)
    
    return total_score

def extract_job_description(job_description):
    """Cleans and preprocesses the job description."""
    return job_description.strip().lower()

def semantic_similarity(resume_text, job_description):
    """Calculate semantic similarity between resume and job description."""
    try:
        job_doc = nlp(job_description)
        resume_doc = nlp(resume_text)
        return job_doc.similarity(resume_doc)
    except Exception as e:
        print(f"Error in semantic similarity calculation: {e}")
        return 0.5  # Fallback to neutral similarity

def process_resumes(files, job_description, weights=None):
    """Processes resumes and ranks them based on advanced analysis algorithms."""
    # Set default weights if not provided
    if weights is None:
        weights = {
            'required_skills': 0.6,
            'preferred_skills': 0.2,
            'semantic_similarity': 0.2
        }
    
    # Process job description
    job_description_text = extract_job_description(job_description)
    job_skills = analyze_job_description(job_description)
    
    results = []

    for file in files:
        try:
            if not file or not file.filename:
                continue  # Skip empty files
                
            # Create temporary file path
            file_path = os.path.join("app", "uploads", file.filename)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save the file
            file.save(file_path)

            # Extract text from resume
            resume_text = extract_text_from_pdf(file_path)
            
            # Skip files with extraction errors
            if resume_text.startswith("Error processing file:"):
                print(f"Skipping {file.filename}: {resume_text}")
                continue
            
            # Extract sections
            sections = extract_sections(resume_text)
            
            # Extract education details
            education = identify_education(sections['education'])
            
            # Extract work experience
            experience = identify_experience(sections['experience'])
            
            # Extract skills and categorize them
            resume_skills = extract_skills(resume_text)
            
            # Calculate skill match
            skill_match = calculate_skill_match(resume_skills, job_skills)
            
            # Calculate semantic similarity
            similarity_score = semantic_similarity(resume_text, job_description_text)
            
            # Add semantic similarity to match scores
            match_scores = {
                'required_score': skill_match['required_score'],
                'preferred_score': skill_match['preferred_score'],
                'semantic_similarity': similarity_score
            }
            
            # Calculate weighted total score
            total_score = calculate_weighted_score(match_scores, weights)

            results.append({
                "file_name": file.filename,
                "required_skills_score": skill_match['required_score'] * 100,  # Convert to percentage
                "preferred_skills_score": skill_match['preferred_score'] * 100,  # Convert to percentage
                "semantic_similarity": similarity_score * 100,  # Convert to percentage
                "total_score": total_score * 100,  # Convert to percentage
                "education": education,
                "experience": experience,
                "skills": resume_skills,
                "skill_gaps": skill_match['skill_gaps'],
                "resume_preview": resume_text[:500],
            })
        
        except Exception as e:
            print(f"Error processing resume {file.filename if file and hasattr(file, 'filename') else 'unknown'}: {e}")
        
        finally:
            # Clean up uploaded file
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:
                pass

    # Sort results by total score
    results.sort(key=lambda x: x["total_score"], reverse=True)
    return results