from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "chat_messages" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "thread_id" VARCHAR(255) NOT NULL,
    "role" VARCHAR(32) NOT NULL,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_chat_messag_thread__f80ebe" ON "chat_messages" ("thread_id");
CREATE TABLE IF NOT EXISTS "conversations" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "thread_id" VARCHAR(255) NOT NULL UNIQUE,
    "title" VARCHAR(255) NOT NULL DEFAULT 'New Chat',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_conversatio_thread__39bdea" ON "conversations" ("thread_id");
CREATE TABLE IF NOT EXISTS "long_term_memory" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "thread_id" VARCHAR(255) NOT NULL,
    "memory" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_long_term_m_thread__90ad4a" ON "long_term_memory" ("thread_id");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmG1P2zAQx79KlFdMYgjCo/aug24w0XaCbEMgFLmJm0Y4dnCclQr1u8/nJHUS2qhFKr"
    "Qs79q7v5O7n2Pf2c9myDxM4p3TIRIdHMfIx+YX49mkKIQfs9zbhomiSDvBIFCfKL0rhU6Y"
    "KpUH9WPBkSukc4BIjKXJw7HLg0gEjEorTQgBI3OlMKC+NiU0eEywI5iPxRBz6bi7l+aAev"
    "hJPjz7Gz04gwATrxR24MG7ld0R40jZLqj4poTwtr7jMpKEVIujsRgyOlUHVIDVxxRzJDA8"
    "XvAEwofosnTzjNJItSQNsTDGwwOUEFFId0EGLqPAT0YTqwTV9Hy29g6OD072jw5OpERFMr"
    "UcT9L0dO7pQEWga5sT5UcCpQqFUXMTQ46R58zCJz8BPptfaVAFowy+ijGHVscxN6wOZIie"
    "HIKpL4ZA7/CwBtvv1tXpeetqS6o+QTJMfs/p197NXFbqA7aaJWcEL4Mx16+KoF5+q0C4by"
    "1AcN+aCxBcZX7ydQKnq7CM0MZPc1ZyYcimUKyhZrdvbAg6jONHUqS11WndKJDhOPNc9rrf"
    "c3mB7ull72uVqlyrMn8HzQB7Jj0iCPEcuKWRFb5eNnQn/7GetE3YqXqUjLMdpY7+Rad9bb"
    "c6P0tTcNay2+CxSvhz69ZR5fuePsT4c2GfG/DXuO1124ogi4XP1Ru1zr41ISaUCOZQNnKQ"
    "V9j8cmsOZgL1b/BQ2MnB0Efuwwhxz3nhYRabp33pCq2wakFUVnUvgwth5t0Bo38xj1E2Gy"
    "+7h6K/vn0oKJv2oWkfXrltr5zj6rsHEYjl2ofpgLerfGYXjww4GphrjbIpeR+o5BUnNom8"
    "V05seWQzse86sSr4NWllLhn1bczDDg4ZH89qZiqK2naGSK0jpNgJtbrpaJqO5r+8ENFrYN"
    "HzvB7RHOeb4/wHLoFrdZxvYR64w1m1L/PU1jykNU2l26BKB/cu2f3MonWuMGRT9uc3KHOw"
    "NJaAmMk3E+De7u4CAKVqLkDlW/Di/8d1r7vsxf8vKhO88wJXbBskiMX9emKtoQhZ1/cN1R"
    "ahUo3gAdA3vGt5mfwD8e22/A=="
)
