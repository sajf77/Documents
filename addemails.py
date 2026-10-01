#!/usr/bin/env python3
import os
import pandas as pd

def main():
    ods_file = "YTcourses.ods"
    output_dir = "Stage4"
    email_col_idx = 2  # Column C
    
    # Mapping of Column Index (A=0, B=1, C=2, D=3...) to Filenames
    subjects = {
        3: "stat.txt",       # D -> stat
        4: "complex.txt",    # E -> complex
        5: "topology.txt",   # F -> Topology
        6: "numerical.txt",  # G -> numerical
        7: "special.txt"     # H -> special
    }

    if not os.path.exists(ods_file):
        print(f"❌ Error: '{ods_file}' not found.")
        return

    # Ensure the Stage4 directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Initialize empty lists for each subject
    collected_emails = {col: [] for col in subjects.keys()}

    print(f"⏳ Reading '{ods_file}'...")
    df = pd.read_excel(ods_file, engine="odf", header=None)

    # Scan all rows
    for index, row in df.iterrows():
        if len(row) > email_col_idx:
            email = str(row[email_col_idx]).strip()
            
            if email.lower() != "nan" and email:
                # Check each subject column for this specific row
                for col_idx in subjects.keys():
                    if len(row) > col_idx:
                        checkbox_val = str(row[col_idx]).strip().lower()
                        
                        if checkbox_val in ["☑", "true", "1.0"]:
                            if email not in collected_emails[col_idx]:
                                collected_emails[col_idx].append(email)

    # Overwrite each text file with its updated list
    print("\n📊 Sync Results:")
    for col_idx, filename in subjects.items():
        filepath = os.path.join(output_dir, filename)
        emails = collected_emails[col_idx]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(",\n".join(emails))
            
        print(f"  ✅ {filename}: {len(emails)} emails")

    print(f"\n🎉 All files in '{output_dir}/' have been updated!")

if __name__ == "__main__":
    main()
