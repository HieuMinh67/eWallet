CREATE TABLE IF NOT EXISTS public.merchant
(
    id UUID primary key,
    name VARCHAR(100) NOT NULL
    account_id foreign key
);

INSERT TABLE public.merchant (id, name) VALUES ('ff2a130a-c135-4f76-833d-6b9483308e8d', 'Flower Shop');