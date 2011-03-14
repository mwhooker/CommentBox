curl "http://encyclopediadramatica.com/Haters_gonna_hate" | grep -o 'http://images.encyclopediadramatica.com/images/thumb/[^"]\+' | sed 's+/thumb++' | while read line; do curl -O $line &; done
