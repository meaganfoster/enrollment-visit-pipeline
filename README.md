# Enrollment and Outpatient Visit Processing Pipeline

This pipeline processes monthly patient enrollment data and calculates continuous enrollment spans, including outpatient visit statistics during those spans.

## Files and Structure
enrollment-visit-pipeline/
├── data/ # Raw input files (not tracked by Git)
├── output/ # Output files (not tracked by Git)
├── pipeline/
│ ├── io.py # Handles input file detection
│ ├── transform.py # Data cleaning and enrollment span labeling
│ ├── enrichment.py # Adds outpatient visit metrics
│ ├── qa.py # Validates enrollment spans
│ └── logger.py # Logging
├── run_enrollment_pipeline.py # Main runner script
├── requirements.txt # Python dependencies
└── README.md # You’re here!

## How It Works

1. Load monthly enrollment data (`patient_id_month_year - patient_id_month_year.csv`) and outpatient visit records (`outpatient_visits_file.csv`)**
2. **Sort and group into continuous enrollment periods**
3. **Run QA checks to identify spacing or formatting issues**
5. **Count visits and distinct visit days per enrollment span**
6. **Output to `output/results.csv`**

## How to Run
# Add enrollment and visits date to /data folder

Input File Expectations
  data/patient_id_month_year - patient_id_month_year.csv
    Columns: patient_id, month_year

  data/outpatient_visits_file.csv
    Columns: patient_id, date, outpatient_visit_count
  
# (Optional) Activate your virtual environment
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Run the pipeline
python run_enrollment_pipeline.py
Note: You’ll be asked whether to enable QA mode (writes step-by-step Excel outputs and runs validation).

Output

  output/results.csv
    Columns: patient_id, enrollment_start_date, enrollment_end_date, ct_outpatient_visits (total visits in the period), ct_days_with_outpatient_visit (number of distinct days with visits)

Git Ignore
All raw data, output files, virtual envs, and logs are excluded from version control by .gitignore.

Author
Meagan Foster
@meaganfoster
