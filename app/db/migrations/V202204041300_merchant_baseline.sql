CREATE TABLE IF NOT EXISTS public.merchant
(
	id UUID PRIMARY KEY,
    account_id UUID NOT NULL,
    url VARCHAR(200) UNIQUE,
    api_key UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY(account_id) REFERENCES account (id)
);

INSERT INTO public.merchant (id, name) VALUES ('ff2a130a-c135-4f76-833d-6b9483308e8d', 'Flower Shop');