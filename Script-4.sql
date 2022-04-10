create table if not exists Genres(
  id serial primary key,
  name varchar(50) unique not null
);

create table if not exists Performers(
  id serial primary key,
  name varchar(50) not null
);

create table if not exists Genres_Performers(
  genre_id integer references Genres(id),
  performer_id integer references Performers(id),
  constraint pk1 primary key (genre_id, performer_id) 
);

create table if not exists Albums(
  id serial primary key,  
  name varchar(50) not null,
  year_ integer not null check(year_ > 0)
);

create table if not exists Performers_Albums(
  performer_id integer references Performers(id),
  album_id integer references Albums(id),
  constraint pk2 primary key (performer_id, album_id) 
);

create table if not exists Tracks(
  id serial primary key,
  album_id integer references Albums(id), --may be null
  name varchar(50) not null,
  duration numeric not null check(duration > 0)
);

create table if not exists Collections(
  id serial primary key,  
  name varchar(50) not null,
  year_ integer not null check(year_ > 0)
);

create table if not exists Collections_Tracks(
  collection_id integer references Collections(id),
  track_id integer references Tracks(id),
  constraint pk3 primary key (collection_id, track_id) 
);