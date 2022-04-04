CREATE TABLE IF NOT EXISTS public.account
(
    id UUID primary key,
    type VARCHAR NOT NULL,
    balance NUMERIC(18,2)
);

INSERT INTO public.account (id, type, balance) VALUES ('4da39078-57ed-4c9b-b8eb-f3dcb0603313', 'PERSONAL', 1000.55);
INSERT INTO public.account (id, type, balance) VALUES ('ff2a130a-c135-4f76-833d-6b9483308e8d', 'MERCHANT', 1050.55);