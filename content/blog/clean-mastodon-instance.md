Title: Cleaning a Mastodon instance
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Self-hosting
Tags: Mastodon
Summary: Save some space on your instance

# Cleaning the cache

	RAILS_ENV=production bin/tootctl cache clear

# Cleaning up orphaned media	

	RAILS_ENV=production bin/tootctl media remove-orphans

# Cleaning up 3 months old media (default)

	RAILS_ENV=production bin/tootctl media remove

# Cleaning up inactive accounts

	RAILS_ENV=production bin/tootctl accounts cull
