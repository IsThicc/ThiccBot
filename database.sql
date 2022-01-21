
-- TODO: Make all the old table names/column names better following camelCase
CREATE TABLE IF NOT EXISTS tags (
    name VARCHAR(30) CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL PRIMARY KEY,
    content VARCHAR(150) CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL,
    owner BIGINT NOT NULL,
    command_id BIGINT NOT NULL,
    createdate DATETIME
);

CREATE TABLE IF NOT EXISTS tickets (
    channel_id BIGINT NOT NULL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    open BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS warnings (
    warn_id VARCHAR(30) CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL PRIMARY KEY,
    user_id BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS Counting (
    LastUser  BIGINT NOT NULL,
    Count     INT    NOT NULL DEFAULT 0,
    ChannelID BIGINT NOT NULL
);


CREATE TABLE IF NOT EXISTS Alphabet (
    LastUser  BIGINT     NOT NULL,
    Letter    VARCHAR(1) NOT NULL DEFAULT 'a',
    ChannelID BIGINT     NOT NULL
);

CREATE TABLE IF NOT EXISTS suggestions (
    owner   BIGINT      NOT NULL, 
    index   INT         NOT NULL, 
    id      BIGINT      NOT NULL, 
    content TEXT        NOT NULL, 
    status  BOOL, 
    reason  TEXT
);