from spreadsheets.spreadsheet import ImportField, SpreadsheetRow
from accounts.managers import get_or_404_by_account
from people.models import Person
from volunteers.models import CompletedShift
from donors.models import Donation
from collections import OrderedDict


class TargetObjectBasedTemplate(object):

    def get_primary_target(self, account=None, target_id=None):
        if not hasattr(self,"primary_target"):
            self.primary_target = get_or_404_by_account(self.model, account, target_id)
        
        return self.primary_target


class PersonBasedTemplate(TargetObjectBasedTemplate):
    model = Person

    def get_target_object_people_Person(self):
        return self.get_primary_target(), False

    def get_target_object_people_Employee(self):
        return self.get_target_object_people_Person()[0].primary_job, False

    def get_target_object_people_Organization(self):
        if self.get_target_object_people_Employee()[0]:
            return self.get_target_object_people_Employee()[0].organization, False
        else: 
            return None, False

class DonationBasedTemplate(TargetObjectBasedTemplate):
    model = Donation


    def get_target_object_donors_Donation(self):
        return self.get_primary_target(), False
    
    def get_target_object_people_Person(self):
        return self.get_target_object_donors_Donation()[0].donor.person, False

    def get_target_object_people_Employee(self):
        return self.get_target_object_people_Person()[0].primary_job, False

    def get_target_object_people_Organization(self):
        if self.get_target_object_people_Employee()[0]:
            return self.get_target_object_people_Employee()[0].organization, False
        else: 
            return None, False


class CompletedShiftBasedTemplate(TargetObjectBasedTemplate):
    model = CompletedShift

    def get_target_object_volunteers_CompletedShift(self):
        return self.get_primary_target(), False

    def get_target_object_people_Person(self):
        return self.get_target_object_volunteers_CompletedShift()[0].volunteer.person, False

    def get_target_object_people_Organization(self):
        return self.get_target_object_people_Person()[0].primary_job, False




class FullContactListTemplate(PersonBasedTemplate):
    template_type = "full_contact_list"
    name = "Full Contact List"
    description = "All of the contact information stored in GoodCloud, including personal and work contact information."
    fields = OrderedDict([
        ("first_name",          ImportField("First Name",                    "people",       "Person",       "first_name",   )),
        ("last_name",           ImportField("Last Name",                     "people",       "Person",       "last_name",    )),
        ("email",               ImportField("Email",                         "people",       "Person",       "email",        )),
        ("phone_number",        ImportField("Home Phone",                    "people",       "Person",       "phone_number", )),
        ("line_1",              ImportField("Home Address 1",                "people",       "Person",       "line_1",       )),
        ("line_2",              ImportField("Home Address 2",                "people",       "Person",       "line_2",       )),
        ("city",                ImportField("City",                          "people",       "Person",       "city",         )),
        ("state",               ImportField("State",                         "people",       "Person",       "state",        )),
        ("postal_code",         ImportField("Zip Code",                      "people",       "Person",       "postal_code",  )),
        ("org_role",            ImportField("Title",                         "people",       "Employee",     "role",         )),
        ("org_phone_number",    ImportField("Work Phone",                    "people",       "Employee",     "phone_number", )),
        ("org_email",           ImportField("Work Email",                    "people",       "Employee",     "email",        )),
        ("org_name",            ImportField("Organization Name",             "people",       "Organization", "name",         )),
        ("org_line_1",          ImportField("Organization Address 1",        "people",       "Organization", "line_1",       )),
        ("org_line_2",          ImportField("Organization Address 2",        "people",       "Organization", "line_2",       )),
        ("org_city",            ImportField("Organization City",             "people",       "Organization", "city",         )),
        ("org_state",           ImportField("Organization State",            "people",       "Organization", "state",        )),
        ("org_postal_code",     ImportField("Organization Zip",              "people",       "Organization", "postal_code",  )),
    ])

class FullContactListTemplateInstance(FullContactListTemplate,SpreadsheetRow):
    pass
                                    
class MailingListTemplate (PersonBasedTemplate):
    template_type = "mailing_list"
    name = "Home Mailing List"
    description = "Home addresses, plain and simple. Great for mail merges."
    fields = OrderedDict([
        ("first_name",          ImportField("First Name",           "people",       "Person",       "first_name",   )),
        ("last_name",           ImportField("Last Name",            "people",       "Person",       "last_name",    )),
        ("line_1",              ImportField("Address 1",            "people",       "Person",       "line_1",       )),
        ("line_2",              ImportField("Address 2",            "people",       "Person",       "line_2",       )),
        ("city",                ImportField("City",                 "people",       "Person",       "city",         )),
        ("state",               ImportField("State",                "people",       "Person",       "state",        )),
        ("postal_code",         ImportField("Zip Code",             "people",       "Person",       "postal_code",  )),
    ])

class MailingListTemplateInstance(MailingListTemplate,SpreadsheetRow):
    pass

class EmailListTemplate (PersonBasedTemplate):
    template_type = "email_list"
    name = "Email List"
    description = "First name, last name, and email. A quick copy-paste box is below."
    fields = OrderedDict([
        ("first_name",          ImportField("First Name",           "people",       "Person",       "first_name",   )),
        ("last_name",           ImportField("Last Name",            "people",       "Person",       "last_name",    )),
        ("email",               ImportField("Email",                "people",       "Person",       "email",        )),
    ])

class EmailListTemplateInstance(EmailListTemplate,SpreadsheetRow):
    pass

class DonationListTemplate (DonationBasedTemplate):
    template_type = "donations"
    name = "Donation List"
    description = "All donations entered into GoodCloud, with the contact information of the donor."
    fields = OrderedDict([
        ("date",                ImportField("Date",                 "donors",    "Donation",     "date",         )),
        ("amount",              ImportField("Amount",               "donors",    "Donation",     "amount",       )),
        # ("category",            ImportField("Category",             "donors",    "Donation",     "category",     )),
        # ("campaign",            ImportField("Campaign",             "donors",    "Donation",     "campaign",     )),
        ("name",                ImportField("Organization Name",    "people",       "Organization", "name",         )),
        ("first_name",          ImportField("First Name",           "people",       "Person",       "first_name",   )),
        ("last_name",           ImportField("Last Name",            "people",       "Person",       "last_name",    )),
        ("email",               ImportField("Email",                "people",       "Person",       "email",        )),
        ("phone_number",        ImportField("Home Phone",           "people",       "Person",       "phone_number", )),
        ("line_1",              ImportField("Home Address 1",       "people",       "Person",       "line_1",       )),
        ("line_2",              ImportField("Home Address 2",       "people",       "Person",       "line_2",       )),
        ("city",                ImportField("City",                 "people",       "Person",       "city",         )),
        ("state",               ImportField("State",                "people",       "Person",       "state",        )),
        ("postal_code",         ImportField("Zip Code",             "people",       "Person",       "postal_code",  )),
    ])

class DonationListTemplateInstance(DonationListTemplate,SpreadsheetRow):
    pass

class DonationSummaryListTemplate (PersonBasedTemplate):
    template_type = "donation_summary"
    name = "Donation Summary List"
    description = "Summary of donations, per person. Includes monthly and yearly totals for all donations in GoodCloud, with the contact information of the donor."
    fields = OrderedDict([
        # ("date",                ImportField("Date",                 "donors",    "Donation",     "date",         )),
        # ("amount",              ImportField("Amount",               "donors",    "Donation",     "amount",       )),
        # ("category",            ImportField("Category",             "donors",    "Donation",     "category",     )),
        # ("campaign",            ImportField("Campaign",             "donors",    "Donation",     "campaign",     )),
        
        ("first_name",          ImportField("First Name",           "people",       "Person",       "first_name",   )),
        ("last_name",           ImportField("Last Name",            "people",       "Person",       "last_name",    )),
        ("email",               ImportField("Email",                "people",       "Person",       "email",        )),
        ("phone_number",        ImportField("Home Phone",           "people",       "Person",       "phone_number", )),
        ("line_1",              ImportField("Home Address 1",       "people",       "Person",       "line_1",       )),
        ("line_2",              ImportField("Home Address 2",       "people",       "Person",       "line_2",       )),
        ("city",                ImportField("City",                 "people",       "Person",       "city",         )),
        ("state",               ImportField("State",                "people",       "Person",       "state",        )),
        ("postal_code",         ImportField("Zip Code",             "people",       "Person",       "postal_code",  )),
        ("name",                ImportField("Organization Name",    "people",       "Organization", "name",         )),

        # ("donation_current_year",            ImportField("2011 Total",           "people",       "Person",       "donation_current_year",   )),
        # ("donation_current_year",            ImportField("2011 Jan",           "people",       "Person",       "donation_current_year",   )),
    ])

class DonationSummaryListTemplateInstance(DonationSummaryListTemplate,SpreadsheetRow):
    pass

class VolunteerHoursTemplate (CompletedShiftBasedTemplate):
    template_type = "volunteer_hours"
    name = "Volunteer Shifts"
    description = "All volunteer hours recorded in GoodCloud, with the contact information of the volunteer."
    fields = OrderedDict([
        ("date",                ImportField("Date",                 "volunteers",    "CompletedShift",     "date",       )),
        ("duration",            ImportField("Hours",                "volunteers",    "CompletedShift",     "duration",   )),
        # ("shift",               ImportField("Category",            "event",         "CompletedShift",     "shift",      )),
       
        ("first_name",          ImportField("First Name",           "people",       "Person",       "first_name",   )),
        ("last_name",           ImportField("Last Name",            "people",       "Person",       "last_name",    )),
        ("email",               ImportField("Email",                "people",       "Person",       "email",        )),
        ("phone_number",        ImportField("Home Phone",           "people",       "Person",       "phone_number", )),
        ("line_1",              ImportField("Home Address 1",       "people",       "Person",       "line_1",       )),
        ("line_2",              ImportField("Home Address 2",       "people",       "Person",       "line_2",       )),
        ("city",                ImportField("City",                 "people",       "Person",       "city",         )),
        ("state",               ImportField("State",                "people",       "Person",       "state",        )),
        ("postal_code",         ImportField("Zip Code",             "people",       "Person",       "postal_code",  )),
        ("name",                ImportField("Organization Name",    "people",       "Organization", "name",         )),
    ])

class VolunteerHoursTemplateInstance(VolunteerHoursTemplate,SpreadsheetRow):
    pass

class VolunteerHoursSummaryTemplate (PersonBasedTemplate):
    template_type = "volunteer_hour_summary"
    name = "Volunteer Hour Summary"
    description = "Total of volunteer hours, per person. Includes monthly and yearly totals for all shifts in GoodCloud, with the contact information of the volunteer."
    fields = OrderedDict([
        ("date",                ImportField("Date",                 "volunteers",    "CompletedShift",     "date",       )),
        ("duration",            ImportField("Hours",                "volunteers",    "CompletedShift",     "duration",   )),
        # ("shift",               ImportField("Category",            "event",         "CompletedShift",     "shift",      )),
       
        ("first_name",          ImportField("First Name",           "people",       "Person",       "first_name",   )),
        ("last_name",           ImportField("Last Name",            "people",       "Person",       "last_name",    )),
        ("email",               ImportField("Email",                "people",       "Person",       "email",        )),
        ("phone_number",        ImportField("Home Phone",           "people",       "Person",       "phone_number", )),
        ("line_1",              ImportField("Home Address 1",       "people",       "Person",       "line_1",       )),
        ("line_2",              ImportField("Home Address 2",       "people",       "Person",       "line_2",       )),
        ("city",                ImportField("City",                 "people",       "Person",       "city",         )),
        ("state",               ImportField("State",                "people",       "Person",       "state",        )),
        ("postal_code",         ImportField("Zip Code",             "people",       "Person",       "postal_code",  )),
        ("name",                ImportField("Organization Name",    "people",       "Organization", "name",         )),

        # ("donation_current_year",            ImportField("2011 Total",           "people",       "Person",       "donation_current_year",   )),
        # ("donation_current_year",            ImportField("2011 Jan",           "people",       "Person",       "donation_current_year",   )),
    ])

class VolunteerHoursSummaryTemplateInstance(VolunteerHoursSummaryTemplate,SpreadsheetRow):
    pass

class CustomTemplate (object):
    template_type = "custom_template"
    name = "Custom Template"
    description = "Pick your own columns and ordering."
    fields =  [ ]


class CustomTemplateInstance(CustomTemplate,SpreadsheetRow):
    pass




SPREADSHEET_TEMPLATES = [
    FullContactListTemplate(),
    MailingListTemplate(),
    EmailListTemplate(),
    DonationListTemplate(),
    # DonationSummaryListTemplate(),
    VolunteerHoursTemplate(),
    # VolunteerHoursSummaryTemplate(),
    # CustomTemplate(),
]
SPREADSHEET_TEMPLATE_INSTANCES = {
    "full_contact_list"      : FullContactListTemplateInstance,
    "mailing_list"           : MailingListTemplateInstance,
    "email_list"             : EmailListTemplateInstance,
    "donations"              : DonationListTemplateInstance,
    # "donation_summary"       : DonationSummaryListTemplateInstance,
    "volunteer_hours"        : VolunteerHoursTemplateInstance,
    # "volunteer_hour_summary" : VolunteerHoursSummaryTemplateInstance,
    # "custom_template"        : CustomTemplateInstance,
}