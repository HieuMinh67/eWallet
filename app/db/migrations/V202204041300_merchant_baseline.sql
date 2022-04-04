CREATE TABLE IF NOT EXISTS public.merchant
(
    account_id UUID,
	id UUID primary key,
    merchantUrl VARCHAR(200),
    name VARCHAR(100) NOT NULL,
    foreign key (account_id)
    references account (id)
);

INSERT INTO public.merchant (id, name) VALUES ('ff2a130a-c135-4f76-833d-6b9483308e8d', 'Flower Shop');