from datetime import date, datetime, timedelta


def get_weekday_from_day (number):
    days={
        0: "Monday", 
        1:"Tuesday", 
        2:"Wednesday",
        3:"Thursday",
        4:"Friday",
        5:"Saturday",
        6:"Sunday"
    }
    return days[number]


def get_birthdays_per_week(users:list[dict]):
   
    current_data= date.today()
    next_week = current_data + timedelta(days=7)
    result= {}
 
    for value in users:
        users_birthday = value["birthday"].replace(year=current_data.year )
        if current_data > users_birthday:
            users_birthday = value["birthday"].replace(year=current_data.year +1)
        
        if current_data < users_birthday <= next_week:
            user_name = value["name"]
            
            if users_birthday.weekday() > 5:
                string_weekday = "Monday"
            else:
                string_weekday = get_weekday_from_day(users_birthday.weekday())
            
            result.setdefault(string_weekday,[])
            result[string_weekday].append(user_name)        
    
        if users_birthday < current_data:
            return result
        
    return result


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
        {"name": "Yegor", "birthday": datetime(1993, 4, 12).date()},
        {"name": "kevin", "birthday": datetime(2041, 11, 23).date()},
        {"name": "Mistake month", "birthday": datetime(1912, 12, 1).date()},
        {"name": "Vit", "birthday": datetime(1994, 12, 8).date()}, #Friday
        {"name": "Evgen", "birthday": datetime(1994, 12, 3).date()}, #Friday
        {"name": "Alex", "birthday": datetime(2021, 12, 5).date()}, #Tuesday
    ]

    result = get_birthdays_per_week(users)
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")


