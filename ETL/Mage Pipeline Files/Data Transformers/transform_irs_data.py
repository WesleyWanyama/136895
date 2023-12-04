import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    #Specify the columns that are to be dropped
    columns_to_drop = ['GHO (CODE)', 'GHO (DISPLAY)', 'GHO (URL)', 'PUBLISHSTATE (CODE)', 'PUBLISHSTATE (DISPLAY)', 'PUBLISHSTATE (URL)', 'YEAR (CODE)', 'YEAR (URL)', 'REGION (CODE)', 'REGION (URL)', 'COUNTRY (CODE)', 'COUNTRY (URL)', 'Display Value', 'Low', 'High', 'StdErr', 'StdDev', 'Comments']

    #Drop the specified columns and create a new dataframe
    df = df[[col for col in df.columns if col not in columns_to_drop]]

    # Removing rows with null values. Here the Numeric column has the null values
    df.dropna(subset=['Numeric'], inplace=True)

    # Create a dictionary to specify the mapping of old column names to new column names
    column_mapping = {
        'YEAR (DISPLAY)': 'Year',
        'REGION (DISPLAY)': 'Region',
        'COUNTRY (DISPLAY)': 'Country',
        'Numeric': 'People Protected',
    }

    # Use the rename() function to rename the columns
    df.rename(columns=column_mapping, inplace=True)

    # Convert 'Year' to datetime
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    df['Year'] = df['Year'].dt.year

    # Use astype to convert the "People Protected" column to an integer
    df['People Protected'] = df['People Protected'].astype(int)

    # Create a irs_coverage_cases table with the selected columns
    irs_coverage_table = df[['Year', 'Region', 'Country', 'People Protected']].copy()
    # Add a new column 'coverage_id' and set it as the index
    irs_coverage_table['coverage_id'] = range(1, len(irs_coverage_table) + 1)
    # Reorder the columns to have 'case_id' as the first column
    irs_coverage_table = irs_coverage_table[['coverage_id', 'Year', 'Region', 'Country', 'People Protected']]

    return {"irs_coverage_table":irs_coverage_table.to_dict(orient="dict")
     }


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
