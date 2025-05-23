# Smart Resume Analyzer

<p align="center">
  <img src="images/logo.png" alt="Smart Resume Analyzer Logo" width="200"/>
  <br>
  <em>Streamlining recruitment through intelligent resume analysis</em>
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#technology-stack">Technology Stack</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#future-roadmap">Future Roadmap</a>
</p>

<p align="center">
  <img src="images/demo.png" alt="Demo" width="600">
</p>

## Overview

Smart Resume Analyzer is an intelligent web application that leverages Natural Language Processing (NLP) to automate the resume screening process. By analyzing resumes against job descriptions, the system provides objective, data-driven insights to help recruiters identify the most suitable candidates efficiently.

## Key Features

✨ **Intelligent Resume Parsing**
- Extracts and categorizes information from PDF resumes
- Identifies education, experience, and skills automatically
- Processes multiple resumes simultaneously

🔍 **Advanced Matching Algorithm**
- Matches resumes against job requirements using weighted criteria
- Distinguishes between required and preferred skills
- Employs semantic similarity for context-aware matching

📊 **Interactive Visualizations**
- Skill category radar charts
- Color-coded skill gap analysis
- Progress indicators for match scores

⚖️ **Customizable Analysis**
- Adjustable weights for different matching criteria
- Interactive sliders for personalized assessment

📋 **Comprehensive Reporting**
- Downloadable PDF reports
- Detailed candidate information and match scores
- Visual representations of strengths and skill gaps

## Technology Stack

### Frontend
- HTML5, CSS3, JavaScript
- Responsive design with custom styling
- Interactive elements for file uploads and parameter adjustment

### Backend
- Python 3.8+
- Flask web framework
- RESTful API endpoints

### NLP & Data Processing
- NLTK for tokenization and lemmatization
- spaCy for entity recognition and semantic analysis
- PyPDF2 for document parsing

### Data Visualization
- Matplotlib for chart generation
- Base64 encoding for web display

### Reporting
- FPDF for PDF generation

## Architecture

Smart Resume Analyzer implements a modular architecture:

```ascii
+---------------------+
|  User Interface     |
|  (Web Frontend)     |
+----------+----------+
           |
           v
+----------+----------+
|  Web Application    |
|  (Flask Server)     |
+----------+----------+
           |
   +-------+-------+
   |       |       |
   v       v       v
+-----+ +-----+ +-----+
|File | |NLP  | |Match|
|Proc.| |Proc.| |Eng. |
+-----+ +-----+ +-----+
   |       |       |
   +-------+-------+
           |
           v
+----------+----------+
| Visualization &     |
| Reporting Engine    |
+----------+----------+
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Setup Process

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/smart-resume-analyzer.git
   cd smart-resume-analyzer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download required NLP models:
   ```bash
   python -m spacy download en_core_web_md
   python -m nltk.downloader punkt stopwords wordnet averaged_perceptron_tagger
   ```

5. Run the application:
   ```bash
   python main.py
   ```

6. Access the application at `http://localhost:5000`

## Usage

### Resume Analysis Process

1. **Upload Resumes**
   - Drag and drop PDF files
   - Or click to browse and select files
   - Multiple files can be uploaded simultaneously

2. **Enter Job Description**
   - Paste job posting text
   - Include required and preferred skills sections for best results

3. **Customize Weights (Optional)**
   - Adjust importance of required skills (default: 60%)
   - Adjust importance of preferred skills (default: 20%)
   - Adjust importance of semantic similarity (default: 20%)

4. **View Results**
   - Overall match scores
   - Skills breakdown by category
   - Education and experience details
   - Skill gap analysis

5. **Download Reports**
   - Generate comprehensive PDF summary
   - Share with team members or stakeholders

## Screenshots

<p align="center">
  <img src="images/upload.png" alt="Upload Interface" width="400"/>
  <br><em>Resume Upload Interface</em>
</p>

<p align="center">
  <img src="images/results.png" alt="Results Dashboard" width="400"/>
  <br><em>Results Dashboard</em>
</p>

<p align="center">
  <img src="images/visualization.png" alt="Skill Visualization" width="400"/>
  <br><em>Skill Analysis Visualization</em>
</p>

## Future Roadmap

### Near-term Enhancements
- Support for DOCX and other resume formats
- Enhanced semantic analysis with BERT/GPT-based embeddings
- Expanded skills database with industry-specific terms

### Long-term Vision
- Integration with Applicant Tracking Systems (ATS)
- Machine learning components for improved matching accuracy
- Mobile application development
- Multi-language support

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

Please ensure your code follows the project's style guidelines and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- NLTK team for natural language processing tools
- spaCy for advanced NLP capabilities
- Flask team for the web framework
- All contributors who have helped shape this project

---

<p align="center">
  <a href="https://github.com/yourusername">GitHub</a> •
  <a href="mailto:your.email@example.com">Contact</a>
</p>