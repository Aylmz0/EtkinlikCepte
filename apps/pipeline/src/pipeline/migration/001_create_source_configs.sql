CREATE TABLE IF NOT EXISTS source_configs (
    id SERIAL PRIMARY KEY,
    source_name VARCHAR(100) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    schedule_cron VARCHAR(50) NOT NULL, -- Örn: "0 */2 * * *"
    rate_limit_seconds INT DEFAULT 5,
    user_agent VARCHAR(255),
    terms_checked_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
