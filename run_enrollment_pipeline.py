import sys
import os
from pipeline.process_enrollment import process_enrollment

if __name__ == "__main__":

    # Add 'pipeline' folder to import modules    
    sys.path.append(os.path.dirname(os.path.abspath('pipeline')))

    # Define input and output directories for data files
    import_dir = "data"
    export_dir = "output"

    # Ask user whether to enable QA (test) mode and generate output files at each step
    qa_input = input("Enable step-by-step validation with Excel outputs? (y/n): ")
    test_mode = qa_input in ['y', 'yes']

    # Run the pipeline
    process_enrollment(
        input_dir=import_dir,
        output_dir=export_dir,
        test_mode=test_mode
    )
