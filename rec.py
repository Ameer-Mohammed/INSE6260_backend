#----------------------------------------api_logic------------------------------------------#

# from flask import Flask, jsonify
# import pandas as pd
#
# app = Flask(__name__)
#
# # Load the places and ratings CSV files into dataframes
# places_df = pd.read_csv('places.csv')
# ratings_df = pd.read_csv('ratings.csv')
#
# # Merge the places and ratings dataframes on the 'placeID' column
# merged_df = pd.merge(places_df, ratings_df, on='placeID')
#
# # Pivot the merged dataframe to create a user-item matrix with the 'userID' as rows and 'Rcuisine' as columns
# pivot_df = pd.pivot_table(merged_df, values='rating', index='userID', columns='Rcuisine')
#
# Define a function to get the top n recommended cuisines for a given user ID
def get_top_recommendations(userID, n):
    # if n in pivot_df.index:
    #     pass
    # else:
    #     return  {'cuisine': 'Index Error', 'rating': 'No user found with provided ID, please check and make sure user exists'}
    if userID not in pivot_df.index:
        return {'error': f'User with ID {userID} does not exist.'}
    # Get the row of the pivot dataframe corresponding to the specified user ID
    user_row = pivot_df.loc[userID]
    # Sort the row in descending order of rating and get the top n cuisine names
    top_cuisines = user_row.sort_values(ascending=False)[:n]
    # Get the ratings for the top recommended cuisines
    top_ratings = merged_df[merged_df['Rcuisine'].isin(top_cuisines.index)][['placeID', 'rating']]
    # Group the ratings by place ID and take the mean
    mean_ratings = top_ratings.groupby('placeID').mean()
    # Get the top n recommended places
    top_places = mean_ratings.sort_values('rating', ascending=False)[:n].reset_index()
    # Merge the top places with the places dataframe to get the place names
    top_places_with_names = pd.merge(top_places, places_df, on='placeID')
    # Create a dictionary to store the top recommendations with their ratings
    top_recommendations = []
    for _, row in top_places_with_names.iterrows():
        recommendation = {
            'cuisine': row['Rcuisine'],
            'placeID': row['placeID'],
            'rating': row['rating']
        }
        top_recommendations.append(recommendation)
    return top_recommendations
#
# @app.route('/api/<int:userID>/<int:n>', methods=['GET'])
# def api(userID, n):
#     # Get the top recommended cuisines for the specified user ID and number of recommendations
#     top_recommendations = get_top_recommendations(userID, n)
#
#     # Create a dictionary to store the JSON response data
#     response_data = {
#         'userID': userID,
#         'num_recommendations': n,
#         'top_recommendations': top_recommendations
#     }
#
#     # Return the JSON response
#     return jsonify(response_data)
#
# if __name__ == '__main__':
#     app.run(debug=True)
#--------------------------------------------------------------------------------------------#






# import pandas as pd
# import numpy as np
# from scipy.spatial.distance import cosine
#
# # Load the places and ratings CSV files into dataframes
# places_df = pd.read_csv('places.csv')
# ratings_df = pd.read_csv('ratings.csv')
#
# # Merge the places and ratings dataframes on the 'placeID' column
# merged_df = pd.merge(places_df, ratings_df, on='placeID')
#
# # Pivot the merged dataframe to create a user-item matrix with the 'userID' as rows and 'Rcuisine' as columns
# pivot_df = pd.pivot_table(merged_df, values='rating', index='userID', columns='Rcuisine')
#
# # Define a function to get the top n recommended cuisines for a given user ID
# def get_top_recommendations(userID, n):
#     if userID not in pivot_df.index:
#         return {'error': f'User with ID {userID} does not exist.'}
#
#     # Get the row of the pivot dataframe corresponding to the specified user ID
#     user_row = pivot_df.loc[userID]
#
#     # Calculate the cosine similarity between the user row and all other rows in the pivot dataframe
#     similarities = pivot_df.apply(lambda row: 1 - cosine(row, user_row), axis=1)
#
#     # Sort the similarities in descending order and get the top n indices
#     top_indices = similarities.sort_values(ascending=False)[:n].index.tolist()
#
#     # Get the ratings for the top recommended cuisines
#     top_ratings = merged_df[merged_df['userID'].isin(top_indices)][['Rcuisine', 'rating']]
#
#     # Group the ratings by cuisine and take the mean
#     mean_ratings = top_ratings.groupby('Rcuisine').mean()
#
#     # Get the top n recommended cuisines
#     top_cuisines = mean_ratings.sort_values('rating', ascending=False)[:n].reset_index()
#
#     # Create a dictionary to store the top recommendations with their ratings
#     top_recommendations = []
#     for _, row in top_cuisines.iterrows():
#         recommendation = {
#             'cuisine': row['Rcuisine'],
#             'rating': row['rating']
#         }
#         top_recommendations.append(recommendation)
#
#     return top_recommendations
#
# user = 1054
# n_recommendations = 5
# recommendations = get_top_recommendations(user, n_recommendations)
# print(f"Top {n_recommendations} recommended cuisine are: {recommendations}")


from flask import Flask, jsonify
import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
from flask_cors import CORS, cross_origin
import csv

app = Flask(__name__)

# Load the places and ratings CSV files into dataframes
places_df = pd.read_csv('places.csv')
ratings_df = pd.read_csv('ratings.csv')

# Merge the places and ratings dataframes on the 'placeID' column
merged_df = pd.merge(places_df, ratings_df, on='placeID')

# Pivot the merged dataframe to create a user-item matrix with the 'userID' as rows and 'Rcuisine' as columns
pivot_df = pd.pivot_table(merged_df, values='rating', index='userID', columns='Rcuisine')

# Group by cuisine and placeID, and calculate the mean rating for each group
grouped_df = merged_df.groupby(['Rcuisine', 'placeID'])['rating'].mean().reset_index()

# Sort the grouped dataframe in descending order of rating, and get the top 5 rows
top_5_df = grouped_df.sort_values(by='rating', ascending=False).head(5)

# # Define a function to get the top n recommended cuisines for a given user ID
# def get_top_recommendations(userID, n):
#     if userID not in pivot_df.index:
#         return {'error': f'User with ID {userID} does not exist.'}
#     # Get the row of the pivot dataframe corresponding to the specified user ID
#     user_row = pivot_df.loc[userID]
#     # Compute the cosine similarity between the user's row and all other rows
#     similarities = pivot_df.apply(lambda row: 1 - cosine(row, user_row), axis=1)
#     # Sort the similarities in descending order
#     similarities_sorted = similarities.sort_values(ascending=False)
#     # Get the top n most similar rows
#     top_similarities = similarities_sorted.iloc[1:n+1]
#     # Get the indices of the top similar rows
#     top_indices = top_similarities.index
#     # Get the top cuisines for the top similar rows
#     top_cuisines = pivot_df.loc[top_indices].mean().sort_values(ascending=False)[:n]
#     # Create a dictionary to store the top recommendations with their ratings
#     top_recommendations = []
#     for cuisine, rating in top_cuisines.iteritems():
#         recommendation = {
#             'cuisine': cuisine,
#             'rating': rating
#         }
#         top_recommendations.append(recommendation)
#     return top_recommendations

# Define a function to get the top n most rated cuisines
def get_top_rcuisines(n):
    # Get the number of ratings for each cuisine
    rcuisine_counts = merged_df['Rcuisine'].value_counts()
    # Get the top n most rated cuisines
    top_rcuisines = rcuisine_counts[:n].index.tolist()
    return top_rcuisines

@app.route('/api/<int:userID>/<int:n>', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def api(userID, n):
    # Get the top recommended cuisines for the specified user ID and number of recommendations
    top_recommendations = get_top_recommendations(userID, n)

    # Create a dictionary to store the JSON response data
    response_data = {
        'userID': userID,
        'num_recommendations': n,
        'top_recommendations': top_recommendations
    }

    # Return the JSON response
    return jsonify(response_data)

# Define a route to get the top n most rated cuisines for a new user
@app.route('/rcuisine/<int:n>', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def rcuisine(n):
    # Call the get_top_rcuisines function to get the top n most rated cuisines
    top_rcuisines = get_top_rcuisines(n)

    result = []
    for cusine in top_rcuisines:
        user_data = {}
        user_data['cuisine'] = cusine
       
        result.append(user_data)
   

    # Return the top n most rated cuisines in JSON format
    return jsonify({'top_rcuisines': result})


@app.route('/rating-history/<int:userID>', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_rating_history(userID):
    rating_history = []
    # Read the ratings CSV file
    with open('ratings.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row['userID']) == userID:
                placeID = int(row['placeID'])
                # Read the places CSV file to get the Rcuisine value
                with open('places.csv', 'r') as placesfile:
                    places_reader = csv.DictReader(placesfile)
                    for places_row in places_reader:
                        if int(places_row['placeID']) == placeID:
                            rating = {
                                'placeID': placeID,
                                'cuisine': places_row['Rcuisine'],
                                'rating': int(row['rating']),
                                'food_rating': int(row['food_rating']),
                                'service_rating': int(row['service_rating'])
                            }
                            rating_history.append(rating)
                            break
    return jsonify(rating_history)

# Define a function to convert the top 5 dataframe to a dictionary
def dataframe_to_dict(dataframe):
    result_dict = []
    for _, row in dataframe.iterrows():
        item_dict = {'cuisine': row['Rcuisine'], 'placeID': row['placeID'], 'rating': round(row['rating'], 2)}
        result_dict.append(item_dict)
    return result_dict

# Define a route to return the top 5 rated Rcuisine and placeID
@app.route('/top_cuisines_and_places', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_top_cuisines_and_places():
    # Get the top 5 rows of the grouped dataframe
    top_5_df = grouped_df.sort_values(by='rating', ascending=False).head(25)
    # Convert the dataframe to a dictionary
    result_dict = dataframe_to_dict(top_5_df)
    # Return the result as JSON
    return jsonify(result_dict)

if __name__ == '__main__':
    app.run(debug=True)
