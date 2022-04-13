CREATE TABLE IF NOT EXISTS public.merchant
(
	id UUID PRIMARY KEY,
    account_id UUID NOT NULL,
    url VARCHAR(200) UNIQUE,
    api_key VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY(account_id) REFERENCES account (id)
);

INSERT INTO merchant(id, account_id, name, url, api_key)
VALUES ('ae10fbde-efd7-4f55-b886-c79b8b3b87fb',
        'ff2a130a-c135-4f76-833d-6b9483308e8d',
        'Flower Shop',
        'flower.com',
        'd0478f876f');