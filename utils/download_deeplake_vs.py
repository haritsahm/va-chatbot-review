import deeplake

# Fastest option - copies everything including version history
ds = deeplake.deepcopy(
    src='hub://haritsahm/spotify_reviews_cleaned_filtered_balanced_50K_docs_1000_chunk',
    dest='deeplake/spotify_reviews_cleaned_filtered_balanced_50K_docs_1000_chunk'
)
