songs = []
genre_count = {}

print("Welcome to the Music Library Manager!\n\nPlease enter 5 songs with their genres.")
for i in range(5):
    song_input = input(f"Enter song {i+1}: ")
    genre_input = input(f"Enter genre for song {i+1}: ")
    print()
    songs.append((song_input, genre_input))

    if genre_input in genre_count:
        genre_count[genre_input] += 1
    else:
        genre_count[genre_input] = 1

print("=== YOUR MUSIC LIBRARY ===")

for i in range(len(songs)):
    song, genre = songs[i]
    print(f"{i+1}. \"{song}\" ({genre})")

print("\n=== GENRE STATISTICS ===")
for genre in genre_count:
    print(f"{genre}: {genre_count[genre]} song(s)")
print("\nThe most popular genre: " +  max(genre_count, key=genre_count.get))
print("\nThank you for using the Music Library Manager!")
