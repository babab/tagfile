SELECT filename, COUNT(filehash)
FROM `index`
GROUP BY filehash
HAVING ( COUNT(filehash) > 1 )
