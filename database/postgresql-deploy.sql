CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE public.book_scraping_data (
    id              UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title           VARCHAR(255) NOT NULL,
    book_url        TEXT NOT NULL,
    price           NUMERIC(10, 2) NOT NULL,
    availability    VARCHAR(100) NOT NULL,
    rating          VARCHAR(20) NULL,
    image_url       TEXT NULL,
    collected_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_book_scraping_title ON public.book_scraping_data (title);
CREATE INDEX idx_book_scraping_rating ON public.book_scraping_data (rating);


select * from book_scraping_data;