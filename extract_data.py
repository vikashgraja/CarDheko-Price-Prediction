import pandas as pd
import ast

def extract_new_car_overview(details):
    if isinstance(details, list):
        return {df['key']: df['value'] for df in details}
    else:
        return {}

def extract_new_car_feature(details):
    if isinstance(details, list):
        return {i: df['value'] for i, df in enumerate(details)}
    else:
        return {}


def extract_new_car_specs(details):
    if isinstance(details, list):
        return {df['key']: df['value'] for df in details}
    else:
        return {}


def convert_binary_cols(df):
    unique_features = pd.Series(df.values.ravel('K')).dropna().unique()
    binary_df = pd.DataFrame(0, index=df.index, columns=unique_features)

    for idx, row in df.iterrows():
        for item in row.dropna():
            binary_df.at[idx, item] = 1
    return binary_df


def extract_data(data):
    data.drop(columns=["car_links"], inplace=True, axis=1)
    data["new_car_detail_dict"] = data["new_car_detail"].apply(ast.literal_eval)

    new_car_detail = pd.json_normalize(data["new_car_detail_dict"])

    data["new_car_overview_dict"] = data["new_car_overview"].apply(ast.literal_eval)
    new_car_overview = pd.json_normalize(data["new_car_overview_dict"])
    new_car_overview.drop(columns=["bottomData"], inplace=True, axis=1)
    new_car_overview = new_car_overview['top'].apply(extract_new_car_overview)
    new_car_overview = pd.json_normalize(new_car_overview)

    data["new_car_feature_dict"] = data["new_car_feature"].apply(ast.literal_eval)

    new_car_feature = pd.json_normalize(data["new_car_feature_dict"])

    new_car_feature.drop(columns=["commonIcon"], inplace=True, axis=1)

    new_car_feature_top = new_car_feature["top"].apply(extract_new_car_feature)
    new_car_feature_top = pd.json_normalize(new_car_feature_top)

    new_car_feature_top = convert_binary_cols(new_car_feature_top)

    new_car_feature_all_data = pd.json_normalize(new_car_feature["data"])
    new_car_feature_extracted = pd.DataFrame()
    for col in new_car_feature_all_data.columns:
        new_car_feature_data = pd.json_normalize(new_car_feature_all_data[col])
        new_car_feature_list = new_car_feature_data["list"].apply(extract_new_car_feature)
        new_car_feature_list = pd.json_normalize(new_car_feature_list)
        new_car_feature_list = convert_binary_cols(new_car_feature_list)
        new_car_feature_extracted = pd.concat([new_car_feature_extracted, new_car_feature_list], axis=1)

    data["new_car_specs_dict"] = data["new_car_specs"].apply(ast.literal_eval)

    new_car_specs = pd.json_normalize(data["new_car_specs_dict"])
    new_car_specs.drop(columns=["commonIcon"], inplace=True, axis=1)

    new_car_specs_top = new_car_specs["top"].apply(extract_new_car_specs)
    new_car_specs_top = pd.json_normalize(new_car_specs_top)
    new_car_specs_data = pd.json_normalize(new_car_specs["data"])
    new_car_specs_data_extracted = pd.DataFrame()
    for col in new_car_specs_data.columns:
        new_car_specs_data_1 = pd.json_normalize(new_car_specs_data[col])
        new_car_specs_list = new_car_specs_data_1["list"].apply(extract_new_car_specs)
        new_car_specs_list = pd.json_normalize(new_car_specs_list)
        new_car_specs_data_extracted = pd.concat([new_car_specs_data_extracted, new_car_specs_list], axis=1)

    extracted_df = pd.concat([new_car_detail, new_car_overview, new_car_specs_top, new_car_specs_data_extracted],
                             axis=1)
    return extracted_df


def rename_duplicate_columns(df):
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        count = 0
        for i in range(len(cols)):
            if cols[i] == dup:
                count += 1
                if count > 1:
                    cols[i] = f"{dup}_{count - 1}"
    df.columns = cols
    return df


def combined_city(city_data):
    all_cities_car_data = [rename_duplicate_columns(df) for df in city_data]

    all_columns = set()
    for df in all_cities_car_data:
        all_columns.update(df.columns)

    for df in all_cities_car_data:
        missing_cols = all_columns - set(df.columns)
        for col in missing_cols:
            df[col] = pd.NA

    all_cities_car_data = [df.reset_index(drop=True) for df in all_cities_car_data]

    combined_df = pd.concat(all_cities_car_data, axis=0, join='outer', ignore_index=True)
    return combined_df

if __name__ == "__main__":
    dataset_list = ['bangalore', 'chennai',
                    'delhi', 'hyderabad',
                    'jaipur', 'kolkata'
                    ]
    city_data = []

    for city in dataset_list:
        data = pd.read_excel(f'Dataset/master/{city}_cars.xlsx')
        df_cleaned = extract_data(data)
        df_cleaned['city'] = city
        city_data += [df_cleaned]

    combined_df = combined_city(city_data)

    combined_df.drop(
        columns=["owner", "centralVariantId", "priceActual", "priceSaving", "priceFixedText", "trendingText.imgUrl",
                 "trendingText.heading", "trendingText.desc", "Registration Year", "RTO", "Ownership",
                 "Engine Displacement", "Seats", "Wheel Size", "Engine Type", "Displacement", "Max Power_1",
                 "Max Torque", "No of Cylinder", "Values per Cylinder", "Values per Cylinder", "Fuel Suppy System",
                 "BoreX Stroke", "Compression Ratio", "Turbo Charger", "Super Charger", "Seating Capacity",
                 "Tyre Type", "Alloy Wheel Size", "Height", "Width", "Wheel Base", "Alloy Wheel Size_1",
                 "Front Tread", "Rear Tread", "Kerb Weight", "Gross Weight", "Ground Clearance Unladen",
                 "Seating Capacity_1", "Seating Capacity_1", "Tyre Type_1", "No Door Numbers_1",
                 "Seating Capacity_2", "Steering Type_2", "Turning Radius", "Front Brake Type", "Rear Brake Type",
                 "Top Speed", "Acceleration", "Tyre Type_2", "No Door Numbers_2", "Alloy Wheel Size_2",
                 "Acceleration_1", "Top Speed_1",
                 "Rear Brake Type_1", "Front Brake Type_1", "Gear Box_1", "Turning Radius_1", "variantName",
                 "Value Configuration", "Steering Type",
                 "No Door Numbers", "Length", "Cargo Volumn", "Drive Type_1", "Torque", "Steering Type_1",
                 "Year of Manufacture", "Max Power", "Transmission",
                 "Fuel Type", "km"], inplace=True, axis=1)

    combined_df.to_excel('Dataset/process/extracted_data.xlsx', index=False)
