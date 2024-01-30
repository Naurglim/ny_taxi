from re import sub
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def snake_case(s):
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
        sub('([A-Z]+)', r' \1',
        s.replace('-', ' '))).split()).lower()

@transformer
def transform(data, *args, **kwargs):

    # Convert datetime columns to date:
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    data['lpep_dropoff_date'] = data['lpep_dropoff_datetime'].dt.date
    
    # Normalize field names:
    data.columns = [snake_case(x) for x in data.columns]

    return data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0) ]


@test
def test_vendor_id(output, *args) -> None:
    #assert ~output['vendor_id'].isin([1,2]).sum() == 0, 'There are invalid Vendor IDs'
    assert 'vendor_id' in output.columns, 'The vendor_id column is missing'

@test
def test_passenger_count(output, *args) -> None:

    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'

@test
def test_trip_distance(output, *args) -> None:

    assert output['trip_distance'].isin([0]).sum() == 0, 'There are trips with zero distance'
