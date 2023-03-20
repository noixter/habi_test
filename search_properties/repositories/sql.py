PROPERTIES_AND_STATUS: str = (
    "SELECT property.id, property.address, property.city, "
    "property.price, property.description, property.year, "
    "status.name as status_name, status.label as status_label "
    "FROM property "
    "JOIN status ON status.id = "
    "(SELECT sh.status_id FROM status_history sh "
    "WHERE sh.property_id = property.id "
    "ORDER BY sh.update_date DESC LIMIT 1) "
)
