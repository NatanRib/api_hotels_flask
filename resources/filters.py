#modulo para conter nossas consultas personalizadas
city_query = "SELECT * FROM hotels WHERE city = ? AND (stars >= ? AND stars <= ?) AND (price >= ? AND price <= ?) LIMIT ? OFFSET ?"
none_city_query = "SELECT * FROM hotels WHERE (stars >= ? AND stars <= ?) AND (price >= ? AND price <= ?) LIMIT ? OFFSET ?"