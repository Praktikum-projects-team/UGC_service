CREATE DATABASE shard;
CREATE DATABASE replica;
CREATE TABLE shard.movie_views (movie_id UUID, user_id UUID, view_progress UInt16, created_at timestamp) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/movie_views', 'replica_1') PARTITION BY toYYYYMMDD(created_at) ORDER BY (user_id, movie_id);
CREATE TABLE replica.movie_views (movie_id UUID, user_id UUID, view_progress UInt16, created_at timestamp) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/movie_views', 'replica_2') PARTITION BY toYYYYMMDD(created_at) ORDER BY (user_id, movie_id);
CREATE TABLE default.movie_views (movie_id UUID, user_id UUID, view_progress UInt16, created_at timestamp) ENGINE = Distributed('company_cluster', '', movie_views, rand());