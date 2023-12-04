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
    columns_to_drop = ['ISO2', 'ADMIN1', 'ADMIN2', 'SITE_NAME', 'SITE_CODE', 'TEST_TYPE', 'TIME_HOLDING_POSTEXPOSURE', 'DATA_SOURCE', 'CITATION', 'CITATION_URL', 'DATA_CURATOR']

    #Drop the specified columns and create a new dataframe
    df = df[[col for col in df.columns if col not in columns_to_drop]]

    #Removing rows with null values in specific columns
    columns_with_nulls = ['INSECTICIDE_CONC', 'INSECTICIDE_INTENSITY', 'RESISTANCE_INTENSITY']
    df.dropna(subset=columns_with_nulls, inplace=True)

    # Check for 'µg' in 'INSECTICIDE_CONC', and convert those values to %
    
    contains_micrograms = df['INSECTICIDE_CONC'].str.contains('µg', na=False)
    df['INSECTICIDE_CONC'] = df['INSECTICIDE_CONC'].str.extract(r'(\d+\.*\d*)')
    df['INSECTICIDE_CONC'] = pd.to_numeric(df['INSECTICIDE_CONC'], errors='coerce') 

    # Calculate the mean of non-null values in 'INSECTICIDE_CONC' with 2 decimal places
    mean_insecticide_conc = df['INSECTICIDE_CONC'].mean()
    mean_insecticide_conc = round(mean_insecticide_conc, 2)

    # Replace null values in 'INSECTICIDE_CONC' with the mean
    df['INSECTICIDE_CONC'].fillna(mean_insecticide_conc, inplace=True)

    #Cleaning the Mosquito Number column
    # Replace non-numeric values with NaN
    df['MOSQUITO_NUMBER'] = pd.to_numeric(df['MOSQUITO_NUMBER'], errors='coerce')

    # Calculate the mean of 'MOSQUITO_NUMBER' (ignoring NaN values)
    mean_mosquito_number = round(df['MOSQUITO_NUMBER'].mean())

    # Replace NaN values in 'MOSQUITO_NUMBER' with the rounded mean
    df['MOSQUITO_NUMBER'].fillna(mean_mosquito_number, inplace=True)

    # Convert 'YEAR_START' to datetime
    df['YEAR_START'] = pd.to_datetime(df['YEAR_START'], format='%Y')
    df['YEAR_START'] = df['YEAR_START'].dt.year

    # Create a dictionary to map old column names to lowercase names
    column_mapping = {col: col.lower() for col in df.columns}

    # Rename the columns
    df.rename(columns=column_mapping, inplace=True)

    # Create a resistance_table with the selected columns
    resistance_table = df[['vector_species', 'country_name', 'latitude', 'longitude', 'insecticide_type', 'resistance_intensity']].copy()
    # Add a new column 'resistance_id' and set it as the index
    resistance_table['resistance_id'] = range(1, len(resistance_table) + 1)
    # Reorder the columns to have 'resistance_id' as the first column
    resistance_table = resistance_table[['resistance_id', 'vector_species', 'country_name', 'latitude', 'longitude', 'insecticide_type', 'resistance_intensity']]

    # Create insecticide_table with the selected columns
    insecticide_table = df[['insecticide_class', 'insecticide_type', 'insecticide_conc', 'insecticide_intensity']].copy()
    # Add a new column 'insecticide_id' and set it as the index
    insecticide_table['insecticide_id'] = range(1, len(insecticide_table) + 1)
    # Reorder the columns to have 'insecticide_id' as the first column
    insecticide_table = insecticide_table[['insecticide_id', 'insecticide_class', 'insecticide_type', 'insecticide_conc', 'insecticide_intensity']]

    # Create malaria_vectors_table with the selected columns
    malaria_vectors_table = df[['vector_species', 'country_name', 'latitude', 'longitude', 'mosquito_number', 'mortality_adjusted', 'resistance_intensity']].copy()
    # Add a new column 'vector_id' and set it as the index
    malaria_vectors_table['vector_id'] = range(1, len(malaria_vectors_table) + 1)
    # Reorder the columns to have 'vector_id' as the first column
    malaria_vectors_table = malaria_vectors_table[['vector_id', 'vector_species', 'country_name', 'latitude', 'longitude', 'mosquito_number', 'mortality_adjusted', 'resistance_intensity']]


    return {"resistance_table":resistance_table.to_dict(orient="dict"),
    "insecticide_table":insecticide_table.to_dict(orient="dict"),
    "malaria_vectors_table":malaria_vectors_table.to_dict(orient="dict") }


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
