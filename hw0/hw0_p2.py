import re
# Read the CSV file and store the data
def read_csv(file_path):
    print("Reading data from file:", file_path)
    data = []
    with open(file_path, 'r') as file:
        headers = file.readline().strip().split(',')
        for line in file:
            data.append(dict(zip(headers, line.strip().split(','))))
    return data

# Question 1: Top-3 movies with the highest ratings in 2016
def top_3_movies_highest_ratings_2016(data):
    movies_2016 = [movie for movie in data if movie['Year'] == '2016']
    top_3_movies = sorted(movies_2016, key=lambda x: float(x['Rating']), reverse=True)[:3]
    titles = [movie['Title'] for movie in top_3_movies]
    return titles

# Question 2: The actor generating the highest average revenue
def actor_highest_avg_revenue(data):
    actor_revenue = {}
    for movie in data:
        actors = re.split(r'\|\s*', movie['Actors'])
        revenue = float(movie['Revenue (Millions)']) if movie['Revenue (Millions)'] else 0
        for actor in actors:
            if actor not in actor_revenue:
                actor_revenue[actor] = []
            actor_revenue[actor].append(revenue)
    
    # Calculate average revenue for each actor
    actor_avg_revenue = {actor: sum(revenues) / len(revenues) for actor, revenues in actor_revenue.items()}
    
    # Find the highest average revenue
    highest_avg_revenue = max(actor_avg_revenue.values())
    
    # Find all actors with the highest average revenue
    highest_avg_revenue_actors = [actor for actor, avg_revenue in actor_avg_revenue.items() if avg_revenue == highest_avg_revenue]
    
    return highest_avg_revenue_actors

# Question 3: The average rating of Emma Watson’s movies
def avg_rating_emma_watson(data):
    emma_movies = [movie for movie in data if 'Emma Watson' in movie['Actors']]
    avg_rating = sum(float(movie['Rating']) for movie in emma_movies) / len(emma_movies)
    return avg_rating

# Question 4: Top-3 directors who collaborate with the most actors
def top_3_directors_most_actors(data):
    director_actors = {}
    for movie in data:
        director = movie['Director']
        actors = set(re.split(r'\|\s*', movie['Actors']))
        if director not in director_actors:
            director_actors[director] = set()
        director_actors[director].update(actors)
    top_3_directors = sorted(director_actors, key=lambda x: len(director_actors[x]), reverse=True)[:3]
    return top_3_directors

# Question 5: Top-2 actors playing in the most genres of movies
def top_2_actors_most_genres(data):
    actor_genres = {}
    for movie in data:
        actors = re.split(r'\|\s*', movie['Actors'])
        genres = movie['Genre'].split('| ')
        for actor in actors:
            if actor not in actor_genres:
                actor_genres[actor] = set()
            actor_genres[actor].update(genres)
    
    # Find the maximum number of genres
    max_genres_count = max(len(genres) for genres in actor_genres.values())
    
    # Find all actors with the maximum number of genres
    top_actors = [actor for actor, genres in actor_genres.items() if len(genres) == max_genres_count]
    
    # Otherwise, find the second maximum number of genres
    second_max_genres_count = max(len(genres) for genres in actor_genres.values() if len(genres) < max_genres_count)
    
    # Find all actors with the second maximum number of genres
    second_top_actors = [actor for actor, genres in actor_genres.items() if len(genres) == second_max_genres_count]
    
    # Combine the top actors and second top actors
    result = top_actors + second_top_actors
    
    return result

# Question 6: The largest maximum gap of years between movies of all actors
def top_3_actors_max_gap_years(data):
    
    # Step 1: Initialize data structures
    actor_years = {}
    
    # Step 2: Build the actor years dictionary
    for movie in data:
        year = int(movie['Year'])
        actors = re.split(r'\|\s*', movie['Actors'])
        for actor in actors:
            if actor not in actor_years:
                actor_years[actor] = []
            actor_years[actor].append(year)
    
    # Step 3: Calculate the maximum gap for each actor
    actor_max_gaps = {actor: max(years) - min(years) for actor, years in actor_years.items() if len(years) > 1}
    
    # Step 4: Find the largest gap
    if not actor_max_gaps:
        return []
    largest_gap = max(actor_max_gaps.values())
    
    # Step 5: Collect all actors with the largest gap
    actors_with_largest_gap = [actor for actor, gap in actor_max_gaps.items() if gap == largest_gap]
    return actors_with_largest_gap

# Question 7: Find all actors who collaborate with Johnny Depp in direct and indirect ways
def collaborators_johnny_depp(data):
    from collections import defaultdict, deque

    # Step 1: Initialize data structures
    actor_collaborations = defaultdict(set)
    
    # Step 2: Build the collaboration graph
    for movie in data:
        actors = re.split(r'\|\s*', movie['Actors'])
        for actor in actors:
            actor_collaborations[actor].update(actors)
            actor_collaborations[actor].remove(actor)

    # Step 3: Initialize BFS
    visited = set()
    queue = deque(['Johnny Depp'])
    collaborators = set()

    # Step 4: Perform BFS
    while queue:
        current_actor = queue.popleft()
        if current_actor not in visited:
            visited.add(current_actor)
            collaborators.update(actor_collaborations[current_actor])
            queue.extend(actor_collaborations[current_actor] - visited)

    # Step 5: Remove Johnny Depp from the result
    collaborators.discard('Johnny Depp')
    return collaborators

# read data and call the functions
# please put "IMDB-Movie-Data.csv" in the same directory as this file
file_path = 'IMDB-Movie-Data.csv'
data = read_csv(file_path)
print("Data loaded successfully.")

print("Top-3 movies with the highest ratings in 2016:", top_3_movies_highest_ratings_2016(data))
print("The actor generating the highest average revenue:", actor_highest_avg_revenue(data))
print("The average rating of Emma Watson\'s movies:", avg_rating_emma_watson(data))
print("Top-3 directors who collaborate with the most actors:", top_3_directors_most_actors(data))
print("Top-2 actors playing in the most genres of movies:", top_2_actors_most_genres(data))
print("all actors with the largest gap year:", top_3_actors_max_gap_years(data))
print("Actors collaborating with Johnny Depp:", collaborators_johnny_depp(data))
