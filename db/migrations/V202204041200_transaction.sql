CREATE TABLE IF NOT EXISTS public.transaction
(
    id UUID primary key,
    merchant_id UUID,
    extra_data VARCHAR(50),
    signature VARCHAR(100),
    amount NUMERIC(18,2),
    account_income VARCHAR(100),
    account_outcome VARCHAR(100),
    status INTEGER,
    FOREIGN KEY (merchant_id)
    REFERENCES merchant(id)
);