import logging
import os
import pandas as pd


def check_span_gaps(df, output_dir=None, logger=None, raise_on_violation=True):
    """Validates that each patient’s enrollment spans are separated by at least 1 full month.

    Raises an exception and logs/export violations if test_mode is enabled.
    """
    df = df.copy()

    # Ensure dates are datetime
    df['enrollment_start_date'] = pd.to_datetime(df['enrollment_start_date'])
    df['enrollment_end_date'] = pd.to_datetime(df['enrollment_end_date'])

    # Sort by patient and start date
    df = df.sort_values(by=['patient_id', 'enrollment_start_date'])

    # Get the previous span’s end date for each patient
    df['prev_end'] = df.groupby('patient_id')['enrollment_end_date'].shift()

    # Compute calendar-month difference
    period_diff = (
        df['enrollment_start_date'].dt.to_period('M') - 
        df['prev_end'].dt.to_period('M')
    )

    df['gap_months'] = period_diff.apply(lambda x: x.n if pd.notnull(x) else None)

    # Find violations
    violations = df[df['gap_months'] < 1]

    if not violations.empty:
        if logger:
            logger.error("Span gap rule violated for some patients.")
        else:
            print("Span gap rule violated for some patients.")

        if output_dir:
            violation_path = os.path.join(output_dir, "span_violations.xlsx")
            violations.to_excel(violation_path, index=False)
            if logger:
                logger.info(f"Violations exported to: {violation_path}")
            else:
                print(f"Violations exported to: {violation_path}")

        if raise_on_violation:
            raise ValueError("Span continuity rule violated — spans not separated by at least 1 full month.")

    else:
        if logger:
            logger.info("QA passed: All enrollment spans are separated by at least 1 full month.")
        else:
            print("QA passed: All enrollment spans are separated by at least 1 full month.")

    return violations