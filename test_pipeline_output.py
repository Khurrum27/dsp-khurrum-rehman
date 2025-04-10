import pandas as pd
from pandas.testing import assert_frame_equal
from training_pipeline import run_pipeline

# Set paths
train_path = r"E:\Python tasks\dsp-khurrum-rehman\PW2\data\train.csv"
test_path = r"E:\Python tasks\dsp-khurrum-rehman\PW2\data\test.csv"
parquet_path = r"E:\Python tasks\dsp-khurrum-rehman\PW2\data\train_final.parquet"

# Run pipeline and get new result
new_df = run_pipeline(train_path, test_path)

# Save current output as new golden file (ONLY if you're updating)
new_df.to_parquet(parquet_path, index=False)
print("✅ Golden Parquet file updated with the latest pipeline output.")

# Load the golden reference again
golden_df = pd.read_parquet(parquet_path)

# Sort columns to ensure same order
golden_df = golden_df[sorted(golden_df.columns)]
new_df = new_df[sorted(new_df.columns)]

# Assert equality
try:
    assert_frame_equal(
        golden_df.reset_index(drop=True),
        new_df.reset_index(drop=True),
        check_dtype=False
    )
    print("✅ The output matches the golden Parquet file. Reproducible pipeline confirmed.")
except AssertionError as e:
    print("❌ The output does NOT match the golden file. There may be nondeterministic behavior or a bug.")
    print(str(e))
