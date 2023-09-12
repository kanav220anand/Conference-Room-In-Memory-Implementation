## Conference Room Booking System(In-Memory Implementation)


Requirements:
- Designing and implementing a robust conference room booking system for a single building with multiple floors and multiple rooms on each floor. The system should efficiently handle bookings for various organizations and their users. The booking system operates in hourly slots using the 24-hour format eg. Book from 1am to 3am {1:3}, from 12pm to 1pm {12:13}. The objective is to create a user-friendly and reliable solution that optimises the utilisation of conference rooms while providing a seamless booking experience.

Considerations:
- NO PERSISTENT STORAGE TO BE USED HERE, INSTEAD IN-MEMORY DATASTRUCTURES TO BE USED.
- One building.
- Booking slots can be for one hour only.
- Each organization has a monthly booking quota of 30 hours.

Application Logic:
There will be two major user types in the system:
- Admin (No Organization)
- Normal User (Belonging to a particular Organization)

Feature set for Admin:
- Create Organization
- Add Users to Organization
- Create Floors
- Add Rooms on each floor

Feature set for User:
- List all available conference rooms with their details.
- Filter suitable conference rooms according to requirements, eg capacity, equipment.
- Book a Room
- Cancel a Booking
- List all his bookings
- List all the bookings of its organization in a given date range


## To start using:
1. Clone repository.
2. Open terminal and change directory to project where main.py is present.
3. Open python shell.
4. To get commands, refer to test_cases.py file.
