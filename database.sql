
-- TODO: Make all the old table names/column names better following camelCase
CREATE TABLE IF NOT EXISTS tags (
    name       VARCHAR(30) CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL PRIMARY KEY,
    owner      BIGINT NOT NULL,
    content    VARCHAR(150) CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL,
    command_id BIGINT NOT NULL,
    createdate DATETIME
);

CREATE TABLE IF NOT EXISTS tickets (
    open       BOOLEAN NOT NULL,
    user_id    BIGINT  NOT NULL,
    channel_id BIGINT  NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS warnings (
    warn_id VARCHAR(30)
        CHARACTER SET utf8 COLLATE utf8_swedish_ci
                   NOT NULL PRIMARY KEY,
    user_id BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS Counting (
    Count     INT    NOT NULL DEFAULT 0,
    LastUser  BIGINT NOT NULL,
    ChannelID BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS Alphabet (
    Mode      VARCHAR(20) NOT NULL DEFAULT 'A_Z',
    Letter    VARCHAR(1)  NOT NULL DEFAULT 'a',
    LastUser  BIGINT      NOT NULL,
    ChannelID BIGINT      NOT NULL
);
