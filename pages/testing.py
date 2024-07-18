import pandas as pd

# Sample data
dogs = pd.DataFrame({
    'DogID': [1, 2],
    'Name': ['Buddy', 'Max'],
    'DateOfBirth': ['2020-01-01', '2021-05-05'],
    'Age': [3, 2],
    'Breed': ['Labrador', 'Beagle'],
    'Weight': [30, 20],
    'Size': ['Large', 'Medium'],
    'Gender': ['Male', 'Male'],
    'RescueDate': ['2021-01-01', '2022-01-01'],
    'Rabies_Done': [True, False],
    'Hexagonal_1': [True, True],
    'Hexagonal_2': [True, False],
    'Hexagonal_3': [False, False],
    'Hexagonal_Done': [True, False],
    'Spayed': [True, False],
    'De-worm': [True, True],
    'Children_Friendly': [True, False],
    'AnimalFriendly': [True, True],
    'HealthStatus': ['Good', 'Needs attention'],
    'EnergyLevel': ['High', 'Medium'],
    'PhotographStatus': ['Yes', 'No'],
    'AdoptionStatus': ['Available', 'Pending'],
    'AdopterID': [None, None],
    'PottyTrained': [True, True],
    'AdoptionName': ['Buddy', 'Max']
})

adopters = pd.DataFrame({
    'dog_chipID': [1, 2],
    'AdopterID': [101, 102],
    'AdopterName': ['Alice', 'Bob'],
    'Second_adopterID': [201, 202],
    'Second_adopterName': ['Charlie', 'Dave'],
    'Floor': [1, 2],
    'Apartment': [101, 202],
    'Address_street_number': [1, 2],
    'Address_street': ['Main St', 'Second St'],
    'Address_city': ['CityA', 'CityB'],
    'adopter_phone_num': ['1234567890', '0987654321'],
    'Second_adopter_phone_num': ['1111111111', '2222222222'],
    'Adopter_mail': ['alice@example.com', 'bob@example.com'],
    'Second_adopter_mail': ['charlie@example.com', 'dave@example.com'],
    'preferences': ['Large dog, Active', 'Small dog, Calm'],
    'LifeStyleInformation': ['Active', 'Calm'],
    'AdoptionDate': ['2023-01-01', '2023-02-01'],
    'Documents': ['Yes', 'No'],
    'ownership_form': ['Yes', 'No'],
    'ownership_transfer': ['Yes', 'No'],
    'Payment_type': ['Credit', 'Cash'],
    'Recieipt_Num': ['12345', '54321'],
    'Security_payment': [100, 200]
})

# Define a function to score adopters
def score_adopter(dog, adopter):
    score = 0
    
    # Criteria 1: Dog's size vs. Adopter's living space (simplified example)
    if dog['Size'] == 'Large' and adopter['preferences'].find('Large dog') != -1:
        score += 10
    if dog['Size'] == 'Medium' and adopter['preferences'].find('Medium dog') != -1:
        score += 10
    if dog['Size'] == 'Small' and adopter['preferences'].find('Small dog') != -1:
        score += 10
    
    # Criteria 2: Dog's energy level vs. Adopter's lifestyle
    if dog['EnergyLevel'] == adopter['LifeStyleInformation']:
        score += 20

    # Criteria 3: Children_Friendly
    if adopter['preferences'].find('Children') != -1 and dog['Children_Friendly']:
        score += 15

    # Criteria 4: AnimalFriendly
    if adopter['preferences'].find('Animal') != -1 and dog['AnimalFriendly']:
        score += 15

    # Criteria 5: HealthStatus
    if dog['HealthStatus'] == 'Good':
        score += 10
    elif dog['HealthStatus'] == 'Needs attention' and adopter['preferences'].find('Special needs') != -1:
        score += 10
    
    # Criteria 6: Spayed/Neutered
    if dog['Spayed'] and adopter['preferences'].find('Spayed') != -1:
        score += 5

    return score

# Calculate scores for each adopter for each dog
scores = []
for i, dog in dogs.iterrows():
    for j, adopter in adopters.iterrows():
        score = score_adopter(dog, adopter)
        scores.append({'DogID': dog['DogID'], 'AdopterID': adopter['AdopterID'], 'Score': score})

# Create a DataFrame with the scores
scores_df = pd.DataFrame(scores)

print(scores_df)
