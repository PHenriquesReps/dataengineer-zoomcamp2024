import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)] 
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    data.columns = (data.columns
                    .str.replace(r'([a-z])([A-Z])', r'\1_\2')
                    .str.replace(' ', '_')
                    .str.lower()
    )

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['vendor_id'] is not None, 'The vendor_id is not present'
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with 0 passengers'
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with 0 distance'