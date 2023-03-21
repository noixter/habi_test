CREATE VIEW property_rating_avg AS
SELECT property_id, AVG(rating) AS rating_average
FROM property_rating
GROUP BY property_id;