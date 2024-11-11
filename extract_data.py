import pandas as pd
import ast

def parse_json_string(cell_value):
    try:
        return ast.literal_eval(cell_value)
    except (ValueError, SyntaxError):
        return None

def clean_data(df):
    df['new_car_detail'] = df['new_car_detail'].apply(parse_json_string)
    df['new_car_overview'] = df['new_car_overview'].apply(parse_json_string)
    df['new_car_feature'] = df['new_car_feature'].apply(parse_json_string)
    df['new_car_specs'] = df['new_car_specs'].apply(parse_json_string)
    
    df['ignition_type'] = df['new_car_detail'].apply(lambda x: x.get('it') if x else None)
    df['fuel_type'] = df['new_car_detail'].apply(lambda x: x.get('ft') if x else None)
    df['body_type'] = df['new_car_detail'].apply(lambda x: x.get('bt') if x else None)
    df['kilometers_driven'] = df['new_car_detail'].apply(lambda x: x.get('km') if x else None)
    df['transmission'] = df['new_car_detail'].apply(lambda x: x.get('transmission') if x else None)
    df['number_of_owners'] = df['new_car_detail'].apply(lambda x: x.get('ownerNo') if x else None)
    df['owner_details'] = df['new_car_detail'].apply(lambda x: x.get('owner') if x else None)
    df['oem'] = df['new_car_detail'].apply(lambda x: x.get('oem') if x else None)
    df['model'] = df['new_car_detail'].apply(lambda x: x.get('model') if x else None)
    df['model_year'] = df['new_car_detail'].apply(lambda x: x.get('modelYear') if x else None)
    df['central_variant_id'] = df['new_car_detail'].apply(lambda x: x.get('centralVariantId') if x else None)
    df['variant_name'] = df['new_car_detail'].apply(lambda x: x.get('variantName') if x else None)
    df['price'] = df['new_car_detail'].apply(lambda x: x.get('price') if x else None)
    
    overview_keys = [
        'Registration Year', 'Insurance Validity', 'Fuel Type', 'Seats',
        'Kms Driven', 'RTO', 'Ownership', 'Engine Displacement',
        'Transmission', 'Year of Manufacture'
    ]
    

    def extract_overview_details(top_list, key_name):
        if isinstance(top_list, list):
            for item in top_list:
                if item.get('key') == key_name:
                    return item.get('value')
        return None
    
    def extract_feature_data(feature_data, section_name):
        if isinstance(feature_data, list):
            for section in feature_data:
                if section.get('heading') == section_name:
                    return ', '.join([item['value'] for item in section.get('list', [])])
        return None
    
    def extract_spec_data(spec_data, key_name):
        if isinstance(spec_data, list):
            for spec in spec_data:
                if spec.get('key') == key_name:
                    return spec.get('value')
        return None
    
    for key in overview_keys:
        column_name = key.replace(' ', '_').lower()
        df[column_name] = df['new_car_overview'].apply(
            lambda x: extract_overview_details(x.get('top') if x else None, key)
        )
    
    df['comfort_features'] = df['new_car_feature'].apply(lambda x: extract_feature_data(x.get('data') if x else None, 'Comfort & Convenience'))
    df['interior_features'] = df['new_car_feature'].apply(lambda x: extract_feature_data(x.get('data') if x else None, 'Interior'))
    df['exterior_features'] = df['new_car_feature'].apply(lambda x: extract_feature_data(x.get('data') if x else None, 'Exterior'))
    df['safety_features'] = df['new_car_feature'].apply(lambda x: extract_feature_data(x.get('data') if x else None, 'Safety'))
    df['entertainment_features'] = df['new_car_feature'].apply(lambda x: extract_feature_data(x.get('data') if x else None, 'Entertainment & Communication'))
    
    
    spec_keys = ['Engine', 'Max Power', 'Torque', 'Wheel Size', 'Seats']
    for key in spec_keys:
        column_name = key.replace(' ', '_').lower()
        df[column_name] = df['new_car_specs'].apply(lambda x: extract_spec_data(x.get('top') if x else None, key))
    
    df_cleaned = df.drop(columns=['new_car_detail', 'new_car_overview', 'new_car_feature', 'new_car_specs','car_links'])
    
    return df_cleaned

if __name__ == "__main__":
    dataset_list =['bangalore','chennai',
                   'delhi','hyderabad',
                   'jaipur','kolkata'
                   ]
    master_data = pd.DataFrame()

    for city in dataset_list:
        data = pd.read_excel(f'Dataset/master/{city}_cars.xlsx')
        df_cleaned = clean_data(data)
        df_cleaned['city'] = city
        master_data = pd.concat([master_data, df_cleaned])

    master_data.to_excel('Dataset/process/extracted_data.xlsx', index=False)
