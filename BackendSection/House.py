class House:
    def __init__(self, house_id, address1, address2, city, state, postal_code, country, photo_path, size, register_date):
        self.__house_id = house_id
        self.__address1 = address1
        self.__address2 = address2
        self.__city = city
        self.__state = state
        self.__postal_code = postal_code
        self.__country = country
        self.__photo_path = photo_path
        self.__size = size
        self.__register_date = register_date

    # Getters
    def get_id(self): 
        return self.__house_id
    def get_address1(self): 
        return self.__address1
    def get_address2(self): 
        return self.__address2
    def get_city(self): 
        return self.__city
    def get_state(self): 
        return self.__state
    def get_postal_code(self): 
        return self.__postal_code
    def get_country(self): 
        return self.__country
    def get_photo_path(self): 
        return self.__photo_path
    def get_size(self): 
        return self.__size
    def get_register_date(self): 
        return self.__register_date

    # Setters
    def set_address1(self, value): self.__address1 = value
    def set_address2(self, value): self.__address2 = value
    def set_city(self, value): self.__city = value
    def set_state(self, value): self.__state = value
    def set_postal_code(self, value): self.__postal_code = value
    def set_country(self, value): self.__country = value
    def set_photo_path(self, value): self.__photo_path = value
    def set_size(self, value): self.__size = value
    def set_register_date(self, value): self.__register_date = value

    def get_insert_values(self):
        return (self.__house_id, self.__address1, self.__address2, self.__city,
                self.__state, self.__postal_code, self.__country, self.__photo_path,
                self.__size, self.__register_date)

    def get_update_values(self):
        return (self.__address1, self.__address2, self.__city, self.__state,
                self.__postal_code, self.__country, self.__photo_path,
                self.__size, self.__register_date, self.__house_id)