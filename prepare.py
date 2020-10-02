# importing
import pandas as pd
from sklearn.model_selection import train_test_split

# creating function to prep data for analysis
def prepare_telco(telco_raw):
    # dropping duplicate rows
    telco_raw.drop_duplicates(inplace=True)

    # creating new column that tells whether the customer makes automatic or manual payments
    # 0 = manual | 1 = automatic
    payment_type_cols = [1, 2, 3, 4]
    telco_raw['is_automatic_payment'] = telco_raw.payment_type_id.replace(payment_type_cols, [0,0,1,1])
    
    # converting no phone service to No to reduce column to binary values
    # phone service column will still tell us if they dont have phone service
    telco_raw["multiple_lines"] = telco_raw["multiple_lines"].replace("No phone service", "No")

    # converting no internet service to No to reduce column to binary values
    # internet service column will still tell us if they dont have internet service
    cols_w_no_internet = ["online_security", "online_backup", "device_protection", "tech_support", "streaming_tv", "streaming_movies"]
    telco_raw[cols_w_no_internet] = telco_raw[cols_w_no_internet].replace("No internet service", "No")

    # converting columns with binary values to 0s and 1s
    # 1 = true, they have the column subject | 0 = false, they do not have the column subject
    binary_value_cols = ["multiple_lines", "online_security", "online_backup", "device_protection", "tech_support", "streaming_tv", "streaming_movies","partner","dependents","phone_service", "paperless_billing","churn"]
    telco_raw[binary_value_cols] = telco_raw[binary_value_cols].replace("Yes", 1)
    telco_raw[binary_value_cols] = telco_raw[binary_value_cols].replace("No", 0)
    
    # renaming gender to female
    telco_raw.rename(columns={'gender':'female'}, inplace=True)
    # replacing genders with 1s and 0s
    # 1 = Female | 0 = Male
    telco_raw["female"] = telco_raw["female"].replace("Female", 1)
    telco_raw["female"] = telco_raw["female"].replace("Male", 0)
    
    # no missing values but there are values with only whitespace in total_charges
    # these are white spaces because their tenure is 0 so they havent been with us a full month, thus they havent been billed so they
    # have $0 in total charges.
    # replacing blank space with value of 0
    telco_raw['total_charges'] = telco_raw.total_charges.where((telco_raw.tenure != 0),0)
    # converting data type to float since we couldnt when there were white space values
    telco_raw['total_charges'] = telco_raw.total_charges.astype(float)
    
    # creating tenure_years column that shows how many years client has been with us
    telco_raw['tenure_years'] = round(telco_raw.tenure / 12, 1)

   # reordering columns so that churn appears last
   # this makes it easier to locate when plotting features
    telco_raw = telco_raw[['customer_id', 'female', 'senior_citizen', 'partner', 'dependents',
       'tenure', 'phone_service', 'multiple_lines',
       'internet_service_type_id', 'online_security', 'online_backup',
       'device_protection', 'tech_support', 'streaming_tv', 'streaming_movies',
       'contract_type_id', 'paperless_billing', 'payment_type_id','is_automatic_payment',
       'monthly_charges', 'total_charges',
       'tenure_years','churn']]
    
    # splitting data into train, test and validate telco_raws
    train_validate, test = train_test_split(telco_raw, test_size = .20, random_state = 123)
    train, validate = train_test_split(train_validate, test_size = .30, random_state = 123)
    
    # returning telco_raws
    return train, validate, test
