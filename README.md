# Smart Resume Analyzer 📄✨

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version"/>
  <img src="https://img.shields.io/badge/Flask-2.0+-green.svg" alt="Flask Version"/>
  <img src="https://img.shields.io/badge/NLP-spaCy%20%7C%20NLTK-yellow.svg" alt="NLP Libraries"/>
  <img src="https://img.shields.io/badge/License-MIT-red.svg" alt="License"/>
</p>

<p align="center">
  <b>Streamlining recruitment through intelligent resume analysis</b>
</p>

![Demo Banner](https://raw.githubusercontent.com/hassanrrraza/resume_analyzer/main/app/static/img/demo.png)

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Future Roadmap](#future-roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## 🔍 Overview

Smart Resume Analyzer is an intelligent web application that leverages Natural Language Processing (NLP) to automate the resume screening process. By analyzing resumes against job descriptions, the system provides objective, data-driven insights to help recruiters identify the most suitable candidates efficiently.

## ✨ Key Features

### Intelligent Resume Parsing
- Extracts and categorizes information from PDF resumes
- Identifies education, experience, and skills automatically
- Processes multiple resumes simultaneously

### Advanced Matching Algorithm
- Matches resumes against job requirements using weighted criteria
- Distinguishes between required and preferred skills
- Employs semantic similarity for context-aware matching

### Interactive Visualizations
- Skill category radar charts
- Color-coded skill gap analysis
- Progress indicators for match scores

### Customizable Analysis
- Adjustable weights for different matching criteria
- Interactive sliders for personalized assessment

### Comprehensive Reporting
- Downloadable PDF reports
- Detailed candidate information and match scores
- Visual representations of strengths and skill gaps

## 🛠️ Technology Stack

<table>
  <tr>
    <td><b>Frontend</b></td>
    <td>
      • HTML5, CSS3, JavaScript<br>
      • Responsive design with custom styling<br>
      • Interactive elements for file uploads and parameter adjustment
    </td>
  </tr>
  <tr>
    <td><b>Backend</b></td>
    <td>
      • Python 3.8+<br>
      • Flask web framework<br>
      • RESTful API endpoints
    </td>
  </tr>
  <tr>
    <td><b>NLP & Data Processing</b></td>
    <td>
      • NLTK for tokenization and lemmatization<br>
      • spaCy for entity recognition and semantic analysis<br>
      • PyPDF2 for document parsing
    </td>
  </tr>
  <tr>
    <td><b>Data Visualization</b></td>
    <td>
      • Matplotlib for chart generation<br>
      • Base64 encoding for web display
    </td>
  </tr>
  <tr>
    <td><b>Reporting</b></td>
    <td>
      • FPDF for PDF generation
    </td>
  </tr>
</table>

## 🏗️ Architecture

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

## ⚙️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Setup Process

1. Clone the repository:
   ```bash
   git clone https://github.com/hassanrrraza/resume_analyzer
   cd resume_analyzer
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

## 🚀 Usage

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

## 📸 Screenshots

<details open>
<summary><b>Resume Upload Interface</b></summary>
<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/hassanrrraza/resume_analyzer/main/app/static/img/upload.png" alt="Upload Interface" width="700"/>
</p>
</details>

<details>
<summary><b>Results Dashboard</b></summary>
<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/hassanrrraza/resume_analyzer/main/app/static/img/results.png" alt="Results Dashboard" width="700"/>
</p>
</details>

<details>
<summary><b>Skill Analysis Visualization</b></summary>
<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/hassanrrraza/resume_analyzer/main/app/static/img/visualization.png" alt="Skill Visualization" width="700"/>
</p>
</details>

## 🔮 Future Roadmap

### Near-term Enhancements
- Support for DOCX and other resume formats
- Enhanced semantic analysis with BERT/GPT-based embeddings
- Expanded skills database with industry-specific terms

### Long-term Vision
- Integration with Applicant Tracking Systems (ATS)
- Machine learning components for improved matching accuracy
- Mobile application development
- Multi-language support

## 👥 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

Please ensure your code follows the project's style guidelines and includes appropriate tests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NLTK team for natural language processing tools
- spaCy for advanced NLP capabilities
- Flask team for the web framework
- All contributors who have helped shape this project

---

<p align="center">
  <a href="https://github.com/hassanrrraza">GitHub</a> •
  <a href="mailto:hassan2056764@gmail.com">Contact</a>
</p>