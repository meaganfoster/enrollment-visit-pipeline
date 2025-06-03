import pandas as pd

def attach_outpatient_visit_counts(enrollment_df, visits_df):
    """Appends outpatient visit metrics to each enrollment span."""
    enrollment_df['enrollment_start_date'] = pd.to_datetime(enrollment_df['enrollment_start_date'])
    enrollment_df['enrollment_end_date'] = pd.to_datetime(enrollment_df['enrollment_end_date'])
    visits_df['date'] = pd.to_datetime(visits_df['date'])

    results = []

    for _, span in enrollment_df.iterrows():
        pid = span['patient_id']
        start = span['enrollment_start_date']
        end = span['enrollment_end_date']

        patient_visits = visits_df[
            (visits_df['patient_id'] == pid) &
            (visits_df['date'] >= start) &
            (visits_df['date'] <= end)
        ]

        ct_outpatient_visits = patient_visits['outpatient_visit_count'].sum()
        ct_days_with_visit = patient_visits['date'].nunique()

        span_result = span.to_dict()
        span_result['ct_outpatient_visits'] = ct_outpatient_visits
        span_result['ct_days_with_outpatient_visit'] = ct_days_with_visit
        results.append(span_result)

    return pd.DataFrame(results)
