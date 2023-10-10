FROM php:8.1-fpm-alpine

COPY --from=composer:2.6 /usr/bin/composer /usr/bin/composer

RUN docker-php-ext-install sockets
