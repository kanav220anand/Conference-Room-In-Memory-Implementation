"""User & Organization related operations"""
import uuid

from exceptions import (AuthorizationException, DuplicateException,
                        NotFoundException, RequiredParameterException)
from utils.generic import get_month_year
from utils.authorization import Authorization


class Organization:
    organizations = {}
    org_user_map = {}
    org_booking_hours = {}

    def create_organization(self, requestor="", name="", 
                            contact_info="", other_details={}):
        """Public function to be called from outside the class
        Requires Manage Organizations Permission"""

        if not self._check_can_create_organization(requestor):  # check permissions
            raise AuthorizationException("Create Organization")
        org_exists = self._check_if_organization_exists(name)  # check duplicate enteries
        if org_exists:
            raise DuplicateException("Organization")

        self.organizations[name] = {
            "id": str(uuid.uuid4()),
            "name": name,
            "contact_info": contact_info,
            "other_details": other_details
        }
        self._add_organization_to_mapping(name)  # create an empty entry in org-user mapping details
        return f"Organization with name {name} created successfully!!"

    def _check_can_create_organization(self, requestor_email):
        """Checks whether requestor is authorized to create organization"""
        requestor_email = requestor_email.lower()
        requestor_details = user_handler.get_user_details(requestor_email)
        return Authorization.can_manage_organizations(requestor_details)

    def _check_if_organization_exists(self, org_name):
        """Internal Class function to check duplicacy"""
        if org_name in self.organizations:
            return True
        return False
    
    def get_organization_details(self, organization_name):
        """Returns Details of one organization via name"""
        if not organization_name:
            raise RequiredParameterException(organization_name)
        return self.organizations.get(organization_name, None)

    def get_all_organizations(self):
        """Returns Details of all organizations"""
        return self.organizations

    def _add_organization_to_mapping(self, org_name=""):
        self.org_user_map[org_name] = {}

    def _add_user_to_organization(self, organization="", user=""):
        """Adds user to organization"""
        self.org_user_map[organization][user] = True
        return "User added to organization"

    def increase_organization_booking_hours(self, organization):
        """Function to increase organization's booking hours in current month"""
        key = self._generate_org_booking_key(organization)
        hr_count = self.org_booking_hours.get(key)
        if hr_count:
            hr_count += 1
            self.org_booking_hours[key] = hr_count
        else:
            self.org_booking_hours[key] = 1
        return f"Increased organization booking hours in current month to {hr_count}"

    def decrease_organization_booking_hours(self, organization):
        """Function to decrease organization's booking hours in current month"""
        key = self._generate_org_booking_key(organization)
        hr_count = self.org_booking_hours.get(key)
        if hr_count:
            hr_count -= 1
            self.org_booking_hours[key] = hr_count
        else:
            self.org_booking_hours[key] = 0
        return f"Decreased organization booking hours in current month to {hr_count}"

    def get_organization_booking_hours(self, organization):
        """Returns organization's booking hours in current month"""
        key = self._generate_org_booking_key(organization)
        return self.org_booking_hours.get(key, 0)
    
    def _generate_org_booking_key(self, organization):
        """A unique key for every organization and month is generated
        so that each month's track records are maintained"""
        return organization + get_month_year()


organization_handler = Organization()


class User:
    users = {}
    admin_role_name = "admin"
    normal_user_role_name = "user"

    def _create_user(self, *args, **kwargs):
        """Private function, to be called from inside the User class only"""
        self.users[kwargs.get("email")] = kwargs
        return True
    
    def create_admin_user(self, email="", full_name=""):
        """Public function to be called from outside the class
        Requires Manage Users Permission"""

        email = email.lower()
        user_exists = self._check_if_user_exists(email)  # check duplicate enteries
        if user_exists:
            raise DuplicateException("Admin User")
        
        permissions = Authorization.get_admin_permissions()  # get list of all the permissions to be assigned

        self._create_user(email=email, full_name=full_name, 
                          role=self.admin_role_name, id=str(uuid.uuid4()),
                          permissions=permissions, organization=""
                          )
        return f"Admin User with email {email} created successfully"

    def create_user(self, requestor = "", email="", 
                    full_name="", organization=""):
        """Public function to be called from outside the class
        Requires Manage Users Permission"""

        email = email.lower()
        if not self._check_can_create_users(requestor):   # check permissions
            raise AuthorizationException("create user")

        user_exists = self._check_if_user_exists(email)  # check duplicate enteries
        if user_exists:
            raise DuplicateException("User")

        organization_details = organization_handler.\
            get_organization_details(organization)
        if not organization_details:
            raise NotFoundException("Organization")

        permissions = Authorization.get_user_permissions()  # get list of all the permissions to be assigned
        self._create_user(email=email, 
                          full_name=full_name, 
                          role=self.normal_user_role_name, 
                          id=str(uuid.uuid4()),
                          permissions=permissions, 
                          organization=organization
                          )

        organization_handler._add_user_to_organization(
            organization, email)  # create user-organization grouping

        return f"User with email {email} created successfully"
    
    def _check_can_create_users(self, requestor_email):
        """Checks whether requestor is authorized to create User"""
        requestor_email = requestor_email.lower()
        requestor_details = self.get_user_details(requestor_email)
        return Authorization.can_manage_users(requestor_details)

    def _check_if_user_exists(self, email):
        """Internal Class function to check duplicacy"""
        if email in self.users:
            return True
        return False
    
    def get_all_users(self):
        """Returns Details of all organizations"""
        return self.users

    def get_organization_from_user(self, user_email):
        """Returns Details of organization from user"""
        user = self.users.get(user_email)
        if not user:
            raise NotFoundException("User")
        return user.get("organization")

    def get_user_details(self, email):
        """Returns Details of one organization via email"""
        if not email:
            raise RequiredParameterException(email)
        return self.users.get(email, None)

user_handler = User()
