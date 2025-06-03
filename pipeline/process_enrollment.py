import os
import pandas as pd
from pipeline.logger import setup_logger
from pipeline.io import import_enrollments, import_outpatient_visits
from pipeline.transform import convert_month_year_to_datetime, sort_by_patient_and_month_year, summarize_enrollment_spans
from pipeline.qa import check_span_gaps
from pipeline.enrichment import attach_outpatient_visit_counts


def process_enrollment(input_dir, output_dir, test_mode=False):
    # Set up logger
    logger = setup_logger()
    logger.info("Starting enrollment processing...")

    # Import enrollment file
    enrollment_path = import_enrollments(input_dir)
    df = pd.read_csv(enrollment_path)
    logger.info(f"Step 1: Loaded enrollment file: {enrollment_path}")

    # QA Check: Print to file
    if test_mode:
        df.to_excel(os.path.join(output_dir, "step1_raw.xlsx"), index=False)
        logger.info("Step 1.1 - Saved step1_raw.xlsx")

    # Format dates
    df = convert_month_year_to_datetime(df, output_dir, test_mode)
    logger.info("Step 2: Converted 'month_year' to datetime.")

    # Sort file
    df = sort_by_patient_and_month_year(df, output_dir, test_mode)
    logger.info("Step 3: Sorted by patient_id and month_year.")

    # Create distinct enrollment periods per patient
    enrollment_spans = summarize_enrollment_spans(df, output_dir, test_mode)
    logger.info("Step 4: Summarized into enrollment spans.")

    # QA check: Confirm enrollment spans are distinct
    if test_mode:
        check_span_gaps(enrollment_spans, output_dir=output_dir, logger=logger, raise_on_violation=True)
        logger.info("Step 4.1 - Enrollment spans check completed.")

    # Save to patient_enrollment_span.csv
    output_path = os.path.join(output_dir, "patient_enrollment_span.csv")
    enrollment_spans.to_csv(output_path, index=False)
    logger.info(f"Final output saved to: {output_path}")
    logger.info(f"Number of rows in patient_enrollment_span.csv:'  {len(enrollment_spans)}")
    logger.info(f"ANSWER 1: Number of distinct rows in patient_enrollment_span.csv:'  {len(enrollment_spans.drop_duplicates())}")

    # Load outpatient visits
    visit_path = import_outpatient_visits(input_dir)
    visits_df = pd.read_excel(visit_path)
    logger.info(f"Loaded outpatient visit file: {visit_path}")

    # Append visit counts
    enrollment_spans = attach_outpatient_visit_counts(enrollment_spans, visits_df)
    logger.info("Step 5: Added outpatient visit metrics.")

    # Save to results.csv
    output_path = os.path.join(output_dir, "results.csv")
    enrollment_spans.to_csv(output_path, index=False)
    logger.info(f"Final output saved to: {output_path}")
    logger.info(f"Number of rows results.csv:'  {len(enrollment_spans)}")
    logger.info(f"Number of distinct rows in results.csv:'  {len(enrollment_spans.drop_duplicates())}")

    # Load the result file (if not already loaded)
    df_result = pd.read_csv("output/results.csv")

    # Count distinct values in ct_days_with_outpatient_visit
    distinct_day_counts = df_result['ct_days_with_outpatient_visit'].nunique()

    print(f"ANSWER 2: Number of distinct values in ct_days_with_outpatient_visit: {distinct_day_counts}")
