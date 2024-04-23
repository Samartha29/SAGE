import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load the CSV data
df = pd.read_csv("coursera_courses.csv")

# Concatenate course information into a single text column for content-based filtering
# df['course_info'] = (df['course_title'] + ' ' + df['course_description']).fillna('')
df['course_info'] = (df['course_title']).fillna('')

# Replace difficulty values with numeric values
difficulty_mapping = {'Beginner': 0, 'Intermediate': 2, 'Mixed': 1, 'Advanced': 3}

# Replace values in 'course_difficulty' column
df['course_difficulty'] = df['course_difficulty'].replace(difficulty_mapping)

# For any other value not in the mapping, replace with 1
df['course_difficulty'] = df['course_difficulty'].fillna(1)

# TF-IDF Vectorization of course information
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['course_info'])

# Compute the cosine similarity matrix offline
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Function to get course recommendations based on student data
def get_recommendations(prompt, advanced, cosine_sim=cosine_sim):
    # TF-IDF Vectorization of student data
    student_tfidf_matrix = tfidf_vectorizer.transform([prompt])

    # Compute the cosine similarity between student data and all courses
    sim_scores = linear_kernel(student_tfidf_matrix, tfidf_matrix)

    #TODO: multiply sim_scores with the respective course_difficulty
    if advanced:
      weighted_scores = sim_scores * (df['course_difficulty'].values+1)
    else:
      weighted_scores = sim_scores * (4-df['course_difficulty'].values)

    # Get the indices of courses with highest similarity scores
    course_indices = weighted_scores.argsort()[:, ::-1]

    # Assuming you have a list of course indices named course_indices
    recommended_courses_indices = course_indices[0]

    # Retrieve 'course_title' and 'course_difficulty' for recommended courses
    recommended_courses_info = df.loc[recommended_courses_indices, ['course_title', 'course_difficulty', 'course_url', 'course_description']]

    # Balance the recommendations (e.g., if advanced=True, return an equal number of advanced and beginner courses)
    num_courses_to_return = min(5, len(recommended_courses_info))
    balanced_recommendations = recommended_courses_info.head(num_courses_to_return)

    # Convert the DataFrame rows to a list of lists
    recommended_courses_combined = balanced_recommendations.values.tolist()

    # Now you have a list containing both 'course_title' and 'course_difficulty' for each recommended course
    return recommended_courses_combined

recommendations = get_recommendations('machine learning', False)
print("Recommended Courses:")
print(recommendations)