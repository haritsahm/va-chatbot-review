import deeplake

# Fastest option - copies everything including version history
ds = deeplake.deepcopy(
    src='hub://haritsahm/spotify_reviews_cleaned_filtered_balanced_50K_docs_1000_chunk',
    dest='deeplake/spotify_reviews_cleaned_filtered_balanced_50K_docs_1000_chunk'
)

# Fastest option - copies everything including version history
ds = deeplake.deepcopy(
    src='hub://haritsahm/spotify_filter_version_ratings_count_balanced_50K_docs_1000_chunk',
    dest='deeplake/spotify_filter_version_ratings_count_balanced_50K_docs_1000_chunk'
)
