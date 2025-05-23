import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, jsonify
from fpdf import FPDF
import matplotlib
matplotlib.use('Agg')  # Set backend for matplotlib
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
from .utils import process_resumes

main = Blueprint("main", __name__)

@main.route("/")
def index():
    """Render the homepage with the upload form."""
    return render_template("index.html")

@main.route("/upload", methods=["POST"])
def upload():
    """Handle file uploads and job description with customizable weights."""
    try:
        # Check if resumes are provided
        if "resumes" not in request.files:
            flash("No resume files were selected. Please upload at least one resume.")
            return redirect(url_for("main.index"))

        # Get uploaded files and job description
        files = request.files.getlist("resumes")
        
        # Check if files were actually selected
        if not files or files[0].filename == '':
            flash("No resume files were selected. Please upload at least one resume.")
            return redirect(url_for("main.index"))
        
        # Get job description
        job_description = request.form.get("job_description", "")
        if not job_description.strip():
            flash("Please provide a job description for analysis.")
            return redirect(url_for("main.index"))

        # Get customizable weights if provided
        weights = {
            'required_skills': float(request.form.get("weight_required", 0.6)),
            'preferred_skills': float(request.form.get("weight_preferred", 0.2)),
            'semantic_similarity': float(request.form.get("weight_similarity", 0.2))
        }
        
        # Ensure uploads directory exists
        upload_dir = os.path.join("app", "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        # Process resumes with the provided weights
        try:
            results = process_resumes(files, job_description, weights)
            
            if not results:
                flash("No valid results could be generated. Please check your files and job description.")
                return redirect(url_for("main.index"))
                
        except Exception as e:
            flash(f"An error occurred while processing resumes: {str(e)}")
            return redirect(url_for("main.index"))

        # Generate visualizations for the results
        visualizations = []
        
        for result in results:
            # Skill match visualization (radar chart)
            skill_match_img = generate_skill_radar_chart(result)
            
            # Skill gaps visualization (bar chart)
            skill_gaps_img = generate_skill_gaps_chart(result)
            
            visualizations.append({
                'file_name': result['file_name'],
                'skill_match': skill_match_img,
                'skill_gaps': skill_gaps_img
            })

        # Pass results and visualizations to the results page
        return render_template("results.html", results=results, visualizations=visualizations)
        
    except Exception as e:
        flash(f"An unexpected error occurred: {str(e)}")
        return redirect(url_for("main.index"))

def generate_skill_radar_chart(result):
    """Generate radar chart for skill match visualization."""
    # Create a radar chart of skill categories
    categories = []
    values = []
    
    # Extract skill categories and their counts
    for category, skills in result['skills'].items():
        categories.append(category)
        values.append(len(skills))
    
    # If no skills found, return empty image
    if not categories:
        return ""
    
    # Create radar chart
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, polar=True)
    
    # Complete the loop for the radar
    categories.append(categories[0])
    values.append(values[0])
    
    # Convert to numpy arrays
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=True)
    values = np.array(values)
    
    # Plot
    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, alpha=0.25)
    
    # Set category labels
    plt.xticks(angles[:-1], categories[:-1])
    
    # Draw axis lines for each angle and label
    ax.set_rlabel_position(0)
    plt.yticks([2, 4, 6, 8, 10], color="grey", size=7)
    plt.ylim(0, 10)
    
    # Convert plot to base64 string
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    plt.close()
    
    return base64.b64encode(img_data.read()).decode('utf-8')

def generate_skill_gaps_chart(result):
    """Generate bar chart for skill gaps visualization."""
    # Get required and preferred skill gaps
    required_gaps = result['skill_gaps']['required']
    preferred_gaps = result['skill_gaps']['preferred']
    
    # If no gaps, return empty image
    if not required_gaps and not preferred_gaps:
        return ""
    
    # Create bar chart with increased width for better label visibility
    fig, ax = plt.subplots(figsize=(8, 4.5))
    
    # Plot required and preferred skill gaps
    y_pos = np.arange(len(required_gaps) + len(preferred_gaps))
    all_gaps = required_gaps + preferred_gaps
    colors = ['red'] * len(required_gaps) + ['orange'] * len(preferred_gaps)
    
    # Add bars with a bit more width
    bars = ax.barh(y_pos, [1] * len(all_gaps), color=colors, alpha=0.7)
    
    # Improve y-axis label display
    ax.set_yticks(y_pos)
    ax.set_yticklabels(all_gaps)
    ax.invert_yaxis()  # Labels read top-to-bottom
    
    # Add more space on the left for labels
    plt.subplots_adjust(left=0.25)
    
    # Add title with a bit more padding
    ax.set_title('Skill Gaps', pad=10)
    
    # Remove x-axis ticks as they're not meaningful in this context
    ax.set_xticks([])
    ax.set_xlim(0, 1.1)  # Set x limit to make bars take most of the width
    
    # Clean up the chart with minimal unnecessary elements
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    # Add legend with better positioning
    red_patch = plt.Rectangle((0, 0), 1, 1, fc="red", alpha=0.7)
    orange_patch = plt.Rectangle((0, 0), 1, 1, fc="orange", alpha=0.7)
    ax.legend([red_patch, orange_patch], ['Required', 'Preferred'], 
              loc='upper right', bbox_to_anchor=(1, 1))
    
    # Convert plot to base64 string
    img_data = BytesIO()
    plt.savefig(img_data, format='png', dpi=100, bbox_inches='tight')
    img_data.seek(0)
    plt.close()
    
    return base64.b64encode(img_data.read()).decode('utf-8')

@main.route("/download", methods=["POST"])
def download_results():
    """Generate and download a PDF of the analysis results."""
    # Check if results are provided in the request
    results = request.get_json()
    if not results:
        return jsonify({"error": "No results available for download"}), 400

    try:
        # Create a PDF report
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add title
        pdf.cell(200, 10, txt="Resume Analysis Results", ln=True, align="C")
        pdf.ln(10)

        # Add results to the PDF
        for result in results:
            pdf.set_font("Arial", 'B', size=14)
            pdf.cell(0, 10, txt=f"Resume: {result['file_name']}", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.ln(5)
            
            # Add scores
            pdf.set_font("Arial", 'B', size=12)
            pdf.cell(0, 10, txt="Scores:", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, txt=f"Required Skills Score: {result['required_skills_score']:.2f}%", ln=True)
            pdf.cell(0, 10, txt=f"Preferred Skills Score: {result['preferred_skills_score']:.2f}%", ln=True)
            pdf.cell(0, 10, txt=f"Semantic Similarity: {result['semantic_similarity']:.2f}%", ln=True)
            pdf.cell(0, 10, txt=f"Total Score: {result['total_score']:.2f}%", ln=True)
            
            # Add education details
            pdf.ln(5)
            pdf.set_font("Arial", 'B', size=12)
            pdf.cell(0, 10, txt="Education:", ln=True)
            pdf.set_font("Arial", size=12)
            if result.get('education'):
                for edu in result.get('education', []):
                    pdf.multi_cell(0, 10, txt=f"- {edu}")
            else:
                pdf.cell(0, 10, txt="No education details found", ln=True)
            
            # Add experience details
            pdf.ln(5)
            pdf.set_font("Arial", 'B', size=12)
            pdf.cell(0, 10, txt="Experience:", ln=True)
            pdf.set_font("Arial", size=12)
            if result.get('experience'):
                for exp in result.get('experience', []):
                    if isinstance(exp, dict):
                        pdf.multi_cell(0, 10, txt=f"- {exp.get('title', '')} at {exp.get('company', '')} ({exp.get('duration', '')})")
                    else:
                        pdf.multi_cell(0, 10, txt=f"- {exp}")
            else:
                pdf.cell(0, 10, txt="No experience details found", ln=True)
            
            # Add skill gaps
            pdf.ln(5)
            pdf.set_font("Arial", 'B', size=12)
            pdf.cell(0, 10, txt="Skill Gaps:", ln=True)
            pdf.set_font("Arial", size=12)
            
            # Required skills
            pdf.set_font("Arial", 'I', size=12)
            pdf.cell(0, 10, txt="Required skills missing:", ln=True)
            pdf.set_font("Arial", size=12)
            if result.get('skill_gaps', {}).get('required'):
                for skill in result.get('skill_gaps', {}).get('required', []):
                    pdf.multi_cell(0, 10, txt=f"- {skill}")
            else:
                pdf.cell(0, 10, txt="None - All required skills matched!", ln=True)
            
            # Preferred skills
            pdf.set_font("Arial", 'I', size=12)
            pdf.cell(0, 10, txt="Preferred skills missing:", ln=True)
            pdf.set_font("Arial", size=12)
            if result.get('skill_gaps', {}).get('preferred'):
                for skill in result.get('skill_gaps', {}).get('preferred', []):
                    pdf.multi_cell(0, 10, txt=f"- {skill}")
            else:
                pdf.cell(0, 10, txt="None - All preferred skills matched!", ln=True)
            
            # Add page break between resumes
            if results.index(result) < len(results) - 1:
                pdf.add_page()

        # Save PDF to a temporary file with a unique timestamp
        import time
        timestamp = int(time.time())
        output_filename = f"results_{timestamp}.pdf"
        output_path = os.path.join("app", "uploads", output_filename)
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Generate the PDF
        pdf.output(output_path)
        
        # Ensure the file exists and has content
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            from flask import Response
            
            # Read the file content
            with open(output_path, 'rb') as f:
                pdf_data = f.read()
            
            # Clean up the file after reading
            try:
                os.remove(output_path)
            except:
                pass
                
            # Return the PDF data with appropriate headers
            response = Response(pdf_data, 
                               mimetype='application/pdf',
                               headers={
                                   'Content-Disposition': f'attachment; filename=resume_analysis_results.pdf',
                                   'Content-Length': len(pdf_data)
                               })
            return response
        else:
            return jsonify({"error": "Failed to generate PDF"}), 500
            
    except Exception as e:
        import traceback
        print(f"Error generating PDF: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@main.route("/customize_weights", methods=["GET", "POST"])
def customize_weights():
    """Allow users to customize the weights for resume analysis."""
    if request.method == "POST":
        # Get customized weights from form
        weights = {
            'required_skills': float(request.form.get("weight_required", 0.6)),
            'preferred_skills': float(request.form.get("weight_preferred", 0.2)),
            'semantic_similarity': float(request.form.get("weight_similarity", 0.2))
        }
        
        # Return to index with the weights as session data
        return render_template("index.html", weights=weights)
    
    # Display the weight customization form
    return render_template("customize_weights.html")

@main.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for debugging."""
    return jsonify({"status": "ok", "message": "Service is running"})