# call sakila database
use sakila;

# 1a. Display the first and last names of all actors from the table actor.
select first_name, last_name
from actor;

/* 1b. Display the first and last name of each actor in a single column in upper case letters.
Name the column Actor Name.*/
select concat(first_name, ' ', last_name) as 'Actor Name'
from actor;

/* 2a. You need to find the ID number, first name, and last name of an actor,
of whom you know only the first name, "Joe."
What is one query would you use to obtain this information?*/
select actor_id, first_name, last_name
from actor
where first_name = 'Joe';

# 2b. Find all actors whose last name contain the letters GEN:
select actor_id, first_name, last_name
from actor
where last_name like '%GEN%';

/* 2c. Find all actors whose last names contain the letters LI.
This time, order the rows by last name and first name, in that order: */
select actor_id, last_name, first_name
from actor
where last_name like '%LI%';

/* 2d. Using IN, display the country_id and country columns of the following countries:
Afghanistan, Bangladesh, and China: */
select country_id, country
from country
where country in ('Afghanistan', 'Bangladesh', 'China');

/* 3a. You want to keep a description of each actor.
You don't think you will be performing queries on a description,
so create a column in the table actor named description and use the data type BLOB 
(Make sure to research the type BLOB, as the difference between it and VARCHAR are significant).
*/
alter table actor
add column description blob after last_name;

select * from actor;

/* 3b. Very quickly you realize that entering descriptions for each actor is too much effort.
Delete the description column. */
alter table actor
drop column description;

select * from actor;

# 4a. List the last names of actors, as well as how many actors have that last name.
select last_name, count(last_name) as last_name_count
from actor
group by last_name;

/* 4b. List last names of actors and the number of actors who have that last name,
but only for names that are shared by at least two actors */
select last_name, count(last_name) as last_name_count
from actor
group by last_name
having count(last_name) > 1;

/* 4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS.
Write a query to fix the record. */
update actor
set first_name = 'HARPO'
where first_name = 'GROUCHO' and last_name = "WILLIAMS";

select *
from actor
where first_name = 'HARPO' and last_name = 'WILLIAMS';

/* 4d. Perhaps we were too hasty in changing GROUCHO to HARPO.
It turns out that GROUCHO was the correct name after all!
In a single query, if the first name of the actor is currently HARPO,
change it to GROUCHO. */
update actor
set first_name = 'GROUCHO'
where first_name = 'HARPO' and last_name = "WILLIAMS";

select *
from actor
where first_name = 'GROUCHO' and last_name = 'WILLIAMS';

/* 5a. You cannot locate the schema of the address table.
Which query would you use to re-create it? */
show create table address;

/* 6a. Use JOIN to display the first and last names, as well as the address,
of each staff member. Use the tables staff and address: */
select first_name, last_name, address, address2, district, postal_code
from staff s
join address a
on s.address_id = a.address_id;

/* 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005.
Use tables staff and payment. */
select first_name, last_name, sum(amount) as total_amount
from staff s
join payment p
on s.staff_id = p.staff_id
group by first_name, last_name;

/* 6c. List each film and the number of actors who are listed for that film.
Use tables film_actor and film. Use inner join. */
select title, count(actor_id) as number_of_actors
from film f
inner join film_actor fa
on f.film_id = fa.film_id
group by title;

# 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
select count(inventory_id) as copies_of_Hunchback_Impossible
from inventory i
join film f
on i.film_id = f.film_id
where f.title = 'Hunchback Impossible';

/* 6e. Using the tables payment and customer and the JOIN command,
list the total paid by each customer.List the customers alphabetically by last name: */
select last_name, first_name, sum(amount) as total_paid
from payment p
join customer c
on p.customer_id = c.customer_id
group by last_name asc;

/* 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence.
As an unintended consequence, films starting with the letters K and
Q have also soared in popularity. Use subqueries to display the titles of
movies starting with the letters K and Q whose language is English. */

alter table language
rename to film_language;

alter table film_language
change column name language_name char(20);

# Subquery
select title
from film
where language_id in (select language_id
						from film_language
                        where language_name = 'English'
                        group by title
                        having title like 'K%' or  title like 'Q%');

# Join
select title
from film f
join film_language fl
on f.language_id = fl.language_id
where language_name = 'English'
group by title
having title like 'K%' or  title like 'Q%';

# 7b. Use subqueries to display all actors who appear in the film Alone Trip.
# Join
select first_name, last_name
from actor a
join film_actor fa
on a.actor_id = fa.actor_id
join film f
on fa.film_id = f.film_id
where f.title = 'Alone Trip';

# Subquery
select first_name, last_name
from actor
where actor_id in (select actor_id
					from film_actor
                    where film_id in (select film_id
										from film
                                        where title = 'Alone Trip'));

/* 7c. You want to run an email marketing campaign in Canada,
for which you will need the names and email addresses of all Canadian customers.
Use joins to retrieve this information. */
select first_name, last_name, email
from customer c
join address a
on c.address_id = a.address_id
join city
on a.city_id = city.city_id
join country ctry
on city.country_id = ctry.country_id
where country = 'Canada';

/* 7d. Sales have been lagging among young families, and
you wish to target all family movies for a promotion.
Identify all movies categorized as family films. */
#film, film_category, category
alter table category
change column name category_name varchar(20);

select title as family_titles
from film f
join film_category fc
on f.film_id = fc.film_id
join category c
on fc.category_id = c.category_id
where category_name = 'family';

# 7e. Display the most frequently rented movies in descending order.
# film(film_id)inventory, inventory(inventory_id)rental, rental(rental_id)
select title, count(rental_id) as times_rented
from film f
join inventory i
on f.film_id = i.film_id
join rental r
on i.inventory_id = r.inventory_id
group by title
order by times_rented desc;

# 7f. Write a query to display how much business, in dollars, each store brought in.
# store(store_id) staff(staff_id) rental(rental_id) payment(rental_id)
SELECT s.store_id, SUM(amount) AS Gross
                 FROM payment p
                 JOIN rental r
                 ON (p.rental_id = r.rental_id)
                 JOIN inventory i
                 ON (i.inventory_id = r.inventory_id)
                 JOIN store s
                 ON (s.store_id = i.store_id)
                 GROUP BY s.store_id;

# 7g. Write a query to display for each store its store ID, city, and country.
select st.store_id, city, country
from store st
join address a
on st.address_id = a.address_id
join city c
on a.city_id = c.city_id
join country ctry
on c.country_id = ctry.country_id
group by st.store_id;

/* 7h. List the top five genres in gross revenue in descending order.
(Hint: you may need to use the following tables: category, film_category, inventory,
payment, and rental.) */
select c.category_name, sum(amount) as Gross_Revenue
from payment p
join rental r
on p.rental_id = r.rental_id
join inventory i
on r.inventory_id = i.inventory_id
join film_category fc
on i.film_id = fc.film_id
join category c
on fc.category_id = c.category_id
group by category_name
order by Gross_Revenue desc
limit 5;

/* 8a. In your new role as an executive, you would like to have an easy way of
viewing the Top five genres by gross revenue. Use the solution from the problem above to
create a view. If you haven't solved 7h, you can substitute another query to create a view. */
create view TopFiveGenres_by_GrossRevenue as
(select c.category_name, sum(amount) as Gross_Revenue
from payment p
join rental r
on p.rental_id = r.rental_id
join inventory i
on r.inventory_id = i.inventory_id
join film_category fc
on i.film_id = fc.film_id
join category c
on fc.category_id = c.category_id
group by category_name
order by Gross_Revenue desc
limit 5);

# 8b. How would you display the view that you created in 8a?
select * from TopFiveGenres_by_GrossRevenue;

# 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.
drop view TopFiveGenres_by_GrossRevenue;