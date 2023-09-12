"""Do we need to take date into consideration while booking"""
import uuid

from exceptions import (AuthorizationException, DuplicateException,
                        NotFoundException, RequiredParameterException)
from users.user import organization_handler, user_handler
from utils.authorization import Authorization
from utils.generic import (check_if_dates_are_same,
                           find_if_date_in_range, get_current_hour_minute,
                           get_date_before, get_time_difference_in_minutes,
                           get_today)
from threading import Lock
lock = Lock()

class Floor:
    floors = {}
    floor_room = {}

    def create_floor(self, requestor = "", number=0, rooms_count=0): # Apply validation on input types
        """Public function to be called from outside the class
        Requires Manage Floor Permission"""
        if not self._check_can_create_floor(requestor):   # check permissions
            raise AuthorizationException("Create Floor")

        floor_exists = self._check_if_floor_exists(number)  # check duplicate enteries
        if floor_exists:
            raise DuplicateException("Floor")

        self.floors[number] = {
            "id": str(uuid.uuid4()),
            "rooms_count": rooms_count
        }

        return f"Floor number {number} created successfully"

    def _check_if_floor_exists(self, floor_number):
        """Internal Class function to check duplicacy"""
        if floor_number in self.floors:
            return True
        return False

    def _check_can_create_floor(self, requestor_email):
        """Checks whether requestor is authorized to create Floor"""
        requestor_email = requestor_email.lower()
        requestor_details = user_handler.get_user_details(requestor_email)
        return Authorization.can_manage_floors(requestor_details)

    def get_floor_details(self, floor_number):
        """Returns Details of one Floor via number"""
        if not floor_number:
            raise RequiredParameterException(floor_number)
        return self.floors.get(floor_number, None)
    
    def get_all_floors(self):
        """Returns Details of all Floors"""
        return self.floors

    def _increase_room_count_of_floor(self, floor_number, increment_count=1):
        """Function to increase room count in a floor"""
        self.floors[floor_number]["rooms_count"] += 1
        return f"Increased room count on floor {floor_number}"

    def _decrease_room_count_of_floor(self, floor_number, increment_count=1):
        """Function to decrease room count in a floor"""
        self.floors[floor_number]["rooms_count"] -= 1
        return f"Decreased room count on floor {floor_number}"

    def add_room_to_floor(self, floor=0, room=""):
        """Adds a room to particular floor in grouping"""
        self.floor_room[floor] = {  # used map because adding/removing is O(1)
            room: True
        }
        self._increase_room_count_of_floor(floor)
        return f"Added room {room} to floor {floor}"


floor_handler = Floor()


class Room:
    rooms = {}
    bookings = {}
    
    def create_room(self, requestor="", name="", floor=1, 
                    capacity=0, is_projector_available=False, 
                    other_details={}):
        """Public function to be called from outside the class
        Requires Manage Rooms Permission"""

        if not self._check_can_create_room(requestor):   # check permissions
            raise AuthorizationException("Create Room")

        room_exists = self._check_if_room_exists(name)  # check duplicate enteries
        if room_exists:
            raise DuplicateException("Room")

        floor_details = floor_handler.get_floor_details(floor)
        if not floor_details:
            raise NotFoundException("Floor")

        self.rooms[name] = {
            "id": str(uuid.uuid4()),
            "name": name,
            "floor": floor,
            "capacity": capacity,
            "is_projector_available": is_projector_available,
            "other_details": other_details,
            "is_available": True
        }
        floor_handler.add_room_to_floor(floor, name)

        return f"Room {name} created successfully"
    
    def _check_if_room_exists(self, room_name):
        """Internal Class function to check duplicacy"""
        # assuming no room in the building will have same name else \
        # apply another filter to check if rooms that exists is on same floor
        if room_name in self.rooms:
            return True
        return False

    def _check_can_create_room(self, requestor_email):
        """Checks whether requestor is authorized to create Room"""
        requestor_email = requestor_email.lower()
        requestor_details = user_handler.get_user_details(requestor_email)
        return Authorization.can_manage_rooms(requestor_details)

    def get_room_details(self, name):
        """Returns Details of Room from name"""
        if not name:
            raise RequiredParameterException(name)
        return self.rooms.get(name, None)
    
    def list_rooms(self, capacity=None, projector_required=False):
        """Returns Details of all Rooms with filters(if applied)"""
        rooms = self.rooms
        if capacity:
            rooms = {i: rooms[i] for i in rooms if rooms[i]["capacity"] >= capacity}
        if projector_required:
            rooms = {i: rooms[i] for i in rooms if rooms[i]["is_projector_available"]}
        return rooms


room_handler = Room()


class Booking:
    bookings = {}
    user_booking_group = {}
    org_booking_group = {}

    def _create_booking_key(self, room_name, date, time_slot):
        """A unique key for every organization and month is generated
        so that each month's track records are maintained"""
        return room_name + date + str(time_slot)

    def book_room(self, requestor="", room_name="",
                  time_slot={}, date=""):
        """Public function to be called from outside the class
        Requires Manage Booking Permission"""
        if not self._check_can_create_booking(requestor):   # check permissions
            raise AuthorizationException("Create Booking")

        requestor_details = user_handler.get_user_details(requestor)
        if not requestor_details:
            raise NotFoundException("User")

        room_details = room_handler.get_room_details(room_name)
        if not room_details:
            raise NotFoundException("Room")

        organization = requestor_details.get("organization")
        booking_hours = organization_handler.get_organization_booking_hours(organization)
        if booking_hours >= 30:
            raise Exception("You have completed your quota of 30 hour booking")

        if not date:
            date = get_today()
        else:
            print("VERIFY THE DATE FORMAT HERE")
        key = self._create_booking_key(room_name, date, time_slot)

        booking_exists = self._check_if_booking_exists(key)
        if booking_exists:
            raise DuplicateException("Room Booking")

        self.bookings[key] = {
            "slot": time_slot,
            "date": date,
            "user": requestor,
            "room": room_name,
            "organization": requestor_details.get("organization")
        }
        self._create_user_booking_mapping(requestor, key)  # add booking against user
        self._create_org_booking_mapping(requestor_details.get("organization"), key)  # add booking against org
        organization_handler.increase_organization_booking_hours(organization)  # update org booking hours

        return f"Room {room_name} booked for time slot {str(time_slot)}"
    
    def _check_can_create_booking(self, requestor_email):
        """Checks whether requestor is authorized to create Booking"""
        requestor_email = requestor_email.lower()
        requestor_details = user_handler.get_user_details(requestor_email)
        return Authorization.can_manage_bookings(requestor_details)

    def _create_user_booking_mapping(self, user="", key=""):
        """add booking against user"""
        user_map = self.user_booking_group.get(user)
        if user_map:
            user_map[key] = 1
        else:
            self.user_booking_group[user] = {key: 1}
        return ""

    def _create_org_booking_mapping(self, org="", key=""):
        """add booking against organization"""
        org_map = self.org_booking_group.get(org)
        if org_map:
            org_map[key] = 1
        else:
            self.org_booking_group[org] = {key: 1}
        return ""

    def _delete_user_booking_mapping(self, user="", key=""):
        """remove booking against user"""
        user_map = self.user_booking_group.get(user)
        if user_map:
            lock.acquire()
            self.user_booking_group[user].pop(key)
            lock.release()
        return ""

    def _delete_org_booking_mapping(self, org="", key=""):
        """Remove booking against Organization"""
        org_map = self.org_booking_group.get(org)
        if org_map:
            lock.acquire()
            self.org_booking_group[org].pop(key)
            lock.release()
        return ""

    def cancel_room_booking(self, requestor="", room="",
                            time_slot={}, date=""):
        """Remove booking function"""
        if not date:
            date = get_today()
        else:
            # TODO: Verify date format here
            pass

        key = self._create_booking_key(room, date, time_slot)
        booking_details = self.get_booking_details(key)
        if not booking_details:
            raise NotFoundException("Booking")
        
        if requestor != booking_details.get("user"):
            raise Exception("Sorry, you are not authorized to delete this booking")
        
        requestor_details = user_handler.get_user_details(requestor)
        if not requestor_details:
            raise NotFoundException("User")
        
        if check_if_dates_are_same(booking_details.get("date"), get_today()):  # if the current date and booking date are same,
            # then only perform logic, else doesn't make sense
            booked_time_str = str(next(iter(time_slot))) + ":00"
            current_time_str = get_current_hour_minute()
            if get_time_difference_in_minutes(booked_time_str, current_time_str) < 15:  # check if less than 15 minutes are remaining in meeting
                raise Exception("Booking can't be cancelled as time for meeting is less than 15 minutes")
        
        organization = requestor_details.get("organization")
        lock.acquire()
        self.bookings.pop(key)  # Delete Booking
        lock.release()
        self._delete_user_booking_mapping(requestor, key)  # Remove booking against user
        self._delete_org_booking_mapping(organization, key)  # Remove booking against Org
        organization_handler.decrease_organization_booking_hours(organization)  # update org booking hours

        return f"Booking for room {room} cancelled"
    
    def _check_if_booking_exists(self, key=None, room_name="", date="", time_slot={}):
        """Internal Class function to check duplicacy"""
        if not key:
            key = self._create_booking_key(room_name, date, time_slot)
        if key in self.bookings:
            return True
        return False

    def get_booking_details(self, key=None):
        """Returns Details of Booking from key"""
        if not key:
            raise RequiredParameterException(key)
        return self.bookings.get(key, None)

    def get_all_bookings(self):
        """Returns Details of all bookings"""
        return self.bookings

    def get_booking_of_organization(self, user="", organization="", 
                                    date_range=[]):
        """Returns Details of all bookings of organization, with filters"""
        last_month_bookings = []
        if user:
            organization = user_handler.get_organization_from_user(user)

        org_bookings = self.org_booking_group.get(organization, None)
        if not org_bookings:
            return last_month_bookings

        for i in org_bookings:
            booking_details = self.bookings[i]
            booking_date = booking_details["date"]
            if len(date_range) > 0:
                if find_if_date_in_range(booking_date, date_range):
                    last_month_bookings.append(booking_details)
            else:
                last_month_bookings.append(booking_details)
        
        return last_month_bookings

    def get_booking_of_user(self, user=""):
        """Returns Details of all bookings of user"""
        last_month_bookings = []
        
        user_bookings = self.user_booking_group.get(user, None)
        if not user_bookings:
            return last_month_bookings

        for i in user_bookings:
            booking_details = self.bookings[i]
            last_month_bookings.append(booking_details)
        
        return last_month_bookings


booking_handler = Booking()
