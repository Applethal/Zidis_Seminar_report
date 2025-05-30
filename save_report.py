import pandas as pd
import os
import glob
import subprocess
from pathlib import Path
from collections import defaultdict

def clean_text(text):
    if pd.isna(text) or text == "" or "[BILD]" in str(text):
        return None

    text = str(text).replace("&", "\\&")
    text = text.replace("%", "\\%")
    text = text.replace("$", "\\$")
    text = text.replace("#", "\\#")
    text = text.replace("_", "\\_")
    text = text.replace("{", "\\{")
    text = text.replace("}", "\\}")
    text = text.replace("^", "\\textasciicircum{}")
    text = text.replace("~", "\\textasciitilde{}")
    text = text.replace("\\", "\\textbackslash{}")

    text = text.replace("ä", "{\\\"a}")
    text = text.replace("ö", "{\\\"o}")
    text = text.replace("ü", "{\\\"u}")
    text = text.replace("Ä", "{\\\"A}")
    text = text.replace("Ö", "{\\\"O}")
    text = text.replace("Ü", "{\\\"U}")
    text = text.replace("ß", "{\\ss}")

    return text.strip()

def escape_filename_for_section(filename):
    escaped = filename.replace("_", "\\textunderscore{}")
    escaped = escaped.replace("ä", "{\\\"a}")
    escaped = escaped.replace("ö", "{\\\"o}")
    escaped = escaped.replace("ü", "{\\\"u}")
    escaped = escaped.replace("Ä", "{\\\"A}")
    escaped = escaped.replace("Ö", "{\\\"O}")
    escaped = escaped.replace("Ü", "{\\\"U}")
    escaped = escaped.replace("ß", "{\\ss}")
    return escaped

def read_csv_with_encoding(csv_file, sep=';'):
    encodings = ['utf-8', 'windows-1252', 'iso-8859-1', 'cp1252', 'latin1']

    for encoding in encodings:
        try:
            return pd.read_csv(csv_file, sep=sep, encoding=encoding)
        except UnicodeDecodeError:
            continue

    try:
        return pd.read_csv(csv_file, sep=sep, encoding='utf-8', errors='ignore')
    except:
        raise Exception(f"Could not read file with any encoding")

def compile_latex(tex_file):
    """Compile LaTeX file to PDF using pdflatex"""
    try:
        print(f"Compiling {tex_file} to PDF...")

        # Run pdflatex twice to ensure proper references and table of contents
        for i in range(2):
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', tex_file],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.abspath(tex_file)) or '.'
            )

            if result.returncode != 0:
                print(f"Error during pdflatex compilation (run {i+1}):")
                print(result.stdout)
                print(result.stderr)
                return False

        pdf_file = tex_file.replace('.tex', '.pdf')
        if os.path.exists(pdf_file):
            print(f"PDF successfully generated: {pdf_file}")
            return True
        else:
            print("PDF file was not created despite successful compilation")
            return False

    except FileNotFoundError:
        print("Error: pdflatex not found. Please ensure LaTeX is installed and pdflatex is in your PATH.")
        return False
    except Exception as e:
        print(f"Error during compilation: {str(e)}")
        return False

def process_csv_files(folder_path, output_file="survey_report.tex"):
    target_columns = [
        "Das war gut:",
        "Das würde ich mir noch wünschen:",
        "Folgende Themen und Tools fand ich besonders nützlich:"
    ]

    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

    if not csv_files:
        print(f"No CSV files found in {folder_path}")
        return

    # Dictionary to store all comments by category
    comments_by_category = defaultdict(list)

    # Process all CSV files and collect comments by category
    processed_files = 0
    for csv_file in sorted(csv_files):
        try:
            df = read_csv_with_encoding(csv_file, sep=';')
            filename = Path(csv_file).stem

            print(f"Processing: {filename}")

            for column in target_columns:
                if column in df.columns:
                    for value in df[column]:
                        cleaned = clean_text(value)
                        if cleaned:
                            # Add source file information to each comment
                            comments_by_category[column].append({
                                'comment': cleaned,
                                'source': filename
                            })
                else:
                    print(f"Warning: Column '{column}' not found in {csv_file}")

            processed_files += 1

        except Exception as e:
            print(f"Error processing {csv_file}: {str(e)}")
            continue

    # Generate LaTeX content
    latex_content = []
    latex_content.append("\\documentclass[12pt,a4paper]{article}")
    latex_content.append("\\usepackage[utf8]{inputenc}")
    latex_content.append("\\usepackage[main=ngerman,provide=*]{babel}")
    latex_content.append("\\usepackage{geometry}")
    latex_content.append("\\geometry{margin=2cm}")
    latex_content.append("\\usepackage{enumitem}")
    latex_content.append("\\usepackage[colorlinks=true,linkcolor=blue,urlcolor=blue]{hyperref}")
    latex_content.append("\\usepackage{xcolor}")
    latex_content.append("")
    latex_content.append("\\title{Seminar Feedback Analyse}")
    latex_content.append("\\author{Zidis}")
    latex_content.append("\\date{\\today}")
    latex_content.append("")
    latex_content.append("\\begin{document}")
    latex_content.append("\\maketitle")
    latex_content.append("")
    latex_content.append(f"\\textbf{{Anzahl verarbeiteter Dateien:}} {processed_files}")
    latex_content.append("")
    latex_content.append("\\tableofcontents")
    latex_content.append("\\newpage")
    latex_content.append("")

    # Create sections for each category with all bundled responses
    for column in target_columns:
        if column in comments_by_category and comments_by_category[column]:
            section_name = column.replace(":", "").strip()
            latex_content.append(f"\\section{{{section_name}}}")
            latex_content.append("")

            total_comments = len(comments_by_category[column])
            latex_content.append(f"\\textbf{{Anzahl Antworten:}} {total_comments}")
            latex_content.append("")

            latex_content.append("\\begin{itemize}[leftmargin=*]")

            for item in comments_by_category[column]:
                # Add the comment with source file reference
                escaped_source = escape_filename_for_section(item['source'])
                latex_content.append(f"\\item {item['comment']} \\textcolor{{gray}}{{\\small({escaped_source})}}")

            latex_content.append("\\end{itemize}")
            latex_content.append("")
            latex_content.append("\\newpage")
        else:
            section_name = column.replace(":", "").strip()
            latex_content.append(f"\\section{{{section_name}}}")
            latex_content.append("")
            latex_content.append("Keine Antworten in dieser Kategorie gefunden.")
            latex_content.append("")
            latex_content.append("\\newpage")

    latex_content.append("\\end{document}")

    # Write LaTeX file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(latex_content))
        print(f"LaTeX document generated successfully: {output_file}")
        print(f"Processed {processed_files} CSV files")

        # Automatically compile to PDF
        success = compile_latex(output_file)
        if success:
            print("Report generation and compilation completed successfully!")
        else:
            print("LaTeX file generated, but PDF compilation failed.")
            print(f"You can manually compile with: pdflatex {output_file}")

    except Exception as e:
        print(f"Error writing output file: {str(e)}")

def main():
    folder_path = "."
    output_file = "survey_report.tex"

    process_csv_files(folder_path, output_file)

if __name__ == "__main__":
    main()
