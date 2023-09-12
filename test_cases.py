from users.user import user_handler, organization_handler
from booking.booking import room_handler, floor_handler, booking_handler

"""Create Admin"""
user_handler.create_admin_user("admin@varaha.com", "Varaha Admin")
user_handler.create_admin_user("admin2@varaha.com", "Varaha Admin 2")
# Error case, 
user_handler.create_admin_user("admin@varaha.com", "Varaha Admin")  # should throw error since same email exists

"""Create Organization"""
organization_handler.create_organization("admin@varaha.com", "Varaha", "7006793206", other_details={"floor": 1})
organization_handler.create_organization("admin@varaha.com", "Olous", "6006793206", other_details={"floor": 1})
# Error case, 
organization_handler.create_organization("admin@varaha.com", "Varaha", 
                                         "9006973206", 
                                         other_details={"floor": 2})  # should throw error since same organization name exists

"""Create Normal User"""
user_handler.create_user("admin@varaha.com", "kanav220anand@gmail.com",
                         "Kanav Anand", "Varaha")
user_handler.create_user("admin@varaha.com", "kanavanand797@gmail.com",
                         "Anand Kanav", "Varaha")
user_handler.create_user("admin@varaha.com", "kanavanand@olous.com",
                         "Olous User", "Olous")
# Error case, 
user_handler.create_user("admin@varaha.com", "kanav220anand@gmail.com",
                         "Kanav Anand", "Varaha")  # should throw error since same email exists
user_handler.create_user("kanav220anand@gmail.com", "kanav.anand@gmail.com",
                         "Kanav Anand", "Varaha")  # should throw error since user doesn't have permissions
user_handler.create_user("kanav220anand@varaha.com", "kanav.anand@gmail.com",
                         "Kanav Anand", "Varaha")  # should throw error since user doesn't exist

# Error case for authorization in organization create
organization_handler.create_organization("kanav220anand@gmail.com", "Riyalto", 
                                         "8008977706", 
                                         other_details={"floor": 3})
organization_handler.create_organization("kanav220anand@varaha.com", "Riyalto", 
                                         "8008977706", 
                                         other_details={"floor": 3})  # USER DOESNOT EXIST


"""Create Floor"""
floor_handler.create_floor("admin@varaha.com", 1)
# Error case, 
floor_handler.create_floor("admin@varaha.com", 1)  # should throw error since same floor exists
floor_handler.create_floor("kanav220anand@gmail.com", 2)  # should throw error since user doesn't have permissions
floor_handler.create_floor("kanav220anand@varaha.com", 2)  # should throw error since user doesn't exist


"""Create Floor"""
room_handler.create_room("admin@varaha.com", name="A1", floor=1, 
                         capacity=10, is_projector_available=True, 
                         other_details={})
room_handler.create_room("admin@varaha.com", name="A2", floor=1, 
                         capacity=20, is_projector_available=True, 
                         other_details={})
room_handler.create_room("admin@varaha.com", name="A3", floor=1, 
                         capacity=30, is_projector_available=True, 
                         other_details={})
room_handler.create_room("admin@varaha.com", name="A4", floor=1, 
                         capacity=30, is_projector_available=False, 
                         other_details={})
# Error case, 
room_handler.create_room("admin@varaha.com", name="A1", floor=2, 
                          capacity=20, is_projector_available=False, 
                          other_details={})  # should throw error since same room exists
room_handler.create_room("kanav220anand@gmail.com", name="B2", floor=2, 
                        capacity=20, is_projector_available=False, 
                        other_details={})  # should throw error since user doesn't have permissions
room_handler.create_room("kanav220anand@varaha.com", name="B2", floor=2, 
                          capacity=20, is_projector_available=False, 
                          other_details={})  # should throw error since user doesn't exist


"""Create Booking"""
booking_handler.book_room("kanav220anand@gmail.com", "A1", {12:13})  # Varaha
booking_handler.book_room("kanav220anand@gmail.com", "A1", {13:14})  # Varaha
booking_handler.book_room("kanavanand797@gmail.com", "A1", {14:15})  # Varaha another user
booking_handler.book_room("kanavanand@olous.com", "A1", {12:13}, date="20-09-2023")
# Error case, 
booking_handler.book_room("kanav220anand@gmail.com", "A1", {14:15})  # slot already booked
booking_handler.book_room("admin@varaha.com", "A1", {20:21})  # permissions
booking_handler.book_room("kanav220anand@gmail.com", "AA2", {15:17})  # No Room Name


"""Cancel Booking"""
booking_handler.cancel_room_booking("kanavanand797@gmail.com", "A1", {14:15})
# Error case, 
booking_handler.cancel_room_booking("kanavanand797@gmail.com", "A1", {18:19})  # No booking exists



"""Fetch Listings"""
user_handler.get_all_users()  # returns all users
organization_handler.get_all_organizations()  # returns all organizations
floor_handler.get_all_floors()  # returns all floors
room_handler.list_rooms()  # returns all rooms
booking_handler.get_all_bookings()  # returns all bookings

room_handler.list_rooms(capacity=20)  # returns all rooms where capacity is atleast 20
room_handler.list_rooms(capacity=20, projector_required=True)  # returns all rooms where capacity is atleast 20 & projector is available

booking_handler.get_booking_of_organization("kanav220anand@gmail.com")  # returns all bookings of organization via user
booking_handler.get_booking_of_organization(organization="Varaha")  # returns all bookings of organization via org name
booking_handler.get_booking_of_organization(organization="Varaha", date_range=["12-09-2023", "14-09-2023"])  # returns all 
# bookings of organization via org name and in date range
booking_handler.get_booking_of_organization(organization="Olous")  # returns all bookings of organization via org name
booking_handler.get_booking_of_organization(organization="Olous", date_range=["12-09-2023", "14-09-2023"])  # returns all 
# bookings of organization via org name and in date range
booking_handler.get_booking_of_user("kanav220anand@gmail.com")  # returns all bookings of user
booking_handler.get_booking_of_user("kanavanand797@gmail.com")  # returns all bookings of user
booking_handler.get_booking_of_user("kanavanand@olous.com")  # returns all bookings of user

organization_handler.get_organization_booking_hours("Varaha")  # returns the booking hours of organization in current month
organization_handler.get_organization_booking_hours("Olous")  # returns the booking hours of organization in current month

# import threading
# def aa():
#     threads = []
#     t1 = threading.Thread(target=booking_handler.book_room, args=("kanav220anand@gmail.com", "A1", {12:13}))
#     threads.append(t1)
#     t2 = threading.Thread(target=booking_handler.book_room, args=("kanav220anand@gmail.com", "A1", {12:13}))
#     threads.append(t2)
#     t3 = threading.Thread(target=booking_handler.book_room, args=("kanav220anand@gmail.com", "A1", {12:13}))
#     threads.append(t3)
#     for i in range(len(threads)):
#         threads[i].start()
#     for i in range(len(threads)):
#         threads[i].join()