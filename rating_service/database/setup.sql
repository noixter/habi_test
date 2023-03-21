CREATE TABLE property_rating (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  property_id INT UNSIGNED NOT NULL,
  user_id INT UNSIGNED NOT NULL,
  rating DECIMAL(3,2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  INDEX idx_property_rating_property_id (property_id),
  INDEX idx_property_rating_created_at (created_at)
  FOREIGN KEY (property_id)
  FOREIGN KEY (property_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;
);
