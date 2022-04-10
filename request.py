import sqlalchemy
import psycopg2
from pprint import pprint

engine = sqlalchemy.create_engine('postgresql://postgres:N7oefgwv@localhost:5432/tasknet2')
pprint(engine)

connection = engine.connect()
print(connection)
pprint(engine.table_names())
print()

# 1. количество исполнителей в каждом жанре;

select_1 = connection.execute('''SELECT g.name genre, COUNT(p.performer_id) count_performers FROM Genres g
LEFT JOIN Genres_Performers p ON g.id = p.genre_id
GROUP BY g.name;''').fetchall()
pprint(select_1)
print()

# 2. количество треков, вошедших в альбомы 2019-2020 годов;

select_2 = connection.execute('''SELECT COUNT(t.id) count_2019_2020 FROM Tracks t
RIGHT JOIN Albums a ON t.album_id = a.id
WHERE year_ BETWEEN 2019 AND 2020;''').fetchall()
pprint(select_2)
print()

# 3. средняя продолжительность треков по каждому альбому;

select_3 = connection.execute('''SELECT a.name album, AVG(t.duration) avg_duration FROM Tracks t
RIGHT JOIN Albums a ON t.album_id = a.id
GROUP BY a.name;''').fetchall()
pprint(select_3)
print()

# 4. все исполнители, которые не выпустили альбомы в 2020 году;

select_4 = connection.execute('''SELECT name FROM Performers 
WHERE name NOT IN (
	SELECT p.name FROM Performers p
	LEFT JOIN Performers_Albums pa ON p.id = pa.performer_id
	LEFT JOIN Albums a ON pa.album_id = a.id
	WHERE year_ = 2020
	);''').fetchall()
pprint(select_4)
print()

# 5. названия сборников, в которых присутствует конкретный исполнитель (выберите сами);

select_5 = connection.execute('''SELECT DISTINCT c.name collections_with_Maksim FROM Collections c 
JOIN Collections_Tracks ct ON c.id = ct.collection_id
JOIN Tracks t ON ct.track_id = t.id
JOIN Albums a ON t.album_id = a.id
JOIN Performers_Albums pa ON a.id = pa.album_id
JOIN Performers p ON pa.performer_id = p.id
WHERE p.name iLIKE '%%maksim%%';''').fetchall()
pprint(select_5)
print()

# 6. название альбомов, в которых присутствуют исполнители более 1 жанра;

select_6 = connection.execute('''SELECT DISTINCT a.name FROM Albums a 
JOIN Performers_Albums pa ON a.id = pa.album_id
WHERE pa.performer_id IN (
	SELECT performer_id FROM (
		SELECT gp.performer_id, COUNT(gp.genre_id) FROM Genres_Performers gp
		GROUP BY gp.performer_id
		HAVING COUNT(gp.genre_id)>1
		) Subtable1
	);''').fetchall()
pprint(select_6)
print()

# 7. наименование треков, которые не входят в сборники;

select_7 = connection.execute('''SELECT name FROM Tracks t 
WHERE id NOT IN (
	SELECT DISTINCT track_id FROM Collections_Tracks);''').fetchall()
pprint(select_7)
print()

# 8. исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);

select_8 = connection.execute('''SELECT DISTINCT p.name FROM Performers p
JOIN Performers_Albums pa ON p.id = pa.performer_id
WHERE album_id IN (
	SELECT album_id FROM Tracks
	WHERE duration = (
		SELECT MIN(duration) FROM Tracks
		)
	);''').fetchall()
pprint(select_8)
print()

# 9. название альбомов, содержащих наименьшее количество треков.

select_9 = connection.execute('''DROP TABLE IF EXISTS Subtable1;
SELECT a.name, COUNT(t.id) amount INTO Subtable1 FROM Albums a
JOIN Tracks t ON a.id = t.album_id
GROUP BY a.name; --создание временной таблицы

SELECT * FROM Subtable1
WHERE amount = (
	SELECT MIN(amount) FROM Subtable1
	);''').fetchall()
pprint(select_9)
print()
